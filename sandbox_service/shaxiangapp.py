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
    try:
        if 'file' not in request.files:
            return jsonify(success=False, message="缺少文件")

        file = request.files['file']
        container_name = request.form.get('sandbox_path')  # 其实是沙箱容器名

        if not file or not container_name:
            return jsonify(success=False, message="缺少文件或沙箱容器名")

        # 安全生成保存路径
        safe_container = secure_filename(container_name)  # 防止路径注入
        sandbox_path = os.path.abspath(os.path.join(BASE_SANDBOX_DIR, safe_container))
        os.makedirs(sandbox_path, exist_ok=True)

        # 保存原始文件
        filename = secure_filename(file.filename)
        save_path = os.path.join(sandbox_path, filename)
        file.save(save_path)

        # 加密 CSV 文件
        if filename.endswith('.csv'):
            df = pd.read_csv(save_path)

            # AES 加密逻辑
            key = b"1234567890abcdef"  # 16字节密钥
            cipher = AES.new(key, AES.MODE_ECB)

            encrypted_rows = []
            for _, row in df.iterrows():
                row_str = ','.join(map(str, row.values))
                encrypted = cipher.encrypt(pad(row_str.encode('utf-8'), AES.block_size))
                encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
                encrypted_rows.append(encrypted_b64)

            encrypted_path = os.path.join(sandbox_path, "encrypted_" + filename)
            with open(encrypted_path, "w", encoding="utf-8") as f:
                for line in encrypted_rows:
                    f.write(line + "\n")

        return jsonify(success=True, message="✅ 上传并加密成功", path=sandbox_path)

    except Exception as e:
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

        if not container_name:
            return jsonify(success=False, message="缺少容器名"), 400

        sandbox_path = os.path.abspath(os.path.join("sandbox_data", container_name))
        if not os.path.exists(sandbox_path):
            return jsonify(success=False, message="沙箱目录不存在"), 404

        # ✅ 打包目录为 tar.gz（内存打包，不写磁盘）
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
