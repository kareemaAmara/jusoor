from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationsView,
    UnreadCountView,
    MarkAsReadView,
    MarkAllAsReadView,
    DeleteNotificationView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('unread/', UnreadNotificationsView.as_view(), name='unread-notifications'),
    path('unread-count/', UnreadCountView.as_view(), name='unread-count'),
    path('read-all/', MarkAllAsReadView.as_view(), name='mark-all-read'),
    path('<int:pk>/read/', MarkAsReadView.as_view(), name='mark-read'),
    path('<int:pk>/', DeleteNotificationView.as_view(), name='delete-notification'),
]