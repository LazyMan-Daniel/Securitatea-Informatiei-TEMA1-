# Tema 1

## Introducere 

Se doreste implementarea unei infrastructuri de comunicatie (server-client) ce utilizeaza criptosistemul AES si modurile de operare pentru cifrurile block ECB si OFB pentru criptarea traficului intre doua noduri A si B

## Librarii folosite:
In implementarea aceste infrastructuri am avut nevoie de urmatoarele librarii:
**Crypto** - pentru criptare ( pentru instalare **pip3 install pycryptodome**)
**random** - pentru generarea random a cheilor K si K'
**string** - pentru a genera chei de tip K si K' cat mai diverse

## Criptarea si decriptarea
ECB -> textul este impartit in blocuri de cate 16bytes si fiecare bloc 
       este criptat/decriptat cu cheia primita (de lungime 16bytes). Aceste
       blocuri sunt salvate intr-ul sir care va reprezenta mesajul codat/decodat
