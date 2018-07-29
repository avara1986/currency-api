import datetime
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from oauth2_provider.models import get_access_token_model, get_application_model
from oauth2_provider.settings import oauth2_settings
from rest_framework.test import APIClient

# Create your tests here.
from rates.factories import CurrentyFactory, RateFactory
from rates.utils import retrive_and_insert_rate_from_provider, time_weighted_rate


class UtilsTests(TestCase):

    def test_retrive_and_insert_rate_from_provider(self):
        date = datetime.datetime.strptime("2018-07-28", "%Y-%m-%d")
        rate, created = retrive_and_insert_rate_from_provider("EUR", date)


class ViewsTests(TestCase):
    def setUp(self):
        # TODO: usar factories con los modelos de auth
        Application = get_application_model()
        UserModel = get_user_model()
        AccessToken = get_access_token_model()
        oauth2_settings._SCOPES = ["read", "write", "scope1", "scope2", "resource1"]

        self.test_user = UserModel.objects.create_user("test_user", "test@example.com", "123456")
        self.dev_user = UserModel.objects.create_user("dev_user", "dev@example.com", "123456")

        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://tests.com",
            user=self.dev_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )

        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            scope="read write",
            expires=datetime.datetime.now() + datetime.timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )
        self.auth = self._create_authorization_header(self.access_token.token)

    def _get_url(self, url, version=None):
        if not version:
            version = settings.DEFAULT_VERSION
        return "/{}{}".format(version, url)

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

    def _create_authorization_header(self, token):
        return "Bearer {0}".format(token)

    def test_authentication_allow(self):
        
        response = self.client.get(self._get_url('/rates/'), HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, 200)

    def test_retrive_status_code(self):
        client = APIClient()
        response = client.get(self._get_url('/rates/'), format='json')

        self.assertEqual(response.status_code, 403)

    def test_retrive_body_v1(self):
        client = APIClient()
        currency = self._create_currency("EUR")
        rate = self._create_rate(currency=currency)
        response = client.get(self._get_url('/rates/', "v1"), format='json', HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.data[0].get("idpublic"), None)
        self.assertEqual(float(response.data[0]["amount"]), rate.amount)
        self.assertEqual(response.data[0]["milestone"], "{}T00:00:00Z".format(rate.milestone))
        self.assertEqual(response.data[0]["currency"]["code"], rate.currency.code)
        self.assertEqual(response.data[0].get("base"), None)

    def test_retrive_body_v2(self):
        client = APIClient()
        currency = self._create_currency("EUR")
        rate = self._create_rate(currency=currency)
        response = client.get(self._get_url('/rates/'), format='json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.data[0]["idpublic"], str(rate.idpublic))
        self.assertEqual(float(response.data[0]["amount"]), rate.amount)
        self.assertEqual(response.data[0]["milestone"], "{}T00:00:00Z".format(rate.milestone))
        self.assertEqual(response.data[0]["currency"]["code"], rate.currency.code)
        self.assertEqual(response.data[0]["base"]["code"], rate.currency.code)

    def test_retrive_body_filter_dates(self):
        client = APIClient()
        currency = self._create_currency("EUR")
        self._create_rate(currency=currency, date="2018-07-28")
        self._create_rate(currency=currency, date="2018-07-27")
        self._create_rate(currency=currency, date="2018-07-26")
        self._create_rate(currency=currency, date="2018-07-25")
        response = client.get(self._get_url('/rates/?start_date=2018-07-26&end_date=2018-07-27'), format='json', HTTP_AUTHORIZATION=self.auth)
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

        response = client.post(self._get_url('/rates/exchange/'), format='json', data={
            "origin_currency": "EUR",
            "target_currency": "USD",
            "amount": amount,
            "date_invested": "2018-07-28"
        }, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual("%.5f" % response.data["result"], "%.5f" % ((rate2.amount / rate1.amount) * amount))

    def test_time_weighted_rate(self):
        client = APIClient()
        amount = 5
        currency1 = self._create_currency("EUR")
        currency2 = self._create_currency("USD")
        rate1 = self._create_rate(currency=currency1, date="2018-07-27")
        rate2 = self._create_rate(currency=currency2, date="2018-07-28")

        response = client.post(self._get_url('/rates/time_weighted_rate/'), format='json', data={
            "origin_currency": "EUR",
            "target_currency": "USD",
            "amount": amount,
            "date_invested": "2018-07-27"
        }, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.data["result"],
                         "%.3f" % (time_weighted_rate(amount, rate1.amount, rate2.amount) * 100))

    def test_graph(self):
        client = APIClient()
        amount = 5
        currency1 = self._create_currency("EUR")
        currency2 = self._create_currency("USD")
        rate1 = self._create_rate(currency=currency1, date="2018-07-28")
        rate2 = self._create_rate(currency=currency2, date="2018-07-28")

        self._create_rate(currency=currency1, date="2018-07-27")
        self._create_rate(currency=currency2, date="2018-07-27")

        response = client.get(self._get_url('/rates/graph/?start_date=2018-07-27&end_date=2018-07-28'), format='json', data={
            "currency": "USD"
        }, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(len(response.data), 2)
