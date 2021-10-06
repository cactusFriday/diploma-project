from django.contrib import admin

from .models import Profile, WorkerBiometric, Transaction

# Register your models here.

class WorkerBioInLine(admin.TabularInline):
    model = WorkerBiometric
    extra = 3

class TransacAdmin(admin.TabularInline):
    model = Transaction
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']
    list_filter = ['user']
    search_fields = ['user']
    inlines = [WorkerBioInLine, TransacAdmin]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(WorkerBiometric)
admin.site.register(Transaction)
