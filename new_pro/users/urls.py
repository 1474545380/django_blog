from django.urls import path
from users.views import RegisterView

urlpatterns=[
    #(路由，视图函数名)
    path('register/',RegisterView.as_view(),name='register'),
]