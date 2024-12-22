import utils
import project_steps

def main():
    project_steps.create_project_root_structure()
    project_steps.start_django_project()
    # TODO: extract SECRET_KEY to local_settings.py
    # TODO: add bootstrap


if __name__ == "__main__":
    main()