from django.db.models import QuerySet
from rest_framework import viewsets, permissions

from main.models import ExternalBank
from .serializers import ExternalBankSerializer


class ExternalBankViewSet(viewsets.ModelViewSet):
    serializer_class = ExternalBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_staff:
            return ExternalBank.objects.all()
        return ExternalBank.objects.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
