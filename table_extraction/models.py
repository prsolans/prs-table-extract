# app_name/models.py
from django.db import models

class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='documents/')
