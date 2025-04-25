#外部访问
from django.http import JsonResponse
import json
from myapp import views
from myapp import viewsmult
from myapp.myjob import selecttable


#接收数据申请结果
def mult_check_apply_re(request):
    if request.method == 'POST':
        try:
            # 解析JSON数据
            data = json.loads(request.body)
            print(data)
            # status=data["status_check"]
            viewsmult.editmultmodelall(request)

            print("数据格式",data)
            # print("数据格式", status)
            # 处理数据的逻辑
            result = {"message": f"Data received and processed: {data}"}
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
