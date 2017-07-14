#!/usr/bin/python
# -*- coding: utf-8 -*-

from wspolne import podajIntZRozkladuGaussa

lista = []
for i in range(200):
    lista.append(podajIntZRozkladuGaussa(10.5, 4, 1, 20, 5))

print
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
    print element
