from rest_framework import serializers
from .models import ClientInfo, ContractInfo

class ClientInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientInfo
        fields = '__all__'        
    class Meta:
        model = ContractInfo
        fields = '__all__'
        