Inserta en la carpeta ./pac los CSV de la Política Agrícola Común

En la carpeta `./poblacion` se encuentra un archivo que se ha generado
utilizando un shell script.

```
cat * | grep --invert-match Municipios | grep --invert-match \"\" | grep Total | cut --complement -d " " -f 1 | awk -F';' '{gsub("\\." , "" , $4); print $1 ";" $3 ";" $4}' > poblacion.csv
```

En la carpeta `./pac`, los datos se han limpiado utilizando:

```
cat B2017.csv | grep "Régimen de pago básico" | awk -F ';' '{gsub("," , "." , $5); print $2 ";" substr($3, 9) ";" $5}' > PAC2017.csv
```
