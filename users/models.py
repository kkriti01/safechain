from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name


class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    locatity = models.CharField(max_length=30, null=True, blank=True)


class AdminUser(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Can add admin fields here except from common fields


class OfficeUser(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Can add office user fields here except from common fields


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_proflie = UserProfile.objects.create(user=instance)
        AdminUser.objects.create(profile=user_proflie)
        OfficeUser.objects.create(profile=user_proflie)

post_save.connect(create_user_profile, sender=User)
