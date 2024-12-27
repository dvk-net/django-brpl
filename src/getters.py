import utils, settings
from yaml import load, Loader

def get_project_config() -> dict:
    with open(settings.BASE_DIR.parent / "project-config.yaml") as fp:
        project_config_yaml = fp.read()
    return load(project_config_yaml, Loader=Loader)

def get_project_stages() -> list:
    project_config = get_project_config()
    return project_config['project']['stages']

def get_project_root():
    project_config = get_project_config()
    return settings.Path(project_config['project']['root_dir'])

def get_django_folder():
    config = get_project_config()['project']['django']
    return get_project_root() / config.get("project_folder_name", "django")

def get_django_src_folder_name() -> str:
    """Returns django source folder name inside django folder.
    Default is "src"

    Returns:
        str: src, or other name
    """
    config = get_project_config()['project']['django']
    return config.get('project_src_folder_name', "src")
