# -*- encoding: utf-8 -*-
import factory

# tuenti imports
from rates.models import Currency, Rate

class CurrentyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency


class RateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rate

    currency = factory.SubFactory(CurrentyFactory)
    base = factory.SubFactory(CurrentyFactory)
