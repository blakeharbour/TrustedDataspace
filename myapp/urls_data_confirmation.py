from django.urls import path
from . import views

urlpatterns = [
    # 数据资产
    path('assets/', views.data_assets_list, name='assets_list'),
    path('assets/<int:asset_id>/', views.data_asset_detail, name='asset_detail'),

    # 数据申请
    path('request/<int:asset_id>/', views.create_data_request, name='create_request'),
    path('my-requests/', views.my_requests, name='my_requests'),

    # 审批管理
    path('pending-approvals/', views.pending_approvals, name='pending_approvals'),
    path('process-request/<int:request_id>/', views.process_request, name='process_request'),

    # 授权记录
    path('authorizations/', views.authorizations, name='authorizations'),

    # 操作日志
    path('logs/', views.operation_logs, name='operation_logs'),
]
##shujuquequanshujuquaunqquuuuuuuuuuiiii