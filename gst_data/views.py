from datetime import date
from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q

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


class FilingSummaryView(APIView):
    def get(self, request):
        rows = (
            GSTINFilingStatus.objects
            .filter(return_type__in=REQUIRED_RETURNS)
            .values('period', 'return_type')
            .annotate(
                filed=Count('id', filter=Q(status='Filed')),
                unfiled=Count('id', filter=~Q(status='Filed')),
            )
            .order_by('period', 'return_type')
        )

        summary = defaultdict(dict)
        for row in rows:
            summary[row['period']][row['return_type']] = {
                'filed': row['filed'],
                'unfiled': row['unfiled'],
                'total': row['filed'] + row['unfiled'],
            }

        results = [
            {'period': period, 'returns': returns}
            for period, returns in summary.items()
        ]

        return Response({'results': results})


class GSTINComplianceRateView(APIView):
    def get(self, request):
        rows = (
            GSTINFilingStatus.objects
            .filter(return_type__in=REQUIRED_RETURNS)
            .values('period', 'return_type')
            .annotate(
                total=Count('id'),
                filed=Count('id', filter=Q(status='Filed')),
            )
            .order_by('period', 'return_type')
        )

        summary = defaultdict(dict)
        for row in rows:
            total = row['total']
            filed = row['filed']
            summary[row['period']][row['return_type']] = round((filed / total) * 100, 1) if total else 0.0

        results = [
            {'period': period, 'compliance_rate': rates}
            for period, rates in summary.items()
        ]

        return Response({'results': results})
