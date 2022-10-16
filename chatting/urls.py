from django.urls import path
from . import views

urlpatterns = [
    path("front", views.front, name='front'),
    path("rooms", views.rooms, name='rooms'),
    path('room/<slug:slug>/', views.room, name='room'),
]