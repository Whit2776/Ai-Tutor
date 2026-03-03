
from login.models import Person

class PersonAuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Default: user is not logged in
    request.person = None

    # Get member_id from session
    person_id = request.session.get('person_id')

    if person_id:
      # Fetch member from DB if active
      person = Person.objects.filter(id=person_id).first()
      if person:
        request.person = person
    # Continue processing the request
    response = self.get_response(request)
    return response
  
  
# class AdminAuthMiddleware:
#   def __init__(self, get_response):
#     self.get_response = get_response

#   def __call__(self, request):
#     # Default: user is not logged in
#     request.admin = None
#     request.family = None

#     # Get member_id from session
#     member_id = request.session.get('admin_id')

#     if member_id:
#       # Fetch member from DB if active
#       member = Member.objects.filter(member_id=member_id, is_active=True).first()
#       if member:
#         request.admin = member
#         request.family = member.family

#     # Continue processing the request
#     response = self.get_response(request)
#     return response