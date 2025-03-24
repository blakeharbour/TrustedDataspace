import requests
from cryptography.fernet import Fernet
import base64
from bs4 import BeautifulSoup
import socket

# 定义解密函数
def decrypt_data(encrypted_data_str, key_str):
    # 解码 base64 编码的字符串
    encrypted_data = base64.b64decode(encrypted_data_str)
    key = base64.b64decode(key_str)
    # 初始化 Fernet 对象并解密数据
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    # 返回解密后的数据
    return decrypted_data.decode()

# 获取客户端 IP 地址
def get_client_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Failed to get client IP: {e}")
        return None

# 定义服务器 URL
url = 'http://10.61.222.249:8000/myapp/get_data/'

# 获取客户端 IP
client_ip = get_client_ip()
if client_ip:
    headers = {'X-Client-IP': client_ip}
    # 发送 GET 请求
    response = requests.get(url, headers=headers)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            # 查找所有的 <th> 标签，定位加密数据的 <th>
            th_elements = soup.find_all('th')
            encrypted_data_str = None
            key_str = None
            for th in th_elements:
                if '加密数据' in th.text:
                    encrypted_data_str = th.find_next('td').text.strip()
                elif '密钥' in th.text:
                    key_str = th.find_next('td').text.strip()
            if not encrypted_data_str or not key_str:
                raise ValueError("找不到加密数据或密钥")
            # 解密数据
            decrypted_data = decrypt_data(encrypted_data_str, key_str)
            # 输出解密后的数据
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            print(f"发生错误: {e}")
    else:
        print(f"请求失败，HTTP 状态码: {response.status_code}")
else:
    print("无法获取客户端 IP，请求未发送。")