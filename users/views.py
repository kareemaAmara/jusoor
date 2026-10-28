from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    OrganizationSerializer,
)
from .models import User, Organization


def get_tokens_for_user(user):
    """Generate access & refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    """POST /api/users/register/ — Create a new account."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Account created successfully',
                'user': UserProfileSerializer(user).data,
                'tokens': tokens,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """POST /api/users/login/ — Authenticate user."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'tokens': tokens,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET & PUT /api/users/profile/ — Get or update own profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class OrganizationView(generics.RetrieveUpdateAPIView):
    """GET & PUT /api/users/organization/ — Get or update org details."""
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Organization.objects.get(user=self.request.user)

        # ========== ADMIN VIEWS ==========

from .serializers import (
    AdminUserListSerializer,
    AdminOrganizationSerializer,
    AdminUserUpdateSerializer,
)


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'admin'
        )


class AdminUserListView(generics.ListAPIView):
    """GET /api/users/admin/users/ — List all users (admin only)."""
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAdminUser]


class AdminUserDetailView(generics.RetrieveAPIView):
    """GET /api/users/admin/users/<id>/ — User details (admin only)."""
    queryset = User.objects.all()
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAdminUser]


class AdminToggleUserStatusView(generics.UpdateAPIView):
    """PUT /api/users/admin/users/<id>/toggle-status/ — Activate/deactivate user."""
    queryset = User.objects.all()
    serializer_class = AdminUserUpdateSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
            'is_active': user.is_active,
        })


class AdminDeleteUserView(APIView):
    """DELETE /api/users/admin/users/<id>/ — Delete a user."""
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prevent deleting other admins
        if user.is_superuser:
            return Response(
                {'error': 'Cannot delete superuser'},
                status=status.HTTP_403_FORBIDDEN
            )

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)


class AdminOrganizationListView(generics.ListAPIView):
    """GET /api/users/admin/organizations/ — List all organizations."""
    queryset = Organization.objects.all().order_by('-id')
    serializer_class = AdminOrganizationSerializer
    permission_classes = [IsAdminUser]


class AdminVerifyOrganizationView(APIView):
    """PUT /api/users/admin/organizations/<id>/verify/ — Verify/unverify an organization."""
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            org = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        org.verified = not org.verified
        org.save()
        return Response({
            'message': f'Organization {"verified" if org.verified else "unverified"} successfully',
            'verified': org.verified,
        })
