from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from users import models


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=False)
    password1 = serializers.CharField(write_only=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'email')


class AdminProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AdminUser
        fields = '__all__'


class OfficeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AdminUser
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    admin_profile = serializers.SerializerMethodField()
    office_profile = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = ('id', 'user', 'admin_profile', 'office_profile', 'profile_picture', 'birth_date', 'address', 'locatity')

    def get_admin_profile(self, instance):
        admin = instance.adminuser_set.all()
        return AdminProfileSerializer(admin, many=True).data

    def get_office_profile(self, instance):
        admin = instance.officeuser_set.all()
        return OfficeProfileSerializer(admin, many=True).data
