"""admin URL Configuration

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
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from admin import settings
from system.base.dict import *
from system.base.file import *
from system.base.login import *
from system.base.notice import *
from system.base.permission import *
from system.base.register import *
from system.base.role import *
from system.base.user import *
from business.views.member import *
from business.views.recruit import *
from business.views.lost import *
from business.views.category import *
from business.views.cart import *
from business.views.orders import *
from business.views.banner import *
from business.views.front import *


urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('logout/<str:id>', LogoutView.as_view()),
    path('user', UserView.as_view(),name="user"),
    path('user/<int:pk>', UserView.as_view(), name='user_detail'),
    path('user/page', UserPageView.as_view(), name="user_page"),
    path('user/del/batch', UserBatchDeleteAPIView.as_view(),name="user_batch_delete"),
    path('user/export', UserExport.as_view(),name="user_export"),
    path('updateUser', UserInfoUpdate.as_view(),name="user_info_update"),
    path('password/change', UserUpdatePwd.as_view(),name="user_update_pwd"),
    path('role', RoleView.as_view(),name="role"),
    path('role/<int:pk>', RoleView.as_view(), name='role_detail'),
    path('role/page', RolePageView.as_view(), name="role_page"),
    path('role/del/batch', RoleBatchDeleteAPIView.as_view(), name="role_batch_delete"),
    path('role/export', RoleExport.as_view(),name="role_export"),
    path('permission', PermissionView.as_view(),name="permission"),
    path('permission/<int:pk>', PermissionView.as_view(), name='permission_delete'),
    path('permission/del/batch', PermissionBatchDeleteAPIView.as_view(), name="permission_batch_delete"),
    path('permission/export', PermissionExport.as_view(),name="permission_export"),
    path('dict', DictView.as_view(), name="dict"),
    path('dict/<int:pk>', DictView.as_view(), name='dict_detail'),
    path('dict/page', DictPageView.as_view(), name="dict_page"),
    path('dict/del/batch', DictBatchDeleteAPIView.as_view(), name="dict_batch_delete"),
    path('dict/export', DictExport.as_view(),name="dict_export"),
    path('file/upload', FileUploadView.as_view(),name="file_upload"),
    path('file/uploadImg', FileUploadEditorView.as_view(),name="file_upload_editor"),
    path('notice', NoticeView.as_view(), name="notice"),
    path('notice/<int:pk>', NoticeView.as_view(), name='notice_detail'),
    path('notice/page', NoticePageView.as_view(), name="notice_page"),
    path('notice/del/batch', NoticeBatchDeleteAPIView.as_view(), name="notice_batch_delete"),
    path('notice/export', NoticeExport.as_view(), name="notice_export"),

    # user
    path('member', MemberView.as_view(), name="member"),
    path('member/<int:pk>', MemberView.as_view(), name='member_detail'),
    path('member/page', MemberPageView.as_view(), name="member_page"),
    path('member/del/batch', MemberBatchDeleteAPIView.as_view(), name="member_batch_delete"),
    path('member/export', MemberExport.as_view(), name="member_export"),
    path('front/member/user/<int:userId>', getMemberByUserId.as_view(), name="getMemberByUserId"),
    path('front/member/update', UpdateMember.as_view(), name="UpdateMember"),

    # Lost and Found
    path('recruit', RecruitView.as_view(), name="recruit"),
    path('recruit/<int:pk>', RecruitView.as_view(), name='recruit_detail'),
    path('recruit/page', RecruitPageView.as_view(), name="recruit_page"),
    path('recruit/del/batch', RecruitBatchDeleteAPIView.as_view(), name="recruit_batch_delete"),
    path('recruit/export', RecruitExport.as_view(), name="recruit_export"),
    path('front/recruit/update', UpdateRecruit.as_view(), name="UpdateRecruit"),
    # Report lost items
    path('lost', LostView.as_view(), name="lost"),
    path('lost/<int:pk>', LostView.as_view(), name='lost_detail'),
    path('lost/page', LostPageView.as_view(), name="lost_page"),
    path('lost/del/batch', LostBatchDeleteAPIView.as_view(), name="lost_batch_delete"),
    path('lost/export', LostExport.as_view(), name="lost_export"),
    path('front/lost/update', UpdateLost.as_view(), name="UpdateLost"),
    # Item Type
    path('category', CategoryView.as_view(), name="category"),
    path('category/<int:pk>', CategoryView.as_view(), name='category_detail'),
    path('category/page', CategoryPageView.as_view(), name="category_page"),
    path('category/del/batch', CategoryBatchDeleteAPIView.as_view(), name="category_batch_delete"),
    path('category/export', CategoryExport.as_view(), name="category_export"),
    path('front/category/update', UpdateCategory.as_view(), name="UpdateCategory"),
    # Information to be claimed
    path('cart', CartView.as_view(), name="cart"),
    path('cart/<int:pk>', CartView.as_view(), name='cart_detail'),
    path('cart/page', CartPageView.as_view(), name="cart_page"),
    path('cart/del/batch', CartBatchDeleteAPIView.as_view(), name="cart_batch_delete"),
    path('cart/export', CartExport.as_view(), name="cart_export"),
    path('front/cart/update', UpdateCart.as_view(), name="UpdateCart"),
    # Lost and found records
    path('orders', OrdersView.as_view(), name="orders"),
    path('orders/<int:pk>', OrdersView.as_view(), name='orders_detail'),
    path('orders/page', OrdersPageView.as_view(), name="orders_page"),
    path('orders/del/batch', OrdersBatchDeleteAPIView.as_view(), name="orders_batch_delete"),
    path('orders/export', OrdersExport.as_view(), name="orders_export"),
    path('front/orders/update', UpdateOrders.as_view(), name="UpdateOrders"),
	
    # Slideshow
    path('banner', BannerView.as_view(), name="banner"),
    path('banner/<int:pk>', BannerView.as_view(), name='banner_detail'),
    path('banner/page', BannerPageView.as_view(), name="banner_page"),
    path('banner/del/batch', BannerBatchDeleteAPIView.as_view(), name="banner_batch_delete"),
    path('banner/export', BannerExport.as_view(), name="banner_export"),

    # Front-end-user
    path('front/user/list', UserListDetail.as_view(), name="front_user_list"),
    path('front/user/<int:pk>', UserListDetail.as_view(), name='front_user_detail'),
    path('front/user/page', UserPage.as_view(), name="front_user_page"),
    # Front Desk - Website Announcement
    path('front/notice/list', NoticeListDetail.as_view(), name="front_notice_list"),
    path('front/notice/<int:pk>', NoticeListDetail.as_view(), name='front_notice_detail'),
    path('front/notice/page', NoticePage.as_view(), name="front_notice_page"),
    # Front-stage - slide show
    path('front/banner/list', BannerListDetail.as_view(), name="front_banner_list"),
    path('front/banner', BannerListDetail.as_view(), name="front_banner"),
    path('front/banner/<int:pk>', BannerListDetail.as_view(), name='front_banner_detail'),
    path('front/banner/page', BannerPage.as_view(), name='front_banner_page'),
    # Front-end-user
    path('front/member/list', MemberListDetail.as_view(), name="front_member_list"),
    path('front/member', MemberListDetail.as_view(), name="front_member"),
    path('front/member/<int:pk>', MemberListDetail.as_view(), name='front_member_detail'),
    path('front/member/page', MemberPage.as_view(), name='front_member_page'),
    # Front Desk - Lost and Found Information
    path('front/recruit/list', RecruitListDetail.as_view(), name="front_recruit_list"),
    path('front/recruit', RecruitListDetail.as_view(), name="front_recruit"),
    path('front/recruit/<int:pk>', RecruitListDetail.as_view(), name='front_recruit_detail'),
    path('front/recruit/page', RecruitPage.as_view(), name='front_recruit_page'),
    # Front Desk - Lost Items Information
    path('front/lost/list', LostListDetail.as_view(), name="front_lost_list"),
    path('front/lost', LostListDetail.as_view(), name="front_lost"),
    path('front/lost/<int:pk>', LostListDetail.as_view(), name='front_lost_detail'),
    path('front/lost/page', LostPage.as_view(), name='front_lost_page'),
    # Front Desk-Item Type
    path('front/category/list', CategoryListDetail.as_view(), name="front_category_list"),
    path('front/category', CategoryListDetail.as_view(), name="front_category"),
    path('front/category/<int:pk>', CategoryListDetail.as_view(), name='front_category_detail'),
    path('front/category/page', CategoryPage.as_view(), name='front_category_page'),
    # Front Desk - Information to be claimed
    path('front/cart/list', CartListDetail.as_view(), name="front_cart_list"),
    path('front/cart', CartListDetail.as_view(), name="front_cart"),
    path('front/cart/<int:pk>', CartListDetail.as_view(), name='front_cart_detail'),
    path('front/cart/page', CartPage.as_view(), name='front_cart_page'),
    # Front Desk - Lost and Found Records
    path('front/orders/list', OrdersListDetail.as_view(), name="front_orders_list"),
    path('front/orders', OrdersListDetail.as_view(), name="front_orders"),
    path('front/orders/<int:pk>', OrdersListDetail.as_view(), name='front_orders_detail'),
    path('front/orders/page', OrdersPage.as_view(), name='front_orders_page'),

    #Modify shopping cart
    path('front/cart/update', UpdateCart.as_view(), name="front_updateCart"),


    #Add/Modify Order
    path('front/orders/update', UpdateOrders.as_view(), name="front_updateOrders"),
    #Cancellation of order
    path('front/orders/cancel/<int:pk>', CancelOrders.as_view(), name="front_cancelOrders"),








] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
