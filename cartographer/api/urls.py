from django.urls import path
from . import views
urlpatterns = [
    path('ping/', views.ping_view, name = 'ping'),
    path('get_most_recent_entities/', views.get_most_recent_entities, name = 'get_most_recent_entities'),
    path('get_most_recent_ten_dev/', views.get_most_recent_ten_dev, name = 'get_most_recent_ten_dev'),
]
