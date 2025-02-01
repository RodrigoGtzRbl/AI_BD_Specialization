# servidor.py en venv39
import socket
from TTS.api import TTS
import sounddevice as sd

# Configuración del servidor
host = '127.0.0.1'  # IP local
port = 65432        # Puerto

# Crear el socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Servidor escuchando en {host}:{port}")
tts = TTS(model_name="tts_models/es/css10/vits")

# Bucle para aceptar múltiples conexiones
try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break  # Cierra la conexión si no hay datos
            print(f"Mensaje recibido: {data.decode()}")

            wav = tts.tts(text=data.decode())
            sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
            sd.wait()
            
            # Responder al cliente
            conn.sendall(b'Mensaje sintetizado')

        conn.close()
except KeyboardInterrupt:
    print("\nServidor detenido manualmente")
finally:
    server_socket.close()
    print("Servidor cerrado")
    
 