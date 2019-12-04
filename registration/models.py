from django.db import models
from users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save

def custome_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return "profiles/"+filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custome_upload_to, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

@receiver(post_save, sender=CustomUser)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        print("se acaba de crear un usuario y su perfil enlazado")