from .serializers import ClientInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import ClientInfo, ContractInfo
from datetime import datetime
from rest_framework import status


# 업체 부분 전체 조회 API
@csrf_exempt
@api_view(['GET'])
def get_client_list(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            userid = request.user.id
            day = datetime.today().strftime('%Y-%m-%d')
            try:    
                client_id = ClientInfo.objects.filter(reporter=userid)
                query_set = ContractInfo.objects.filter(client__in = client_id, paid_yn = True, 
                                                        started_date_time__lte = day, expired_date_time__gte = day)
                if not query_set:
                    raise ContractInfo.DoesNotExist("조회된 업체가 없습니다.")

                serializer = ClientInfoSerializer(query_set, many=True) # JSON으로 변환
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK) # JSON타입의 데이터로 응답
            except ContractInfo.DoesNotExist as e:
                content = {"status_code":status.HTTP_404_NOT_FOUND,
                           "userid":userid,
                           "message": str(e)}  
                return JsonResponse(content, status=404)
    else:
        return Response("로그인이 필요합니다", status=status.HTTP_400_BAD_REQUEST)