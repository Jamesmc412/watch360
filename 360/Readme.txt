Create a virtual python environment on your computer. Install Django in the virtual environment. For the background info to work, you will need to install:


"pip install daphne"
"pip install --upgrade Django daphne channels"
"pip install -U rdflib"
"pip install django-background-tasks"

in your virtual environment. Clone this branch into the virtual environment. Run the command "python manage.py runserver" to start the server.

Admin page: http://localhost:8000/admin Login page: http://localhost:8000/login Register page: http://localhost:8000/register

Plug a URL into the search bar and it will then create a card that displays the video info
