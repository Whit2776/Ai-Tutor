from django.shortcuts import redirect, render
from login.models import Person
from functools import wraps


def login_required(view_func):
  @wraps(view_func)
  def wrapper(request, *args, **kwargs):
    person = request.person
    if not person:
      return redirect('login')
    return view_func(request, *args, **kwargs)
  return wrapper

# def admin_login_required(view_func):
#   @wraps(view_func)
#   def wrapper(request, *args, **kwargs):
#     id = request.session.get('admin_id')
#     if not id:
#       return redirect('admin-login')
#     member = Member.objects.filter(member_id = id).first()
#     request.family = member.family
#     request.member = member
#     return view_func(request, *args, **kwargs)
#   return wrapper