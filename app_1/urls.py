from django.urls import path
from .import views
urlpatterns = [
  path('chat-box', views.chat_box, name='chat_box'),
]