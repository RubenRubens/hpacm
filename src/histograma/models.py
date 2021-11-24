from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Municipio(models.Model):
    """
    Lista de todos los municipios de España y numero de veces que han sido
    consultados.

    Los municipios son insertados con los datos de la PAC de 2017. Hay un script
    que se ocupa de ello.
    """

    municipio = models.CharField(max_length=100)
    numero_consultas = models.IntegerField(default=0)


class Histograma(models.Model):
    """
    Cache que guarda los histogramas de matplotlib.

    matplotlib guarda en memoria los archivos SVG y luego son
    guardados en la base de datos como texto plano.
    """

    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    año = models.IntegerField(validators=[MinValueValidator(2017), MaxValueValidator(2020)])
    per_capita = models.BooleanField()
    cuantil_inferior = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(30)])
    cuantil_superior = models.IntegerField(default=95, validators=[MinValueValidator(70), MaxValueValidator(100)])
    tamaño_contenedor = models.IntegerField(default=1000, validators=[MinValueValidator(100), MaxValueValidator(5000)])
    svg_histograma = models.TextField()
