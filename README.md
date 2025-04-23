# Mini-RAG

This is a minimal implementation of the RAG model for question Answering .

## Requirements for windows
 
 - python 3.8 or later

### install Dependencies
```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```
 ##### install python using Miniconda for Windows

1) Download and install Miniconda .

2) create a new environment using the following command :
```bash 
$ conda create -n RAG python=3.8

```
3) Activate the environment :
```bash 
$ conda activate RAG 

```
## Requirements for WSL :

- python 3.8 or later

##### install WSL :
* Download and install the file following this link: 
```bash
https://github.com/microsoft/WSL/releases/tag/2.3.17

```
* open powershell as admin:
```bash
wsl --version
```

* install Ubuntu :
```bash
 wsl --install Ubuntu

 ```
 * open Ubuntu from start and create username and possword and apply :

 ```bash
 sudo apt update

 ```

* open the path project in Ubuntu  :
* open ubuntu terminal 
```bash
cd /mnt/path_project 

```
* for example :
```bash 
cd /mnt/c/Users/Desktop/RAG

```
* open the VScode from ubuntu terminal:
```bash

code .

```
#### Download miniconda inside vscode to use wsl :
```bash 
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

``` 
#### convert mode :
```bash
 chmod +x Miniconda3-latest-Linux-x86_64.sh  
```
#### install miniconda
```bash
./Miniconda3-latest-Linux-x86_64.sh

```
#### close and open vscode :

* create env:
```bash
conda create -n  RAG python=3.8

```
#### Activate the env :
```bash

conda activate RAG

```
#### shorten the code for Ubuntu :
```bash

export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "

```


#### Install the required packages
```bash
$ pip install -r requirements.txt
```

#### setup the environment variables

```bash
$ cp .env.copy .env
```
set your environment variables in the `.env` file like `OPENAI_API_KEY` value .

#### Run Docker compose :

```bash
cd docker
cp .env.example .env
```

* update `.env` with your credetials
#### This is a set of codes that work to clean and remove Containers and images to start over

#### Stop all Containers if used WSl and if used windows just remove sudo  in this code :
```bash
sudo docker stop $(docker ps -aq)
```

#### Remove all Containers:
```bash 
sudo docker rm $(docker ps -aq)
```

#### Remove all images :
```bash 
sudo docker rmi $(docker images -q) -f

```
#### cleaning all system :
```bash
sudo docker system prune -a --volumes
```
#### Run the docker compose :
```bash
sudo docker compose up -d
```


#### Run The API Server :
```bash 
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000

```

### Stop the docker compose :
```bash
sudo docker compose stop
```

### Update the Ubuntu in wsl :
```bash 
sudo apt update && sudo apt upgrade -y
```

### Install Rust and Cargo in wsl :
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

. "$HOME/.cargo/env"

```

### Run Ollama in google colab and convert the url local to public url

#### first download the ollama in linux :
```bash
!curl https://ollama.ai/install.sh | sh
```

#### Select the models :

```bash
ollama_model_id_1 = "gemma2:9b-instruct-q5_0"
ollama_model_id_2 ="nomic-embed-text" 

```

#### This is the kill server :
```bash
!pkill -f ollama
```

### pull the models :
```bash
!ollama pull {ollama_model_id_1}
!ollama pull {ollama_model_id_2}

```
###  Run the Ollama in backgraund and show the tail in this file :
```bash
!nohup bash -c "OLLAMA_HOST=0.0.0.0:8000 OLLAMA_ORIGIN=* ollama run {ollama_model_id_1}"  &
!nohup bash -c "OLLAMA_HOST=0.0.0.0:8001 OLLAMA_ORIGIN=* ollama run {ollama_model_id_2}"  &
!sleep 5 && tail /content/nohup.out
```

### Request the ollama model Generation :
```bash
%%bash
curl http://localhost:8000/api/chat -d '{
  "model": "gemma2:9b-instruct-q5_0",
  "stream": false,
  "messages": [
    { "role": "user", "content": "ما عاصمة مصر؟" }
  ]
}'
```

### Request the ollama model Embedding :
```bash
%%bash
curl http://localhost:8001/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'
```

### convert the url local to public url

#### install PyNgrok:
```bash
! pip install pyngrok==7.2.0
````
### Connect to token pyngrok and configration and apply public url.
#### model Generation:

```bash
from google.colab import userdata
from pyngrok import ngrok, conf

ngrok_auth = userdata.get('colab-ngrok')

conf.get_default().auth_token = ngrok_auth

port = "8000"

public_url = ngrok.connect(port).public_url
print(public_url)
```
#### model Embedding :
```bash
from google.colab import userdata
from pyngrok import ngrok, conf

ngrok_auth = userdata.get('colab-ngrok')

conf.get_default().auth_token = ngrok_auth

port = "8001"

public_url = ngrok.connect(port).public_url
print(public_url)
```
### now to use the puplic url in local or in colab :
```bash
%%bash
curl https://a0b3-34-143-137-ngrok-free.app/api/chat -d '{
  "model": "gemma2:9b-instruct-q5_0",
  "stream": false,
  "messages": [
    { "role": "user", "content": "ما عاصمة مصر؟" }
  ]
}'
```


### put public url in `.env` :
```bash
https://ac51-35-198-249-50.ngrok-free.app/v1
```
## postman collection :

download postman collection from [src/assets/mini-RAG.postman_collection_v3](src/assets/mini-RAG.postman_collection_v3)
