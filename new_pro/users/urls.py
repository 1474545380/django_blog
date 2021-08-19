from django.urls import path
from users.views import RegisterView, ImageCodeView, SmsCodeView, LoginView,LogoutView,ForgetPasswordView,UserCenterView

urlpatterns=[
    #(路由，视图函数名)
    #注册页面
    path('register/',RegisterView.as_view(),name='register'),
    #图片验证码
    path('imagecode/',ImageCodeView.as_view(),name='imagecode'),
    #短信验证码
    path('smscode/',SmsCodeView.as_view(),name='smscode'),
    #登陆页面
    path('login/',LoginView.as_view(),name='login'),
    #登出
    path('logout/',LogoutView.as_view(),name='logout'),
    #忘记密码
    path('forgetpassword/',ForgetPasswordView.as_view(),name='forgetpassword'),
    #用户中心
    path('center/',UserCenterView.as_view(),name='center'),
]