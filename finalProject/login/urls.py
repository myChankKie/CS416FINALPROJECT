from django.urls import path
from . import views

urlpatterns = [
    path('1/', views.login, name='login'),
    path('2/', views.create_account, name='create-account')
]