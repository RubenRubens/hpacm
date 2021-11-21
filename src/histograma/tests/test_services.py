from django.test import TestCase

from ..services import ranking_mas_consultados
from ..models import Municipio

class TestServicices(TestCase):

	def test_ranking_mas_consultados(self):
		municipio = Municipio.objects.get(municipio__contains="Murchante")
		municipio.numero_consultas = 4
		municipio.save()
		
		top_ranking = ranking_mas_consultados(1)
		self.assertEquals(top_ranking[0], ("Murchante", 4))
