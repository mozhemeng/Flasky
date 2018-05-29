# Flasky
A small SNS build by Flask and MySQL, Reference:<< Flask Web Development: Developing Web Application With Python >>
Improvement:
 - Use Flask CLI instead of Flask-Script
 - Use .env file to export environment variables

## Get start
**!! Using `python3.6` or later version.**
```bash
$ git clone [this project]
```

## Commands
```bash
$ flask --help
```

## Create and edit .env
```
DEV_DATABASE_URL=mysql+pymysql://username:password@localhost:3306/flasky?charset=utf8mb4
FLASKY_ADMIN=admin email address
FLASKY_MAIL_SENDER='Flasky <admin email address>'
MAIL_SERVER=smtp server for your admin email
MAIL_USERNAME=admin email address
MAIL_PASSWORD=admin email address password
```

## Create database and basic roles
```bash
$ flask deploy
```

## Database migration
```bash
$ # do it only if no `migrations` folder under your project folder
$ flask db init
$ # do it every time before submitting changes of models
$ flask db migrate
$ # do it so database is upgraded with your changes of models
$ flask db upgrade
$ flask db --help
```

## Run app
```bash
$ # use flask cli
$ flask run
$ # use gunicorn
$ gunicorn -w 4 -b 0.0.0.0:5000 manage:app
```
