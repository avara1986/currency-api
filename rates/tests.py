import random
from datetime import datetime

from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.
from rates.factories import CurrentyFactory, RateFactory
from rates.utils import retrive_and_insert_rate_from_provider


class UtilsTests(TestCase):

    def test_retrive_and_insert_rate_from_provider(self):
        date = datetime.strptime("2018-07-28", "%Y-%m-%d")
        rate, created = retrive_and_insert_rate_from_provider("EUR", date)


class ViewsTests(TestCase):

    def test_retrive_status_code(self):
        client = APIClient()
        response = client.get('/rates/', format='json')

        assert response.status_code == 200

    def _create_currency(self, code=None):
        currency = CurrentyFactory(code=code)
        return currency

    def _create_rate(self, currency: CurrentyFactory, date=None):
        if not date:
            date = "2018-07-28"
        rate = RateFactory(
            currency=currency,
            base=currency,
            amount=float("%.5f" % random.random()),
            milestone=date,
            provider="MOCK_TESTS",
        )
        rate.save()
        return rate

    def test_retrive_body(self):
        client = APIClient()
        currency = self._create_currency("EUR")
        rate = self._create_rate(currency=currency)
        response = client.get('/rates/', format='json')
        self.assertEqual(float(response.data[0]["amount"]), rate.amount)

    def test_retrive_body_filter_dates(self):
        client = APIClient()
        currency = self._create_currency("EUR")
        self._create_rate(currency=currency, date="2018-07-28")
        self._create_rate(currency=currency, date="2018-07-27")
        self._create_rate(currency=currency, date="2018-07-26")
        self._create_rate(currency=currency, date="2018-07-25")
        response = client.get('/rates/?start_date=2018-07-26&end_date=2018-07-27', format='json')
        # self.assertEqual(float(response.data[0]["amount"][0]["amount"]), rate.amount)
        self.assertEqual(response.data[0]["milestone"], "2018-07-27T00:00:00Z")
        self.assertEqual(response.data[1]["milestone"], "2018-07-26T00:00:00Z")

    def test_exchange(self):
        client = APIClient()
        amount = 5
        currency1 = self._create_currency("EUR")
        currency2 = self._create_currency("USD")
        rate1 = self._create_rate(currency=currency1, date="2018-07-28")
        rate2 = self._create_rate(currency=currency2, date="2018-07-28")

        self._create_rate(currency=currency1, date="2018-07-27")
        self._create_rate(currency=currency2, date="2018-07-27")

        response = client.post('/rates/exchange/', format='json', data={
            "origin_currency": "EUR",
            "target_currency": "USD",
            "amount": amount,
            "date_invested": "2018-07-28"
        })
        self.assertEqual("%.5f" % response.data["result"], "%.5f" % ((rate2.amount / rate1.amount) * amount))
