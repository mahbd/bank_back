from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from .models import Contact, FAQ, Others, HeroImage, NavbarFooter
from .serializers import ContactSerializer, FAQSerializer, OthersSerializer, HeroImageSerializer, NavbarSerializer, \
    FooterSerializer


class ContactPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    permission_classes = [ContactPermission]
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_processed', 'submission_date']


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class OthersViewSet(viewsets.ModelViewSet):
    queryset = Others.objects.all()
    serializer_class = OthersSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HeroImageViewSet(viewsets.ModelViewSet):
    queryset = HeroImage.objects.all()
    serializer_class = HeroImageSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class NavbarViewSet(viewsets.ModelViewSet):
    serializer_class = NavbarSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return NavbarFooter.objects.filter(is_navbar=True)

    def perform_create(self, serializer):
        serializer.save(is_navbar=True)


class FooterViewSet(viewsets.ModelViewSet):
    serializer_class = FooterSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return NavbarFooter.objects.filter(is_footer=True)

    def perform_create(self, serializer):
        serializer.save(is_footer=True)
