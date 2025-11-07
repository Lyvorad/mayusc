
#se hace un conteo de latreas y a eso se les pone letras aleatorias cada ese numero de letras y luego se convierte en el sistema decimal en numeros 


import random
import string

def generar_con_ruido_circular(palabra, max_ruido=5):
    resultado = ""
    for i, letra in enumerate(palabra):
        # Contador reinicia después de max_ruido
        ruido_len = (i % max_ruido) + 1
        ruido = ''.join(random.choices(string.ascii_lowercase, k=ruido_len))
        resultado += ruido + letra
    return resultado

# Ejemplo
mon = "envolver"
print("Resultado con 'envolver':", generar_con_ruido_circular(mon))
