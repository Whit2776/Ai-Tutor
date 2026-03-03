from django.shortcuts import render
from login.decorators import login_required
from .models import *
from app_1.models import *
from login.utils import render_page


@login_required
def chatroom(request):
  member = request.member
  family = request.family

  chats = member.chats.all().order_by('-order')
  members = family.members.filter(is_accepted = True).order_by('name')
  for chat in chats:
    chat.other_user = chat.get_other_user(member.id)
  context = {'chats':chats, 'members':members}
  return render_page(request, 'chatroom.html', context)

@login_required
def chat(request,link):
  member = request.member
  chat = Chat.objects.filter(link = link).first()
  other_user = chat.get_other_user(member.id)
  chat.other_user = other_user
  
  groups = Chat.objects.filter(users = member, is_group = True).filter(users = other_user)
  
  chats = member.chats.all().order_by('-order')
  for c in chats:
    c.other_user = c.get_other_user(member.id)
  context = {'chat':chat, 'chats':chats, 'member':member, 'groups':groups}
  return render_page(request, 'chat_page.html', context )


@login_required
def family_members(request):
  member = request.member
  family = request.family
  
  members = family.members.filter(is_accepted = True).exclude(member_id = member.member_id)
  context = {'members':members}
  return render_page(request, 'chatlist.html', context)

# from uuid import uuid4

# employees = list(Employee.objects.all())

# for i in range(len(employees)):
#   for j in range(i + 1, len(employees)):  # avoid duplicates
#     e1 = employees[i]
#     e2 = employees[j]

#     # Check if a chat already exists between these 2
#     chat_exists = Chat.objects.filter(users=e1).filter(users=e2).exists()

#     if not chat_exists:
#       c = Chat.objects.create(
#           link=str(uuid4()),
#           type='chat'
#       )
#       c.users.set([e1, e2])
#       c.save()

#       print(f"Created chat: {e1.name} ↔ {e2.name}")