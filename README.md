# django-brpl - New Django project with one command!

# Not tested on Windows! 
[Documentation](https://dvk-net.github.io/django-brpl/)

a collection of scripts to roll out Django projects localy:

## Requirements:
 - Docker, compose (actually optional if docker and compose sections have `generate: false`)
 - Python3

## How to use

1. Clone the repo
    ```bash
    git clone https://github.com/dvk-net/django-brpl
    ```
1. Create `venv` and install deps
    ```bash
    cd django-brpl
    python3 -m venv env # create venv
    . ./env/bin/activate  # activate venv
    pip install -r ./requirements.txt
    ```
1. Adjust `project-config.yaml`
1. CD into clonned repo's folder `src`
1. run to create a new Djungo project for local dev with docker
    ```python3
    python3 main.py
    ```
1. CD to your brend new project and run
    ```bash
    docker compose -f ./compose.dev.yaml up
    ```
    It will build a container with your Django app, map your local src folder, storage/media, storage/statis into your running container
1. Your app is ready for local development


### It will do the following:

1. Preate `root_dir` folder
1. Create using Jinja2 templates in `templates` dir:
    - .gitignore
    - README
    - LICENSE
1. Initiate a git repo
1. Create django project dir
1. Create virtual env
1. Install Django and other packages from `project-config.yaml` into venv
1. Create requirements.txt
1. Move `SECRET_KEY` into `local_settings.py`
1. Add `local_settings.py` into `.gitignore`
1. Adjust `settings.py` to use `SECRET_KEY` from `local_settings.py`
1. Create Dockerfile.dev
1. Create comp compose.dev.yaml

### TODO:


1. Unittests
1. Add first app
1. Add DRF
1. Add bootstrap
1. Dockerise 
    1. Add POSTGRE
    1. Redis

### Tested on Django 5.1.4
