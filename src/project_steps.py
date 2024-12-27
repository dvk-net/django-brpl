import utils, settings, getters, copy

project_config = getters.get_project_config()
project_root = getters.get_project_root()

def create_project_root_structure():
    utils.delete_dir(project_config['project']['root_dir'])
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
    if not generate:
        settings.logger.info("Creating Django is disabled in settings - skipping")
        return
    django_folder_path = settings.Path(getters.get_django_folder())
    django_venv_path = django_folder_path / "env"
    packages = config.get("packages")
    utils.create_dir(django_folder_path)
    settings.logging.info(f"Django folder was created: {django_folder_path}")
    utils.create_python_venv(django_venv_path)
    utils.install_python_packages(django_venv_path, packages)
    requirements_txt = utils.get_pip_freeze_output(django_venv_path)
    utils.save_text_to_file(django_folder_path / "requirements.txt", requirements_txt)
    utils.create_dir(django_folder_path / getters.get_django_src_folder_name())
    utils.create_django_project(django_venv_path, settings.DEFAULT_PROJECT_NAME, django_folder_path / getters.get_django_src_folder_name())
    secret = utils.extract_secret_from_settings(django_folder_path / getters.get_django_src_folder_name() / settings.DEFAULT_PROJECT_NAME)
    changes = copy.deepcopy(settings.LOCAL_SETTINGS_STATIC_MEDIA_CHANGES_INIT_DEV)
    changes.update({'SECRET_KEY': secret})
    utils.update_local_settings_file(
        path_to_settings_folder=getters.get_django_folder() / getters.get_django_src_folder_name() / settings.DEFAULT_PROJECT_NAME,
        changes=changes)
    utils.update_settings_file(django_folder_path / getters.get_django_src_folder_name() / settings.DEFAULT_PROJECT_NAME)

def create_docker_images():
    django_folder = project_config['project']['django'].get("project_folder_name", "django")
    for stage in getters.get_project_stages():
        try:
            config = project_config['project']['django']['docker'][stage]

        except KeyError as e:
            settings.logger.warning(f"{e} environment is missing in django/docker config in yaml.")
            continue
        file_dest=project_root / django_folder / f"Dockerfile.{stage}"
        utils.create_file_from_template(
            config=config,
            file_dest=file_dest
        )
        settings.logger.info(f"Created Docker file {file_dest}")

def create_docker_compose():
    for stage in getters.get_project_stages():
        try:
            config = project_config['project']['compose'][stage]
        except KeyError as e:
            settings.logger.warning(f"{e} environment is missing in project/compose config in yaml.")
            continue
        if stage == "dev":
            utils.create_dir(project_root / "storage" / "media")
            utils.create_dir(project_root / "storage" / "static")
        file_dest=project_root / f"compose.{stage}.yaml"
        utils.create_file_from_template(
            config=config,
            file_dest=file_dest
        )
        settings.logger.info(f"Created compose file {file_dest}")
        utils.update_local_settings_file(
            getters.get_django_folder() / getters.get_django_src_folder_name() / settings.DEFAULT_PROJECT_NAME,
            settings.LOCAL_SETTINGS_STATIC_MEDIA_CHANGES_DOCKER_DEV
        )
        settings.logger.info(f"STATIC and MEDIA serttings were updated to be used with docker for {stage} stage")