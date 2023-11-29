from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="ticketmaster-index"),
    path('add/<int:event_id>/', views.add_favorite, name="ticketmaster-add-favorite"),
    path('favorites/', views.favorites_view, name="ticketmaster-favorites"),
]