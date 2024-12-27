import utils
import project_steps

def main():
    project_steps.create_project_root_structure()
    project_steps.start_django_project()
    # TODO: create_docker_images for all blocks
    project_steps.create_docker_images()
    project_steps.create_docker_compose()
    # TODO: extract SECRET_KEY to local_settings.py
    # TODO: add bootstrap


if __name__ == "__main__":
    main()