import io
import json
import subprocess
import webbrowser

from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse
import os
from django.http import HttpResponse


def mult_open_file(request):
    try:
        # 使用 xdg-open 命令打开文件资源管理器
        proobj = request.body
        print(proobj)
        # 将字节串解码为字符串
        proobj_str = proobj.decode('utf-8')
        # 将字符串解析为字典
        data_dict = json.loads(proobj_str)

        absolute_path= data_dict[0].get("address")
        print("文件地址是", absolute_path)
        # os.startfile(absolute_path)
        subprocess.run(['xdg-open', absolute_path])
        # subprocess.run(["xdg-open", absolute_path])

        # 返回成功的 JSON 响应
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # 返回错误的 JSON 响应，包含错误信息
        return JsonResponse({'status': 'error', 'message': str(e)})

def mult_open_png(request):
    try:
        # 使用 xdg-open 命令打开文件资源管理器
        proobj = request.body
        print(proobj)
        # 将字节串解码为字符串
        proobj_str = proobj.decode('utf-8')
        # 将字符串解析为字典
        data_dict = json.loads(proobj_str)

        png_path= data_dict[0].get("address")
        print("图片地址是", png_path)
        with open(png_path, 'rb') as f:
            image_data = f.read()

        # 使用PIL库打开图片
        img = Image.open(io.BytesIO(image_data))
        img.show()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # 返回错误的 JSON 响应，包含错误信息
        return JsonResponse({'status': 'error', 'message': str(e)})
