##NomNow

NomNow is a restaurant recommending web application used to eliminate the hassle of indecisively filtering through long lists of restaurants when deciding where to eat. 

####Running the project:

1. Run "git clone git@github.com:RMWong/NomNow.git".

2. Go to the directory of the cloned project and run "pip install -r requirements.txt" to install all dependencies.

3. If running on a development server, locate the local_settings_template.py file and enter the appropriate keys to set the environment variables. Rename this file to local_settings.py to ensure that all keys are kept out of source control.

4. Run the application using "python manage.py runserver" in the terminal/command prompt.

Note: Ensure that the DEBUG variable in settings.py is set to False in production environments. Otherwise, set the DEBUG variable to True in development.

####Deploying to Heroku:

1. Specify the Python version in runtime.txt.

2. Enter all config variables specified in local_settings_template.py into Heroku. Because local_settings.py is in the .gitignore, the application will look for the config variables set in Heroku.
