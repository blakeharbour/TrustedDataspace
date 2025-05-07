from django.urls import path
from . import views_data_confirmation

app_name = 'data_confirmation'

urlpatterns = [
    path('assets/', views_data_confirmation.data_assets_list, name='assets_list'),
    path('assets/<int:asset_id>/', views_data_confirmation.data_asset_detail, name='asset_detail'),
    path('request/<int:asset_id>/', views_data_confirmation.create_data_request, name='create_request'),
    path('my-requests/', views_data_confirmation.my_requests, name='my_requests'),
    path('pending-approvals/', views_data_confirmation.pending_approvals, name='pending_approvals'),
    path('process-request/<int:request_id>/', views_data_confirmation.process_request, name='process_request'),
    path('authorizations/', views_data_confirmation.authorizations, name='authorizations'),
    path('logs/', views_data_confirmation.operation_logs, name='operation_logs'),
]

