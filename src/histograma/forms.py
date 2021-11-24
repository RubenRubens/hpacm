from django import forms

from .models import Histograma, Municipio
from . import analisis_datos


class FormularioHPACM(forms.ModelForm):

    municipios_criterio_busqueda = None
    municipio = None

    class Meta:
        model = Histograma
        exclude = ["svg_histograma", "municipio"]

    municipio_buscado = forms.CharField(max_length=100)

    def busca_municipio(self):
        m_buscado = self.cleaned_data["municipio_buscado"]
        
        # Comprueba si la lista de municipios buscado con ese criterio es unica
        self.municipios_criterio_busqueda = Municipio.objects.filter(municipio__icontains=m_buscado)
        if len(self.municipios_criterio_busqueda) == 1:
            self.municipio = self.municipios_criterio_busqueda[0]
            return True
        
        # Si hay varios municipios que contienen el texto busca si alguno coincide
        # de manera exacta
        for m in self.municipios_criterio_busqueda:
            if m.municipio.lower() == m_buscado.lower():
                self.municipio = m
                return True
        
        return False
    
    def incrementa_visitas(self):
        self.municipio.numero_consultas += 1
        self.municipio.save()

    def lista_nombres_municipios(self):
        """
        Devuelve una lista con los nombres que cumplen el criterio de busqueda.
        """
        return [m.municipio for m in self.municipios_criterio_busqueda]
    
    def lista_nombres_municipios_similares(self):
        """
        Devuelve lista con nombres similares al munipio buscado.
        
        Ejemplo: 'Brcelona' -> ['Barcelona']
        """
        import difflib
        if len(self.municipios_criterio_busqueda) == 0:
            mun = self.cleaned_data["municipio_buscado"]
            municipios = Municipio.objects.only("municipio")
            similar = difflib.get_close_matches(mun, [i.municipio for i in municipios], n=3, cutoff=0.8)
            return similar
        else:
            raise ValueError('Existen municipios con ese nombre')

    def nombre_municipio(self):
        return self.municipio.municipio

    def id_municipio(self):
        return self.municipio.id

    def save(self):
        histograma = analisis_datos.histograma(
            municipio=self.nombre_municipio(),
            año=self.cleaned_data["año"],
            per_capita=self.cleaned_data["per_capita"],
            cuantil_inf=self.cleaned_data["cuantil_inferior"],
            cuantil_sup=self.cleaned_data["cuantil_superior"],
            tamaño_contenedor=self.cleaned_data["tamaño_contenedor"]
        )
        return Histograma.objects.create(
            municipio_id=self.id_municipio(),
            año=self.cleaned_data["año"],
            per_capita=self.cleaned_data["per_capita"],
            cuantil_inferior=self.cleaned_data["cuantil_inferior"],
            cuantil_superior=self.cleaned_data["cuantil_superior"],
            tamaño_contenedor=self.cleaned_data["tamaño_contenedor"],
            svg_histograma=histograma
        )
