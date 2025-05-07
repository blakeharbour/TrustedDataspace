from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
import json
import os
import datetime

# 静态数据 - 数据资产列表
STATIC_ASSETS = [
    {
        'id': 1,
        'name': '铁路准入(出)到货信息',
        'asset_type': '铁路准入到货信息',
        'owner': 'railway',
        'owner_display': '铁路',
        'description': '包含传输人代码、航次号、运单号等信息的铁路准入到货数据',
        'created_at': '2025-04-01',
    },
    {
        'id': 2,
        'name': '铁路预配舱单',
        'asset_type': '预配舱单',
        'owner': 'railway',
        'owner_display': '铁路',
        'description': '铁路预配舱单数据，包含详细货物信息',
        'created_at': '2025-04-05',
    },
    {
        'id': 3,
        'name': '理货报告编制要求',
        'asset_type': '理货报告编制要求',
        'owner': 'customs',
        'owner_display': '海关',
        'description': '海关制定的理货报告编制要求，包含标准和格式规范',
        'created_at': '2025-03-15',
    },
    {
        'id': 4,
        'name': '出境货物标准',
        'asset_type': '出境货物标准',
        'owner': 'customs',
        'owner_display': '海关',
        'description': '海关制定的出境货物检验标准和规范',
        'created_at': '2025-03-20',
    },
    {
        'id': 5,
        'name': '原始舱单',
        'asset_type': '舱单',
        'owner': 'port',
        'owner_display': '港口',
        'description': '港口记录的原始舱单数据，包含货物详情和配载信息',
        'created_at': '2025-04-03',
    },
    {
        'id': 6,
        'name': '理货报告',
        'asset_type': '理货报告',
        'owner': 'port',
        'owner_display': '港口',
        'description': '港口理货员编制的理货报告，记录实际装卸货情况',
        'created_at': '2025-04-08',
    },
    {
        'id': 7,
        'name': '运单信息',
        'asset_type': '运单',
        'owner': 'foreign',
        'owner_display': '外方',
        'description': '外方提供的运单信息，包含货主、货物、目的地等详情',
        'created_at': '2025-03-28',
    },
    {
        'id': 8,
        'name': '元数据标准',
        'asset_type': '元数据',
        'owner': 'railway',
        'owner_display': '铁路',
        'description': '铁路系统的数据元标准，规定各类数据的格式和规范',
        'created_at': '2025-03-10',
    }
]

# 静态数据 - 数据申请列表
STATIC_REQUESTS = [
    {
        'id': 1,
        'asset_id': 1,
        'asset_name': '铁路准入(出)到货信息',
        'asset_owner': 'railway',
        'asset_owner_display': '铁路',
        'requester_name': '张三',
        'request_reason': '需要调度港口作业资源',
        'request_purpose': '优化港口资源配置，提前为货物到达做准备',
        'status': 'approved',
        'status_display': '已批准',
        'created_at': '2025-04-10',
        'remark': '批准使用，有效期30天'
    },
    {
        'id': 2,
        'asset_id': 2,
        'asset_name': '铁路预配舱单',
        'asset_owner': 'railway',
        'asset_owner_display': '铁路',
        'requester_name': '李四',
        'request_reason': '需要了解货物详情便于通关准备',
        'request_purpose': '提前准备通关文件，加速通关流程',
        'status': 'pending',
        'status_display': '待审核',
        'created_at': '2025-04-15',
        'remark': ''
    },
    {
        'id': 3,
        'asset_id': 3,
        'asset_name': '理货报告编制要求',
        'asset_owner': 'customs',
        'asset_owner_display': '海关',
        'requester_name': '王五',
        'request_reason': '编制理货报告需要参考最新标准',
        'request_purpose': '确保理货报告符合海关要求',
        'status': 'rejected',
        'status_display': '已拒绝',
        'created_at': '2025-04-12',
        'remark': '请先完成理货员培训再申请'
    },
    {
        'id': 4,
        'asset_id': 5,
        'asset_name': '原始舱单',
        'asset_owner': 'port',
        'asset_owner_display': '港口',
        'requester_name': '赵六',
        'request_reason': '需要核对货物信息',
        'request_purpose': '与实际到货情况进行比对，保证数据一致',
        'status': 'pending',
        'status_display': '待审核',
        'created_at': '2025-04-17',
        'remark': ''
    },
    {
        'id': 5,
        'asset_id': 7,
        'asset_name': '运单信息',
        'asset_owner': 'foreign',
        'asset_owner_display': '外方',
        'requester_name': '张三',
        'request_reason': '需要获取货主联系方式',
        'request_purpose': '联系货主确认交付时间和地点',
        'status': 'pending',
        'status_display': '待审核',
        'created_at': '2025-04-18',
        'remark': ''
    },
    {
        'id': 6,
        'asset_id': 4,
        'asset_name': '出境货物标准',
        'asset_owner': 'customs',
        'asset_owner_display': '海关',
        'requester_name': '李四',
        'request_reason': '需要了解最新的货物出境检验标准',
        'request_purpose': '确保货物符合出境要求，避免延误',
        'status': 'approved',
        'status_display': '已批准',
        'created_at': '2025-04-05',
        'remark': '已批准，注意标准中的危险品处理要求'
    }
]

# 静态数据 - 授权记录
STATIC_AUTHORIZATIONS = [
    {
        'id': 1,
        'request_id': 1,
        'asset_name': '铁路准入(出)到货信息',
        'requester_name': '张三',
        'authorizer_name': '铁路管理员',
        'authorized_at': '2025-04-11',
        'is_active': True,
        'status_display': '有效',
        'remark': '批准使用，有效期30天'
    },
    {
        'id': 2,
        'request_id': 6,
        'asset_name': '出境货物标准',
        'requester_name': '李四',
        'authorizer_name': '海关管理员',
        'authorized_at': '2025-04-06',
        'is_active': True,
        'status_display': '有效',
        'remark': '已批准，注意标准中的危险品处理要求'
    },
    {
        'id': 3,
        'request_id': 3,
        'asset_name': '理货报告编制要求',
        'requester_name': '王五',
        'authorizer_name': '海关管理员',
        'authorized_at': '2025-04-13',
        'is_active': False,
        'status_display': '已拒绝',
        'remark': '请先完成理货员培训再申请'
    }
]

# 静态数据 - 操作日志
STATIC_LOGS = [
    {
        'id': 1,
        'operation_type': 'request',
        'operation_type_display': '申请数据',
        'operator_name': '张三',
        'operation_time': '2025-04-10 10:30:00',
        'operation_detail': '申请数据资产: 铁路准入(出)到货信息'
    },
    {
        'id': 2,
        'operation_type': 'approve',
        'operation_type_display': '批准申请',
        'operator_name': '铁路管理员',
        'operation_time': '2025-04-11 14:20:00',
        'operation_detail': '批准数据申请: 铁路准入(出)到货信息'
    },
    {
        'id': 3,
        'operation_type': 'request',
        'operation_type_display': '申请数据',
        'operator_name': '李四',
        'operation_time': '2025-04-15 09:15:00',
        'operation_detail': '申请数据资产: 铁路预配舱单'
    },
    {
        'id': 4,
        'operation_type': 'request',
        'operation_type_display': '申请数据',
        'operator_name': '王五',
        'operation_time': '2025-04-12 16:40:00',
        'operation_detail': '申请数据资产: 理货报告编制要求'
    },
    {
        'id': 5,
        'operation_type': 'reject',
        'operation_type_display': '拒绝申请',
        'operator_name': '海关管理员',
        'operation_time': '2025-04-13 11:05:00',
        'operation_detail': '拒绝数据申请: 理货报告编制要求'
    },
    {
        'id': 6,
        'operation_type': 'request',
        'operation_type_display': '申请数据',
        'operator_name': '赵六',
        'operation_time': '2025-04-17 08:45:00',
        'operation_detail': '申请数据资产: 原始舱单'
    },
    {
        'id': 7,
        'operation_type': 'request',
        'operation_type_display': '申请数据',
        'operator_name': '张三',
        'operation_time': '2025-04-18 10:20:00',
        'operation_detail': '申请数据资产: 运单信息'
    },
    {
        'id': 8,
        'operation_type': 'request',
        'operation_type_display': '申请数据',
        'operator_name': '李四',
        'operation_time': '2025-04-05 14:30:00',
        'operation_detail': '申请数据资产: 出境货物标准'
    },
    {
        'id': 9,
        'operation_type': 'approve',
        'operation_type_display': '批准申请',
        'operator_name': '海关管理员',
        'operation_time': '2025-04-06 09:25:00',
        'operation_detail': '批准数据申请: 出境货物标准'
    },
    {
        'id': 10,
        'operation_type': 'view',
        'operation_type_display': '查看数据',
        'operator_name': '张三',
        'operation_time': '2025-04-12 11:40:00',
        'operation_detail': '查看数据资产: 铁路准入(出)到货信息'
    }
]

# 角色枚举
ROLE_TYPES = [
    ('customs', '海关'),
    ('port', '港口'),
    ('railway', '铁路'),
    ('foreign', '外方'),
]

# 数据资产类型枚举
DATA_ASSET_TYPES = [
    ('铁路准入到货信息', '铁路准入到货信息'),
    ('预配舱单', '预配舱单'),
    ('理货报告编制要求', '理货报告编制要求'),
    ('出境货物标准', '出境货物标准'),
    ('舱单', '舱单'),
    ('理货报告', '理货报告'),
    ('运单', '运单'),
    ('元数据', '元数据'),
]

# 申请状态枚举
REQUEST_STATUS = [
    ('pending', '待审核'),
    ('approved', '已批准'),
    ('rejected', '已拒绝'),
]

# 操作类型枚举
OPERATION_TYPES = [
    ('request', '申请数据'),
    ('approve', '批准申请'),
    ('reject', '拒绝申请'),
    ('view', '查看数据'),
]


# ----- 视图函数 -----

def data_assets_list(request):
    """数据资产列表页"""
    # 筛选条件
    asset_type = request.GET.get('asset_type', '')
    owner = request.GET.get('owner', '')

    # 筛选数据
    assets = STATIC_ASSETS.copy()
    if asset_type:
        assets = [a for a in assets if a['asset_type'] == asset_type]
    if owner:
        assets = [a for a in assets if a['owner'] == owner]

    context = {
        'assets': assets,
        'asset_types': DATA_ASSET_TYPES,
        'owners': ROLE_TYPES,
        'current_asset_type': asset_type,
        'current_owner': owner,
    }
    return render(request, 'data_confirmation/assets_list.html', context)


def data_asset_detail(request, asset_id):
    """数据资产详情页"""
    # 查找指定ID的资产
    asset = next((a for a in STATIC_ASSETS if a['id'] == asset_id), None)
    if not asset:
        return redirect('data_confirmation:assets_list')

    # 模拟当前用户名
    username = "当前用户"

    # 检查是否有待审批的申请
    has_pending_request = any(r for r in STATIC_REQUESTS if r['asset_id'] == asset_id
                              and r['requester_name'] == username and r['status'] == 'pending')

    # 检查是否有获得授权
    has_authorization = any(a for a in STATIC_AUTHORIZATIONS if a['request_id'] in
                            [r['id'] for r in STATIC_REQUESTS if r['asset_id'] == asset_id
                             and r['requester_name'] == username and r['status'] == 'approved'])

    context = {
        'asset': asset,
        'is_owner': False,  # 简化，假设当前用户不是所有者
        'has_authorization': has_authorization,
        'has_pending_request': has_pending_request
    }
    return render(request, 'data_confirmation/asset_detail.html', context)


def create_data_request(request, asset_id):
    """创建数据申请"""
    # 查找指定ID的资产
    asset = next((a for a in STATIC_ASSETS if a['id'] == asset_id), None)
    if not asset:
        return redirect('data_confirmation:assets_list')

    if request.method == 'POST':
        # 处理表单提交
        reason = request.POST.get('request_reason')
        purpose = request.POST.get('request_purpose')

        if not reason or not purpose:
            messages.error(request, "请填写申请原因和用途说明")
            return render(request, 'data_confirmation/create_request.html', {'asset': asset})

        messages.success(request, "申请已提交，请等待审批")
        return redirect('data_confirmation:my_requests')

    return render(request, 'data_confirmation/create_request.html', {'asset': asset})


def my_requests(request):
    """我的申请列表"""
    # 模拟当前用户名
    username = "当前用户"

    # 筛选条件
    status = request.GET.get('status', '')

    # 筛选数据 - 假设"张三"是当前用户
    requests = [r for r in STATIC_REQUESTS if r['requester_name'] == '张三']
    if status:
        requests = [r for r in requests if r['status'] == status]

    context = {
        'requests': requests,
        'statuses': REQUEST_STATUS
    }
    return render(request, 'data_confirmation/my_requests.html', context)


def pending_approvals(request):
    """待审批申请列表"""
    # 筛选待审核的申请
    pending_requests = [r for r in STATIC_REQUESTS if r['status'] == 'pending']

    # 打印调试信息
    print(f"待审批申请数量: {len(pending_requests)}")
    for req in pending_requests:
        print(f"待审批申请: ID={req['id']}, 资产={req['asset_name']}, 申请人={req['requester_name']}")

    return render(request, 'data_confirmation/pending_approval.html', {
        'pending_requests': pending_requests
    })


def process_request(request, request_id):
    """处理数据申请(批准/拒绝)"""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action not in ['approve', 'reject']:
            messages.error(request, "无效的操作")
        elif action == 'approve':
            messages.success(request, "已批准数据申请")
        else:
            messages.success(request, "已拒绝数据申请")

    return redirect('data_confirmation:pending_approvals')


def authorizations(request):
    """授权记录列表"""
    return render(request, 'data_confirmation/authorizations.html', {
        'authorizations': STATIC_AUTHORIZATIONS
    })


def operation_logs(request):
    """操作日志查询"""
    # 筛选条件
    operation_type = request.GET.get('operation_type', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # 筛选数据
    logs = STATIC_LOGS.copy()
    if operation_type:
        logs = [l for l in logs if l['operation_type'] == operation_type]

    context = {
        'logs': logs,
        'operation_types': OPERATION_TYPES,
        'current_operation_type': operation_type,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'data_confirmation/operation_logs.html', context)