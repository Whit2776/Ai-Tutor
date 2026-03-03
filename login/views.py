from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from login.models import Person, Email_Link
from django.http import HttpResponse
from .utils import render_page, login


def login(request):
  return render(request, 'login.html')

def sign_up(request):
  return render(request, 'sign-up.html')

def set_password(request, link, token):
  email_link = Email_Link.objects.filter(token = token).first()
  person = Person.objects.filter(link = link).first()
  if not email_link or not person:
    return render(request, 'validators/link_invalid.html')
  elif email_link.used:
    return render(request, 'validators/link_used.html')
  
  elif email_link.is_expired:
    return render(request, 'validators/link_expired.html')
  return render(request, 'set-password.html')

def test_auth(request):
  if request.person:
    return HttpResponse(f"Logged in as: {request.person.name}")
  return HttpResponse("Not logged in")