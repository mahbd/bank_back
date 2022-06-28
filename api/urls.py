from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from . import views
from home import views as home_views

app_name = 'api'

router = DefaultRouter()
router.register(r'external-bank', views.ExternalBankViewSet, basename='external_bank')
router.register(r'kyc', views.KYCViewSet, basename='kyc')
router.register(r'transaction', views.TransactionViewSet, basename='transaction')
router.register(r'contact', home_views.ContactViewSet, basename='contact')
router.register(r'faq', home_views.FAQViewSet, basename='faq')
router.register(r'others', home_views.OthersViewSet, basename='others')
router.register(r'hero-image', home_views.HeroImageViewSet, basename='hero_image')
router.register(r'navbar', home_views.NavbarViewSet, basename='navbar')
router.register(r'footer', home_views.FooterViewSet, basename='footer')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
