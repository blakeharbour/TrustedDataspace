import subprocess
import re
import sys
import threading
import time
import webbrowser
import os
import queue
import asyncio
from tensorboard import program


class TensorBoardService:
    def __init__(self, logdir, port=6006):
        self.logdir = logdir
        self.port = port
        self.process = None
        self.output_queue = queue.Queue()
        self.url = None  # 添加一个属性用于存储 URL
        self.read_output_active_lock = asyncio.Lock()
        self.read_output_active = True  # 控制 read_output 循环的标志

    async def run_tensorboard(self):
        if 'apt_pkg' in sys.modules:
            del sys.modules['apt_pkg']
            print("delete")
        await self.start_tensorboard()

    async def read_output(self, stream):
        print("read_output 进入循环")
        try:
            while self.read_output_active:
                line = await asyncio.wait_for(stream.readline(), timeout=10.0)
                if not line:
                    break  # 如果读到 EOF，退出循环
                decoded_line = line.decode().strip()
                print(f"读取行: {decoded_line}")
                if "TensorBoard" in decoded_line and "http" in decoded_line:
                    url_match = re.search(r'http://[^\s]*', decoded_line)
                    if url_match:
                        async with self.read_output_active_lock:
                            self.url = url_match.group()
                            print(f'read_output TensorBoard 已在 {self.url} 启动')
                            self.read_output_active = False  # 设置标志为 False，退出循环
        except asyncio.CancelledError:
            # 当协程被取消时，捕获异常以避免输出错误信息
            pass
        except Exception as e:
            print(f"read_output 发生异常: {e}")
            raise  # 将异常重新抛出以确保协程终止


    async def start_tensorboard(self):
        command = ['tensorboard', f'--logdir={self.logdir}', '--host=0.0.0.0', f'--port={self.port}']
        print(f'TensorBoard 命令行参数： {" ".join(command)}')
        self.process = await asyncio.create_subprocess_exec(
            *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # 同时异步读取标准输出和标准错误输出
        read_output_tasks = [
            asyncio.ensure_future(self.read_output(self.process.stdout)),
            asyncio.ensure_future(self.read_output(self.process.stderr)),
        ]

        print( "read_output finish")

        # 等待所有任务完成
        done, pending = await asyncio.wait(read_output_tasks, return_when=asyncio.FIRST_COMPLETED)

        # 取消未完成的任务
        for task in pending:
            task.cancel()

        print("start process_output")

        # 处理输出
        await self.process_output()

        print("TensorBoard 进程完成")

    async def process_output(self):
        while not self.output_queue.empty():
            line = await self.output_queue.get()
            print(f"Processed line: {line}")
            # 处理输出内容，提取 TensorBoard URL 等...
            if "TensorBoard" in line and "http" in line:
                url_match = re.search(r'http://[^\s]*', line)
                if url_match:
                    url = url_match.group()
                    print(f'process_output TensorBoard 已在 {url} 启动')

    def stop_tensorboard(self):
        if self.process and self.process.returncode is None:
            self.process.terminate()
            print('TensorBoard stopped')
