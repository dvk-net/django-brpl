import utils, settings

project_config = utils.load_project_config()
project_root = settings.Path(project_config['project']['root_dir'])

def create_project_root_structure():
    utils.create_dir(project_config['project']['root_dir'])
    settings.logger.info("Trying to create a license file")
    utils.create_file_from_template(
        project_config['project']['license'],
        project_root / 'LICENCE'
    )
    settings.logger.info("license file was created")
    settings.logger.info("Trying to create a gitignore file")
    utils.create_file_from_template(
        project_config['project']['gitignore'],
        project_root / '.gitignore'
    )
    settings.logger.info("gitignore file was created")
    settings.logger.info("Trying to create README file")
    utils.create_file_from_template(
        project_config['project']['readme'],
        project_root / 'README.md'
    )
    settings.logger.info("README file was created")
    settings.logger.info("Initialize git repo")
    utils.create_git_repo(project_root)
    settings.logger.info("git repo is created")

def start_django_project():
    """Creates Django Project
       Gets project.django yaml tree as config
       generate flag must be `true` to generate django project
    """
    config = project_config['project']['django']
    generate = config.get('generate')
    django_src_folder = config.get('project_src_folder_name', "src")
    django_folder = project_root / config.get("project_folder_name", "django")
    if generate:
        django_folder_path = settings.Path(django_folder)
        django_venv_path = django_folder_path / "env"
        packages = config.get("packages")
        utils.create_dir(django_folder_path)
        settings.logging.info(f"Django folder was created: {django_folder_path}")
        utils.create_python_venv(django_venv_path)
        utils.install_python_packages(django_venv_path, packages)
        requirements_txt = utils.get_pip_freeze_output(django_venv_path)
        utils.save_text_to_file(django_folder_path / "requirements.txt", requirements_txt)
        utils.create_dir(django_folder_path / django_src_folder)
        utils.create_django_project(django_venv_path, settings.DEFAULT_PROJECT_NAME, django_folder_path / django_src_folder)
        secret = utils.extract_secret_from_settings(django_folder_path / django_src_folder / settings.DEFAULT_PROJECT_NAME)
        utils.save_text_to_file(django_folder_path / django_src_folder / settings.DEFAULT_PROJECT_NAME/ "local_settings.py", secret)
        utils.update_settings_file(django_folder_path / django_src_folder / settings.DEFAULT_PROJECT_NAME)