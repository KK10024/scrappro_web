from tabnanny import verbose

from django.db import models
from provider.models import ProviderInfo
# Create your models here.

# 뉴스 정보
class NewsInfo(models.Model):
    no = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    provider = models.ForeignKey(ProviderInfo, null=False, on_delete=models.PROTECT, verbose_name="언론사 아이디")
    published_date_time = models.DateField(null=False, verbose_name="발행일")
    code = models.CharField(db_index=True, max_length=20, null=False, verbose_name="뉴스코드")

    def __str__(self):
        return str(self.no)

    class Meta:
        db_table = 'news_info'
        verbose_name = "뉴스 정보"
        verbose_name_plural = "뉴스 목록"

# 지면 정보
class PagerInfo(models.Model):
    no = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    news = models.ForeignKey(NewsInfo,on_delete=models.PROTECT, null=False, verbose_name="뉴스 아이디")
    page = models.CharField(max_length=5, null=False, verbose_name="페이지명")
    pager_image = models.ImageField(upload_to="news/paper", max_length=100, null=False, verbose_name="지면 이미지")
    order = models.IntegerField(null=False, verbose_name="순서")
    code = models.CharField(db_index=True, max_length=25, null=False, verbose_name="지면코드")

    def __str__(self):
        return str(self.no)

    class Meta:
        db_table = 'paper_info'
        verbose_name = "지면 정보"
        verbose_name_plural = "지면 목록"

#기사 정보
class ArticleInfo(models.Model):
    no = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    raw_article = models.ForeignKey("RawArticleInfo", null=False, on_delete=models.PROTECT, verbose_name="원본기사 아이디")
    paper = models.ForeignKey(PagerInfo, on_delete=models.PROTECT, verbose_name="지면 아이디")
    paper_image = models.ImageField(upload_to="news/article", max_length=100, null=False, verbose_name="기사 이미지")
    code = models.CharField(db_index=True, max_length=30, null=False, verbose_name="기사코드")

    def __str__(self):
        return str(self.no)

    class Meta:
        db_table = 'article_info'
        verbose_name = "기사 정보"
        verbose_name_plural = "기사 목록"

# 원본 기사정보
class RawArticleInfo(models.Model):
    no = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    code = models.CharField(db_index=True, null=False, max_length=30, verbose_name="기사코드")
    title = models.CharField(null=False, max_length=100, verbose_name="제목")
    content = models.TextField(null=False, verbose_name="본문")
    provider = models.CharField(null=False, max_length=20, verbose_name="언론사명")
    category = models.CharField(null=False, max_length=20, verbose_name="뉴스 통합분류체계")
    byline = models.CharField(null=False, max_length=50, verbose_name="기자 이름")
    provider_news_id = models.CharField(null=False, max_length=200, verbose_name="언론사 뉴스ID")
    publisher_code = models.CharField(null=False, max_length=200, verbose_name="언론사 뉴스 코드")
    provider_link_page = models.CharField(blank=True, max_length=200, verbose_name="언론사 원본 링크페이지")
    printing_page = models.CharField(null=False, max_length=200, verbose_name="지면번호 이름")
    published_at = models.DateTimeField(verbose_name="발행일")
    enveloped_at = models.DateTimeField(verbose_name="수집일시")
    dateline = models.DateTimeField(verbose_name="출고시간")

    def __str__(self):
        return str(self.no)

    class Meta:
        db_table = 'raw_article_info'
        verbose_name = "원본기사 정보"
        verbose_name_plural = "원본기사 목록"



# 기사 이미지 정보

class RawArticleImageInfo(models.Model):
    no = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    raw_article = models.ForeignKey(RawArticleInfo, null=False, on_delete=models.PROTECT, verbose_name="기사아이디")
    address = models.CharField(null=False, max_length=200, verbose_name="주소")

    def __str__(self):
        return self.no

    class Meta:
        db_table = 'raw_article_image_info'
        verbose_name = "기사 이미지 정보"
        verbose_name_plural = "기사 이미지 목록"


# 사건사고 분류
class IncidentInfo(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    name = models.CharField(null=False, max_length=20, verbose_name="분류체계")
    code = models.CharField(null=False, max_length=20, verbose_name="코드값")
    raw_article = models.ManyToManyField(RawArticleInfo, verbose_name="뉴스아이디", blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'incident_info'
        verbose_name = "사건사고 정보"
        verbose_name_plural = "사건사고 목록"




# 카테고리 정보

class CategoryInfo(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    name = models.CharField(null=False, max_length=20, verbose_name="이름")
    raw_article = models.ManyToManyField(RawArticleInfo, verbose_name="고유번호", blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'category_info'
        verbose_name = "카테고리 정보"
        verbose_name_plural = "카테고리 목록"





