from project.settings import *

DEBUG = True

CURRENCY_PROVIDER = "mock"
CURRENCY_BASE = "EUR"

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
             ] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1', '::1']

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]
