from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.api.serializers import *
from app_1.models import *
from chat.models import *
from app_1.views import *

from datetime import datetime
from django.utils.timezone import make_aware
from decimal import Decimal, ROUND_HALF_UP
import os
from django.db.models import Count
from django.db import transaction
from django.urls import reverse
from rest_framework import status

def get_ext_name (file_path):
  file_name, file_extension = os.path.splitext(str(file_path))
  return file_name, file_extension

def get_type (file):
  return file.content_type
  
@api_view(['GET'])
def get_messages(request, link, num):
  member = request.member
  chat = Chat.objects.get(link = link)
  messages = chat.messages.all().order_by('created')
  files_json = None

  is_group = chat.is_group
  
  if not is_group:
    received_messages = member.received_messages.filter(chat = chat)
    
    for m in received_messages:
      m.state = 'Read'
      m.save()

  serializer = MesSerializer(messages, many =True)
  data = serializer.data
  
  for d in data:
    files = list(File.objects.filter(message = Mes.objects.get(id = d['id'])))
    d['files'] = []
    
    if len(files) > 0:
      files_json = [
        {
          "id": f.id,
          "path": f.path.url if f.path else None,
          "type": f.type,
          "name": f.name,
          "size": f.size,
        }
        for f in files
      ]
      d['files'] = files_json

  return Response({'data':data, 'is_group': is_group})

@api_view(['GET'])
def get_message(request, link):
  member = request.member
  files_json = None
  
  chat = Chat.objects.filter(link = link, users = member).first()
  
  if not chat:
    return Response({'success':False, 'message':'Chat not found', 'status': 404})
  
  last_message = chat.messages.order_by('-created').first()
  
  is_group = chat.is_group
  
  
  dif = Decimal((make_aware(datetime.now()) - last_message.created).total_seconds()) if last_message != 0 else 0
  
  if dif > 3:
    return Response({'success':False, 'message': 'Last message was sent over 3 seconds ago', 'status':404})
  
  serializer = MesSerializer(last_message)
  data = serializer.data
  files = list(File.objects.filter(message = last_message))
  data['files'] = []
  if len(files) > 0:
    files_json = [
      {
        "id": f.id,
        "path": f.path.url if f.path else None,
        "type": f.type,
        "name": f.name,
        "size": f.size,
      }
      for f in files
    ]
    data['files'] = files_json
    
  return Response({'data':data, 'is_group':is_group, 'status': 200})
    
  
@api_view(['POST'])
def post_message(request, link):
  r = request.data
  f = request.FILES
  member = request.member
  family = member.family
  chat = Chat.objects.get(link = link)
  message = None
  
  d_message = r.get('message')
  d_replyto = r.get('reply_to_id')
  
  ty = r.get('message-type')
  
  with transaction.atomic():
    if chat.is_group:
      if ty == '' or ty == 'normal':
        message = Mes.objects.create(chat = chat, message = d_message, sender=member)
      elif ty == 'reply':
        message = Mes.objects.create(chat = chat, message = d_message, sender=member, type = ty, reply_to = d_replyto)
    else:
      if ty == '':
        message = Mes.objects.create(chat = chat, message = d_message, sender=member, receiver=chat.get_other_user(member.id))
      elif ty == 'reply':
        message = Mes.objects.create(chat = chat, message = d_message, sender=member, receiver=chat.get_other_user(member.id), type = ty, reply_to = d_replyto)
      elif ty == 'forward':
        ids = r.getlist('message-id')
        chats = r.getlist('chat')
        
        if not ids:
          return Response({'type': 'Error', 'message':'Ids not submitted'})
        
        if not chats:
          return Response({'type': 'Error', 'message':'Chats not submitted'})
        
        for id in ids:
          mes = Mes.objects.filter(id = id).first()
          if not mes:
            return Response({'type': 'Error', 'message':'Exact message not found'})
            
          files = File.objects.filter(message = mes)
          
          for c in chats:
            chat = Chat.objects.get(link = c)
            message = Mes.objects.create(chat = chat, message = mes.message, sender = member, receiver = chat.get_other_user(member.id), type = ty)
            if len(files) != 0:
              for g in files:
                file = File.objects.create(family = family, name=g.name, path = g.path, ext = g.ext, message = message, type=g.type, chat = chat)
    if not message:
      return Response({'success':False, 'message':'Message not created', 'status':401})
    chat.order = message.created
    chat.save()

    for file in f.getlist('files'):
      name, ext = get_ext_name(file)
      fie = File.objects.create(family = family, name=name, path = file, ext = ext, message = message, type=get_type(file), chat = chat)

    
    message.state = 'delivered'
    message.save()

  return Response({'Success':True, 'message':'Message sent', 'Is group':chat.is_group})

@api_view(['POST'])
def delete_message(request):
  r = request.POST
  for id in r.getlist('ids'):
    mes = Mes.objects.get(id = id)
    mes.delete()
    
  return Response({'type':'alert', 'message': 'Successfully Deleted', 'success':True})

def create_chat_logic( member, other_member):
  key = f'{max(member.id, other_member.id)}_{min(member.id, other_member.id)}'
  chat = Chat.objects.filter(chat_key=key).first()
  
  if chat:
    return chat, False
  
  
  with transaction.atomic():
    chat = Chat.objects.create()
    chat.chat_key = key
    
    chat.save(update_fields = ['chat_key'])
    
    chat.users.add(member, other_member)
    message = Mes.objects.create(chat = chat, message = 'You have been Connected', type = 'system')
  return chat, True
  
@api_view(['POST'])
def create_chat(request):
  r = request.data
  member = request.member
  family = member.family
  z = r.get('family-member') 
  id = z.strip() if z else None
  
  if not id:
    return Response({'success':False, 'message':'Member does not exist'})
  other_member = Member.objects.filter(member_id = id, family=family).first()
  
  if not other_member:
    return Response({'success':False, 'message':'Member does not exist'})
  
  if not other_member.status == 'verified' or not other_member.is_active:
    return Response({'success':False, 'message':'You cannot send a message to this member'})
  
  chat = create_chat_logic(member, other_member)
  return Response({'success': True, 'link':chat.get_link(), 'message':'Started Chat with user'})

@api_view(['GET'])
def get_chat_media(request, link):
  member = request.member
  if not member:
    return Response({'success':False, 'message': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
  
  chat = Chat.objects.filter(users = member, link = link).first()
  if not chat:
    return Response({'success':False, 'message': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
  
  files = chat.files.all().order_by('-created')[:30]
  serializer = FileSerializer(files, many = True)
  
  return Response({'success':True, 'message': 'Files found', 'files':serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_new_chat(request):
  r = request.data
  member = request.member
  family = request.family
  members = family.members.all()
  other_member = members.filter(member_id = r.get('member_id')).first()
  group_name = r.get('group_name')
  if group_name:
    if not group_name.strip():
      return Response({"success": False, "messsage": "Groups cannot have empty names"})
    
    group_members = r.getlist('group_member')
    
    with transaction.atomic():
      group = Chat.objects.create(is_group = True, admin = member, name = group_name.strip())
      first_message = Mes.objects.create(chat= group, message=f'Group created by {member.name}', type='system')
      members = Member.objects.filter(member_id__in = group_members)
      group.users.add(*members)
      
    return Response({'success': True, 'message': 'Group created successfully'})
  
  if not other_member:
    return Response({'success':False, 'message':'Other Member not found'})
  
  chat, created = create_chat_logic(member, other_member)
  if not created:
    return Response({'success':True, 'link':chat.get_link(), 'message': 'Already talking', 'created': False})
  else:
    return Response({'success':True, 'link':chat.get_link(), 'created':True, 'other_member':{'name':other_member.name}})
  
