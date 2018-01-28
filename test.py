#!/usr/bin/env python3

from wspolne import *

lista = []
for i in range(200):
    lista.append(podaj_int_z_rozkladu_Gaussa(10.5, 3, 1, 20, -2))

print()
nowa_lista = []
sek = []
ostatni = 0
for i, element in enumerate(sorted(lista)):
    if i == 0:
        sek.append(element)
        ostatni = element
        continue
    if element == ostatni:
        sek.append(element)
        if i == len(lista) - 1:
            if sek != []:
                nowa_lista.append(sek)
    else:
        if sek != []:
            nowa_lista.append(sek)
        sek = []

    ostatni = element

for element in nowa_lista:
    print(element)

# https://en.wikipedia.org/wiki/List_of_naval_ship_classes_in_service
