from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from accounts.models import DoctorProfile
from health_records.models import HealthRecord, DoctorAnnotation
from health_records.serializers import (
    HealthRecordSerializer, HealthRecordDetailSerializer, DoctorProfileSerializer,
    DoctorAnnotationSerializer, DoctorAnnotationDetailSerializer
)
from accounts.choices import UserRoleChoices
from health_records.permissions import ReadOnly
from rest_framework import generics

class HealthRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing HealthRecord objects.
    Patients can view and create their records; Doctors have read-only access.
    """

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRoleChoices.PATIENT:
            return HealthRecord.objects.select_related('patient','patient__user').filter(patient=user.patient_profile)
        elif user.role == UserRoleChoices.DOCTOR:
            return HealthRecord.objects.select_related('doctor','doctor__user').filter(doctor=user.doctor_profile)
        return HealthRecord.objects.none()

    def get_permissions(self):
        """
        Assign permissions based on user role:
        - Patients: IsAuthenticated
        - Doctors: IsAuthenticated + ReadOnly
        """
        if self.request.user.is_authenticated:
            if self.request.user.role == UserRoleChoices.PATIENT:
                return [IsAuthenticated()]
            elif self.request.user.role == UserRoleChoices.DOCTOR:
                return [IsAuthenticated(), ReadOnly()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return HealthRecordDetailSerializer
        return HealthRecordSerializer

    def perform_create(self, serializer):
        """
        Automatically assign the current user’s patient profile as patient on record creation.
        """
        serializer.save(patient=self.request.user.patient_profile)


class DoctorView(generics.ListAPIView):
    """
    Generics view to list all doctors.
    """
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]


class DoctorAnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing DoctorAnnotation objects.
    Patients have read-only access; doctors can create and edit annotations.
    """

    def get_queryset(self):
        """
        Return annotations related to the current user, either as doctor or patient.
        """
        user = self.request.user
        queryset = DoctorAnnotation.objects.select_related('record', 'doctor', 'doctor__user', 'record__patient').filter(
            Q(doctor__user=user) | Q(record__patient__user=user))
        return queryset

    def get_permissions(self):
        """
        Assign permissions based on user role:
        - Patients: ReadOnly
        - Doctors: full access
        """
        if self.request.user.is_authenticated:
            if self.request.user.role == UserRoleChoices.PATIENT:
                return [ReadOnly()]
            elif self.request.user.role == UserRoleChoices.DOCTOR:
                return []
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return DoctorAnnotationDetailSerializer
        return DoctorAnnotationSerializer

    def perform_create(self, serializer):
        """
        Automatically assign the current user’s doctor profile as doctor on annotation creation.
        """
        serializer.save(doctor=self.request.user.doctor_profile)
