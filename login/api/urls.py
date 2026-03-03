from django.urls import path
from login.api import views

urlpatterns = [
  path('sign-up', views.sign_up,),
  path('login', views.login),
  path('log-out', views.log_out),
  path('set-password/<str:link>/<str:token>', views.set_password),
]
