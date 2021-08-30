from django.urls import path

from . import views

histograma_urls = [
    path("hpacm/", views.pagina_inicio),
    path("svg/<int:histograma_id>", views.svg),
]
