from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserTypes(models.TextChoices):
    DONOR: Any = "DONOR", _("Donor")
    PATIENT: Any = "PATIENT", _("Patient")
    
class GenderType(models.TextChoices):
    MALE: Any = 'MALE', _('Male')
    FEMALE: Any = 'FEMALE', _('Female')
    
class BloodTypes(models.TextChoices):
    A_PLUS: Any = 'A+', 'A+',
    A_MINUS: Any = 'A-', 'A-',
    B_PLUS: Any = 'B+', 'B+',
    B_MINUS: Any = 'B-', 'B-',
    O_PLUS: Any = 'O+', 'O+',
    O_MINUS: Any = 'O-', 'O-',
    AB_PLUS: Any = 'AB+', 'AB+',
    BA_MINUS: Any = 'AB-', 'AB-'
    
class Status(models.TextChoices):
    COMPLETED: Any = 'completed', 'Completed',
    CANCELLED: Any = 'cancelled', 'Cancelled',
    PENDING: Any = 'pending', 'pending',