from django import forms

from .models import Histograma, Municipio
from genera_histograma import analisis

class FormularioHPACM(forms.ModelForm):
	class Meta:
		model = Histograma
		exclude = ['svg_histograma', 'municipio']

	municipio = forms.CharField(max_length=100)
	
	def nombre_municipio(self):
		mun = self.cleaned_data['municipio']
		mun = Municipio.objects.filter(municipio__contains=mun).only('municipio')
		return mun[0].municipio

	def id_municipio(self):
		mun = self.cleaned_data['municipio']
		mun = Municipio.objects.filter(municipio__contains=mun).only('id')
		return mun[0].id

	def save(self):
		histograma = analisis.histograma(
			municipio = self.nombre_municipio(),
			año = self.cleaned_data['año'],
			per_capita = self.cleaned_data['per_capita'],
			cuantil_inf = self.cleaned_data['cuantil_inferior'],
			cuantil_sup = self.cleaned_data['cuantil_superior'],
			tamaño_contenedor = self.cleaned_data['tamaño_contenedor']
		)
		return Histograma.objects.create(
			municipio_id = self.id_municipio(),
			año = self.cleaned_data['año'],
			per_capita = self.cleaned_data['per_capita'],
			cuantil_inferior = self.cleaned_data['cuantil_inferior'],
			cuantil_superior = self.cleaned_data['cuantil_superior'],
			tamaño_contenedor = self.cleaned_data['tamaño_contenedor'],
			svg_histograma = histograma
		)