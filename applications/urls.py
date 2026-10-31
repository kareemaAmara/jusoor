from django.urls import path
from .views import (
    ApplicationCreateView,
    MyApplicationsView,
    OpportunityApplicationsView,
    OrganizationApplicationsView,
    ApplicationUpdateView,
    WithdrawApplicationView,
    ParticipationCreateView,
    MyParticipationView,
    VolunteerStatsView,
    MyCertificatesView,
    DownloadCertificateView,
)

urlpatterns = [
    # Applications
    path('', ApplicationCreateView.as_view(), name='application-create'),
    path('my/', MyApplicationsView.as_view(), name='my-applications'),
    path('received/', OrganizationApplicationsView.as_view(), name='org-applications'),
    path('opportunity/<int:opportunity_id>/', OpportunityApplicationsView.as_view(), name='opportunity-applications'),
    path('<int:pk>/update-status/', ApplicationUpdateView.as_view(), name='application-update'),
    path('<int:pk>/withdraw/', WithdrawApplicationView.as_view(), name='application-withdraw'),

    # Participation
    path('participation/', ParticipationCreateView.as_view(), name='participation-create'),
    path('participation/my/', MyParticipationView.as_view(), name='my-participation'),
    path('stats/', VolunteerStatsView.as_view(), name='volunteer-stats'),

    # Certificates
    path('certificates/', MyCertificatesView.as_view(), name='my-certificates'),
    path('certificates/<int:pk>/download/', DownloadCertificateView.as_view(), name='download-certificate'),
]