from django.urls import path, re_path

from backoffice import views

urlpatterns = [
    path('', views.graphs),
]