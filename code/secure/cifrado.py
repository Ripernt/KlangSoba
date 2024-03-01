from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
class Cifradito:
    def __init__(self):

        self.clave =  b'Fast-Stern123-CE'

        self.iv = b'Fast-Stern123-CE'

        self.cipher = Cipher(algorithms.AES(self.clave), modes.CFB(self.iv), backend=default_backend())

    def encriptado(self, plaintext):
        """
        Encripta el texto proporcionado.

        :param plaintext: El texto que se va a encriptar.
        :return: El texto cifrado.
        """
        if not isinstance(plaintext, str):
            raise ValueError("El texto debe ser una cadena de caracteres.")
        
        encryptor = self.cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        return ciphertext

    def desencriptado(self, ciphertext):
        """
        Descifra el texto cifrado proporcionado.

        :param ciphertext: El texto cifrado que se va a descifrar.
        :return: El texto descifrado.
        """
        if not isinstance(ciphertext, bytes):
            raise ValueError("El texto cifrado debe ser un objeto bytes.")
        
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode('utf-8')  # Decodificar a cadena de texto al descifrar

