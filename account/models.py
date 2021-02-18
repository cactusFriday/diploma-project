from django.db import models
import datetime as dt
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    date_of_birth = models.DateField(blank=True, null=True)
    # photo = models.ImageField(upload_to='faces/%Y/%m/%d', blank=True)
    # face_embeding = models.IntegerField()

    def __str__(self):
        return f'Profile for user {self.user.username}'

class WorkerBiometric(models.Model):
    # link to Profile model
    person = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    # name for exact node 
    name = models.CharField(max_length = 30, default = 'face_image')
    face_pic = models.FileField(upload_to='faces/', blank = True, null = True)
    date_stored = models.DateField('date saved')
    class Meta:
        ordering = ['person']
    def __str__(self):
        return self.name
