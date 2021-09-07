from django.test import TestCase

from ..forms import FormularioHPACM
from ..models import Municipio


class FormularioTest(TestCase):
    def test_vacio(self):
        formulario = FormularioHPACM()
        self.assertFalse(formulario.is_valid())

    def test_normal(self):
        """
        Todos los datos son los esperados y faciles de procesar
        """
        formulario = FormularioHPACM(
            {
                "municipio": "Tudela",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())

    def test_caps(self):
        """
        Los caracteres del nombre pueden ser mayuscula o minuscula
        """
        formulario = FormularioHPACM(
            {
                "municipio": "tUdElA",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())

    def test_lista_nombres_municipios(self):
        """
        Varios municipios contienen ese string
        """
        formulario = FormularioHPACM(
            {
                "municipio": "Palma",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        lista_municipios = formulario.lista_nombres_municipios()
        datos_test = [m.municipio for m in Municipio.objects.filter(municipio__contains='Palma')]
        self.assertEqual(lista_municipios, datos_test)
        