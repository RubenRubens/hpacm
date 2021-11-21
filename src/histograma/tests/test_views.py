from django.test import TestCase, Client

from ..models import Municipio

class TestViews(TestCase):
	
	def test_numero_visitas_municipio(self):
		"""
		Comprueba que las visitas de un municipio se incrementan al hacer
		una consulta
		"""
		
		# Crea un cliente de prueba
		c = Client()
		
		# Realiza una primera  consulta
		c.post(
			'/hpacm/',
			{
                "municipio": "Murchante",
                "año": 2017,
                "per_capita": False,
                "cuantil_inferior": 0,
                "cuantil_superior": 95,
                "tamaño_contenedor": 1000,
			}
		)

		consultas = Municipio.objects.get(municipio__contains='Murchante').numero_consultas
		self.assertEquals(consultas, 1)
		
		# Realiza una segunda consulta en el mismo municipio
		c.post(
			'/hpacm/',
			{
                "municipio": "Murchante",
                "año": 2018,
                "per_capita": True,
                "cuantil_inferior": 0,
                "cuantil_superior": 100,
                "tamaño_contenedor": 2000,
			}
		)

		consultas = Municipio.objects.get(municipio__contains='Murchante').numero_consultas
		self.assertEquals(consultas, 2)
