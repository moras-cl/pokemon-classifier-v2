# Como Generar un Dataset Propio

> [!CAUTION]
> Al generar un dataset mediante este método no se contempla el aumento de datos, el cual sí contiene el dataset por defecto utilizado en el archivo ``.ipynb``.

## Descripción

Esta carpeta contiene el archivo utilizado para generar el dataset mediante web scrapping, en el que se busca obtener alrededor de 500 imágenes por Pokémon, estas teniendo una resolución de ``224x224`` píxeles.

Sin embargo, finalmente se terminaron por utilizar tan solo 100 imágenes por Pokémon (sin contar aumentación), esto debido al tiempo que tomaría etiquetar manualmente la cantidad completa de imágenes (alrededor de 125.000).

Se decidió implementar un archivo auxiliar tipo ``.json``, esto para coordinar y distribuir la carga a través de los integrantes del equipo, además de que este enfoque permite guardar el progreso entre sesiones de scrapping.

Se decidió incluir múltiples categorías de imágenes para conformar el dataset, las cuales son las siguientes:
- ``<nombre_de_pokemon>``.
- ``<nombre_de_pokemon> pokemon anime``.
- ``<nombre_de_pokemon> pokemon illustration``.
- ``<nombre_de_pokemon> pokemon hd``.
- ``pokemon <nombre_de_pokemon> official art``.
- ``<nombre_de_pokemon> pokemon fanart``.
- ``<nombre_de_pokemon> pokemon 3d render``.
- ``<nombre_de_pokemon> pokemon card``.
- ``<nombre_de_pokemon> pokemon wallpaper``.

## Instrucciones

Para ejecutar el código se recomienda la creación de un entorno virtual de Python y la instalación de los requisitos mediante la siguiente serie de comandos de bash:

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

y posteriormente ejecutar el código mediante el siguiente comando bash

``` bash
python3 pokemon_playwright.py
```
