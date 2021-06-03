from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
import shortuuid
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class tinyURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dst = models.URLField()
    src = models.CharField(max_length=10, unique=True)
    counter = models.PositiveIntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.src == '':
            count = 0
            while True:
                try:
                    self.src = shortuuid.uuid()[:6]
                    return super().save(*args, **kwargs)
                except Exception as E:
                    count += 1
                    if count == 4:
                        raise E
        return super().save(*args, **kwargs)
                  

class Profile(models.Model):
    GENDERS = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='m')
    date_of_birth = models.DateField(default=timezone.now)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()