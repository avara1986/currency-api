"""project URL Configuration
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from rates.views import RateViewSet

router = routers.DefaultRouter()
router.register(r'rates', RateViewSet, base_name="rates")

schema_view = get_swagger_view(title='Currency API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', schema_view),
    url(r'^v1/', include((router.urls, "ratesv1"), namespace='v1')),
    path('v2/', include((router.urls, "ratesv2"), namespace='v2')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('backoffice/', include('backoffice.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
