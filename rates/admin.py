from django.contrib import admin

from rates.models import Currency, Rate


class RateAdmin(admin.ModelAdmin):
    pass


class CurrencyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rate, RateAdmin)
admin.site.register(Currency, CurrencyAdmin)
