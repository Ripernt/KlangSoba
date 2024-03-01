from cifrado import Cifradito

cifrado = Cifradito()
texto = "holamundo"
texto_cifrado = cifrado.encriptado(texto)
print("texto cifrado" , texto_cifrado, type(texto_cifrado))

texto_decifrado = cifrado.desencriptado(texto_cifrado)
print("texto decifrado" , texto_decifrado)

