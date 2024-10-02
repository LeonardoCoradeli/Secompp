from django.db import models
from usuarios.models import BaseControlModel
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.utils import timezone

CustomUser = get_user_model()
    
class Emails(BaseControlModel):
    emailId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    emailUid = models.BigIntegerField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sender = models.EmailField()
    receiver = models.EmailField()
    received_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    
class Markers(BaseControlModel):
    markerId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class UserMarker(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_markers')
    markerId = models.ForeignKey(Markers, on_delete=models.CASCADE, related_name='user_markers')

    def __str__(self):
        return f'{self.userId} - {self.markerId}'
    
class UserEmailMarker(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_email_markers')
    markerId = models.ForeignKey(Markers, on_delete=models.CASCADE, related_name='user_email_markers')
    emailId = models.ForeignKey(Emails, on_delete=models.CASCADE, related_name='user_email_markers')

    def __str__(self):
        return f'{self.userId} - {self.markerId} - {self.emailId}'

