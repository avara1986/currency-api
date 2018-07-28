import datetime
import json
import unittest

import requests_mock

from currency_providers.driver import BaseProviderDriver
from currency_providers.providers.fixer.driver import Driver


# from django.test import TestCase


class DriverFixerCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provider = Driver("EUR")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_provider(self):
        self.assertTrue(isinstance(self.provider, BaseProviderDriver))

    def test_get_provider_url(self):
        self.assertTrue(self.provider.base_url is not None)

    @requests_mock.mock()
    def test_get_rates(self, mock_requests):
        url = self.provider.base_url + "latest"
        currency = "AED"
        amount = 4.280022
        response = json.dumps({
            "success": True,
            "timestamp": 1532783107,
            "base": "EUR",
            "date": "2018-07-28",
            "rates": {
                currency: amount,
            }
        })
        mock_requests.get(url, text=response)
        result_response, amount_response, _ = self.provider.rates(currency=currency)
        self.assertEqual(result_response, True)
        self.assertEqual(amount_response, amount)

    @requests_mock.mock()
    def test_get_rates_dates(self, mock_requests):
        """
        Validar que si pedimos el día X, pero todavía los datos en la API no se han actualizado, nos devolverá
        X - 1 días
        :param mock_requests:
        :return:
        """
        date = datetime.datetime.now()
        date_validate = date - datetime.timedelta(days=1)
        date_str = date_validate.strftime("%Y-%m-%d")
        url = self.provider.base_url + date.strftime("%Y-%m-%d")
        currency = "AED"
        amount = 4.280022
        response = json.dumps({
            "success": True,
            "timestamp": 1532783107,
            "base": "EUR",
            "date": date_str,
            "rates": {
                currency: amount,
            }
        })
        mock_requests.get(url, text=response)
        result_response, _, milestone_response = self.provider.rates(currency=currency, date=date)
        self.assertEqual(result_response, True)
        self.assertEqual(milestone_response, date_validate.replace(hour=0, minute=0, second=0, microsecond=0))

    @requests_mock.mock()
    def test_get_exchanges(self, mock_requests):
        url = self.provider.base_url + "convert"
        currency = "AED"
        amount = 10
        rate = 4.280022
        response = json.dumps({
            "success": True,
            "query": {
                "from": "GBP",
                "to": "JPY",
                "amount": amount
            },
            "info": {
                "timestamp": 1519328414,
                "rate": rate
            },
            "historical": "",
            "date": "2018-02-22",
            "result": amount * rate
        })
        mock_requests.get(url, text=response)
        result_response, amount_response, _ = self.provider.exchanges(currency, "EUR", 10)
        self.assertEqual(result_response, True)
        self.assertEqual(amount_response, amount * rate)
