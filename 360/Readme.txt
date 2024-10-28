Create a virtual python environment on your computer. Install Django in the virtual environment. For the background info to work, you will need to install:


"pip install daphne"
"pip install --upgrade Django daphne channels"
"pip install -U rdflib"
"pip install django-background-tasks"
"channels==4.1.0"
"channels-redis==4.2.0"
"charset-normalizer==3.3.2"
"Django==5.1.2"
"django-allauth==65.0.2"
"django-background-tasks==1.2.8"
"django-cleanup==9.0.0"
"django-friendship==1.9.6"
"django-htmx==1.19.0"
"requests==2.32.3"
"virtualenv==20.27.0"

in your virtual environment. Clone this branch into the virtual environment. Run the command "python manage.py runserver" to start the server.

Admin page: http://localhost:8000/admin Login page: http://localhost:8000/login Register page: http://localhost:8000/register

Plug a URL into the search bar and it will then create a card that displays the video info
