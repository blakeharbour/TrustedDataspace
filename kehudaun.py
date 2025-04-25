import requests
import json
import base64
from cryptography.fernet import Fernet
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)

def decrypt_data(encrypted_data, key):
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data.decode()
    except Exception as e:
        logging.error(f"解密失败: {str(e)}")
        raise

def receive_data_packet(url):
    try:
        response = requests.get(url, timeout=10)  # 设置请求超时
        response.raise_for_status()  # 如果状态码不是 200，会抛出异常

        packet = response.json()
        encrypted_data = packet['encrypted_data']
        key = packet['key']
        client_ip = packet['client_ip']  # 获取客户端 IP 地址
        user_agent = packet.get('user_agent', 'Unknown')  # 如果不存在则返回 'Unknown'
        timestamp = packet.get('timestamp', 'Unknown')  # 如果不存在则返回 'Unknown'
        request_url = packet.get('url', 'Unknown')  # 使用 .get() 访问 'url'，如果没有则返回 'Unknown'
        query_params = packet.get('query_params', {})  # 如果不存在则返回空字典

        # 解密数据
        decrypted_data = decrypt_data(encrypted_data, base64.b64decode(key))

        # 将解密后的数据转换为 JSON 格式
        data_dict = json.loads(decrypted_data)

        # 打印解密后的数据
        logging.info(f"接收到的数据包来自 IP: {client_ip}")
        logging.info(f"User-Agent: {user_agent}")
        logging.info(f"请求时间戳: {timestamp}")
        logging.info(f"请求的 URL: {request_url}")
        logging.info(f"查询参数: {query_params}")
        logging.info("接收到的数据包内容:")
        logging.info(json.dumps(data_dict, ensure_ascii=False, indent=4))
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败: {str(e)}")
    except Exception as e:
        logging.error(f"接收数据失败: {str(e)}")

def main():
    url = "http://10.61.222.249:5000/get_data"  # 发送端的地址
    receive_data_packet(url)

if __name__ == "__main__":
    main()