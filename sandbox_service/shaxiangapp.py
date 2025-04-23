from flask import Flask, request, jsonify
import docker
import os
import time
import threading
from datetime import datetime
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import base64
import pandas as pd
from werkzeug.utils import secure_filename
import os
import io
import tarfile
import docker
import random
import threading
import time
import shutil

from flask import request, jsonify, send_file
app = Flask(__name__)
client = docker.from_env()
CORS(app)  # 允许所有跨域

# ✅ 创建沙箱
@app.route('/api/createSandbox', methods=['POST'])
def create_sandbox():
    try:
        data = request.get_json()
        save_url = data.get('saveUrl')
        expire = data.get('sandbox_expire', '')
        auth_scope = data.get('auth_scope', '')
        destroy_strategy = data.get('destroy_strategy', '')

        if not save_url:
            return jsonify(success=False, message='缺少 saveUrl'), 400

        # ✅ 构造唯一容器名
        container_name = "sandbox_" + os.path.basename(save_url).replace('.', '_')

        # ✅ 检查是否已存在同名容器
        for c in client.containers.list(all=True):
            if c.name == container_name:
                return jsonify(success=False, message=f"容器名 {container_name} 已存在，请先销毁"), 409

        # ✅ 拉取镜像（建议提前 pull 或缓存）
        image = "python:3.10-slim"
        try:
            client.images.pull(image)
        except Exception as e:
            return jsonify(success=False, message=f"拉取镜像失败：{str(e)}"), 500

        # # ✅ 创建容器
        # container = client.containers.run(
        #     image=image,
        #     name=container_name,
        #     command="tail -f /dev/null",
        #     detach=True,
        #     tty=True,
        #     labels={"sandbox": "true"},
        #     environment={
        #         "SAVE_URL": save_url,
        #         "EXPIRE_TIME": expire,
        #         "AUTH_SCOPE": auth_scope,
        #         "DESTROY_STRATEGY": destroy_strategy
        #     }
        # )
        host_sandbox_path = os.path.abspath("sandbox_data/" + container_name)
        os.makedirs(host_sandbox_path, exist_ok=True)

        container = client.containers.run(
            image=image,
            name=container_name,
            command="tail -f /dev/null",
            detach=True,
            tty=True,
            labels={"sandbox": "true"},
            volumes={
                host_sandbox_path: {
                    'bind': '/sandbox',  # 容器内路径
                    'mode': 'rw'
                }
            },
            environment={
                "SAVE_URL": save_url,
                "EXPIRE_TIME": expire,
                "AUTH_SCOPE": auth_scope,
                "DESTROY_STRATEGY": destroy_strategy
            }
        )

        return jsonify(success=True, message=f"容器 {container_name} 创建成功")

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

BASE_SANDBOX_DIR = os.path.abspath("sandbox_data")  # 沙箱基目录（建议用绝对路径）
os.makedirs(BASE_SANDBOX_DIR, exist_ok=True)
@app.route('/api/uploadToSandbox', methods=['POST'])

def upload_to_sandbox():
    print("📥 收到上传请求")

    try:
        if 'file' not in request.files:
            print("❌ 未收到文件 file 字段")
            return jsonify(success=False, message="缺少文件")

        file = request.files['file']
        container_name = request.form.get('sandbox_path')  # 沙箱容器名
        print("📦 沙箱容器名（前端传入）:", container_name)

        if not file or not container_name:
            print("❌ 缺少文件或容器名")
            return jsonify(success=False, message="缺少文件或沙箱容器名")

        # ✅ 安全生成沙箱路径（容器名中将 / 替换为 _）
        safe_container = secure_filename(container_name.replace("/", "_"))
        sandbox_path = os.path.abspath(os.path.join(BASE_SANDBOX_DIR, safe_container))
        os.makedirs(sandbox_path, exist_ok=True)
        print("📁 沙箱保存路径:", sandbox_path)

        # ✅ 检查是否为 CSV 文件
        if not file.filename.endswith('.csv'):
            print("⚠️ 只支持 CSV 文件")
            return jsonify(success=False, message="仅支持 CSV 文件加密")

        print("🔐 检测到 CSV，开始加密...")
        df = pd.read_csv(file)

        # ✅ AES 加密逻辑
        key = b"1234567890abcdef"  # 固定 16 字节密钥
        cipher = AES.new(key, AES.MODE_ECB)

        encrypted_rows = []
        for _, row in df.iterrows():
            row_str = ','.join(map(str, row.values))
            encrypted = cipher.encrypt(pad(row_str.encode('utf-8'), AES.block_size))
            encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
            encrypted_rows.append(encrypted_b64)

        # ✅ 构造目标加密文件名
        suffix = container_name.split("/")[-1]
        encrypted_filename = f"encrypted_{secure_filename(suffix)}.csv"
        encrypted_path = os.path.join(sandbox_path, encrypted_filename)

        # ✅ 若旧加密文件存在，先删除
        if os.path.exists(encrypted_path):
            print("🧹 检测到旧加密文件，正在删除：", encrypted_path)
            os.remove(encrypted_path)

        # ✅ 保存加密数据
        with open(encrypted_path, "w", encoding="utf-8") as f:
            for line in encrypted_rows:
                f.write(line + "\n")

        print(f"✅ 加密文件已保存：{encrypted_path}")
        return jsonify(success=True, message="✅ 上传并加密成功", path=encrypted_path)

    except Exception as e:
        print("❌ 后端异常：", str(e))
        return jsonify(success=False, message="❌ 后端异常：" + str(e))




# ✅ 查看所有沙箱
@app.route('/api/listSandboxes', methods=['GET'])
def list_sandboxes():
    try:
        containers = client.containers.list(all=True, filters={"label": "sandbox=true"})
        result = []
        for c in containers:
            envs = c.attrs['Config']['Env']
            env_dict = {e.split('=')[0]: e.split('=')[1] for e in envs if '=' in e}
            result.append({
                "name": c.name,
                "status": c.status,
                "save_url": env_dict.get("SAVE_URL", ""),
                "expire_time": env_dict.get("EXPIRE_TIME", ""),
                "auth_scope": env_dict.get("AUTH_SCOPE", ""),
                "destroy_strategy": env_dict.get("DESTROY_STRATEGY", "")
            })
        return jsonify(success=True, data=result)
    except Exception as e:
        return jsonify(success=False, message=str(e))


@app.route('/api/exportSandbox', methods=['POST'])
def export_sandbox():
    try:
        data = request.get_json()
        container_name = data.get('container_name')
        print("📦 收到导出请求，container_name:", container_name)

        if not container_name:
            return jsonify(success=False, message="缺少容器名"), 400

        sandbox_path = os.path.abspath(os.path.join("sandbox_data", container_name))
        print("📁 尝试查找目录：", sandbox_path)

        if not os.path.exists(sandbox_path):
            print("❌ 目录不存在")
            return jsonify(success=False, message="沙箱目录不存在"), 404

        # 正常导出
        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode="w:gz") as tar:
            tar.add(sandbox_path, arcname=container_name)
        tar_stream.seek(0)

        return send_file(
            tar_stream,
            as_attachment=True,
            download_name=f"{container_name}_export.tar.gz",
            mimetype="application/gzip"
        )

    except Exception as e:
        print("❌ 异常：", str(e))
        return jsonify(success=False, message=f"导出异常：{str(e)}"), 500

# ✅ 定时销毁线程（每分钟自动检测）
def auto_destroy_job():
    while True:
        time.sleep(60)
        print("[定时检查] 正在扫描沙箱销毁策略...")

        containers = client.containers.list(all=True, filters={"label": "sandbox=true"})

        for c in containers:
            try:
                envs = c.attrs['Config']['Env']
                env_dict = {e.split('=')[0]: e.split('=')[1] for e in envs if '=' in e}
                strategy = env_dict.get("DESTROY_STRATEGY", "")
                expire_time = env_dict.get("EXPIRE_TIME", "")

                if strategy == "使用后立即销毁":
                    print(f"[销毁] {c.name} - 使用后立即销毁")
                    c.stop()
                    c.remove()

                elif strategy == "沙箱有效期到期后自动销毁":
                    if expire_time:
                        try:
                            expire_dt = datetime.strptime(expire_time, "%Y-%m-%d")
                            if datetime.now() > expire_dt:
                                print(f"[销毁] {c.name} - 有效期已过")
                                c.stop()
                                c.remove()
                        except Exception as e:
                            print(f"[解析时间失败] {c.name} - {str(e)}")
            except Exception as e:
                print(f"[扫描失败] {str(e)}")


@app.route('/api/generateReadonlyLink', methods=['POST'])
def generate_readonly_link():
    try:
        data = request.get_json()
        container_name = data.get('container_name')
        if not container_name:
            return jsonify(success=False, message="缺少容器名")


        BASE_SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "sandbox_data"))

        # 1️⃣ 检查沙箱数据是否存在
        sandbox_path = os.path.abspath(os.path.join(BASE_SANDBOX_DIR, container_name))

        if not os.path.exists(sandbox_path):
            return jsonify(success=False, message="沙箱目录不存在")

        # 2️⃣ 构建路径、分配端口、容器名
        port = random.randint(6050, 6090)
        readonly_container_name = f"readonly_{container_name}"
        viewer_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "readonly_template"))

        temp_container_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "temp_viewers", readonly_container_name))

        if os.path.exists(temp_container_path):
            shutil.rmtree(temp_container_path)
        shutil.copytree(viewer_template_path, temp_container_path)

        # 3️⃣ 拷贝数据至 sandbox_data 内部
        # 将加密数据拷贝至统一目录 sandbox_encrypted_data_txt 下
        target_data_path = os.path.join(temp_container_path, "sandbox_data", "sandbox_encrypted_data_txt")
        os.makedirs(target_data_path, exist_ok=True)

        # 拷贝 csv 文件进来
        for fname in os.listdir(sandbox_path):
            fpath = os.path.join(sandbox_path, fname)
            if os.path.isfile(fpath) and fname.endswith(".csv"):
                shutil.copy2(fpath, os.path.join(target_data_path, fname))

        # 4️⃣ 使用已有 trustedreadonlysandboxviewer 镜像启动容器（你打包时的镜像名）
        client = docker.from_env()
        container = client.containers.run(
            image="trustedreadonlysandboxviewer",
            name=readonly_container_name,
            ports={f'{6064}/tcp': port},
            environment={"VIEWER_PORT": "6064"},  # ✅ 告诉容器内部用哪个端口
            volumes={temp_container_path: {'bind': '/app', 'mode': 'rw'}},
            working_dir="/app",
            detach=True
        )

        # 5️⃣ 自动销毁机制
        def cleanup():
            time.sleep(600)
            try:
                container.stop()
                container.remove()
                shutil.rmtree(temp_container_path)
                print(f"✅ 10分钟到期：已销毁 {readonly_container_name}")
            except Exception as e:
                print("❌ 清理失败：", e)

        threading.Thread(target=cleanup, daemon=True).start()

        # 6️⃣ 返回链接地址
        # 返回链接地址
        ip = request.host.split(":")[0]
        link = f"http://{ip}:{port}/?container={container_name}"
        return jsonify(success=True, link=link)

    except Exception as e:
        return jsonify(success=False, message=f"后端异常：{str(e)}")


# ✅ 手动销毁某个沙箱容器
@app.route('/api/destroySandbox/<string:container_name>', methods=['DELETE'])
def destroy_sandbox(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        print(f"[手动销毁] {container_name} 已销毁")
        return jsonify(success=True, message="沙箱已销毁")
    except docker.errors.NotFound:
        return jsonify(success=False, message=f"容器 {container_name} 不存在"), 404
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

# @app.route('/api/uploadToSandbox', methods=['POST'])
# def upload_to_sandbox():
#     try:
#         file = request.files['file']
#         sandbox_path = request.form.get('sandbox_path')
#
#         if not file or not sandbox_path:
#             return jsonify(success=False, message="缺少文件或沙箱路径")
#
#         filename = secure_filename(file.filename)
#         save_path = os.path.join(sandbox_path, filename)
#
#         if not os.path.exists(sandbox_path):
#             os.makedirs(sandbox_path)
#
#         file.save(save_path)
#         return jsonify(success=True, message="上传成功")
#     except Exception as e:
#         return jsonify(success=False, message=str(e))

# ✅ 启动定时线程
def start_destroy_thread():
    t = threading.Thread(target=auto_destroy_job, daemon=True)
    t.start()


if __name__ == '__main__':
    start_destroy_thread()
    app.run(host='0.0.0.0', port=5001)
