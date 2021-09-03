from django.test import TestCase

from ..forms import FormularioHPACM


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
