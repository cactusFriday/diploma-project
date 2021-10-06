from django.db import models
import datetime as dt
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    date_of_birth = models.DateField(blank=True, null=True)

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

class Transaction(models.Model):
    date = models.DateTimeField(verbose_name='Время создания')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    data = models.CharField(max_length = 90, default = '')
    saved = models.BooleanField(blank=False, null=False, editable=True, default=False)
    def strformat(self):
        '''
        return all attributes in string format
        '''
        s = f'[user:{self.user.user.username}, date:{str(self.date)}, data:{str(self.data)}, saved:{str(self.saved)}]'
        return s
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return str(f'Transaction for user {self.user.user.username}')
