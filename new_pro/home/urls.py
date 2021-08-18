from django.urls import path
from new_pro.home.views import IndexView
urlpatterns=[
    path('',IndexView.as_view(),name='index')
]