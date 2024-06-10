from .serializers import ContractInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from client.models import ContractInfo
from datetime import datetime
from rest_framework import status
from .models import ProviderInfo, ProviderCategoryInfo

# 계약된 언론사 목록
@csrf_exempt
@api_view(['GET'])
def get_provider_list(request, client):
    if request.user.is_authenticated:
        if request.method == 'GET':
            try:
                day = datetime.today().strftime('%Y-%m-%d')
                query_set = ContractInfo.objects.get(client=client, paid_yn = True, 
                                                            started_date_time__lte = day, expired_date_time__gte = day)
                provider = query_set.provider_no.all()
          
                serializer = ContractInfoSerializer(provider, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

            except ContractInfo.DoesNotExist:
                content = {"status_code":status.HTTP_404_NOT_FOUND,
                           "client_id": client,
                           "message":"조회할 데이터가 없습니다."} 
                return Response(content, status=404)
    else:
        return JsonResponse("로그인이 필요합니다", safe=False, status=status.HTTP_400_BAD_REQUEST)