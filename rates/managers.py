from django.db import models
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDay

from common.managers import SelectRelatedManager


class RatesQuerySet(models.query.QuerySet):
    """Base queryset to all bookings
    Shortcuts to define methods, the prefix:
    f_ -> filters
    e_ -> excludes
    x_ -> extras
    """

    def group_months(self):
        """TODO: conocer si el valor que interesa de cada día es la media de todos los valores o el último
        """
        return (self.order_by('-milestone').annotate(day=TruncDay('milestone'))
                .values('day')
                .annotate(num_records=Count('id'))
                .annotate(total=Sum('amount'))
                .annotate(wieght=F('num_records') / F('num_records'))
                .values('day', 'wieght', 'total', 'num_records'))


class RatesManager(SelectRelatedManager):

    def get_queryset(self):
        return RatesQuerySet(self.model).distinct()
