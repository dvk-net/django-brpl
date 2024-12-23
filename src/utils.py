import settings
import subprocess
import venv, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from yaml import load, Loader
from typing import List



def create_git_repo(repo_path):
    subprocess.run(['git', 'init', repo_path])

def load_project_config() -> dict:
    with open(settings.BASE_DIR.parent / "project-config.yaml") as fp:
        project_config_yaml = fp.read()
    return load(project_config_yaml, Loader=Loader)

def create_dir(dir_abs_path: str, parents: bool=True,  exist_ok: bool=True):
    path = Path(dir_abs_path)
    path.mkdir(parents=parents, exist_ok=exist_ok)

def save_text_to_file(file_name, text):
    with open(file_name, 'w') as fp:
        fp.write(text)

def render_jinja_template(template_file: str, context: dict, template_sub_folder):
    file_loader = FileSystemLoader(settings.BASE_DIR.parent / 'templates'/ template_sub_folder )
    jinja_env = Environment(loader=file_loader)
    jinja_env.globals["now"] = datetime.now()
    template = jinja_env.get_template(template_file)
    rendered_template = template.render(context)
    return rendered_template

def create_file_from_template(config: dict, file_dest: Path):
    generate = config.get('generate')
    if generate:
        template_sub_folder = config.get('template_sub_folder', "")
        template_file = config.get('file')
        if not template_file:
            raise ValueError('file creation is activated but filename was not provided')
        context = {}
        context['params'] = config['params']
        rendered_tex = render_jinja_template(template_file, context, template_sub_folder)
        save_text_to_file(file_dest, rendered_tex)
    else:
        settings.logging.warning("file creation is off")

def create_python_venv(venv_folder_path):
    create_dir(venv_folder_path)
    venv.create(venv_folder_path, with_pip=True)
    settings.logging.info(f"python virtual envoronment was created in: {venv_folder_path}")

def install_python_packages(env_path: Path, packages: List[str]):
    pip_executable = Path(env_path) / 'bin' / 'pip' if sys.platform != 'win32' else Path(env_path) / 'Scripts' / 'pip.exe'
    for package in packages:
        subprocess.run([pip_executable, 'install', package])
    settings.logging.info(f"Python packages: \n{"\n".join(packages)} \n were installed")

def get_pip_freeze_output(env_path: Path) -> str:
    pip_executable = Path(env_path) / 'bin' / 'pip' if sys.platform != 'win32' else Path(env_path) / 'Scripts' / 'pip.exe'
    result = subprocess.run([pip_executable, 'freeze'], capture_output=True, text=True)
    settings.logging.info("File requirements.txt was created")
    return result.stdout


def create_django_project(env_path, project_name, project_path):
    django_admin = Path(env_path) / 'bin' / 'django-admin' if sys.platform != 'win32' else Path(env_path) / 'Scripts' / 'django-admin.exe'
    subprocess.run([django_admin, 'startproject', project_name, project_path])
    settings.logging.info(f"Django project {project_name} was created")

def create_django_app(project_path, app_name):
    manage_py = Path(project_path) / 'manage.py'
    subprocess.run([sys.executable, manage_py, 'startapp', app_name], cwd=project_path)

def extract_secret_from_settings(path_to_settings) -> str:
    secret = ""
    with open(path_to_settings / "settings.py") as fp:
        for line in fp:
            if 'SECRET_KEY' in line:
                secret = line
        if not secret:
            raise ValueError("SECRET_KEY wasn't found in settings.py")
    return secret

def check_line_in_local_settings(path_to_settings, line) -> bool:
    result = False
    settings.logging.info(f"Checking if {line} was moved to local_settings.py")
    with open(path_to_settings / "local_settings.py") as fp:
        for file_line in fp:
            if line in file_line:
                result = True
                break
    if not result:
        settings.logging.warning("Line with `{line}` is missing in local_settings.py")


def update_settings_file(path_to_settings_folder):
    settings_py = ""
    with open(path_to_settings_folder / "settings.py") as fp:
        for line in fp:
            if 'from pathlib import Path' in line:
                settings_py += 'from . import local_settings\n' + line
                settings.logging.info("adding 'from . import local_settings'")
            elif 'SECRET_KEY' in line:
                settings_py += "SECRET_KEY = local_settings.SECRET_KEY\n"
                settings.logging.info("adding 'SECRET_KEY = local_settings.SECRET_KEY'")
                check_line_in_local_settings(path_to_settings_folder, 'SECRET_KEY')
            else:
                settings_py += line
    with open(path_to_settings_folder / "settings.py", "w") as fp:
        fp.write(settings_py)
        settings.logging.info("settings.py was updated")

