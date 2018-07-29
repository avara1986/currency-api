from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class RetriveRatesTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        date = "2018-07-28"
        call_command('retrive_rates', "USD", date, stdout=out)
        self.assertIn('Successfully rate [{} 00:00:00] [USD]'.format(date), out.getvalue())


class GenerateRandomDataTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        values = 1
        call_command('generate_random_data', "USD", values, stdout=out)
        self.assertIn('Successfully rate', out.getvalue())
