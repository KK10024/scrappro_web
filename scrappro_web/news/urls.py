from django.urls import path, include
from .views import get_article_list, get_news_list, raw_article_info, get_pager_list, article_info, article_create, article_search, raw_article_create

urlpatterns = [
    path('news-list/<int:provider>', get_news_list),
    path('pager-list/<int:news>', get_pager_list),
    path('article-list/<int:paper>', get_article_list),
    path('article-info/<int:no>', article_info),
    path('article-create', article_create),
    path('article-search', article_search),
    path('raw-articles', raw_article_info),
    path('raw-article-create', raw_article_create)
]