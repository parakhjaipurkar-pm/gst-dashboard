from django.urls import path
from .views import UnfiledGSTINsView, FilingSummaryView

urlpatterns = [
    path('unfiled-gstins/', UnfiledGSTINsView.as_view(), name='unfiled-gstins'),
    path('filing-summary/', FilingSummaryView.as_view(), name='filing-summary'),
]
