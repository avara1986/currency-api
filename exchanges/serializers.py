
from rest_framework import serializers

from exchanges.models import Exchange


# Serializers define the API representation.
class ColorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exchange
        fields = ('id', 'name', 'timestamp')