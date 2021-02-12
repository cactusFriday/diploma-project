from django.contrib import admin

from .models import Profile, WorkerBiometric

# Register your models here.

admin.site.register(Profile)
admin.site.register(WorkerBiometric)
