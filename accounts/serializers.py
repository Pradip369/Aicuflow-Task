from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from accounts.choices import UserRoleChoices
from aicuflow_proj.global_config.error_messages import PASWORD_NOT_MATCH
from accounts.models import PatientProfile, DoctorProfile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates password confirmation and creates a new user with hashed password.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserRoleChoices.choices, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        """Ensure both password fields match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": PASWORD_NOT_MATCH})
        return attrs

    def create(self, validated_data):
        """Create a user after removing password confirmation."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        """Return user data with JWT tokens after registration."""
        data = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic user details"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['role', 'username', 'id']


class PatientProfileSerializer(serializers.ModelSerializer):
    """Serializer for patient profile details."""

    class Meta:
        model = PatientProfile
        exclude = ['user', 'created_at', 'updated_at']


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for doctor profile details."""

    class Meta:
        model = DoctorProfile
        exclude = ['user', 'created_at', 'updated_at']


class PatientUserProfileSerializer(serializers.ModelSerializer):
    """Serializer to retrieve and update User along with linked PatientProfile."""
    profile = PatientProfileSerializer(source='patient_profile')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'profile']
        read_only_fields = ['role', 'username', 'id']

    def update(self, instance, validated_data):
        """Update user and nested patient profile."""
        patient_profile = validated_data.pop('patient_profile')
        patient_serializer = PatientProfileSerializer(instance=instance.patient_profile, data=patient_profile)
        patient_serializer.is_valid(raise_exception=True)
        patient_serializer.save()
        instance = super().update(instance, validated_data)
        return instance


class DoctorUserProfileSerializer(serializers.ModelSerializer):
    """Serializer to retrieve and update User along with linked DoctorProfile."""
    profile = DoctorProfileSerializer(source='doctor_profile')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'profile']
        read_only_fields = ['role', 'username', 'id']

    def update(self, instance, validated_data):
        """Update user and nested doctor profile."""
        doctor_profile = validated_data.pop('doctor_profile')
        doctor_serializer = DoctorProfileSerializer(instance=instance.doctor_profile, data=doctor_profile)
        doctor_serializer.is_valid(raise_exception=True)
        doctor_serializer.save()
        instance = super().update(instance, validated_data)
        return instance
