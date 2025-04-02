Documenting the 10'th semester project (THE MASTER PROJECT)

We'll be doing AI stuff in here

The code is based on https://openai.github.io/openai-agents-python/voice/quickstart/

# setup

Man skal have installeret
- [ ] GIT https://git-scm.com/downloads
- [ ] Python
- [ ] virtuel envionment https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

1) Åben en mappe i vscode hvor du gerne vil have projektet
2) Klon projektet og gå ind i mappen
```
git clone https://github.com/JeppeGivskud/OpenAIDigitalHuman.git
cd OpenAIDigitalHuman
```

3) Lav virtuelt miljø så du nemt kan slette alting igen 
4) Installer ting og sager
```
python -m venv env
source env/Scripts/activate
```

Hvis alt er gået godt og der står (env) foran din terminal
```
python.exe -m pip install --upgrade pip
pip install openai-agents[voice]
pip install sounddevice==0.4.2
pip install scipy
pip install grpcio==1.51.3
pip install numpy==2.2.0
pip install protobuf==3.17.3
pip install soundfile
```

5) Få fat i en OpenAPI nøgle (hold den hemmelig for guds skyld)
6) https://platform.openai.com/docs/libraries?desktop-os=macOS#create-and-export-an-api-key

Nu burde du kunne køre main.py
