from rest_framework import serializers
from login.models import *

class PersonSerializer(serializers.ModelSerializer):
  class Meta:
    model =  Person
    exclude = ['created', 'updated', 'password', 'link']
