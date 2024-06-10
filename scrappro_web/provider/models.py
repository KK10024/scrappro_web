from django.db import models
from django.utils import timezone

# 언론사 category 정보
class ProviderCategoryInfo(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    name = models.CharField(max_length=20,  null=False, verbose_name="카테코리명")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'provider_category_info'
        verbose_name = "언론사 카테고리"
        verbose_name_plural = "언론사 카테고리 목록"
# 언론사 정보
class ProviderInfo(models.Model):
    no = models.BigAutoField(primary_key=True, null=False,verbose_name="고유번호")
    category = models.ForeignKey(ProviderCategoryInfo, on_delete=models.PROTECT, null=False, verbose_name="카테고리")
    name = models.CharField(max_length=20, null=False, verbose_name="언론사명")
    copyright_fee = models.IntegerField(default=0, verbose_name="저작권료")
    code = models.CharField(max_length=10, null=False, verbose_name="언론사코드")

    def __str__(self):
        return str(self.no)

    class Meta:
        db_table = 'provider_info'
        verbose_name = "언론사"
        verbose_name_plural = "언론사 목록"
