from django.db import models
from django.conf import settings

class Documents(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files')
    filename = models.CharField(max_length = 100, default = None)
    permission = models.IntegerField(default=0)
    size = models.IntegerField(default=0)

    def fill(self, dic):
        self.created_by = dic['user']
        self.file = dic['file']
        self.filename = self.file.name
        self.permission = dic['permission']
        self.size = self.file.size

    def __str__(self):
        return f'{self.filename} загруженный пользователем {self.created_by.username}'
# Create your models here.
