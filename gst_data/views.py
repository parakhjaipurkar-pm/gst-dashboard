from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import OnboardedGSTIN, GSTINFilingStatus

REQUIRED_RETURNS = ['GSTR1', 'GSTR3B']


class UnfiledGSTINsView(APIView):
    def get(self, request):
        current_period = date.today().strftime('%b-%Y')  # e.g. "Mar-2026"

        filed = (
            GSTINFilingStatus.objects
            .filter(period=current_period, status='Filed', return_type__in=REQUIRED_RETURNS)
            .values_list('gstin_id', 'return_type')
        )
        filed_map: dict[int, set[str]] = {}
        for gstin_id, return_type in filed:
            filed_map.setdefault(gstin_id, set()).add(return_type)

        results = []
        for gstin in OnboardedGSTIN.objects.filter(is_active=True):
            filed_returns = filed_map.get(gstin.pk, set())
            missing = [rt for rt in REQUIRED_RETURNS if rt not in filed_returns]
            if missing:
                results.append({
                    'gstin': gstin.gstin,
                    'business_name': gstin.trade_name,
                    'admin_email': gstin.admin_email,
                    'period': current_period,
                    'missing_returns': missing,
                })

        return Response({'period': current_period, 'count': len(results), 'results': results})
