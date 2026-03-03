from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from login.api.serializers import *
from login.brevo import send_brevo_email

from app_1.models import *

from chat.models import *

from PIL import Image
from io import BytesIO
from uuid import uuid4
from datetime import timedelta

from login.utils  import login

from django.urls import reverse

def resize_image(image_file, max_width=500, max_height=500):
  """
  Resize the image while keeping aspect ratio.
  Returns a Django-friendly ContentFile.
  """
  img = Image.open(image_file)
  img.thumbnail((max_width, max_height))  # maintains aspect ratio

  # Save the resized image to memory
  img_io = BytesIO()
  img_format = img.format if img.format else 'PNG'
  img.save(img_io, format=img_format)
  img_content = ContentFile(img_io.getvalue(), name=image_file.name)

  return img_content

@api_view(['POST'])
def sign_up(request):
  r = request.data
  
  with transaction.atomic():
    person_serializer = PersonSerializer(data = r)
    if not person_serializer.is_valid():
      return Response({'success': False, 'errors': person_serializer.errors}, status=status.HTTP_403_FORBIDDEN)
    person = person_serializer.save()
    email_link = Email_Link.objects.create(email = person.email)
    set_up = request.build_absolute_uri(reverse('set_password', args = [person.link, email_link.token]))
    
    send_brevo_email(
      template_id=7,
      to_email=person.email,
      to_name=person.name or person.user_name or person.first_name,
      params={
        "company_name": settings.COMPANY_NAME,
        "user_name": person.name or person.user_name or person.first_name,
        "set_up":set_up
      },
    )
    redirect_url = request.build_absolute_uri(reverse('check_email'))
  
  return Response({'success':True, 'redirect_url': redirect_url})

@api_view(['POST'])
def set_password(request, link, token):
  r = request.data
  person = Person.objects.filter(link = link).first()
  email_link = Email_Link.objects.filter(token = token).first()
  
  if not person or not email_link:
    return Response({'success': False, 'message':'Link Invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)
  
  p1 = r.get('pass-1')
  p2 = r.get('pass-2')
  
  if p1 != p2:
    return Response({'success': False, 'message': 'Passwords do not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)  
  person.password = make_password(p1)
  person.save(update_fields=['password'])
  login(request, person)
  email_link.used = True
  email_link.save(update_fields=['used'])
  redirect_url = request.build_absolute_uri(reverse('chat_box'))
  return Response({'success':True, 'redirect_url':redirect_url})


@api_view(['POST'])
def log_in(request):
  r = request.data
  user_name = r.get('user_name')
  password = r.get('password')
  
  person = Person.objects.filter(user_name = user_name).first()
  
  if not person or not check_password(password, person.password):
    print('Pass word not correct')
    return Response({'success':False}, status=status.HTTP_404_NOT_FOUND)

  login(request, person)
  return Response({'success': True})

@api_view(['GET'])
def log_out(request):
  del request.session['person_id']
  return Response({'':''})


# @api_view(['POST'])
# def admin_login(request):
#   r = request.data
  
#   admin_id = r.get('admin_id')
#   password = r.get('password')
  
#   admin = Member.objects.get(member_id = admin_id)
#   if not check_password(password, admin.password):
#     return Response({'type':'error', 'message':'Incorrect Credentials'})
  
#   if not admin.permissions.can_use_admin_system:
#     return Response({'type': 'error', 'message': 'You have no access to this page', 'status':False})
#   request.session['admin_id'] = admin_id
#   return Response({"":""})

# @api_view(['POST'])
# def create_family(request):
#   r = request.data
#   family_name = r.get('family-name')
#   description = r.get('family-description')
#   email = r.get('email')
  
#   if family_name.strip() == '' or description.strip() == '' or email.strip() == '' or not '@' in email:
#     return Response({'success': False, 'message':'Kindly fill in all required fields properly'}, status=status.HTTP_400_BAD_REQUEST)
  
#   with transaction.atomic():
#     try:
#       family = Family.objects.create(name = family_name, description='description', link = uuid4())
      
      
#       email_link = EmailLink.objects.create(email = email, type='admin-sign-up')
      
      
#       set_up = request.build_absolute_uri(reverse('admin-sign-up',args= [family.link, email_link.token ]))
      
#       send_brevo_email(1, email, family.name, params={
#         "family_name":family.name,
#         "set_up":set_up
#       })
      
#     except Exception as e:
#       print('Error, could not create family, ', e)
#       return Response({'success': False, 'message': f'Error, \n {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
    
#   return Response({'type':'Alert', 'message': 'You have successfully created a family. Kindly check your email for a link to set up your admin profile.'})

# @api_view(['POST'])
# def set_password(request, member_id):
#   r = request.data
#   member = Member.objects.filter(member_id = member_id).first()
#   family = member.family
#   perms = request.perms
  
#   if not perms.can_activate_links:
#     return Response({'type':'Error', 'message':'Haha, real funny'})
#   if not member:
#     return Response({'type':'Error', 'message':'Member not found'})
  
  
#   email_link = EmailLink.objects.create(email = member.email, type='set-password', expires_at = timezone.now() + timedelta(minutes = 10))
  
#   set_up_link = request.build_absolute_uri(reverse('set-password', args =[member.link, email_link.token]))
  
#   send_brevo_email(3, member.email, member.name, params={
#     "user_name":member.name,
#     "company_name":"Ran Inc",
#     "member_id":member.member_id,
#     "set_up":set_up_link
#   })
#   return Response({'success':True, 'message':'Successfully created link', 'set_up_link':set_up_link}, status=status.HTTP_200_OK)
