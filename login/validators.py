from django.shortcuts import render

def check_email(request):
  return render(request, 'validators/check_email.html')