This is an example with two environments connected with sockets like client and server, the server is the venv39 (python 3.9) with coqui TTS, where the model is created and could be reusable, optimizing the TTS time.

The 'client' is the venv313 which sends text to the 'server' (venv39) to be sintetized.

The 'client' starts with subprocess the 'client', wait and make 5 tries to make the connection with the 'server'

To install the libraries you should use the requeriments.txt for venv39

If the comands from https://github.com/coqui-ai/TTS?tab=readme-ov-file are not working, use which tts to search the path and export it with export PATH=$PATH:/home/[user]/.local/bin
