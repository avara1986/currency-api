from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from rates.models import Rate, Currency
from rates.serializers import RateSerializer, RateSerializerVersion2
from rates.utils import time_weighted_rate
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class MilestoneRangeFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='milestone', lookup_expr=('gte'), )
    end_date = filters.DateFilter(field_name='milestone', lookup_expr=('lte'))
    date_invested = filters.DateFilter(field_name='milestone')
    currency = filters.CharFilter(field_name='currency')

    class Meta:
        model = Rate
        fields = ['milestone']


# ViewSets define the view behavior.
class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MilestoneRangeFilter
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return RateSerializer
        return RateSerializerVersion2

    @action(methods=['post'], detail=False)
    def exchange(self, request):
        currency_from = Currency.objects.get(code=request.data["origin_currency"])
        currency_to = Currency.objects.get(code=request.data["target_currency"])
        amount = request.data["amount"]
        date_invested = request.data["date_invested"]

        filters_from = {"currency": currency_from}
        filters_to = {"currency": currency_to}
        if date_invested:
            filters_from.update({"milestone": date_invested})
            filters_to.update({"milestone": date_invested})

        rate_from = Rate.objects.filter(**filters_from).order_by("-milestone").first()
        rate_to = Rate.objects.filter(**filters_to).order_by("-milestone").first()

        rate = (rate_to.amount / rate_from.amount)

        return Response({
            "success": True,
            "query": {
                "from": currency_from.code,
                "to": currency_to.code,
                "amount": amount
            },
            "info": {
                "rate": rate
            },
            "date": rate_from.milestone,
            "result": amount * rate
        })

    @action(methods=['post'], detail=False)
    def time_weighted_rate(self, request):
        currency_from = Currency.objects.get(code=request.data["origin_currency"])
        currency_to = Currency.objects.get(code=request.data["target_currency"])
        amount = request.data["amount"]
        date_invested = request.data["date_invested"]

        filters_from = {"currency": currency_from}
        filters_to = {"currency": currency_to}

        filters_from.update({"milestone": date_invested})

        rate_from = Rate.objects.filter(**filters_from).order_by("-milestone").first()
        rate_to = Rate.objects.filter(**filters_to).order_by("-milestone").first()

        return Response({
            "success": True,
            "from": currency_from.code,
            "to": currency_to.code,
            "result": "%.3f" % (time_weighted_rate(amount, rate_from.amount, rate_to.amount) * 100)
        })

    @action(methods=['get'], detail=False)
    def graph(self, request):
        query = self.get_queryset().filter(currency=request.query_params["currency"].upper())

        return Response({"date": k["day"], "amount": k["wieght"]} for k in query.group_months())