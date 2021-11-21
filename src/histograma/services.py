from .models import Municipio

def ranking_mas_consultados(top: int):
	"""
	Devuelve una lista con los municipios mas consultados
	"""
	municipios_ordenados = Municipio.objects.all().order_by("-numero_consultas")[:top]
	return [(m.municipio, m.numero_consultas) for m in municipios_ordenados] 
