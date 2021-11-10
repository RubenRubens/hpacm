from django import forms

from .models import Histograma, Municipio
from genera_histograma import analisis


class FormularioHPACM(forms.ModelForm):
    
    class Meta:
        model = Histograma
        exclude = ["svg_histograma", "municipio"]

    municipio = forms.CharField(max_length=100)
    
    def lista_nombres_municipios(self):
        """
        Devuelve una lista con el nombre de todos los municipios que contienen en
        su nombre el texto buscado. Se pueden utilizar caracteres en mayuscula o
        minuscula.
        
        Ejemplo: 'bilbao' -> 'Bilbao'
        """
        mun = self.cleaned_data["municipio"]
        municipios = Municipio.objects.filter(municipio__icontains=mun).only("municipio")
        return [m.municipio for m in municipios]
    
    def lista_nombres_municipios_similares(self):
        """
        Devuelve lista con nombres similares al munipio buscado.
        
        Ejemplo: 'Brcelona' -> ['Barcelona']
        """
        import difflib
        if len(self.lista_nombres_municipios()) == 0:
            mun = self.cleaned_data["municipio"]
            municipios = Municipio.objects.only("municipio")
            similar = difflib.get_close_matches(mun, [i.municipio for i in municipios], n=3, cutoff=0.8)
            return similar
        else:
            raise ValueError('Existen municipios con ese nombre')

    def nombre_municipio(self):
        return self.lista_nombres_municipios()[0]

    def id_municipio(self):
        mun = self.cleaned_data["municipio"]
        mun = Municipio.objects.filter(municipio__icontains=mun).only("id")
        return mun[0].id

    def save(self):
        histograma = analisis.histograma(
            municipio=self.nombre_municipio(),
            año=self.cleaned_data["año"],
            per_capita=self.cleaned_data["per_capita"],
            cuantil_inf=self.cleaned_data["cuantil_inferior"],
            cuantil_sup=self.cleaned_data["cuantil_superior"],
            tamaño_contenedor=self.cleaned_data["tamaño_contenedor"],
        )
        return Histograma.objects.create(
            municipio_id=self.id_municipio(),
            año=self.cleaned_data["año"],
            per_capita=self.cleaned_data["per_capita"],
            cuantil_inferior=self.cleaned_data["cuantil_inferior"],
            cuantil_superior=self.cleaned_data["cuantil_superior"],
            tamaño_contenedor=self.cleaned_data["tamaño_contenedor"],
            svg_histograma=histograma,
        )
