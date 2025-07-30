
#se hace un conteo de latreas y a eso se les pone letras aleatorias cada ese numero de letras y luego se convierte en el sistema decimal en numeros 


import random
import string

def generar_con_ruido(palabra, ruido_len=5):
    resultado = ""
    for letra in palabra:
        # Generamos letras aleatorias antes y después de la letra real
        antes = ''.join(random.choices(string.ascii_lowercase, k=ruido_len))
        despues = ''.join(random.choices(string.ascii_lowercase, k=ruido_len))
        resultado += antes + letra + despues
    return resultado

# Ejemplo con 'lag'
mon = "lag"
resultado = generar_con_ruido(mon)
print("Resultado con 'lag':", resultado)

# Ejemplo con 'mania'
mon = "mania"
resultado = generar_con_ruido(mon)
print("Resultado con 'mania':", resultado)