# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from abc import abstractmethod, ABCMeta
from typing import Text, Tuple

from currency_providers.requests import Request

logger = logging.getLogger(__name__)


class BaseProviderDriver(object, metaclass=ABCMeta):
    base_url = ""
    prefix_url = ""
    base = ""

    def __init__(self, base):
        if not base:
            Exception("Es necesario definir una moneda base para recuperar los valores del proveedor")
        self.base = base
        self.request = Request(base_url=self.base_url)

    @abstractmethod
    def rates(self, currency: Text, date: datetime = None) -> Tuple[bool, float]:
        pass

    @abstractmethod
    def exchanges(self, currency_origin: Text, currency_destination: Text, amount: int) -> Tuple[bool, float]:
        pass

    @abstractmethod
    def time_weighted_rate(self) -> Tuple[bool, float]:
        pass
