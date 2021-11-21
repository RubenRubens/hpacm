import unittest

from ..analisis_datos import *

class TestAnalisisDatos(unittest.TestCase):

	def test_poblacion(self):
		poblacion = numero_habitantes("Murchante", 2019)
		self.assertEquals(poblacion, 4154)

	def test_pagos_basicos_municipio(self):
		pagos = pagos_basicos("Murchante", 2017, 0, 100)
		self.assertEquals(len(pagos), 76)

	def test_pagos_basicos_cuantiles(self):
		# Test cuantil superior
		pagos = pagos_basicos("Barillas", 2017, 0, 99)
		self.assertEquals(len(pagos), 2)
		
		# Test cuantil inferior
		pagos = pagos_basicos("Barillas", 2017, 1, 100)
		self.assertEquals(len(pagos), 2)
		
		# Test cuantil superior e inferior
		pagos = pagos_basicos("Barillas", 2017, 1, 99)
		self.assertEquals(len(pagos), 1)

	def test_histograma(self):
		histograma_texto = histograma("Barillas", 2019, False, 0, 100, 2000)
		self.assertTrue(isinstance(histograma_texto, str))

		histograma_texto_per_capita = histograma("Barillas", 2019, True, 0, 100, 2000)
		self.assertTrue(isinstance(histograma_texto_per_capita, str))
