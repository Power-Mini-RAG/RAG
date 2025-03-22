# mini-RAG

This is a minimal implementation of the RAg model for question Answering .

## Requirements
 
 - python 3.8 or later

 ##### install python using Miniconda 

1) Download and install Miniconda .

2) create a new environment using the following command :
```bash 
$ conda create -n RAG python =3.8

```
3) Activate the environment :
```bash 
$ conda activate RAG 

```

## instalation
### install the required packages
```bash
$ pip install -r requirements.txt
```

### setup the environment variables

```bash
$ cp .env.copy .env
```
set your environment variables in the 'env' file like 'OPENAI_API_KEY' value .

## Run The API Server :
```bash 
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000

```
## postman collection :
download postman collection from [text](assets/mini-RAG.postman_collection.json)

