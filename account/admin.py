from django.contrib import admin

from .models import Profile, WorkerBiometric

# Register your models here.

class WorkerBioInLine(admin.TabularInline):
    model = WorkerBiometric
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']
    list_filter = ['user']
    search_fields = ['user']
    inlines = [WorkerBioInLine]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(WorkerBiometric)
