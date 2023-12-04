from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="ticketmaster-index"),
    path('add/<int:event_id>/', views.add_favorite, name="ticketmaster-add-favorite"),
    path('create/', views.create_favorite, name='ticketmaster-create-favorite'),
    path('favorites/', views.favorites_view, name="ticketmaster-favorites"),
    path('update/<int:event_id>',views.update_favorite,name="ticketmaster-update-favorite"),
    path('delete/<int:event_id>',views.delete_favorite,name="ticketmaster-delete-favorite")
]