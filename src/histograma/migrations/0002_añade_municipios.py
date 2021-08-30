from django.db import migrations
import pandas as pd

def datos_iniciales():
    '''
    Datos para iniciar la tabla "Municipio" con los datos de un CSV de la PAC.
    Se ha elegido el CSV del año 2017 de manera arbitraria.
    Devuelve una estructura de datos similar a la utilizada en JSON.
    El numero de consultas del modelo Municipio tiene un valor inicial de 0 por defecto.
    '''
    
    # Lectura de CSV de la PAC del año 2017
    pac = pd.read_csv('genera_histograma/datos/Beneficiarios_municipio_ejercicio_2017.txt',
        header=0, delimiter=';', encoding='cp1252', decimal=',',
    )

    # Devuelve todos los municipios que aparecen
    lista_municipios = pac['MUNICIPIO'].unique().tolist()
    return lista_municipios


def añade_datos_iniciales(apps, schema_editor):
    Municipio = apps.get_model('histograma', 'Municipio')
    
    for m in datos_iniciales():
        # Elimina del municipio los 8 primeros carracteres.
        # Los municipios siguen en el CSV la estructura:
        # 50042 - Balconchán                              
        # 09478 - Vizcaínos                               
        # 04033 - Castro de Filabres                      
        # 09277 - Puentedura                              
        # 08216 - Sant Jaume de Frontanyà                 
        # 44018 - Almohaja
        m = m[8:]

        # Crea el municipio
        Municipio.objects.create(municipio=m)


class Migration(migrations.Migration):

    dependencies = [
        ('histograma', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(añade_datos_iniciales),
    ]
