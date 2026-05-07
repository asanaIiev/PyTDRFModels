from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    STATUS_CHOICES = (
    ('Free', 'Free'),
    ('Pro', 'Pro')
    )
    THEMES_CHOICES = (
    ('Code', 'Code'),
    ('Business', 'Business'),
    ('Learn', 'Learn'),
    ('Work', 'Work'),
    ('Daily', 'Daily')
    )
    themes = MultiSelectField(choices=THEMES_CHOICES, max_length=16, max_choices=5)
    status = models.CharField(choices=STATUS_CHOICES, max_length=16, default='Free')
    registered_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.status}'