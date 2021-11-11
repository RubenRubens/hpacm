import io
import re
import pandas as pd
from matplotlib import pyplot as plt

# Estilo de graficos de pyplot
plt.style.use("dark_background")


def histograma(municipio: str, año: str, per_capita: bool, cuantil_inf: int, cuantil_sup: int, tamaño_contenedor: int):
    """
    Genera histograma en memoria, no en un fichero
    """
    pagos = pagos_basicos(municipio, año, cuantil_inf, cuantil_sup)
    grafica = genera_grafica(pagos, tamaño_contenedor)
    return grafica


def pagos_basicos(municipio: str, año: str, cuantil_inf: int, cuantil_sup: int):
    """
    Filtra por los pagos basicos (un tipo de ayuda comun a todos los agricultores)
    """
    
    # Lee datos de los PAC de CSV
    pac = pd.read_csv(f"/datos/pac/Beneficiarios_municipio_ejercicio_{año}.txt", header=0, delimiter=";", encoding="cp1252", decimal=",")

    # Filtra por nombre de municipio
    pac = pac[pac["MUNICIPIO"].str.contains(municipio)]

    # Filtra por la medida de "regimen de pago basico"
    pac = pac[pac["MEDIDA"].str.contains("II.1 ")]

    # Filtra por cuantiles
    cuantil_sup /= 100
    cuantil_inf /= 100
    pac = pac[pac.IMPORTE_EUROS < pac.IMPORTE_EUROS.quantile(cuantil_sup)]

    # Selecciona el importe de los pagos basicos
    pagos = pac["IMPORTE_EUROS"]

    return pagos


def genera_grafica(pagos, tamaño_contenedor):
    # Crea una lista (contenedor) con valores empezando por el cero y
    # acaba por el maximo de pagos, en intervalos del tamaño del contenedor.
    valor_max = max(pagos)
    contenedor = range(0, int(valor_max + valor_max % tamaño_contenedor), tamaño_contenedor)

    # Crea titulos para la grafica
    plt.hist(pagos, bins=contenedor, color="#FAEBD7")  # This color is called antiquewhite
    plt.xlabel("€")
    plt.ylabel("Numero de agricultores")

    # Genera el histograma en memoria
    buf = io.StringIO()
    plt.savefig(buf, format="svg")
    plt.close()
    buf.seek(0)
    grafica = buf.read()

    return grafica


def numero_habitantes(municipio, año):
    # Lee datos del CSV
    poblacion = pd.read_csv(
        f"/datos/poblacion/poblacion.csv",
        header=None,
        delimiter=";",
        dtype={"municipio": str, "año": int, "poblacion": int},
        names=["municipio", "año", "poblacion"],
        engine="python"
    )

    # Filtra por nombre de municipio
    poblacion = poblacion[poblacion["municipio"].str.contains(municipio)]
    
    # Filtra por el año
    poblacion = poblacion[poblacion["año"] == año]

    return poblacion["poblacion"].values[0]

