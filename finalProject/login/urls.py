from django.urls import path, include
from . import views

urlpatterns = [
    path('1/', views.login, name='login'),
    path('2/', views.create_account, name='create-account'),

]