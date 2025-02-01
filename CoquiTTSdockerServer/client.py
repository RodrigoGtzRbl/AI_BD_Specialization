import socket
import os
import sounddevice as sd
import wave
import time
import numpy as np
import subprocess

# Server conf
host = '127.0.0.1'  # Server ip
port = 65432        # Server port

# Create the path vars
rootPath = os.getcwd()

audio_directory = os.path.join(rootPath, 'shared')
dockerComposePath = os.path.join(rootPath, 'kamehouse0-tts-server/docker-compose.yml')

# Start the container
startDocker = ["docker", "compose", "-f", f'{dockerComposePath}', "up", "-d"]
subprocess.run(startDocker)

print('Starting docker...')
# Loop to check if the file is received
while True:
    psDocker = ["docker", "compose", "-f", f'{dockerComposePath}', "ps"]
    output = subprocess.run(psDocker, capture_output=True, text=True)
    if "Up" in output.stdout:
        break
    else:
        print('Waiting for the connection...')
    time.sleep(1)

def sintetize(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # Make a conn that brokes when the 'with' statement is closed
        client_socket.connect((host, port)) # Connect to the server

        # Send and get a response
        client_socket.sendall(text.encode()) # Send msg
        response = client_socket.recv(1024).decode() # WAV file encoded: 172.18.0.1

        # Check the response, if there is not any response, it would end the function, broken the connection
        if not response:
            print('Server is not giving a response, try again')
            return False

        else:
            # Get the filename and construct the file path
            filename = response.split(': ')[1] + '.wav'
            filePath = os.path.join(audio_directory, filename,)
            # Check if the file is available
            while not os.path.exists(filePath):
                print(f"Waiting WAV {filename} in: .{filePath}... trying in 5s...")
                time.sleep(5)
            
            # Play audio
            print(f"Playing audio: {filename}")
            with wave.open( filePath, 'rb') as wf:
                audio_data = wf.readframes(wf.getnframes())
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                sd.play(audio_array, samplerate=wf.getframerate())
                sd.wait()
            
            # Delete the audio and exit from function
            os.remove(filePath)
            return True
#-------------------------------------------------------------------------------------------

# Loop to prevent not receiving any response from server
# Thats because server could take more than 5s in create a TTS instance
while True:
    result = sintetize('De... puta... madre...')
    if result:
        break
    else:
        print('Trying in 5s...')
        time.sleep(5)


# Close docker
stopDocker = ["docker", "compose", "-f", f'{dockerComposePath}', "stop"]
subprocess.run(stopDocker)
