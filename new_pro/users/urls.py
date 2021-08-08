from django.urls import path
from users.views import RegisterView, ImageCodeView

urlpatterns=[
    #(路由，视图函数名)
    path('register/',RegisterView.as_view(),name='register'),
    #图片验证码
    path('imagecode/',ImageCodeView.as_view(),name='imagecode')
]