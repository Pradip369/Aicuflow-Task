from django.urls import path, include
from rest_framework.routers import DefaultRouter
from health_records.views import HealthRecordViewSet, DoctorView, DoctorAnnotationViewSet

app_name = 'health_record'

router = DefaultRouter()
router.register(r'health_record_detail', HealthRecordViewSet, basename='health_record_detail')
router.register(r'doctor_annotation', DoctorAnnotationViewSet, basename='doctor_annotation')

urlpatterns = [
    path('', include(router.urls)),
    path('doctor/', DoctorView.as_view(), name='doctor'),
]
