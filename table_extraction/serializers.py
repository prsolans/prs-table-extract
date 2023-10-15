# serializers.py

from rest_framework import serializers
from .models import Document

class TableDataSerializer(serializers.Serializer):
    data = serializers.JSONField()

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
