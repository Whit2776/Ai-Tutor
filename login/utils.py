from django.shortcuts import render

def render_page(request, temp, context = None,):
  context_1 = {
    'member': request.member,
    'family': request.family,
    'perms': request.perms
  }
  if context:
    context_1.update(context)
    
  return render(request, temp, context_1)

def login(request, user):
  try:
    request.session['person_id'] = user.id
    request.session.cycle_key() 
    return True
  except Exception as e:
    print('Error: \n', str(e))
    return False