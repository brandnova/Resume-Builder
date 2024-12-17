from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import re

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Profile picture field with validation
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],
        null=True,
        blank=True,
        verbose_name="Profile Picture"
    )
    
    # Phone number field
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name="Phone Number"
    )
    
    # Brief bio or professional summary
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Professional Bio"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def profile_picture_url(self):
        """
        Returns the URL of the profile picture or a default placeholder
        """
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/assets/images/default-profile.webp'  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)