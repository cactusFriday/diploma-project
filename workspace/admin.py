from django.contrib import admin
from .models import Documents

# class DocsAdmin(admin.ModelAdmin):
#     model = Documents
#     list_display = ['user', 'date_of_birth']
#     list_filter = ['user']
#     search_fields = ['user']
    # extra = 3
# Register your models here.

admin.site.register(Documents)
