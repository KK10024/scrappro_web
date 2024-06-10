from django.db import models
from django.utils import timezone
from django.conf import settings


# 프로그램 정보
class ProgramInfo(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    version = models.CharField(max_length=5, blank=True, verbose_name="버전")
    file_path = models.FileField(max_length=100, blank=True, verbose_name="파일")
    is_use = models.BooleanField(null=True, verbose_name="사용여부")
    create_date_time = models.DateTimeField(auto_now=True, null=True, verbose_name="생성일시")

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if (self.is_use == 1):
            programs = ProgramInfo.objects.filter(is_use=1)
            programs.update(is_use=0)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'program_info'
        verbose_name = "프로그램 정보"
        verbose_name_plural = "프로그램 목록"