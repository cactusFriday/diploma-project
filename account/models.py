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
    face_pic = models.ImageField()
    date_stored = models.DateField()
    # worker_login = models.ForeignKey()
