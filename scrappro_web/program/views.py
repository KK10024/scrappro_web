from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoginSerializer, UserInfoSerializer
from django.contrib.auth import login
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProgramSerializer
from .models import ProgramInfo
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

# 로그인 부분 API
@csrf_exempt
@api_view(['POST'])
def program_login(request):
    login_serailizer = LoginSerializer(data=request.data)
    if login_serailizer.is_valid():
        # 유효한 입력의 경우 로그인
        user = login_serailizer.validated_data['user']
        user_info = UserInfoSerializer(user)
        login(request, user)
        return Response({"detail": user_info.data}, status=status.HTTP_200_OK)
    else:
        return Response(login_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)

# 유저 조회API
@csrf_exempt
@api_view(['GET'])
def UserDetail_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            userid = request.user.id
            query_set = User.objects.filter(id=userid)
            serializer = UserInfoSerializer(query_set, many=True) # JSON으로 변환
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK) # JSON타입의 데이터로 응답
    else:
        return Response("로그인이 필요합니다", status=status.HTTP_400_BAD_REQUEST)


# 프로그램 버전 조회 API
@csrf_exempt
@api_view(['GET'])
def program_version(request):
    if request.method == 'GET':
        object = ProgramInfo.objects.get(is_use=True)
        serializer = ProgramSerializer(object)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)