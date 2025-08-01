"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views, api_multviews, mult_open_views, modelapp_portview
from myapp import  viewsmult
from myapp import  api_views
from myapp import  open_views
from django.contrib import admin
from django.urls import path, include
from myapp import views, modelappview
from myapp.views import show_latest_ip, get_data

from myapp import views, modelappview

# from django.conf.urls.static import static
# from django.conf import settings
# from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    #校验登录
    path('jxclogin/', views.jxclogin),
    # 校验登录
    path('register/', views.register),
    #用户增删改查
    path('createuser/', views.createuser),
    path('deleteuser/', views.deleteuser),
    path('edituser/', views.edituser),
    #返回全部用户信息
    path('searchuser/', views.searchuser),
    #返回指定id的用户信息
    path('oneuser/', views.oneuser),
    #
    path('changepassword/', views.changepassword),

    #跳转到前端页面
    path('login/', views.login_page),
    path('', views.login_page),
    path('registeruser/', views.registeruser),
    path('tdindex/', views.tdindex),


    #用户管理界面
    path('user-list/', views.user_list),
    path('searchlogin/', views.searchlogin),
    path('login-add/', views.login_add),
    path('login-edit/', views.login_edit),
    path('createlogin/', views.createlogin),
    path('deletelogin/', views.deletelogin),
    path('searchonelogin/', views.searchonelogin),

    path('api/check_sandbox_ip/', views.check_sandbox_ip),

    #数据接口界面
    path('wb-interface/', views.wb_interface),
    path('searchinterface/', views.searchinterface),
    path('interface-add/', views.interface_add),
    path('createinterface/', views.createinterface),
    path('deleteinterface/', views.deleteinterface),
    path('interface-edit/', views.interface_edit),
    path('searchoneinterface/', views.searchoneinterface),
    path('useBlockchain/', views.useBlockchain),

    # 数据沙箱界面
    path('sjsx-interface/', views.sjsx_interface),
    path('createinterfacesx/', views.createinterfacesx),
    path('searchinsbsxterface/', views.searchinsbsxterface),

    path('sjtzadd/', views.sjtzadd),
path('useBlockchainshaxiang/', views.useBlockchainshaxiang),
path('shaxiangip/', views.shaxiangip),
path('shaxiangipbox/', views.shaxiangipbox),
    path('create-sandbox/', views.createsandbox),
    path('create-ip/', views.createip),
path('insert-readonly-link/', views.insertreadonlylink),
    path('create-ipbox/', views.createipbox, name='createipbox'),

path('sjsxinterface-edit/', views.sjsxinterface_edit),
path('delete_sandbox_info/', views.delete_sandbox_info),

    path('sysxsearchoneinterface/', views.sysxsearchoneinterface),
path('sysxdeleteinterface/', views.sysxdeleteinterface),
path('upload_to_sandbox/', views.upload_to_sandbox),

path('xqflist_open/', views.xqflist_open),
path('getreadonlylink/', views.getreadonlylink),
# 沙箱接口
# path('api/listSandboxes', views.list_sandboxes),
# path('api/createSandbox', views.create_sandbox),
# path('api/destroySandbox/<str:sandbox_name>', views.destroy_sandbox),





    #以下为旧平台方法
    path('index/', views.index),
    path('mutiindex/', views.mutiindex),
    path('member-list/', views.member_list),
    path('member-add/', views.member_add),
    path('member-edit/', views.member_edit),
    path('welcome/', views.welcome),

    # 参与者管理页面
    path('guest-list/', views.guest_list),
    path('guest-add/', views.guest_add),
    path('guest-edit/', views.guest_edit),
    path('deleteguest/', views.deleteguest),
    # 参与者管理方法
    path('createguest/', views.createguest),
    path('editguest/', views.editguest),
    path('pingtest/', views.ping_view),
    # 返回全部用户信息
    path('searchguest/', views.searchguest),

    #模型训练页面
    path('model-list/', views.model_list),
    path('model-add/', views.model_add),
    path('modeldel-list/<str:parameter>/', views.modeldel_list),
    path('modeldel-add/<str:parameter>/', views.modeldel_add),
    #模型管理方法
    path('searchmodel/', views.searchmodel),
    path('searchmodeldel/', views.searchmodeldel),
    path('createmodel/', views.createmodel),
    path('deletemodel/', views.deletemodel),
    path('upload/', views.upload_modelapply),
    path('updatemodeldel/', views.updatemodeldel),
    path('updatemodel1/', views.updatemodel1),
    path('updatemodel/', views.updatemodel),
    path('deletemodeldel/', views.deletemodeldel),

    path('createmodeldel/', views.createmodeldel),

    path('modeltest/', views.model_test),#测试

    #样本对齐
    path('sample-alignment/', views.sample_alignment),
    #搜索样本对齐状态
    path('searchSampleAlignment/', views.searchSampleAlignment),

    #模型训练结果查看
    path('train-model/', views.train_model),
    path('train_model_board/', views.train_model_board),
    path('train_model_boardnew/', views.train_model_boardnew),

    #项目管理
    path('project_notarization/', views.project_notarization),
    path('pengding_project/', views.pending_project),

    # path('datasharing_add/', views.datasharing_add),
    # 返回所有存证信息
    path('search_notarization/', views.search_notarization),
    # 返回按项目名称查询存证信息
    path('search_notarization_by_projectname/', views.search_notarization_by_projectname),

    #模型应用
    path('model-application/', modelappview.model_application),
    path('model-application_search/', modelappview.searchModelApplication),
    path('application_status_modify/', modelappview.editModelApplicationStatus),
    path('application_model-main/', modelappview.model_main),
    path('application_model-main_search/', modelappview.searchmodel),
    path('application_result/', modelappview.application_result),
    path('application_result_search/', modelappview.searchapplication_result),
    path('application_result_shappng/<int:i>', modelappview.application_result_shappng),
    path('application_result_analysis/', modelappview.application_result_analysis),
    path('application_result_open_file_manager/', modelappview.open_file_manager),
    path('model-predict/', modelappview.model_predict),
    path('model_predict_port/', modelapp_portview.model_predict_port),
    # path('model-application-port/', modelapp_portview.model_application),
    # path('model-application_search-port/', modelapp_portview.searchModelApplication),
    # path('application_status_modify-port/', modelapp_portview.editModelApplicationStatus),
    # path('offer_status_modify-port/', modelapp_portview.editModelOfferStatus),
    path('offer_status_modify/', modelappview.editModelOfferStatus),


    #外部调用
    path('port_method/', viewsmult.port_method),
    path('check_apply_re/', api_views.check_apply_re),
    #打开文件资源管理器
    path('open_file_manager/<str:parameter>/', open_views.open_file_manager),
    path('open_file_manager/', open_views.open_file_manager),
    path('open_file_manager1/', open_views.open_file_manager1),
    path('application_result_shappng/<int:i>', open_views.application_result_shappng),


    # 参与者管理页面
    path('multguest-list/', viewsmult.multguest_list),
    path('multguest-add/', viewsmult.multguest_add),
    # 参与者管理方法
    path('multeditguest/', viewsmult.editmultguest),
    path('multpingtest/', viewsmult.multpingtest),
    # 返回全部用户信息
    path('searchmultguest/', viewsmult.searchmultguest),
    path('getagreement/', viewsmult.getagreement),
    path('createmultguest/', viewsmult.createmultguest),
    #返回指定id的w外部合作者信息
    path('getMultInfoById/', viewsmult.getMultInfoById),
    path('multguestedit/',viewsmult.multguestedit),

    #样本对齐
    path('multsample-alignment/', viewsmult.sample_alignment),
    #搜索样本对齐状态
    path('multsearchSampleAlignment/', viewsmult.searchSampleAlignment),

    #模型训练结果查看
    path('multtrain-model/', viewsmult.train_model),
    # 模型明细页面
    path('multmodel-add/', viewsmult.multmodel_add),
    path('multmodeldel-list/<str:parameter>/', viewsmult.multmodeldel_list),
    path('searchmultmodeldel/', viewsmult.searchmultmodeldel),
    path('createmultmodeldel/', viewsmult.createmultmodeldel),
    path('multmodeldel-add/', viewsmult.multmodeldel_add),


    # 模型管理方法
    path('searchmultmodel/', viewsmult.searchmultmodel),
    path('getmodelagreement/', viewsmult.getmodelagreement),
    path('createmultmodel/', viewsmult.createmultmodel),
    path('multmodel-list/', viewsmult.multmodel_list),
    path('multupload/', viewsmult.upload_multmodelapply),
    path('multmodeltest/', viewsmult.multmodel_test),  # 测试


    # 数据确权记录相关URLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    path('data-confirmation/', views.data_confirmation_list, name='data_confirmation_list'),
    path('data-confirmation/detail/<str:record_id>/', views.data_confirmation_detail, name='data_confirmation_detail'),

    # 申请数据确权相关URL
    path('data-confirmation/apply/', views.data_right_application_add, name='data_right_application_add'),

    # 审核数据确权相关URL
    path('data-confirmation/review/', views.data_right_application_list, name='data_right_application_list'),
    path('data-confirmation/review/<str:application_id>/', views.data_right_application_review,
         name='data_right_application_review'),
#略
    path('data-confirmation/delete/<str:record_id>/', views.delete_data_confirmation_record, name='delete_data_confirmation_record'),
    path('data-confirmation/batch-delete/', views.batch_delete_data_confirmation_records, name='batch_delete_data_confirmation_records'),
    # AJAX接口URL
    path('api/data-confirmation/application/<str:application_id>/', views.get_application_detail,
         name='get_application_detail'),

    # 数据确权记录相关URLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    # 数据资产管理
    path('data_asset_list/', views.data_asset_list, name='data_asset_list'),  # 确保配置正确
    path('data_asset_add/', views.add_data_asset, name='data_asset_add'),
    path('data_asset_edit/<int:asset_id>/', views.edit_data_asset),
    path('batch-delete-data-asset/', views.batch_delete_data_asset, name='batch_delete_data_asset'),


    # path('fetch/', views.fetch_and_save_asset_data, name='fetch_asset_data'),
    path('records/', views.asset_record_list, name='asset_record_list'),

    # 外部调用
    path('mult_check_apply_re/', api_multviews.mult_check_apply_re),

    # 打开文件资源管理器
    path('mult_open_file_manager/', mult_open_views.mult_open_file),
    path('mult_open_png/', mult_open_views.mult_open_png),


    # 模型应用
    path('multapplication_model-main/', viewsmult.multmodel_main),
    path('multapplication_result/', viewsmult.multapplication_result),
    path('multapplication_model-main_search/', viewsmult.searchmultmodel_appl),
    path('multmodel-application/', viewsmult.multmodel_application),
    path('multmodel-apply-add/', viewsmult.multmodel_applyadd),
    path('createmultmodelapply/', viewsmult.createmultmodelapply),
    path('multmodel_apply_list/', viewsmult.multmodel_apply_list),
    path('multmodel_application_result_open_file_manager/', viewsmult.open_file_manager),
    path('multmodel_application_result_search/', viewsmult.multmodel_application_result_search),
    path('multmodel_application_result_shappng/<int:i>', open_views.multmodel_application_result_shappng),
    path('getmultmodel_apply/<int:i>', viewsmult.getmultmodel_apply),
    path('runModel/<int:i>', viewsmult.runModel),

    path('multmodel-predict/', viewsmult.multimodel_predict),
    path('multmodel_predict_port/', viewsmult.multmodel_predict_port),


    path('multmodel_application_result_analysis/', viewsmult.multmodel_application_result_analysis),
    path('multmodel_application_status_modify/', viewsmult.editMultModelApplicationStatus),

    # 项目管理
    # 项目管理
    path('established_project/', views.established_project),
    path('pengding_project/', views.pending_project),
    path('project_add/', views.project_add),
    path('create_project/', views.create_project),
    path('audit_project/', views.audit_project),
    path('submit_project/', views.submit_project),

    path('submit_project_toblockchain/', views.submit_project_toblockchain),
    path('get_project_data/', views.get_project_data),
    path('search_project_data/', views.search_project_data),
    path('search_pending_project_data/', views.search_pending_project_data),
    path('get_pending_project_data/', views.get_pending_project_data),
    path('delete_project/', views.delete_project),
    path('update_project/', views.update_project),

    # ip追踪
    path('data-model/', views.data_model),
    # path('show_latest_ip/', show_latest_ip, name='show_latest_ip'),
    # path('admin/', admin.site.urls),
   # path('myapp/', include('myapp.urls')),  # 包含 myapp 的 URL 配置
    path('get_data/', get_data, name='get_data'),  # 让主界面直接访问 /get_data/

]

