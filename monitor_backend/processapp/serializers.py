from rest_framework import serializers
from .models import ProcessData, SystemInfo

class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = '__all__'

class ProcessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessData
        fields = '__all__'
