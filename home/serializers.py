from rest_framework import serializers

from .models import Contact, FAQ, Others, HeroImage, NavbarFooter


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class OthersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Others
        fields = '__all__'


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = '__all__'


class NavbarSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarFooter
        fields = '__all__'
        read_only_fields = ('is_navbar', 'is_footer')


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarFooter
        fields = '__all__'
        read_only_fields = ('is_navbar', 'is_footer')
