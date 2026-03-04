from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import OnboardedGSTIN, GSTINFilingStatus


def make_gstin(gstin='99ZZZZZ9999Z1ZZ', trade_name='Test Co', state='Maharashtra', is_active=True):
    return OnboardedGSTIN.objects.create(
        gstin=gstin,
        trade_name=trade_name,
        legal_name=f'{trade_name} Pvt Ltd',
        state=state,
        admin_email='admin@test.com',
        is_active=is_active,
    )


def make_filing(gstin, return_type, period, status, due_date=None, filed_date=None):
    return GSTINFilingStatus.objects.create(
        gstin=gstin,
        return_type=return_type,
        period=period,
        status=status,
        due_date=due_date or date(2026, 3, 11),
        filed_date=filed_date,
    )


CURRENT_PERIOD = date.today().strftime('%b-%Y')
TEST_GSTIN = '99ZZZZZ9999Z1ZZ'


def find_result(results, gstin=TEST_GSTIN):
    return next((r for r in results if r['gstin'] == gstin), None)


class UnfiledGSTINsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('unfiled-gstins')

    def test_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_gstin_with_no_filings_is_included(self):
        make_gstin()
        response = self.client.get(self.url)
        result = find_result(response.data['results'])
        self.assertIsNotNone(result)
        self.assertEqual(result['missing_returns'], ['GSTR1', 'GSTR3B'])

    def test_gstin_with_both_filed_is_excluded(self):
        gstin = make_gstin()
        make_filing(gstin, 'GSTR1', CURRENT_PERIOD, 'Filed', filed_date=date.today())
        make_filing(gstin, 'GSTR3B', CURRENT_PERIOD, 'Filed', filed_date=date.today())
        response = self.client.get(self.url)
        self.assertIsNone(find_result(response.data['results']))

    def test_gstin_missing_only_gstr3b(self):
        gstin = make_gstin()
        make_filing(gstin, 'GSTR1', CURRENT_PERIOD, 'Filed', filed_date=date.today())
        response = self.client.get(self.url)
        result = find_result(response.data['results'])
        self.assertEqual(result['missing_returns'], ['GSTR3B'])

    def test_gstin_missing_only_gstr1(self):
        gstin = make_gstin()
        make_filing(gstin, 'GSTR3B', CURRENT_PERIOD, 'Filed', filed_date=date.today())
        response = self.client.get(self.url)
        result = find_result(response.data['results'])
        self.assertEqual(result['missing_returns'], ['GSTR1'])

    def test_inactive_gstin_is_excluded(self):
        make_gstin(is_active=False)
        response = self.client.get(self.url)
        self.assertIsNone(find_result(response.data['results']))

    def test_pending_status_counts_as_unfiled(self):
        gstin = make_gstin()
        make_filing(gstin, 'GSTR1', CURRENT_PERIOD, 'Pending')
        make_filing(gstin, 'GSTR3B', CURRENT_PERIOD, 'Pending')
        response = self.client.get(self.url)
        self.assertIsNotNone(find_result(response.data['results']))

    def test_response_contains_expected_fields(self):
        make_gstin()
        response = self.client.get(self.url)
        result = find_result(response.data['results'])
        self.assertIn('gstin', result)
        self.assertIn('business_name', result)
        self.assertIn('admin_email', result)
        self.assertIn('period', result)
        self.assertIn('missing_returns', result)

    def test_period_in_response_matches_current_month(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['period'], CURRENT_PERIOD)
