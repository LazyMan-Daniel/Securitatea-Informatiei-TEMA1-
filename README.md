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
OFB -> initialization vector-ul este criptat cu cheia data (ambele de lungime
       16 bytes). Blocul rezultat va fi folosit: 1. pentru a face xor cu 
       plaintext-ul si de a face rost de textul cifrat si 2. pentru a fi folosit
       ca initialization Vector pentru urmatorul bloc de criptat/decriptat
       
## Arhitectura aplicatiei
1. **Alegerea modului de criptare** de catre nodul **A**, urmand sa trimita nodului **B** aceasta infromatie
2. Se face schimbul de chei ( **KM** trimite lui **A** **cheia de criptare**, care prin **A** va ajunge si la **B**
3. **A** si **B** se folosesc de **K'** si **cheia de criptare** pentru a afla valoarea cheii **K**
4. **A** cripteaza continutul luat din fisierul message.txt cu cheia **K** si trimite mesajul criptat la **B**
5. **B** decripteaza mesajul folosind cheia **K** si afiseaza la consola rezultatul obtinut (mesajul decriptat)

## Infrastructura aplicatiei:
1. python CryptoFile.py
2. python main.py
3. text message.txt
       
