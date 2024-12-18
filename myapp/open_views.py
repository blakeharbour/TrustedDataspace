import subprocess
from django.shortcuts import render
from django.http import JsonResponse
import os


def open_file_manager(request,parameter):
    try:
        # 使用 xdg-open 命令打开文件资源管理器
        absolute_path='./myapp/fed_PU_sci1203/result/nnPU/'
        print(absolute_path)
        # os.startfile(absolute_path)
        subprocess.run(['xdg-open', absolute_path])
        # subprocess.run(["xdg-open", absolute_path])

        # 返回成功的 JSON 响应
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # 返回错误的 JSON 响应，包含错误信息
        return JsonResponse({'status': 'error', 'message': str(e)})
def open_file_manager1(request):
    try:
        # 使用 xdg-open 命令打开文件资源管理器
        absolute_path='./myapp/fed_PU_sci1203/result/nnPU/'
        print(absolute_path)
        # os.startfile(absolute_path)
        subprocess.run(['xdg-open', absolute_path])
        # subprocess.run(["xdg-open", absolute_path])

        # 返回成功的 JSON 响应
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # 返回错误的 JSON 响应，包含错误信息
        return JsonResponse({'status': 'error', 'message': str(e)})
from django.http import HttpResponse
def application_result_shappng(request,i):
    shappng_dic = request.GET.get('pngpath', None)
    print(shappng_dic)
    with open(shappng_dic,'rb') as f:
        return HttpResponse(f.read(),content_type="image/png")

def multmodel_application_result_shappng(request,i):
    shappng_dic = request.GET.get('pngpath', None)
    print(shappng_dic)
    with open(shappng_dic,'rb') as f:
        return HttpResponse(f.read(),content_type="image/png")