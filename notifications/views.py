from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """GET /api/notifications/ — List all notifications for the logged-in user."""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class UnreadNotificationsView(generics.ListAPIView):
    """GET /api/notifications/unread/ — List only unread notifications."""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            is_read=False
        ).order_by('-created_at')


class UnreadCountView(APIView):
    """GET /api/notifications/unread-count/ — Returns the count of unread notifications."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


class MarkAsReadView(APIView):
    """PUT /api/notifications/<id>/read/ — Mark a notification as read."""
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})


class MarkAllAsReadView(APIView):
    """PUT /api/notifications/read-all/ — Mark all notifications as read."""
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        updated = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': f'{updated} notifications marked as read'})


class DeleteNotificationView(APIView):
    """DELETE /api/notifications/<id>/ — Delete a notification."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        notification.delete()
        return Response({'message': 'Notification deleted'}, status=status.HTTP_200_OK)

        # ========== REPORTS ==========

class OrganizationReportsView(APIView):
    """GET /api/notifications/reports/organization/ — Reports for the organization."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from users.models import Organization
        from opportunities.models import Opportunity
        from applications.models import Application, Participation

        try:
            org = Organization.objects.get(user=request.user)
        except Organization.DoesNotExist:
            return Response(
                {'error': 'Only organizations can access these reports'},
                status=status.HTTP_403_FORBIDDEN
            )

        opportunities = Opportunity.objects.filter(organization=org)
        applications = Application.objects.filter(opportunity__organization=org)
        participations = Participation.objects.filter(opportunity__organization=org, verified=True)

        total_hours = sum(p.hours_completed for p in participations)
        unique_volunteers = applications.filter(status='accepted').values('volunteer').distinct().count()

        return Response({
            'organization_name': org.org_name,
            'opportunities': {
                'total': opportunities.count(),
                'open': opportunities.filter(status='open').count(),
                'closed': opportunities.filter(status='closed').count(),
                'draft': opportunities.filter(status='draft').count(),
            },
            'applications': {
                'total': applications.count(),
                'under_review': applications.filter(status='under_review').count(),
                'accepted': applications.filter(status='accepted').count(),
                'rejected': applications.filter(status='rejected').count(),
                'withdrawn': applications.filter(status='withdrawn').count(),
            },
            'volunteers': {
                'total_unique': unique_volunteers,
            },
            'hours': {
                'total_completed': total_hours,
                'activities_completed': participations.count(),
            },
        })


class AdminReportsView(APIView):
    """GET /api/notifications/reports/admin/ — System-wide reports (Admin only)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser and request.user.role != 'admin':
            return Response(
                {'error': 'Only admins can access these reports'},
                status=status.HTTP_403_FORBIDDEN
            )

        from users.models import User, Organization
        from opportunities.models import Opportunity, Category
        from applications.models import Application, Participation

        total_hours = sum(p.hours_completed for p in Participation.objects.filter(verified=True))

        # Top 5 organizations by number of opportunities
        from django.db.models import Count
        top_organizations = Organization.objects.annotate(
            opportunity_count=Count('opportunities')
        ).order_by('-opportunity_count')[:5]

        top_orgs_data = [
            {
                'id': org.id,
                'name': org.org_name,
                'opportunities_count': org.opportunity_count,
            }
            for org in top_organizations
        ]

        return Response({
            'users': {
                'total': User.objects.count(),
                'volunteers': User.objects.filter(role='volunteer').count(),
                'organizations': User.objects.filter(role='organization').count(),
                'admins': User.objects.filter(role='admin').count(),
                'active': User.objects.filter(is_active=True).count(),
            },
            'organizations': {
                'total': Organization.objects.count(),
                'verified': Organization.objects.filter(verified=True).count(),
                'unverified': Organization.objects.filter(verified=False).count(),
            },
            'opportunities': {
                'total': Opportunity.objects.count(),
                'open': Opportunity.objects.filter(status='open').count(),
                'closed': Opportunity.objects.filter(status='closed').count(),
                'categories': Category.objects.count(),
            },
            'applications': {
                'total': Application.objects.count(),
                'accepted': Application.objects.filter(status='accepted').count(),
                'rejected': Application.objects.filter(status='rejected').count(),
            },
            'participation': {
                'total_hours': total_hours,
                'total_activities': Participation.objects.filter(verified=True).count(),
            },
            'top_organizations': top_orgs_data,
        })