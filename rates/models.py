# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models

from common.models import AppModel
from rates.managers import RatesManager


class Currency(AppModel):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        self.code = str(self.code).upper()
        super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return "[{}] {}".format(self.code, self.name)


class Rate(AppModel):
    base = models.ForeignKey(Currency, verbose_name='Moneda de referencia', related_name="retes_base",
                             on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, verbose_name="", related_name='rates', on_delete=models.CASCADE)
    milestone = models.DateTimeField(verbose_name="Fecha y hora del precio en el mercado")
    amount = models.DecimalField(verbose_name="Precio", max_digits=15, decimal_places=6)
    # Guardamos provider dando por hecho que nuestro sistema solo puede convivir con un origen de datos del valor de las
    # moneas. Por ello, asumiendo que en algún momento podemos cambiar este origen, filtrando nuestra API por este campo
    # Podemos hacer convivir 2 origenes hasta que el nuevo haya ingestado to do el contenido y se pueda pasar de uno a otro
    provider = models.CharField(max_length=30)

    objects = RatesManager()

    def __str__(self):
        return "[{}] {} - {}".format(self.milestone, self.currency, self.amount)

    class Meta:
        db_table = 'rates'
        indexes = [
            models.Index(fields=['-milestone', ]),
        ]
