# Zadanie 1
Program gitopodobny znajduje się w katalogu zad1/jbgit

## Podstawowe wymagania
Python 2.7
## Wymagania uruchomienia testów jednostkowych
mock (https://pypi.python.org/pypi/mock)

## Instalacja
Instalacja poprzez wrzucenie symlinka do /usr/bin.
Należy uruchomić przez terminal skrypt install:
[~/jbgit]:sudo ./install

## Użycie 
W dowolnym miejscu od razu będzie się dało wywołać komendę "jbgit".

## Komendy
- **jbgit init** - tworzy z obecnego katalogu repozytorium, dodaje plik .jbgit
- **jbgit add [args]** - oznacza podane w [args] pliki jako staged
- **jbgit add * ** - robi podobnie dla wszystkich nowych lub zmienionych plikow, rekursywnie po calym repozytorium
- **jbgit commit** - commituje pliki staged file

Program dodatkowo :
- wykrywa usunięte pliki (zapomina o nich), 
- rozważa pliki w podkatalogach. Uwaga - użycie dir/* jest niepoprawne. "*" w zamyśle oznacza wszystko i może być użyte tylko samodzielnie,
- radzi sobie z dziwnymi ścieżkami w stylu "./dir/../dir/x". Jednocześnie nie doda nic spoza obecnego katalogu.

# Zadanie 2
