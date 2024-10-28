Create a virtual python environment on your computer. Install Django in the virtual environment. For the background info to work, you will need to install:


"pip install daphne"
"pip install --upgrade Django daphne channels"
"pip install -U rdflib"
"pip install django-background-tasks"
"pip install channels==4.1.0"
"pip install channels-redis==4.2.0"
"pip install charset-normalizer==3.3.2"
"pip install Django==5.1.2"
"pip install django-allauth==65.0.2"
"pip install django-background-tasks==1.2.8"
"pip install django-cleanup==9.0.0"
"pip install django-friendship==1.9.6"
"pip install django-htmx==1.19.0"
"pip install requests==2.32.3"
"pip install virtualenv==20.27.0"
"pip install beautifulsoup"

in your virtual environment. Clone this branch into the virtual environment. Run the command "python manage.py runserver" to start the server.

Admin page: http://localhost:8000/admin Login page: http://localhost:8000/login Register page: http://localhost:8000/register

Plug a URL into the search bar and it will then create a card that displays the video info
