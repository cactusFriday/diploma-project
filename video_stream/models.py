from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=30, help_text='Enter username')
    user_pass = models.CharField(max_length=20, help_text='Enter your password')
    class Meta:
        ordering = ['user_name']        # allow django to store user names sorted alphabetically

    def __str__(self):
        return self.user_name
    
    # def get_absolute_url(self):
        # return reverse()
    
# user: Alexey
# pass: lexPass1