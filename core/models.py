
import uuid
from .managers import *


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from global_data.enums import GenderType, BloodTypes, UserTypes, Status

'''
My BBMS Model, By: christianhonore2003@gmail.com
'''

# Create your models here.
class BloodBaseModel(models.Model):
    id = models.UUIDField(_("ID"), null=False, blank=False, default=uuid.uuid4,primary_key=True)
    metadata = models.JSONField(_("meta data"), default=dict, blank=True, null=True)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False, blank=True, null=True)
    created = models.DateTimeField(_("Time Created"), auto_now=True, auto_now_add=False)
    modified = models.DateTimeField(_("Time Modified"), auto_now=True, auto_now_add=False)
    status = models.CharField( _("Status"), choices=Status.choices, default=Status.PENDING, max_length=50)
    
    class Meta:
        abstract = True
        

class Donation(BloodBaseModel):
    """Model to record blood donations"""
    donor = models.ForeignKey(User, on_delete=models.CASCADE, choices=UserTypes.choices)
    date = models.DateField()
    volume = models.PositiveIntegerField()  # Volume in milliliters
    blood_group = models.CharField(max_length=50, choices=BloodTypes.choices, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.donor.username} - {self.date}"
    
    
class Request(BloodBaseModel):
    """Model to record blood donations"""
    user_requesting = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'donor'})
    date = models.DateField()
    volume = models.PositiveIntegerField()  # Volume in milliliters
    blood_group = models.CharField(max_length=50, choices=BloodTypes.choices, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_requesting.username} - {self.date}"