from django.db import models
import datetime as dt
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class WorkerBiometric(models.Model):
    name = models.CharField(max_length = 30, default = 'face_image')
    # face_pic = models.ImageField(blank = True, null = True, upload_to = 'faces/%Y/%m/%d/')
    face_pic = models.FileField(upload_to='faces/', blank = True, null = True)
    date_stored = models.DateField('date saved')
    # worker_login = models.ForeignKey()
    def __str__(self):
        return self.name
