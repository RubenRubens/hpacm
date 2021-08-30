from django.http.response import HttpResponse
from django.shortcuts import render

import histograma
from .forms import FormularioHPACM
from .models import Histograma, Municipio

def pagina_inicio(request):
	if request.method == 'POST':
		formulario = FormularioHPACM(request.POST)
		if formulario.is_valid():
			# Comprueba si ya se ha realizado en otra ocasion la misma consulta
			try:
				cache = Histograma.objects.get(
					municipio__id=formulario.id_municipio(),
					año=formulario.cleaned_data['año'],
					per_capita=formulario.cleaned_data['per_capita'],
					tamaño_contenedor=formulario.cleaned_data['tamaño_contenedor'],
					cuantil_inferior=formulario.cleaned_data['cuantil_inferior'],
					cuantil_superior=formulario.cleaned_data['cuantil_superior']
				)
				histograma_id = cache.id
			
			# Si no esta en el cache (en la BBDD) entonces crea un nuevo registro
			except:
				nuevo_registro = formulario.save()
				histograma_id = nuevo_registro.id
			
			# TODO: Añadir parametros del formulario
			return render(request, 'histograma/formulario_y_grafica.html', {'histograma_id': histograma_id, 'formulario': formulario.cleaned_data})
		return HttpResponse(f'Formulario no valido. Errores del formulario: {formulario.errors}')
	
	elif request.method == 'GET':
		return render(request, 'histograma/solo_formulario.html')
	
	return HttpResponse('Solo son aceptados los metodos http GET y POST.')

def svg(request, histograma_id):
	documento_svg = Histograma.objects.get(id=histograma_id)
	return HttpResponse(documento_svg.svg_histograma, content_type='image/svg+xml')