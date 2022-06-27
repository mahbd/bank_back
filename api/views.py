from django.db.models import QuerySet
from rest_framework import viewsets, permissions

from main.models import ExternalBank, KYC
from .serializers import ExternalBankSerializer, KYCSerializer


class ExternalBankViewSet(viewsets.ModelViewSet):
    serializer_class = ExternalBankSerializer
    permission_classes = [permissions.IsAuthenticated]
    model_class = ExternalBank

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_staff:
            return self.model_class.objects.all()
        return self.model_class.objects.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class KYCViewSet(ExternalBankViewSet):
    serializer_class = KYCSerializer
    model_class = KYC
