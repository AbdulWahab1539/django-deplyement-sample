from django.urls import path, include
from auth_app import views


app_name = 'auth_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login')
]