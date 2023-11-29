from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="ticketmaster-index"),
    path('favorites/', views.favorites_view, name="ticketmaster-favorites"),
]