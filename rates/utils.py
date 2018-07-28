import logging
from datetime import datetime
from typing import Text, Tuple

from django.conf import settings

from currency_providers import provider
from rates.models import Rate, Currency

logger = logging.getLogger(__name__)


def retrive_and_insert_rate_from_provider(currency: Text, date: datetime) -> Tuple[Rate, bool]:
    created = False
    rate = None

    prov = provider(settings.CURRENCY_PROVIDER, base=settings.CURRENCY_BASE)
    result, amount, milestone = prov.rates(currency=currency, date=date)
    logger.info("{} {} {}".format(result, amount, milestone))
    if result:
        currency_object, _ = Currency.objects.get_or_create(code=currency)
        base_object, _ = Currency.objects.get_or_create(code=settings.CURRENCY_BASE)

        try:
            rate = Rate.objects.get(
                base=base_object,
                currency=currency_object,
                milestone=milestone,
                amount=amount,
                provider=settings.CURRENCY_PROVIDER
            )
            created = False
        except Rate.DoesNotExist:
            rate = Rate(
                base=base_object,
                currency=currency_object,
                milestone=milestone,
                amount=amount,
                provider=settings.CURRENCY_PROVIDER
            )
            created = True

        rate.save()

    return rate, created


def time_weighted_rate(amount, rate_from_amount, rate_to_amount):
    amount_from = amount * rate_from_amount
    amount_to = amount * rate_to_amount
    result = (amount_to - amount_from) / amount_from
    logger.debug("amount_to {} amount_from {} = {}".format(amount_from, amount_to, result))
    return result
