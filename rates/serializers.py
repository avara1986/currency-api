from rest_framework import serializers

from rates.models import Rate, Currency


# Serializers define the API representation.
class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', )


# Serializers define the API representation.
class RateSerializer(serializers.HyperlinkedModelSerializer):
    currency = CurrencySerializer(required=False, )

    class Meta:
        model = Rate
        fields = ('amount', 'milestone', 'currency')
