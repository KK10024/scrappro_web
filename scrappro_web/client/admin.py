from django.contrib import admin
from .models import ClientInfo, ContractInfo
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# Register your models here.

# Client 관리
# admin.site.register(ClientInfo)
class ClientInfoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']
    list_display = ['id', 'name', 'reporter', 'agent_name', 'agent_phone']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClientInfoAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields["reporter"]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
        field.widget.can_view_related = False
        return form

admin.site.register(ClientInfo, ClientInfoAdmin)

# 계약 정보
class ContractInfoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'client']
    list_display = ['id', 'client', 'paid_yn', 'started_date_time', 'expired_date_time']
    list_filter = ('paid_yn', ('started_date_time', DateRangeFilter))
    fields = ['client', 'paid_yn', 'agency_fee', 'started_date_time', 'expired_date_time', 'is_delete','provider_no']
    filter_horizontal = ('provider_no',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContractInfoAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields["client"]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
        field.widget.can_view_related = False
        return form

admin.site.register(ContractInfo, ContractInfoAdmin)


# # 계약 및 언론사 목록
# class ContractProviderInfoAdmin(admin.ModelAdmin):
#     search_fields = ['contract_id', 'provider_no']
#     list_display = ['contract_id_id', 'provider_no_id']
#
# admin.site.register(ContractProviderInfo, ContractProviderInfoAdmin)

# # 정산 정보
# class CalcInfoAdmin(admin.ModelAdmin):
#     search_fields = ['no', 'client_id']
#     list_display = ['no', 'client_id', 'price']


# admin.site.register(CalcInfo, CalcInfoAdmin)

