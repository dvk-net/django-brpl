# django-brpl - New Django project with one command!

a collection of scripts to roll out Django projects localy: 

## How to use

1. Clone the repo
    ```bash
    git clone https://github.com/dvk-net/django-brpl
    ```
1. Adjust `project-config.yaml`
1. CD into clonned repo's folder `src`
1. run
    ```python3
    python3 main.py
    ```


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

### TODO:

1. Add first app
1. Add DRF
1. Add bootstrap
1. Dockerise 
    1. Add POSTGRE
    1. Redis
