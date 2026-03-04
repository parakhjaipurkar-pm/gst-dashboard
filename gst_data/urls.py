from django.urls import path
from .views import UnfiledGSTINsView, FilingSummaryView, GSTINComplianceRateView

urlpatterns = [
    path('unfiled-gstins/', UnfiledGSTINsView.as_view(), name='unfiled-gstins'),
    path('filing-summary/', FilingSummaryView.as_view(), name='filing-summary'),
    path('gstin-compliance-rate/', GSTINComplianceRateView.as_view(), name='gstin-compliance-rate'),
]
