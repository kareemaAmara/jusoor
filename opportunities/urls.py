from django.urls import path
from .views import (
    CategoryListView,
    OpportunityListCreateView,
    OpportunityDetailView,
    MyOpportunitiesView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('my/', MyOpportunitiesView.as_view(), name='my-opportunities'),
    path('', OpportunityListCreateView.as_view(), name='opportunities-list'),
    path('<int:pk>/', OpportunityDetailView.as_view(), name='opportunity-detail'),
]