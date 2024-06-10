from django.contrib import admin
from .models import ArticleInfo, PagerInfo, NewsInfo, RawArticleInfo, CategoryInfo, IncidentInfo

class NewsInfoAdmin(admin.ModelAdmin):
    search_fields = ['code', 'provider']
    list_display = ['no', 'provider_id', 'published_date_time', 'code']
    ordering = ['no']
admin.site.register(NewsInfo, NewsInfoAdmin)

class PagerInfoAdmin(admin.ModelAdmin):
    search_fields = ['code']
    list_display = ['no', 'news_id', 'page', 'order', 'code']
    ordering = ['no']
admin.site.register(PagerInfo, PagerInfoAdmin)

class ArticleInfoAdmin(admin.ModelAdmin):
    search_fields = ['code']
    list_display = ['no', 'raw_article_id', 'paper_id', 'code']
    ordering = ['no']
admin.site.register(ArticleInfo, ArticleInfoAdmin)

class RawArticleInfoAdmin(admin.ModelAdmin):
    search_fields = ['code']
    list_display = ['no', 'title', 'provider', 'category', 'byline']
    ordering = ['no']
admin.site.register(RawArticleInfo, RawArticleInfoAdmin)

class CategoryInfoAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id','name']
    ordering = ['id']
admin.site.register(CategoryInfo, CategoryInfoAdmin)

class IncidentInfoAdmin(admin.ModelAdmin):
    search_fields = ['code']
    list_display = ['id','name','code']
    ordering = ['id']
admin.site.register(IncidentInfo, IncidentInfoAdmin)



