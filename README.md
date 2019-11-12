# django-misclientes
A simple django app to manage clients

Thanks to all [Django Cuba](https://t.me/DjangoCuba) Telegram Group!!!!!
* Luis Miguel Pozo Gonzalez
* @codeshard
* @Felix Pupo
* @Guillermo Roig


## Create virtual environment and install requirements

### Define virtualenv environment

```
virtualenv -p python .venv
```

### Install requirements

```
pip install -r requirements
```

## Run server in local environment

### Clone this repository

````git
git clone https://github.com/dcruz1990/django-misclientes
````

### Activate virtualenv on .venv 

```
source .venv/bin/activate
```

### Run migrations

````
python manage.py migrate
````

### Compile .po to .mo

````
python manage.py compilemessages
````

### Update assets

````
python manage.py collectstatic --noinput

````

### Run server for development 

```
python manage.py runserver
```

### Visit you application 

```
http://localhost:8000/
```

## Run with Docker

### Requirements
- Docker
- docker-compose
- Docker image for python >= 3.6 (https://hub.docker.com/_/python)  
- Docker image for nginx:alpine (https://hub.docker.com/_/nginx)

### Build and run containers stack with docker-compose

````
docker-compose -f ./container/docker-compose up -d --build
````

If it's the first time, wait to compile your application Docker's image or wait that required Docker's images be downloaded to compile your application Docker's image

### Visit you application

```
http://localhost/
```

## Contact
* druzbv1990@gmail.com
* lpozo1990@gmail.com


[]: https://t.me/DjangoCuba
