from django.db import models
from django.utils import timezone
from django.conf import settings
from provider.models import ProviderInfo


# 업체 정보
class ClientInfo(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name="보고자 아이디")
    name = models.CharField(max_length=20, null=False, verbose_name="업체 이름")
    memo = models.CharField(max_length=50, blank=True, verbose_name="업체 메모")
    agent_name = models.CharField(max_length=5, blank=True, verbose_name="담당자 이름")
    agent_phone = models.CharField(max_length=15, blank=True, verbose_name="담당자 연락처")
    is_delete = models.BooleanField(default=False, null=False, verbose_name="삭제여부")
    created_date_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name="생성 일시")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'client_info'
        verbose_name = "업체"
        verbose_name_plural = "업체 목록"

# 계약 정보
class ContractInfo(models.Model):
    id = models.BigAutoField(primary_key=True, null=False, verbose_name="고유번호")
    client = models.ForeignKey(ClientInfo, on_delete=models.PROTECT, null=False, verbose_name="업체")
    provider_no = models.ManyToManyField(ProviderInfo, verbose_name="계약 및 언론사 정보", blank=True)
    agency_fee = models.IntegerField(null=False, verbose_name="대행 수수료")
    paid_yn = models.BooleanField(null=False, verbose_name="결제 여부")
    created_date_time = models.DateTimeField(null=False, auto_now_add=True, verbose_name="생성일시")
    is_delete = models.BooleanField(null=False, default=False, verbose_name="삭제여부")
    started_date_time = models.DateField(null=False, default=timezone.now, verbose_name="계약 시작일")
    expired_date_time = models.DateField(null=False, verbose_name="계약 만료일")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'contract_info'
        verbose_name = "계약"
        verbose_name_plural = "계약 목록"



# 계약_언론사 정보
# class ContractProviderInfo(models.Model):
#     contract_id = models.ForeignKey(ContractInfo,
#                                     on_delete=models.CASCADE, null=False,
#                                     verbose_name="계약 아이디")
#     provider_no = models.ForeignKey(ProviderInfo,
#                                     on_delete=models.CASCADE, null=False,
#                                     verbose_name="언론사 아이디")
#
#     def __str__(self):
#         return str(self.provider_no)
#
#     class Meta:
#         verbose_name = "계약 및 언론사"
#         verbose_name_plural = "계약 및 언론사 목록"


# # 정산 정보
#
# class CalcInfo(models.Model):
#     no = models.IntegerField(primary_key=True, verbose_name="정산 정보")
#     client_id = models.ForeignKey(ClientInfo,
#                                   on_delete=models.DO_NOTHING, null=False,
#                                   verbose_name="업체 아이디")
#     price = models.IntegerField(null=False, verbose_name="이용료")
#     created_date_time = models.DateTimeField(
#         auto_now_add=True, verbose_name="생성일시"
#     )
#
#     def __int__(self):
#         return self.no
#
#     class Meta:
#         verbose_name = "정산"
#         verbose_name_plural = "정산 목록"
