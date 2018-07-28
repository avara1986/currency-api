import datetime
import random
from typing import Text, Tuple

from currency_providers.driver import BaseProviderDriver


class Driver(BaseProviderDriver):
    base_url = "http://data.fixer.io/api/"
    access_key = "1d3ef12f7d656b3e63cbee7e6874702f"

    def __init__(self, base):
        super().__init__(base=base)
        self._mock_data = {}
        for currency in ["EUR", "CHF", "USD", "GBP"]:
            self._mock_data[currency] = {}
            for i in range(0, 1400):  # 4 años
                date = datetime.datetime.now() - datetime.timedelta(days=i)
                self._mock_data[currency][self._parse_date(date)] = random.random()

    @staticmethod
    def _parse_date(date):
        return date.strftime("%Y-%m-%d")

    def rates(self, currency: Text, date: datetime = None) -> Tuple[bool, float, datetime.datetime]:
        if not date:
            date = datetime.datetime.now()
        date_str = self._parse_date(date)
        return True, self._mock_data[currency][date_str], date

    def exchanges(self, currency_origin: Text, currency_destination: Text, amount: int) -> Tuple[
        bool, float, datetime.datetime]:
        first_key = next(i for i in self._mock_data[currency_origin])
        amount_origin = self._mock_data[currency_origin][first_key]
        amount_destination = self._mock_data[currency_destination][first_key]
        return True, (amount * (amount_origin / amount_destination)), datetime.datetime.strptime(first_key, "%Y-%m-%d")

    def time_weighted_rate(self) -> Tuple[bool, float]:
        response, content = self.request.request(url="latest", method="get", data={"access_key": ""})
        return content
