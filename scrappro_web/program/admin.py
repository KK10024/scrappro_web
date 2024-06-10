from django.contrib import admin
from .models import ProgramInfo

# Register your models here.
class ProgramInfoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'version']
    list_display = ['id', 'version', 'file_path', 'is_use', 'create_date_time']
    list_filter = ['is_use']

admin.site.register(ProgramInfo, ProgramInfoAdmin)

