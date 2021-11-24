from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import histograma
from .forms import FormularioHPACM
from .models import Histograma, Municipio
from .services import ranking_mas_consultados


def pagina_inicio(request):
    if request.method == "POST":
        formulario = FormularioHPACM(request.POST)
        if formulario.is_valid():

            # Comprueba que el municipio buscado es inequivoco (solo hay uno)
            nombres_municipios = formulario.lista_nombres_municipios()
            if len(nombres_municipios) == 1:

                # Añade una visita al municipio
                municipio = Municipio.objects.get(municipio__contains=formulario.nombre_municipio())
                municipio.numero_consultas += 1
                municipio.save()

                # Comprueba si ya se ha realizado en otra ocasion la misma consulta
                try:
                    cache = Histograma.objects.get(
                        municipio__id=formulario.id_municipio(),
                        año=formulario.cleaned_data["año"],
                        per_capita=formulario.cleaned_data["per_capita"],
                        tamaño_contenedor=formulario.cleaned_data["tamaño_contenedor"],
                        cuantil_inferior=formulario.cleaned_data["cuantil_inferior"],
                        cuantil_superior=formulario.cleaned_data["cuantil_superior"],
                    )
                    histograma_id = cache.id

                # Si no esta en el cache (en la BBDD) entonces crea un nuevo registro
                except ObjectDoesNotExist:
                    nuevo_registro = formulario.save()
                    histograma_id = nuevo_registro.id

                return render(
                    request,
                    "histograma/pagina_inicio/grafica.html",
                    {
                        "histograma_id": histograma_id,
                        "municipio": formulario.nombre_municipio(),
                        "formulario": formulario.cleaned_data
                    }
                )
            
            # Comprueba si hay varios municipios que contienen el nombre buscado
            elif nombres_municipios:
                return render(
                    request,
                    "histograma/pagina_inicio/lista_municipios.html",
                    {"municipios": nombres_municipios}
                )
            
            # Comprueba si hay municipios con un nombre similar
            elif formulario.lista_nombres_municipios_similares():
                return render(
                    request,
                    "histograma/pagina_inicio/municipios_similares.html",
                    {"municipios_similares": formulario.lista_nombres_municipios_similares()}
                )
            
            # Si todo lo anterior falla, no se encuentra ningun municipio (ni ninguno parecido)
            return render(request, "histograma/pagina_inicio/no_se_encuentra_municipio.html")

        # Informa de los errores del formulario en caso de que no sea valido
        return HttpResponse(f"Formulario no valido. Errores del formulario: {formulario.errors}")

    elif request.method == "GET":
        return render(request, "histograma/pagina_inicio/solo_formulario.html", {"form": FormularioHPACM()})

    return HttpResponse("Solo son aceptados los metodos http GET y POST.")


def svg(request, histograma_id):
    documento_svg = Histograma.objects.get(id=histograma_id)
    return HttpResponse(documento_svg.svg_histograma, content_type="image/svg+xml")


def about(request):
    return render(request, "histograma/about.html")


def municipios_mas_consultados(request):
    top = ranking_mas_consultados(10)
    return render(request, "histograma/municipios_mas_consultados.html", {"top": top})