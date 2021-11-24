import io
import re
import pandas as pd
from matplotlib import pyplot as plt
import numpy

# Estilo de graficos de pyplot
plt.style.use("dark_background")

# Numero de habitantes que se utilizan para normalizar per capita
HABITANTES = 1_000

def histograma(municipio: str, año: str, per_capita: bool, cuantil_inf: int, cuantil_sup: int, tamaño_contenedor: int) -> str:
    """
    Genera el histograma en memoria, no en un fichero
    """
    pagos = pagos_basicos(municipio, año, cuantil_inf, cuantil_sup)
    if per_capita:
        return genera_grafica_per_capita(pagos, tamaño_contenedor, municipio, año)
    else:
        return genera_grafica_absoluta(pagos, tamaño_contenedor)


def pagos_basicos(municipio: str, año: int, cuantil_inf: int, cuantil_sup: int) -> pd.DataFrame:
    """
    Obtiene los pagos basicos dado un municipio y año y filtra por cuatiles
    """
    
    # Lee datos de los PAC de CSV
    pac = pd.read_csv(
        f"/datos/pac/PAC{año}.csv",
        header=None,
        dtype={"PROVINCIA": str, "MUNICIPIO": str, "IMPORTE_EUROS": float},
        names=["PROVINCIA", "MUNICIPIO", "IMPORTE_EUROS"],
        engine="python",
        delimiter=";",
        encoding="utf-8",
        decimal="."
    )

    # Filtra por nombre de municipio
    pac = pac[pac["MUNICIPIO"].str.contains(municipio)]

    # Filtra por cuantiles
    cuantil_sup /= 100
    cuantil_inf /= 100
    pac = pac[pac.IMPORTE_EUROS.quantile(cuantil_inf) <= pac.IMPORTE_EUROS]
    pac = pac[pac.IMPORTE_EUROS <= pac.IMPORTE_EUROS.quantile(cuantil_sup)] 

    # Selecciona el importe de los pagos basicos
    pagos = pac["IMPORTE_EUROS"]

    return pagos


def genera_grafica_absoluta(pagos, tamaño_contenedor: int) -> str:
    """
    Genera el histograma en memoria con matplotlib sin normalizar resultados per capita
    """
    
    # Crea una lista (contenedor) con valores empezando por el cero y
    # acaba por el maximo de pagos, en intervalos del tamaño del contenedor.
    valor_max = max(pagos)
    num_bins = int(valor_max / tamaño_contenedor) + 1

    # Crea titulos para la grafica
    plt.hist(pagos, bins=num_bins, color="#FAEBD7")
    plt.xlabel("€")
    plt.ylabel("Numero de agricultores")

    # Genera el histograma en memoria
    buf = io.StringIO()
    plt.savefig(buf, format="svg")
    plt.close()
    buf.seek(0)
    grafica = buf.read()

    return grafica


def genera_grafica_per_capita(pagos, tamaño_contenedor: int, municipio: str, año: int) -> str:
    """
    Genera el histograma en memoria con matplotlib normalizando el numero de agricultores
    per capita
    """
    
    # Crea una lista (contenedor) con valores empezando por el cero y
    # acaba por el maximo de pagos, en intervalos del tamaño del contenedor.
    valor_max = max(pagos)
    num_bins = int(valor_max / tamaño_contenedor) + 1

    # Normaliza los datos del histograma
    counts, bins = numpy.histogram(pagos, bins=num_bins)
    poblacion = numero_habitantes(municipio, año)
    counts = [HABITANTES * i / poblacion for i in counts]

    # Crea titulos para la grafica
    plt.hist(bins[:-1], bins, weights=counts, color="#FAEBD7")
    plt.xlabel("€")
    plt.ylabel(f"Numero de agricultores / {HABITANTES} habitantes")

    # Genera el histograma en memoria
    buf = io.StringIO()
    plt.savefig(buf, format="svg")
    plt.close()
    buf.seek(0)
    grafica = buf.read()

    return grafica


def numero_habitantes(municipio: str, año: int) -> int:
    """
    Obtiene el numero de habitantes que viven en un municipio un año dado.
    """
    # Lee datos del CSV
    poblacion = pd.read_csv(
        f"/datos/poblacion/poblacion.csv",
        header=None,
        delimiter=";",
        dtype={"MUNICIPIO": str, "AÑO": int, "POBLACION": int},
        names=["MUNICIPIO", "AÑO", "POBLACION"],
        engine="python"
    )

    # Filtra por nombre de municipio
    poblacion = poblacion[poblacion["MUNICIPIO"].str.contains(municipio)]
    
    # Filtra por el año
    poblacion = poblacion[poblacion["AÑO"] == año]

    return poblacion["POBLACION"].values[0]
