from django.urls import path
from . import views, validators

urlpatterns = [
  path('login', views.login, name='login'),
  path('sign-up', views.sign_up, name='sign_up'),
  path('set-password/<str:link>/<str:token>', views.set_password, name ='set_password'),
  path('check_email', validators.check_email, name = 'check_email')
]