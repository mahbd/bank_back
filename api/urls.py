from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from . import views

router = DefaultRouter()
router.register(r'external-bank', views.ExternalBankViewSet, basename='external_bank')
router.register(r'kyc', views.KYCViewSet, basename='kyc')
router.register(r'transaction', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
