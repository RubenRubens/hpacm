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
                "municipio_buscado": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        lista_municipios = formulario.lista_nombres_municipios()
        self.assertEqual(lista_municipios, ["Murchante"])


    def test_lista_nombres_municipios_caps(self):
        """
        Los caracteres del nombre pueden ser mayuscula o minuscula
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "mUrcHantE",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        lista_municipios = formulario.lista_nombres_municipios()
        self.assertEqual(lista_municipios, ["Murchante"])

    
    def test_lista_nombres_municipios(self):
        """
        Varios municipios contienen ese texto
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "Tudela",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        lista_municipios = formulario.lista_nombres_municipios()
        self.assertEqual(lista_municipios, ["Tudela", "Tudela de Duero"])


    def test_lista_nombres_municipios_similares(self):
        """
        Lista municipios similares
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "Mrchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        similares = formulario.lista_nombres_municipios_similares()
        self.assertEqual(similares, ["Murchante"])
    
    
    def test_lista_nombres_municipios_similares_error(self):
        """
        El municipio aparece en la lista de municipios y produce un error
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        with self.assertRaises(ValueError):
            formulario.lista_nombres_municipios_similares()


    def test_nombre_municipio_simple(self):
        """
        El municipio que se busca es el unico con ese nombre exacto
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        self.assertEqual(formulario.nombre_municipio(), "Murchante")


    def test_nombre_municipio_multiples_resultados(self):
        """
        El municipio que se busca aparece en el nombre de otro municipio
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "tudela",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        self.assertEqual(formulario.nombre_municipio(), "Tudela")
    
    
    def test_nombre_municipio(self):
        """
        Nombre del municipio dado en minusculas
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        self.assertEqual(formulario.nombre_municipio(), "Murchante")

    def test_id_es_un_numero(self):
        """
        Compruba que el id del municipio es un numero entero
        """
        formulario = FormularioHPACM(
            {
                "municipio_buscado": "murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
            }
        )
        self.assertTrue(formulario.is_valid())
        formulario.busca_municipio()
        id = formulario.id_municipio()
        self.assertTrue( isinstance(id, int) )
