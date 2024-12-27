import settings
import subprocess, shutil
import venv, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from typing import List



def create_git_repo(repo_path):
    subprocess.run(['git', 'init', repo_path])

def delete_dir(dir_abs_path: str):
    dir_path = Path(dir_abs_path)
    try:
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
            settings.logger.info(f"Directory {dir_path} has been deleted.")
        else:
            settings.logger.info(f"Directory {dir_path} does not exist.")
    except Exception as e:
        settings.logger.error(f"Error: {e}")


def create_dir(dir_abs_path: str, parents: bool=True,  exist_ok: bool=True):
    path = Path(dir_abs_path)
    path.mkdir(parents=parents, exist_ok=exist_ok)
    settings.logger.info(f"Directory {dir_abs_path} has been created.")


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
    """Uses junja2 to create a file from a template

    Args:
        config (dict): a section in **project-config.yaml** file containing
                generate (bool): if the section must be processed
                template_sub_folder (str): subfolder in templates folder to look for the template
                template_file (str): template file to be used in `template_sub_folder`
        file_dest (Path): where to store the rendered file

    Raises:
        ValueError: if the template is missing
    """
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
    settings_py = []
    with open(path_to_settings_folder / "settings.py") as fp:
        for line in fp:
            if 'from pathlib import Path' in line:
                settings_py.append('from . import local_settings\n')
                settings_py.append(line)
                settings.logging.info("adding 'from . import local_settings'")
            elif 'SECRET_KEY' in line:
                settings_py.append("SECRET_KEY = local_settings.SECRET_KEY\n")
                settings.logging.info("adding 'SECRET_KEY = local_settings.SECRET_KEY'")
                check_line_in_local_settings(path_to_settings_folder, 'SECRET_KEY')
            elif "STATIC_URL = 'static/'" in line:
                settings_py.append("STATIC_URL = local_settings.STATIC_URL\n")
                settings_py.append("STATIC_ROOT = local_settings.STATIC_ROOT\n")
                settings_py.append("MEDIA_URL = local_settings.MEDIA_URL\n")
                settings_py.append("MEDIA_ROOT = local_settings.MEDIA_ROOT\n")
            else:
                settings_py.append(line)
    save_text_to_file(path_to_settings_folder / "settings.py", "".join(settings_py))


def update_local_settings_file(path_to_settings_folder, changes: dir):
    try:
        with open(path_to_settings_folder / "local_settings.py") as fp:
            initial_settings = fp.readlines()
    except FileNotFoundError:
        initial_settings = []
        settings.logging.info("file `initial_settings.py is missing and will be creted`")
    for look_for, change_to in changes.items():
        local_settings_py = []
        found = False
        for line in initial_settings:
            if look_for in line:
                local_settings_py.append(change_to + "\n")
                found = True
            else:
                local_settings_py.append(line)
        if not found:
            local_settings_py.append(change_to + "\n")
        initial_settings = None
        initial_settings = local_settings_py
    save_text_to_file(path_to_settings_folder / "local_settings.py", "".join(local_settings_py))