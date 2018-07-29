import logging
import datetime

from django.core.management.base import BaseCommand

from rates.utils import retrive_and_insert_rate_from_provider

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('currency', type=str)
        parser.add_argument('days', type=int)

    def handle(self, *args, **options):
        currency = options['currency']
        numdays = options['days']

        a = datetime.datetime.today()
        for x in range(0, numdays):
            date = (a - datetime.timedelta(days=x))
            rate, created = retrive_and_insert_rate_from_provider(currency, date)
            if rate:
                self.stdout.write(self.style.SUCCESS('Successfully rate %s. Created %s' % (rate, created)))
            else:
                self.stdout.write(self.style.ERROR('Error creating created rate'))
