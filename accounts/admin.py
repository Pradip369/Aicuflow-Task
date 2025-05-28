from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, PatientProfile, DoctorProfile

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'gender', 'date_of_birth')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('gender',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('user__username',)

    fieldsets = (
        (None, {
            'fields': ('user', 'phone_number', 'gender', 'date_of_birth', 'address', 'insurance_details', 'profile_picture')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'gender', 'specialization', 'license_number', 'years_of_experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number', 'specialization')
    list_filter = ('gender', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('user__username',)

    fieldsets = (
        (None, {
            'fields': ('user', 'phone_number', 'gender', 'date_of_birth', 'specialization', 'license_number',
                       'years_of_experience', 'description', 'profile_picture', 'available_times')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
