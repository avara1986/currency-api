import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from rates.utils import retrive_and_insert_rate_from_provider

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('currency', type=str)
        parser.add_argument('date', type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        currency = options['currency']
        date = options['date']
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        rate, created = retrive_and_insert_rate_from_provider(currency, date)
        if rate:
            self.stdout.write(self.style.SUCCESS('Successfully rate %s. Created %s' % (rate, created)))
        else:
            self.stdout.write(self.style.ERROR('Error creating created rate'))
