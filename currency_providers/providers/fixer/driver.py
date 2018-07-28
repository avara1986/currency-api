from datetime import datetime
from typing import Text, Tuple

from currency_providers.driver import BaseProviderDriver


class Driver(BaseProviderDriver):
    base_url = "http://data.fixer.io/api/"
    access_key = "1d3ef12f7d656b3e63cbee7e6874702f"

    def __init__(self, base):
        super().__init__(base=base)
        self.data = {
            "access_key": self.access_key,
            "base": self.base,
        }

    def _get_data(self):
        return self.data.copy()

    @staticmethod
    def _parse_date(date):
        return date.strftime("%Y-%m-%d")

    def rates(self, currency: Text, date: datetime = None) -> Tuple[bool, float, datetime]:
        url = "latest"
        result = False
        amount = 0
        milestone = datetime.now()
        if date:
            url = self._parse_date(date)

        data = self._get_data()
        data.update({
            "symbols": currency
        })
        response, content = self.request.request(url=url, method="get", data=data)
        if response.status_code == 200 and content.get("success") and content["rates"].get(currency):
            result = True
            amount = content["rates"].get(currency)
            milestone = datetime.strptime(content["date"], "%Y-%m-%d")
        return result, amount, milestone

    def exchanges(self, currency_origin: Text, currency_destination: Text, amount: int) -> Tuple[bool, float, datetime]:
        result = False
        amount = 0
        milestone = datetime.now()
        data = self._get_data()
        data.update({
            "from": currency_origin,
            "to": currency_destination,
            "amount": currency_destination,
        })
        response, content = self.request.request(url="convert", method="get", data=data)
        if response.status_code == 200 and content.get("success"):
            result = True
            amount = content["result"]
            milestone = datetime.strptime(content["date"], "%Y-%m-%d")
        return result, amount, milestone

    def time_weighted_rate(self) -> Tuple[bool, float]:
        response, content = self.request.request(url="latest", method="get", data={"access_key": ""})
        return content
