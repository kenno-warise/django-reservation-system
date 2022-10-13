from django.urls import path

from . import views

app_name = "reserve"

urlpatterns = [
        path('index/', views.index, name='index'),
        path('confirm/', views.confirm, name='confirm'),
        path('complete/', views.complete, name='complete'),
        path('login/', views.Login.as_view(), name='login'),
        path('logout/', views.Logout.as_view(), name='logout'),
        path('reserve_list/', views.reserve_list, name='reserve_list'),
        path('setting/<int:id>', views.setting, name='setting'),
        path('pulldown_access/', views.pulldown_access, name='pulldown_access'),
]
