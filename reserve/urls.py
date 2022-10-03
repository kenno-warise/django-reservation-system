from django.urls import path

from . import views

app_name = "reserve"

urlpatterns = [
        path('index/', views.index, name='index'),
        path('confirm/', views.confirm, name='confirm'),
        path('complete/', views.complete, name='complete'),
        path('reserve_list/', views.reserve_list, name='reserve_list'),
        path('setting/', views.setting, name='setting'),
]
