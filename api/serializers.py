from rest_framework import serializers

from main.models import ExternalBank


class ExternalBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalBank
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
