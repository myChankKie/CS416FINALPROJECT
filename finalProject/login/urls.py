from django.urls import path, include
from . import views

urlpatterns = [
    path('1/', views.login_view, name='login'),
    path('2/', views.create_account_view, name='create-account'),
    path('3/', views.logout_view, name='logout'),

]