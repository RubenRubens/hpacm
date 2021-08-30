# h.p.a.c.m.

## Notas para desarrolladores

### Archivos con los datos de la Política Agrícola Común

Los archivos de la PAC disponibles en la página de la
[FEGA](https://www.fega.es/es/datos-abiertos/consulta-de-beneficiarios-pac/descarga-de-ficheros)
no se incluyen en el repositorio.
La forma de inclurlos es descargando los CSV de la ayudas por municipios en el directorio `datos/pac`.

### Credenciales de la base de datos

En primer lugar es necesario crear un archivo llamado `postgres_user` que
contenga el usuario de la base de datos y otro llamado `postgres_psswd` que
contenga la contraseña. Estos archivos son provados y no pueden ser
compartidos.

### Configuración de VSCode en el contenedor de desarrollo

`.vscode/settings.json`

```json
{
	"python.pythonPath": "/usr/local/bin/python"
}
```

`.env`

```
PYTHONPATH=src
```


### Ejecutar el servidor web (desde el contenedor)

```
./manage.py runserver 0.0.0.0:8000
```

### Acceder a la web (desde el host)

```
curl htttp://0.0.0.0:8000/hpacm
```
