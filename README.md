# Flasky
Flask小型社交应用，狗书内容的完整实现。  
改进：
 - 使用flask cli 代替 flask-script

## Get start
**!! Using `python3.6` or later version.**
```bash
$> git clone [this project]
```

## Commands
```
$> flask --help
```

## create and edit .env
```
DEV_DATABASE_URL=
FLASKY_ADMIN=
MAIL_SERVER=
MAIL_USERNAME=
MAIL_PASSWORD=
```

## Create Database and basic roles
```
$> flask deploy
```

## Database Migration
```bash
$ # do it only if no `migrations` folder under your project folder
$ flask db init
$ # do it every time before submitting changes of models
$ flask db migrate
$ # do it so database is upgraded with your changes of models
$ flask db upgrade
$ flask db --help
```
