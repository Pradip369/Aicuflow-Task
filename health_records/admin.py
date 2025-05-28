from django.contrib import admin
from .models import HealthRecord, DoctorAnnotation

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'visit_reason', 'status', 'follow_up_date', 'created_at')
    list_filter = ('status', 'doctor', 'follow_up_date', 'created_at')
    search_fields = ('patient__user__username', 'patient__full_name', 'doctor__full_name', 'visit_reason', 'diagnosis')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('patient', 'doctor', 'visit_reason', 'notes', 'status', 'follow_up_date', 'attachment')
        }),
        ('Vitals', {
            'fields': ('blood_pressure', 'heart_rate', 'temperature', 'respiratory_rate', 'weight', 'height')
        }),
        ('Medical Details', {
            'fields': ('diagnosis', 'prescriptions', 'recommended_tests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(DoctorAnnotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('record', 'doctor', 'comment_summary', 'created_at')
    list_filter = ('doctor', 'created_at')
    search_fields = ('record__patient__full_name', 'doctor__full_name', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def comment_summary(self, obj):
        return (obj.comment[:75] + '...') if len(obj.comment) > 75 else obj.comment
    comment_summary.short_description = 'Comment'
