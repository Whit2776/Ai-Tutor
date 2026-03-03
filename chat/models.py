from django.db import models
from app_1.models import *
from uuid import uuid4
# Create your models here.
from .utils import min, max


# class Chat(models.Model):
#   users = models.ManyToManyField(Member, related_name = 'chats')
#   link = models.CharField(max_length=50)
#   order = models.DateTimeField(null = True, blank = True)
#   chat_key = models.TextField(null = True)
#   last_message = models.TextField(default = '')
  
#   is_group = models.BooleanField(default=False)
#   is_main_family_group_chat = models.BooleanField(default = False)
#   family = models.ForeignKey(Family, related_name='many_gc', null=True, blank=True, on_delete=models.SET_NULL)
#   admin = models.ForeignKey(Member, related_name='created_groups', null=True, blank = True, on_delete = models.PROTECT)
#   name = models.CharField(max_length = 300, null = True, blank = True)
#   group_picture = models.ImageField(default = 'defaults/d.jpg')
  
#   def save(self, *args, **kwargs):
#     if not self.link:
#       self.link = str(uuid4())
      
#     super().save(*args, **kwargs)
  
#   def get_link(self):
#     return f'/chat/{self.link}'
  
#   def get_other_user(self, user_id):
#     o = self.users.exclude(id = user_id).first()
#     if not o:
#       print('Member does not exist')
#       return False
#     return o


# class Mes(models.Model):
#   chat = models.ForeignKey(Chat, on_delete=models.PROTECT, related_name = 'messages')
#   sender = models.ForeignKey(Member, related_name = 'sent_messages', on_delete=models.PROTECT, null = True)
#   receiver = models.ForeignKey(Member, related_name = 'received_messages', on_delete=models.PROTECT, null=True)
#   message = models.TextField(null = True, blank = True)
#   state = models.CharField(default = 'not delivered', max_length=100)
#   type = models.CharField(max_length = 300, null = True, default = 'normal')
  
#   #If message type = reply
#   reply_to = models.PositiveIntegerField(null = True)
#   reply_message = models.TextField(null=True)
  
#   #UTILS
#   sender_name = models.CharField(max_length = 300, default = '')

#   created = models.DateTimeField(auto_now_add = True)
#   updated = models.DateTimeField(auto_now = True)
  
#   def save(self, *args, **kwargs):
#     if self.chat.is_group:
#       if self.type == 'normal':
#         self.sender_name = self.sender.name if len(self.sender.name) > 0 else 'No name'
#     super().save(*args, **kwargs)

# class File(models.Model):
#   family = models.ForeignKey(Family, on_delete = models.CASCADE, null=True, related_name = 'files')
#   chat = models.ForeignKey(Chat, on_delete = models.CASCADE, null = True, related_name = 'files')
#   name = models.CharField(max_length=300, blank = True, null = True)
#   path = models.FileField(max_length=300, upload_to='Files')
#   ext = models.CharField(max_length=50, null = True)
#   type = models.CharField(max_length=50, null = True)
#   # folder = models.ForeignKey(Folder, null = True, on_delete = models.CASCADE, related_name = 'files')
#   size = models.CharField(null = True, max_length=300)
#   created = models.DateTimeField(auto_now_add = True)
#   message = models.ForeignKey(Mes, on_delete = models.PROTECT, null = True, related_name = 'files')

#   def __str__(self):
#     return f'{self.type}'