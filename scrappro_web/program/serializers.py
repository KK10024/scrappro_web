from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import ProgramInfo

# 로그인 검증 부분 API
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if len(username) > 0 or len(password) > 0:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
            else:
                raise AuthenticationFailed('아이디나 비밀번호가 다릅니다')
        else:
            raise AuthenticationFailed('아이디와 비밀번호 모두 입력해야합니다')

        return data

class UserInfoSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ['id', 'username', 'password']  # 프로필 필드
        # fields = '__all__'  # 프로필 전체 조회


# 프로그램 부분
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramInfo
        fields = ['id', 'version', 'is_use']