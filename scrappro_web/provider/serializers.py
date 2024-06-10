from rest_framework import serializers
from client.models import  ContractInfo
from django.contrib.auth.models import User
from .models import ProviderInfo



class ContractInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractInfo
        fields = ['id', 'client', 'provider_no']

    class Meta:
        model = ProviderInfo
        fields = ['no', 'name', 'copyright_fee', 'category']
        
