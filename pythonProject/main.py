from CryptoFile import CryptoFile
import random
import string


class manager:
    def __init__(self, text, K, Ksecund, cheieCriptare, iv):
        self.text = text
        self.K = K
        self.Ksecund = Ksecund
        self.cheieCriptare = cheieCriptare
        self.iv = iv

    def generareRandomK(self, nrBytes):
        self.K = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(nrBytes))
        print("[KM] Am generat random pe K -line 15")
        print(f"Cheia K este {self.K}")
        print("__")

    def generareCheieCriptare(self, tipCriptare):
        if (tipCriptare == "ecb") or (tipCriptare == "ECB"):
            return CryptoFile.ECBencrypt(self.K, self.Ksecund)
        if (tipCriptare == "ofb") or (tipCriptare == "OFB"):
            return CryptoFile.OFBencrypt(self.K, self.Ksecund, self.iv)


class nodA:
    def __init__(self, mesaj, mesajCriptat, K, Kprim, iv, cheieCriptare):
        self.mesaj = mesaj
        self.mesajCriptat = mesajCriptat
        self.K = K
        self.iv = iv
        self.Kprim = Kprim
        self.cheieCriptare = cheieCriptare
        print("[A] alege modul de criptare (ecb/ofb)")
        self.tipCriptare = input()

    def incepeComunicarea(self, KM, B):
        print("[A] incep comunicarea cu B si KM pentru cheia de criptare -line 39")
        self.cheieCriptare = KM.generareCheieCriptare(tipCriptare=self.tipCriptare)
        B.cheieCriptare = self.cheieCriptare
        B.tipCriptare = self.tipCriptare
        print(f"[A] cheia de criptare este {self.cheieCriptare} -line 43")

    def decripteazaK(self):
        if (self.tipCriptare == 'ecb'):
            self.K = CryptoFile.ECBdecrypt(self.cheieCriptare, self.Kprim).decode()
            print(f"[A] AM decriptat cheia K: {self.K} -line 48")
        if (self.tipCriptare == 'ofb'):
            self.K = CryptoFile.OFBdecrypt(self.cheieCriptare, self.Kprim, self.iv).decode()
            print(f"[A] Am decriptat cheia K: {self.K} -line 51")

    def cripteazaMesaj(self):
        if self.tipCriptare == 'ecb':
            self.mesajCriptat = CryptoFile.ECBencrypt(self.mesaj, self.K)
        if self.tipCriptare == 'ofb':
            self.mesajCriptat = CryptoFile.OFBencrypt(self.mesaj, self.K, self.iv)
        print(f"[A] Am citit mesajul:: {self.mesaj} -line 58")
        print(f"[A] Si l-am criptat in {self.mesajCriptat.decode('latin-1')} -line 58")

    def trimiteMesajLaB(self, B):
        B.mesajCriptat = self.mesajCriptat
        print("[A] Mesajul criptat ajunge la B -line 62")


class nodB:
    def __init__(self, mesaj, mesajCriptat, K, Kprim, iv, cheieCriptare, tipCriptare):
        self.mesaj = mesaj
        self.mesajCriptat = mesajCriptat
        self.K = K
        self.iv = iv
        self.Kprim = Kprim
        self.cheieCriptare = cheieCriptare
        self.tipCriptare = tipCriptare

    def decripteazaK(self):
        if (self.tipCriptare == 'ecb'):
            self.K = CryptoFile.ECBdecrypt(self.cheieCriptare, self.Kprim).decode()
            print(f"[B] Am decriptat cheia K: {self.K} -line 77")
        if (self.tipCriptare == 'ofb'):
            self.K = CryptoFile.OFBdecrypt(self.cheieCriptare, self.Kprim, self.iv).decode()
            print(f"[B] Am decriptat cheia K: {self.K} -line 80")

    def decripteazaMesaj(self):
        if self.tipCriptare == 'ecb':
            self.mesaj = CryptoFile.ECBdecrypt(self.mesajCriptat, self.K).decode('latin-1')
        if self.tipCriptare == 'ofb':
            self.mesaj = CryptoFile.OFBdecrypt(self.mesajCriptat, self.K, self.iv).decode('latin-1')
        print(f"[B] Decriptez mesajul, acesta fiind:")
        print(self.mesaj)


if __name__ == '__main__':
    # Construim un iv global care va fi in A,B si KM
    iv = '8592572985981463'

    # Generam RANDOM cheia K' pe care o vom trimite la KM,A si B
    cheiaKprim = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))

    # Construim KeyManager-ul, oferindu-i cheia K' si construind random pe K
    KM = manager("", "", cheiaKprim, "", iv)
    KM.generareRandomK(16)

    # Am construit A si B, cunoscand DOAR IV si K'
    A = nodA("", "", "", cheiaKprim, iv, "")
    B = nodB("", "", "", cheiaKprim, iv, "", "")

    # Incepem comunicarea dintre A si KM
    A.incepeComunicarea(KM, B)

    # Atat A, cat si B decripteaza pe K
    A.decripteazaK()
    B.decripteazaK()

    print("Citim din fisier mesajul, in introducem in A, unde il criptam cu K")
    # Citim din fisier mesajul
    file = open('message.txt', 'r')
    A.mesaj = file.read()

    # Criptam in A mesajul
    A.cripteazaMesaj()
    # Trimitem de la A la B mesajul criptat
    A.trimiteMesajLaB(B)
    # B decripteaza mesajul si il afiseaza
    B.decripteazaMesaj()
