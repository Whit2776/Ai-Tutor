from rest_framework.serializers import ModelSerializer
from chat.models import *

class MesSerializer(ModelSerializer):
  class Meta:
    model = Mes
    fields = '__all__'
    

class FileSerializer(ModelSerializer):
  class Meta:
    model = File
    fields = '__all__'
    
    