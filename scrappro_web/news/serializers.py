from rest_framework import serializers
from .models import ArticleInfo, NewsInfo, RawArticleInfo, PagerInfo
from provider.models import ProviderInfo



class NewsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsInfo
        fields = '__all__'

class PagerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagerInfo
        fields = '__all__'


class RawArticleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawArticleInfo
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='raw_article.provider')
    published_at = serializers.ReadOnlyField(source='raw_article.published_at')

    class Meta:
        model = ArticleInfo
        # fields = ['no', 'raw_article','provider_name']
        fields = '__all__'
