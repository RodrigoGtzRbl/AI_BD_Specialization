# **Local TTS using docker**

Here you can use [Coqui TTS](https://github.com/coqui-ai/TTS) in docker with the objetive of solving these problems:
- The instance of TTS could take more than 6s
- Sintetizing more than 1 time is required for achieve the proyect objective
- The venv with all the TTS libraries could take more than 7GB


<div align = "center">
If you have any of these problems (like me) that could be your solution
</div>

## Structure

The project is a venv with the python 3.13v which has:
- *client.py* as the main script of the project
- *kamehouse0-tts-server* dir; inside exists a docker compose file and another dir with the Dockerfile and another dir with files, these files are the requirements for the Dockerfile and the server script
- *shared* dir, this file is shared with the docker container making easy the audio connection between client and server


## How it works

***First of all, you need to create your own venv, then clone these files into your venv***

The client script uses 

- *os* library to create the paths
```python	
	rootPath = os.getcwd()

	audio_directory = os.path.join(rootPath, 'shared')
	dockerComposePath = os.path.join(rootPath, 'kamehouse0-tts-server/docker-compose.yml')	
```

- *subprocess* library to start and close the docker container, also checks the status of the container waiting to be up
```python	
	startDocker = ["docker", "compose", "-f", f'{dockerComposePath}', "up", "-d"]
	subprocess.run(startDocker)	
	
	while True:
    		psDocker = ["docker", "compose", "-f", f'{dockerComposePath}', "ps"]
    		output = subprocess.run(psDocker, capture_output=True, text=True)
    		if "Up" in output.stdout:
        		break
    		else:
        		print('Waiting for the connection...')
    		time.sleep(1)
```

- Function *sintetize* with a dinamic connection, that make able to close the connection dinamically

- *While* loop checking if the conn returns any response, thats because docker could takes a few seconds to start and the TTS instance could take more than 8 seconds, these loop prevents the broken pipe, because it creates a new connection with server every loop
```python	
	while True:
    	result = sintetize('De... puta... madre...')
    	if result:
        	break
   	 else:
   	     print('Trying in 5s...')
    	    time.sleep(5)
```


By the moment only spanish voice is set in server script, that could be easily changed starting the docker container and use the command:
```bash
tts --list_models
```




## License

This project is licensed under the MIT License - see the below for details.

MIT License

Copyright (c) 2025 Rodrigo Gutierrez Ribal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
