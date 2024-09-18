# EXPRESS21_PARTNER_BE

## Description
A base template for Flask Back-End

## requirements
- this projects need to have python, pip, and git installed for setting up the apps

## Installation
1. First, you have to pull/download the codebase from git. The folder which our codebase is will be called "work folder" for future reference

2. Our apps will be running in virtual environment in order not to disrupt our other projects in our machine. In order to do so, run in our work folder command prompt
"python -m venv venv"
the command will enable our work folder to do virtual environment

3. before we setup our projects in our work folder, we have to enable virtual environment. So run
"venv\Scripts\activate.bat"
In the command prompt where we have our codebase and venv set

4. Afterwards, install all the dependencies in requirements.txt
- comment the "python-magic-bin" first
- "pip install -r requirements.txt"
- uncomment the "python-magic-bin"
- pip install again

5. Set up a .env file, ask for other developers for the .env variables value

## Database Setup

1. After we already install requirements for python, next we had to setup our database. Create an empty schema in the database first (postgresql or mysql, for now still using mysql), then insert the name of the database to our .env

2. do the migration in flask. Use the following command :
- flask db migrate (create migration version of our table)
- flask db upgrade (create table on our database based on the migration version)

if things go wrong, you can use "flask db downgrade" to reset the database update. But its not recommended to do so.

3. after we create our table, we need to initiate 1 account to start our operations in using our API
- create 1 role manually in the database directly, by doing SQL query to user_roles database
- create 1 account using API endpoint "account/register"

4. Try running the app using command
"python run.py"


## Environment File Config
CONFIGURATION_SETUP="config.DevelopmentConfig"
DB_USER="change"
DB_PASSWORD="change"
DB_HOST="localhost"
DB_PORT="change"
DEPLOY_PLATFORM="DEV"
DB_NAME="change"
SECRET_KEY="change"
