This is an example with two environments connected with sockets like client and server, the server is the venv39 (python 3.9) with coqui TTS, where the model is created and could be reusable, optimizing the TTS time.

The 'client' is the venv313 which sends text to the 'server' (venv39) to be sintetized.

The 'client' starts with subprocess the 'client', wait and make 5 tries to make the connection with the 'server'

To install the libraries you should use the requeriments.txt for venv39

If the comands from https://github.com/coqui-ai/TTS?tab=readme-ov-file are not working, use which tts to search the path and export it with export PATH=$PATH:/home/[user]/.local/bin




## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
