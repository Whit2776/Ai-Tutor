from django.shortcuts import render
from login.decorators import login_required
# Create your views here.
@login_required
def chat_box(request):
  return render(request, 'ai-chat-bot.html')

