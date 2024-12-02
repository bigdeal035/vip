from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class myUser(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True, null=True)
    image=models.ImageField(null=True, upload_to='user_image')
    phone=models.CharField(max_length=20, null=True)
    dob=models.DateField(null=True, blank=True)
    REQUIRED_FIELDS=[]
   ## USERNAME_FIELD = 'email'
    



#For participant
class Participant(models.Model):  
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField( null=True)
    phone=models.CharField(max_length=20, null=True)
    def __str__(self):
        return f'{self.name} - {self.email}'

class Speaker(models.Model):
    user=models.ForeignKey(myUser, on_delete=models.CASCADE, null=True, blank=True)
    vip_name=models.CharField(max_length=200, null=True)
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField( null=True, blank=True)
    image=models.ImageField(upload_to='speaker_image')
    bio=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class vip(models.Model):
    user=models.ForeignKey(myUser, on_delete=models.CASCADE, null=True, blank=True)
    organizer_email=models.EmailField( null=True, blank=True)
    title=models.CharField(max_length=200, null=True)
    slug=models.SlugField(unique=True)
    description=models.TextField()
    image=models.ImageField(upload_to='vip_image')
    location_name=models.CharField(max_length=200, null=True)
    location_address=models.CharField(max_length=200, null=True)
    participant=models.ManyToManyField(Participant, null=True, blank=True)
    activate=models.BooleanField(default=True)
    vip_speakers=models.ManyToManyField(Speaker,blank=True, null=True)
    create=models.DateTimeField(auto_now_add=True)
    vip_date=models.DateField(blank=True, null=True)
    vip_time=models.TimeField()
    to_date=models.DateField()
    def __str__(self):
        return self.title