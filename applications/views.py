from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Application, Participation
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationListSerializer,
    ApplicationStatusUpdateSerializer,
    ParticipationSerializer,
    ParticipationCreateSerializer,
)
from users.models import Organization


# ========== APPLICATIONS ==========

class ApplicationCreateView(generics.CreateAPIView):
    """POST /api/applications/ — Volunteer applies to an opportunity."""
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()

        # Create notification for the organization
        from notifications.models import Notification
        org_user = application.opportunity.organization.user
        Notification.objects.create(
            user=org_user,
            title='New application received',
            message=f'{application.volunteer.username} applied to "{application.opportunity.title}"',
            type='application_status',
        )

        return Response({
            'message': 'Application submitted successfully',
            'application': ApplicationListSerializer(application).data,
        }, status=status.HTTP_201_CREATED)


class MyApplicationsView(generics.ListAPIView):
    """GET /api/applications/my/ — Volunteer's own applications."""
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            volunteer=self.request.user
        ).order_by('-applied_date')


class OpportunityApplicationsView(generics.ListAPIView):
    """GET /api/applications/opportunity/<id>/ — Applications for a specific opportunity (org only)."""
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        opportunity_id = self.kwargs['opportunity_id']
        user = self.request.user

        # Only the organization owner can see applications
        try:
            org = Organization.objects.get(user=user)
            return Application.objects.filter(
                opportunity_id=opportunity_id,
                opportunity__organization=org
            ).order_by('-applied_date')
        except Organization.DoesNotExist:
            return Application.objects.none()


class OrganizationApplicationsView(generics.ListAPIView):
    """GET /api/applications/received/ — All applications received by an organization."""
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            org = Organization.objects.get(user=self.request.user)
            return Application.objects.filter(
                opportunity__organization=org
            ).order_by('-applied_date')
        except Organization.DoesNotExist:
            return Application.objects.none()


class ApplicationUpdateView(generics.UpdateAPIView):
    """PUT /api/applications/<id>/update-status/ — Organization accepts/rejects an application."""
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        user = request.user

        # Only the organization that owns the opportunity can update
        try:
            org = Organization.objects.get(user=user)
            if application.opportunity.organization_id != org.id:
                return Response(
                    {'error': 'You do not have permission to update this application'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Organization.DoesNotExist:
            return Response(
                {'error': 'Only organizations can update application status'},
                status=status.HTTP_403_FORBIDDEN
            )

        response = super().update(request, *args, **kwargs)

        # Create notification for the volunteer about status change
        from notifications.models import Notification
        application.refresh_from_db()
        if application.status == 'accepted':
            Notification.objects.create(
                user=application.volunteer,
                title='Application accepted! 🎉',
                message=f'Your application to "{application.opportunity.title}" has been accepted.',
                type='application_status',
            )
        elif application.status == 'rejected':
            Notification.objects.create(
                user=application.volunteer,
                title='Application update',
                message=f'Your application to "{application.opportunity.title}" was not accepted this time.',
                type='application_status',
            )

        return response

class WithdrawApplicationView(APIView):
    """DELETE /api/applications/<id>/withdraw/ — Volunteer withdraws their application."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        # Only the volunteer who applied can withdraw
        if application.volunteer_id != request.user.id:
            return Response(
                {'error': 'You can only withdraw your own applications'},
                status=status.HTTP_403_FORBIDDEN
            )

        application.status = 'withdrawn'
        application.save()
        return Response({'message': 'Application withdrawn successfully'}, status=status.HTTP_200_OK)


# ========== PARTICIPATION ==========

class ParticipationCreateView(generics.CreateAPIView):
    """POST /api/applications/participation/ — Organization records volunteer hours."""
    serializer_class = ParticipationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'organization':
            return Response(
                {'error': 'Only organizations can record volunteer hours'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class MyParticipationView(generics.ListAPIView):
    """GET /api/applications/participation/my/ — Volunteer's participation history."""
    serializer_class = ParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Participation.objects.filter(
            volunteer=self.request.user
        ).order_by('-completion_date')


class VolunteerStatsView(APIView):
    """GET /api/applications/stats/ — Total hours for the logged-in volunteer."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        participations = Participation.objects.filter(volunteer=request.user, verified=True)
        total_hours = sum(p.hours_completed for p in participations)
        total_activities = participations.count()

        return Response({
            'total_hours': total_hours,
            'total_activities': total_activities,
            'applications_count': Application.objects.filter(volunteer=request.user).count(),
            'accepted_count': Application.objects.filter(volunteer=request.user, status='accepted').count(),
        })