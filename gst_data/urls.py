from django.urls import path
from .views import UnfiledGSTINsView

urlpatterns = [
    path('unfiled-gstins/', UnfiledGSTINsView.as_view(), name='unfiled-gstins'),
]
