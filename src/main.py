import utils
import project_steps

def main():
    project_steps.create_project_root_structure()
    project_steps.start_django_project()
    project_steps.create_docker_images()
    # TODO: extract SECRET_KEY to local_settings.py
    # TODO: add bootstrap


if __name__ == "__main__":
    main()