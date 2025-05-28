from django.contrib.auth import get_user_model
from rest_framework import serializers
from health_records.models import HealthRecord, DoctorAnnotation
from accounts.models import PatientProfile, DoctorProfile
from accounts.serializers import UserSerializer

User = get_user_model()

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = '__all__'

class HealthRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ['patient']


class HealthRecordDetailSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)

    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ['patient']

class DoctorAnnotationSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(source='doctor',read_only=True)

    class Meta:
        model = DoctorAnnotation
        fields = ['id','record','comment','attachment','doctor_profile']
        read_only_fields = ['id']

class DoctorAnnotationDetailSerializer(serializers.ModelSerializer):
    record = HealthRecordDetailSerializer(read_only=True)

    class Meta:
        model = DoctorAnnotation
        fields = ['id','record','comment','attachment']
        read_only_fields = ['id']
