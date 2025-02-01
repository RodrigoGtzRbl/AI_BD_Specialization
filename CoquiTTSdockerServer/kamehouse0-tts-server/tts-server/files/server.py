import socket
from TTS.api import TTS
import os

# Server conf
host = '0.0.0.0'  # Listening all interfaces
port = 65432      # Port

# Create socket to conn
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server listening in: {host}:{port}")

shared_directory = '/app/shared'

# Load TTS model
tts = TTS(model_name="tts_models/es/css10/vits")

# Loop to accept more than 1 conn
try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected with: {addr}")

        while True:
            data = conn.recv(1024)  # Receive clients data
            if not data:
                break  # Close conn if no data
            text = data.decode().strip()
            print(f"Text received: {text}")

            # Sintetize audio
            wav = tts.tts(text=text)

            ip_address = addr[0]
            file_path = os.path.join(shared_directory, f"{ip_address}.wav")

            # Saving audio
            tts.tts_to_file(text=text, file_path=file_path)
            
            # Send the path to the client
            conn.sendall(f"WAV file encoded: {ip_address}".encode())


        conn.close()
except KeyboardInterrupt:
    print("\Server closed manually")
finally:
    server_socket.close()
    print("Server closed")
