from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Opportunity
from .serializers import (
    CategorySerializer,
    OpportunityListSerializer,
    OpportunityDetailSerializer,
    OpportunityCreateUpdateSerializer,
)
from users.models import Organization


class IsOrganizationOwner(permissions.BasePermission):
    """Only the organization that created the opportunity can edit/delete it."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            org = Organization.objects.get(user=request.user)
            return obj.organization_id == org.id
        except Organization.DoesNotExist:
            return False


# ========== CATEGORIES ==========
class CategoryListView(generics.ListCreateAPIView):
    """GET & POST /api/opportunities/categories/"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# ========== OPPORTUNITIES ==========
class OpportunityListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/opportunities/  — List all open opportunities (public)
    POST /api/opportunities/  — Create a new opportunity (organization only)
    """
    queryset = Opportunity.objects.filter(status='open').order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location', 'status']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'start_date', 'hours']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OpportunityCreateUpdateSerializer
        return OpportunityListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        # Only organizations can create
        if request.user.role != 'organization':
            return Response(
                {'error': 'Only organizations can create opportunities'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class OpportunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/opportunities/<id>/  — View details (public)
    PUT    /api/opportunities/<id>/  — Update (owner only)
    DELETE /api/opportunities/<id>/  — Delete (owner only)
    """
    queryset = Opportunity.objects.all()
    permission_classes = [IsOrganizationOwner]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OpportunityCreateUpdateSerializer
        return OpportunityDetailSerializer


class MyOpportunitiesView(generics.ListAPIView):
    """GET /api/opportunities/my/ — Organization's own opportunities."""
    serializer_class = OpportunityListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            org = Organization.objects.get(user=self.request.user)
            return Opportunity.objects.filter(organization=org).order_by('-created_at')
        except Organization.DoesNotExist:
            return Opportunity.objects.none()