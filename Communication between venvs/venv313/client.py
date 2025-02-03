# cliente_control.py en venv312
import subprocess
import time
import socket
from pathlib import Path

# Define la ruta al script 'scriptTTS.py' y los argumentos
path = Path().resolve()

venv39 = path / 'venv39'
python_venv39 = venv39 / 'bin' / 'python3.9'

server = venv39 / 'server.py'


# Configuración del servidor
servidor_script = server

# Iniciar el servidor en un subproceso
subprocess.Popen([python_venv39, servidor_script], cwd=venv39, shell=False)

# Esperar un poco para asegurarse de que el servidor esté listo (ajusta el tiempo si es necesario)
time.sleep(5)

# Configuración del cliente para conectarse al servidor
host = '127.0.0.1'
port = 65432

max_intentos = 5
# Intentar conectar al servidor con un bucle
for intento in range(1, max_intentos + 1):
    try:
        # Crear el socket cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Conexión al servidor exitosa")
        break  # Salir del bucle si la conexión es exitosa
    except ConnectionRefusedError:
        print(f"Intento {intento}: No se pudo conectar al servidor. Esperando 2 segundos...")
        time.sleep(2)
        if intento == max_intentos:
            print("Se alcanzó el número máximo de intentos. No se pudo conectar al servidor.")
            break
    except Exception as e:
        print(f"Error inesperado en el intento {intento}: {e}")
        break

# Enviar un mensaje al servidor
client_socket.sendall(b'Mensaje del cliente')

# Recibir la respuesta del servidor
response = client_socket.recv(1024)
print(f"Respuesta del servidor: {response.decode()}")


mensajes = [
    "Hola, soy el cliente 1",
    "Mensaje de prueba, cliente 2",
    "Conexión establecida, cliente 3",
    "Datos enviados, cliente 4",
    "Mensaje corto, cliente 5",
    "¡Hola desde el cliente 6!",
    "Mensaje de prueba número 7",
    "Cliente 8: prueba de comunicación",
    "Mensaje de cliente 9, ¿me escuchas?",
    "Cliente 10, ¡saludos desde el otro lado!"
    ]

for i in range(0,10):
    print(f'{i+1}. Mandando mensaje: {mensajes[i]}')
    client_socket.sendall(mensajes[i].encode())
    response = client_socket.recv(1024)
    time.sleep(3)


# Cerrar la conexión
client_socket.close()

