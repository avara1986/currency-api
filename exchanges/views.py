from rest_framework import viewsets

from exchanges.models import Exchange
from exchanges.serializers import ExchangeSerializer


# ViewSets define the view behavior.
class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer