Directory Structure
===========================

This overview describes the directory structure of the `watch360` project, highlighting important files and folders.

**Project Tree**::

| watch360/
| ├── watchapp/                # Main application folder with app-specific code
| │   ├── migrations/          # Django migrations
| │   ├── templates/           # HTML templates
| │   └── views.py             # Application views
| ├── docs/                    # Documentation files
| │   ├── source/              # Sphinx source files (.rst)
| │   └── build/               # Built HTML documentation
| ├── manage.py                # Django management script
| ├── requirements.txt         # List of dependencies
| └── README.md                # Project overview

Key Directories::

    - watchapp/: Contains core app code.
    - docs/: Holds Sphinx documentation files.
    - manage.py: Used to run and manage the Django project.
