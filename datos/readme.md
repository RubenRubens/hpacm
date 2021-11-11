Inserta en la carpeta ./pac los CSV de la Política Agrícola Común

En la carpeta ./poblacion se encuentra un archivo que se ha generado
utilizando un shell script.

```
cat * | grep --invert-match Municipios | grep --invert-match \"\" | grep Total | cut --complement -d " " -f 1 | awk -F';' '{print $1 ";" $3 ";" $4}' | sed 's/\.//' > poblacion.csv
```
