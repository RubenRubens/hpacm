from django.test import TestCase

from ..forms import FormularioHPACM

class FormularioTest(TestCase):

    def test_vacio(self):
        formulario = FormularioHPACM()
        self.assertFalse(formulario.is_valid())


    def test_lista_nombres_municipios_simple(self):
        """
        Un solo municipio tiene ese nombre
        """
        formulario = FormularioHPACM(
            {
                "municipio": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        lista_municipios = formulario.lista_nombres_municipios()
        self.assertEqual(lista_municipios, ["Murchante"])


    def test_lista_nombres_municipios_caps(self):
        """
        Los caracteres del nombre pueden ser mayuscula o minuscula
        """
        formulario = FormularioHPACM(
            {
                "municipio": "mUrcHantE",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        lista_municipios = formulario.lista_nombres_municipios()
        self.assertEqual(lista_municipios, ["Murchante"])

    
    def test_lista_nombres_municipios(self):
        """
        Varios municipios contienen ese texto
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
        lista_municipios = formulario.lista_nombres_municipios()
        self.assertEqual(lista_municipios, ["Tudela", "Tudela de Duero"])


    def test_lista_nombres_municipios_similares(self):
        """
        Lista municipios similares
        """
        formulario = FormularioHPACM(
            {
                "municipio": "Mrchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        similares = formulario.lista_nombres_municipios_similares()
        self.assertEqual(similares, ["Murchante"])
    
    
    def test_lista_nombres_municipios_similares_error(self):
        """
        El municipio aparece en la lista de municipios y produce un error
        """
        formulario = FormularioHPACM(
            {
                "municipio": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        with self.assertRaises(ValueError):
            formulario.lista_nombres_municipios_similares()


    def test_nombre_municipio(self):
        formulario = FormularioHPACM(
            {
                "municipio": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        self.assertEqual(formulario.nombre_municipio(), "Murchante")
    
    
    def test_nombre_municipio(self):
        """
        Nombre del municipio dado en minusculas
        """
        formulario = FormularioHPACM(
            {
                "municipio": "murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        self.assertEqual(formulario.nombre_municipio(), "Murchante")

    def test_id_es_un_numero(self):
        """
        Compruba que el id del municipio es un numero entero
        """
        formulario = FormularioHPACM(
            {
                "municipio": "murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        id = formulario.id_municipio()
        self.assertTrue( isinstance(id, int) )
