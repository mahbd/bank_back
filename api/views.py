from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import ExternalBank, KYC, Transaction
from .serializers import ExternalBankSerializer, KYCSerializer, TransactionSerializer


class IsOwnerOrHasPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        # If user not staff or superuser, automatically filter out all objects that are not owned by the user
        if (request.user.is_authenticated and not request.user.is_staff) or request.user.is_superuser:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.is_superuser:
            return True
        return super().has_object_permission(request, view, obj)


class ExternalBankViewSet(viewsets.ModelViewSet):
    serializer_class = ExternalBankSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrHasPermission]
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


class TransactionViewSet(ExternalBankViewSet):
    serializer_class = TransactionSerializer
    model_class = Transaction
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'status']

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def accept_transaction(self, request, *args, **kwargs):
        transaction = self.get_object()
        transaction.accept_transaction()
        return Response(status=status.HTTP_200_OK, data={'message': 'Transaction accepted'})

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def reject_transaction(self, request, *args, **kwargs):
        transaction = self.get_object()
        transaction.reject_transaction()
        return Response(status=status.HTTP_200_OK, data={'message': 'Transaction rejected'})
