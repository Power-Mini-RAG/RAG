# mini-RAG

This is a minimal implementation of the RAG model for question Answering .

## Requirements for windows
 
 - python 3.8 or later

 ##### install python using Miniconda for Windows

1) Download and install Miniconda .

2) create a new environment using the following command :
```bash 
$ conda create -n RAG python =3.8

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
### install miniconda
```bash
./Miniconda3-latest-Linux-x86_64.sh

```
### close and open vscode :

* create env:
```bash
conda create -n  RAG python=3.8

```
## Activate the env :
```bash

conda activate RAG

```
### shorten the code for Ubuntu :
```bash

export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "

```


## Install the required packages
```bash
$ pip install -r requirements.txt
```

### setup the environment variables

```bash
$ cp .env.copy .env
```
set your environment variables in the `.env` file like `OPENAI_API_KEY` value .

### Run Docker compose :

```bash
cd docker
cp .env.example .env
```

* update `.env` with your credetials
##### This is a set of codes that work to clean and remove Containers and images to start over

##### Stop all Containers if used WSl and if used windows just remove sudo  in this code :
```bash
sudo docker stop $(docker ps -aq)
```

### Remove all Containers:
```bash 
sudo docker rm $(docker ps -aq)
```

### Remove all images :
```bash 
sudo docker rmi $(docker images -q) -f

```
### cleaning all system :
```bash
sudo docker system prune -a --volumes
```
### Run the docker compose :
```bash
sudo docker compose up -d
```


## Run The API Server :
```bash 
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000

```
## postman collection :
download postman collection from [text](assets/mini-RAG.postman_collection.json)

