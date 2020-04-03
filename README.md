![MisClientes](https://i.ibb.co/CwrcqrW/Arco-Linux-2020-03-18-1584545696-screenshot-1366x768.jpg)
![MisClientes](https://i.ibb.co/3zHRXkv/Arco-Linux-2020-03-18-1584545727-screenshot-1366x768.jpg)
![MisClientes](https://i.ibb.co/mvDqNtD/Arco-Linux-2020-03-18-1584545739-screenshot-1366x768.jpg)

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

### Install WeasyPrint

* Please follow [this official guide](https://weasyprint.readthedocs.io/en/latest/install.html).

If you are using Debian like distributions you need to install these packages:

```sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info```


## Run server in local environment

### Clone this repository

````git
git clone https://github.com/dcruz1990/django-misclientes
````

### Activate virtualenv on .venv 

```
source .venv/bin/activate
```

### Run makemigrations

````
python manage.py makemigrations
````


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
