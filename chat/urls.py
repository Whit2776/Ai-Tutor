from django.urls import path
from . import views

urlpatterns = [
  path('chatroom', views.chatroom, name = 'chatroom'),
  path('contact-list', views.family_members, name = 'family_members'),
  path('<str:link>', views.chat, name = 'chat'),
]