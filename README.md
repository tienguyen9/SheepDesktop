# SheepDesktop
SheepDesktop is a part of the Sheep Tracker system, a complete system for registering sheep developed in conjunction with a Master's thesis submitted to NTNU.

## Getting Started
This section will show you how to run the application on Windows.
### Dependencies
* Python 3

### Installing
* If you don't have Python 3 installed, install it on https://www.python.org/downloads/ . The application has been tested with Python version 3.9.4. Make sure to check "Add Python 3.9 to PATH" on the first setup page. 
* Download the repository by cloning through git or by downloading the ZIP and unzipping.
* Open the Command Prompt and change the directory to the downloaded repository. This is done by entering "cd <path_to_repository>"
* Enter "python get-pip.py"
* Enter "python -m pip install -r requirements.txt*

## Launching
* Enter "python manage.py runserver" to launch the application
* In a web browser, enter 127.0.0.1:8000/ to display

The database files in the repository contain example data for demonstration purposes. When downloading a new database, this example data will be overwritten

## Google Drive Access
For using the Google Drive feature, a JSON file containing the appplication credentials are required. This file should be put in the root directory of the project. If you wish to test the feature, please contact contactsheeptracker@gmail.com to gain the credentials.

## Contact
For additional support, please contact: contactsheeptracker@gmail.com
