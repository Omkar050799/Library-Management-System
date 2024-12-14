# library-management-system

Go to the directotry 

First Step :
pip install -r requirenment.txt for install the packages which we used in this project

Second Step:
Export the environment on which we wants to run our server, local for this use command,
export  DJANGO_SETTINGS_MODULE='library_management.settings.local'

Third Step : 
For User and Details first create Super User with command
python3 manage.py createsuperuser

Fourth Step :
After this we need to add some fixtures command which is required for User Authentication Process
for this we need to run command
python manage.py loaddata fixtures/oauth_provider.json
python manage.py loaddata fixtures/demoprj.json

Fifth Step:
Use python manage.py runserver 
for run the project

For Swagger you can use 
http://127.0.0.1:8000/api/v1/swagger/