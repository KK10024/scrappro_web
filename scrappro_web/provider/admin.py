from django.contrib import admin
from .models import ProviderInfo, ProviderCategoryInfo

# 언론사 관리

class ProviderCategoryInfoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']
    list_display = ['id', 'name']
    ordering = ['id', 'name']
admin.site.register(ProviderCategoryInfo, ProviderCategoryInfoAdmin)


class ProviderInfoAdmin(admin.ModelAdmin):
    search_fields = ['no', 'category_id', 'name', 'copyright_fee']
    list_display = ['no', 'category_id', 'name', 'copyright_fee']
    ordering = ['no', 'category_id', 'name', 'copyright_fee']

admin.site.register(ProviderInfo, ProviderInfoAdmin)




