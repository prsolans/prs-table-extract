# serializers.py

from rest_framework import serializers

class TableDataSerializer(serializers.Serializer):
    data = serializers.JSONField()
