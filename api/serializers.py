from rest_framework import serializers

from main.models import ExternalBank, KYC, Transaction


class ExternalBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalBank
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
