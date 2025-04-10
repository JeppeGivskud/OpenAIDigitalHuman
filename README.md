Documenting the 10'th semester project (THE MASTER PROJECT)

We'll be doing AI stuff in here

The code is based on https://openai.github.io/openai-agents-python/voice/quickstart/
- openai-agents[voice]'
- soundfile
- sounddevice==0.4.2
- keyboard

The audio2face-3d is based on the streaming guide for omniverse audio2face-3d from https://docs.omniverse.nvidia.com/audio2face/latest/user-manual/audio2face-tool/streaming-audio-player.html

Required pip packages to be installed for A2F 2023.1
- grpcio==1.51.3
- numpy==1.22.4
- scipy==1.8.1
- sounddevice==0.4.2
- protobuf==3.17.3


# Setup

The following should be installed first:
- [ ] GIT https://git-scm.com/downloads
- [ ] Python 3.11 (this is due to the package scipy==1.8.1 which requires python < 3.11)
- [ ] virtuel envionment https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
    - [ ] pip install virtualenv

1) Open a folder where you want to store the project
2) Clone the project by pasting the following into terminal:

```
git clone https://github.com/JeppeGivskud/OpenAIDigitalHuman.git
cd OpenAIDigitalHuman
```

3) Make a virtual environment such that all the packages don't conflict and can be deleted again

```
python -m venv env
```
4) Find out which terminal you are using and activate the environment with the proper command for that terminal
For Bash:
```
source env/Scripts/activate
```

For powershell
```
env/Scripts/Activate
```

You should see (env) in your terminal.

5) Install all the required packages by pasting all these lines into the terminal. Make sure everything is installed properly

```
python.exe -m pip install --upgrade pip
pip install 'openai-agents[voice]'
pip install sounddevice==0.4.2
pip install scipy
pip install grpcio==1.51.3
pip install numpy==2.2.0
pip install protobuf==3.17.3
pip install soundfile
pip install keyboard
```

6) Get an OpenAPI key and export it into your path (DO NOT SHARE THIS KEY) https://platform.openai.com/docs/libraries?desktop-os=macOS#create-and-export-an-api-key

Now main.py should be able to run
