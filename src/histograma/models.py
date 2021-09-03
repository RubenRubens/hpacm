from django.db import models
from django.core.exceptions import ValidationError


def valida_cuantil_inferior(cuantil_inf):
    if cuantil_inf < 0:
        raise ValidationError("El cuantil inferior debe de ser igual o mayor a 0")
    maximo = 80
    if cuantil_inf > maximo:
        raise ValidationError(f"El cuantil inferior introducido no puede ser mayor a {maximo}")


def valida_cuantil_superior(cuantil_sup):
    if cuantil_sup > 100:
        raise ValidationError("El cuantil superior debe de ser igual o menor a 100")
    minimo = 20
    if cuantil_sup < minimo:
        raise ValidationError(f"El cuantil superior introducido no puede ser menor a {minimo}")


def valida_tamaño_contenedor(tamaño):
    minimo = 100
    maximo = 2000
    if tamaño < minimo:
        raise ValidationError(f"El tamaño del contenedor tiene que ser mayor o igual a {minimo}")
    elif tamaño > maximo:
        raise ValidationError(f"El tamaño del contenedor tiene que ser menor o igual a {maximo}")


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
    guardados en la base de datos como text plano.
    """

    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    año = models.IntegerField()
    per_capita = models.BooleanField()
    cuantil_inferior = models.IntegerField(default=0, validators=[valida_cuantil_inferior])
    cuantil_superior = models.IntegerField(default=95, validators=[valida_cuantil_superior])
    tamaño_contenedor = models.IntegerField(default=1000, validators=[valida_tamaño_contenedor])
    svg_histograma = models.TextField()
