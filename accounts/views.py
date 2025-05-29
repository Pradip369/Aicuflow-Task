from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from accounts.choices import UserRoleChoices
from accounts.serializers import UserRegistrationSerializer, PatientUserProfileSerializer, \
    DoctorUserProfileSerializer, UserSerializer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """Generics view to handle user registration."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Generics view to retrieve and update the authenticated user's profile."""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Returns the current authenticated user."""
        return self.request.user

    def get_serializer_class(self):
        """Returns serializer class based on user's role."""
        user = self.get_object()
        if user.role == UserRoleChoices.PATIENT:
            return PatientUserProfileSerializer
        elif user.role == UserRoleChoices.DOCTOR:
            return DoctorUserProfileSerializer
        return UserSerializer
