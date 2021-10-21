from Crypto.Cipher import AES


class CryptoFile:
    ivBlock = b'8592572985981463'

    # pentru blocurile care nu contin 16 bytes se vor adauga spatii goale
    @staticmethod
    def fillBlock(block, fillValue, size):
        while len(block) < size:
            block += fillValue
        return block

    # se face xor intre blocurile de cate 16 bytes in procesul de criptare/decriptare
    @staticmethod
    def xoring(block1, block2):
        if type(block1) == str:
            block1 = block1.encode()
        if type(block2) == str:
            block2 = block2.encode()
        xored = bytearray()
        for first, second in zip(block1, block2):
            xored.append(first ^ second)
        return xored

    @staticmethod
    def ECBencrypt(message, key):

        first, last = 0, 16

        # transformam var key intr o variabila de tip bytes
        key = key.encode()
        cryptedMessage = "".encode()

        # aplicam algoritmul AES pe cheia noastra
        cipher = AES.new(key, AES.MODE_ECB)

        if len(message) < 16:
            message = CryptoFile.fillBlock(message, ' ', 16)

        while first < len(message):
            plainText = message[first:last]

            if len(plainText) < 16:
                plainText = CryptoFile.fillBlock(plainText, ' ', 16)

            # criptam blocul de 16 bytes cu cifrul calculat mai sus
            cryptedBlock = cipher.encrypt(plainText.encode())
            cryptedMessage = cryptedMessage + cryptedBlock

            #luam urmatorii 16 bytes din mesaj
            first = last
            last = min(last + 16, len(message))

        return cryptedMessage

    @staticmethod
    def ECBdecrypt(criptedMessage, key):

        first, last = 0, 16
        decryptedMessage = "".encode()

        # transformam var key intr o variabila de tip bytes
        key = key.encode()
        # aplicam algoritmul AES pe cheia noastra
        decrypter = AES.new(key, AES.MODE_ECB)

        while first < len(criptedMessage):
            # criptam blocul de 16 bytes cu cifrul calculat mai sus
            notPlainText = criptedMessage[first:last]
            decryptedMessage = decryptedMessage + decrypter.decrypt(notPlainText)

            first = last
            last = min(last + 16, len(criptedMessage))

        return decryptedMessage

    @staticmethod
    def OFBencrypt(message, key, initVector):
        first, last = 0, 16
        key = key.encode()
        cryptedMessage = "".encode()

        #transformam iv-ul intr o var de tip bytes ca sa putem sa criptam mesajul
        initVector = initVector.encode()
        #calculam cifrul cu ajutorul AES, in functie de iv
        cipher = AES.new(key, AES.MODE_OFB, iv=initVector)

        if len(message) < 16:
            message = CryptoFile.fillBlock(message, ' ', 16)

        while first < len(message):
            plainText = message[first:last]

            if len(plainText) < 16:
                plainText = CryptoFile.fillBlock(plainText, ' ', 16)

            initVector = cipher.encrypt(initVector)
            #folosim functia descrisa mai sus pentru a face xor intre iv-ul criptat si textul primit pentru a cripta blocul
            cryptedMessage += CryptoFile.xoring(plainText, initVector)

            first = last
            last = min(last + 16, len(message))

        return cryptedMessage

    @staticmethod
    def OFBdecrypt(criptedMessage, key, initVector):
        first, last = 0, 16
        key = key.encode()
        decryptedMessage = "".encode()

        initVector = initVector.encode()
        decrypter = AES.new(key, AES.MODE_OFB, iv=initVector)

        while first < len(criptedMessage):
            realMessage = criptedMessage[first:last]
            initVector = decrypter.encrypt(initVector)
            decryptedMessage += CryptoFile.xoring(realMessage, initVector)

            first = last
            last = min(last + 16, len(criptedMessage))

        print(decryptedMessage.decode('latin-1'))
        return decryptedMessage
