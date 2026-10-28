from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    OrganizationView,
    AdminUserListView,
    AdminUserDetailView,
    AdminToggleUserStatusView,
    AdminDeleteUserView,
    AdminOrganizationListView,
    AdminVerifyOrganizationView,
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('organization/', OrganizationView.as_view(), name='organization'),

    # Admin — Users
    path('admin/users/', AdminUserListView.as_view(), name='admin-users-list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/toggle-status/', AdminToggleUserStatusView.as_view(), name='admin-user-toggle'),
    path('admin/users/<int:pk>/delete/', AdminDeleteUserView.as_view(), name='admin-user-delete'),

    # Admin — Organizations
    path('admin/organizations/', AdminOrganizationListView.as_view(), name='admin-orgs-list'),
    path('admin/organizations/<int:pk>/verify/', AdminVerifyOrganizationView.as_view(), name='admin-org-verify'),
]