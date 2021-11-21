from django.urls import path

from . import views

histograma_urls = [
    path("hpacm/", views.pagina_inicio),
    path("svg/<int:histograma_id>", views.svg),
    path("about/", views.about, name="about"),
    path("municipios_mas_consultados/", views.municipios_mas_consultados, name="top_consultados"),
]
