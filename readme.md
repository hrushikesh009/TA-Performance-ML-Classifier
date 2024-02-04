# Project Overview

## Purpose

This initiative focuses on evaluating Teaching Assistant (TA) performance using the Teaching Assistant Evaluation Dataset. Comprising assessments from various semesters and summer engagements, scores are categorized as "low," "medium," and "high."

## Machine Learning Model

Built around the dataset, a machine learning model is created and deployed through a Flask microservice.
If you are interested in going deeper into the understanding and training of the ML model, please see `TA_Performance_ML_Classifier.ipynb`. It offers a complete guide to training, evaluating, and fine-tuning/optimizing the ML model.

## TA Evaluation

### Endpoint: `/home`

Visit the home page, fill a basic form to evaluate TA performance. Upon form submission, receive a projected score based on provided data.

## Backend Services

### Endpoint: `/predict_score`

This endpoint processes user-submitted data before feeding it to the model. The evaluated score is displayed on the output.html page.

### Microservice Endpoints

1. `/add_TA [POST]`
2. `/update_ta/<int:id> [PUT]`
3. `/retrieve_ta/<int:id> [GET]`
4. `/delete_ta/<int:id> [DELETE]`

Note: Above endpoints are JWT token-protected. Users register and generate unique tokens to access these services.

5. `/register_user` - Register new user
6. `/login_user` - Generate unique token for authentication

The microservice design is simple yet elegant.

## Using the Project

### Basics

1. **Fork/Clone**
2. **Activate a virtualenv**
3. **Install requirements**

### Set Environment Variables

Update *project/server/config.py* and run:

```sh
$ set APP_SETTINGS="server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

Create a .env file and place the SECRET_KEY:

```sh
$ SECRET_KEY="change_me"
```

### Create Database

Create databases in `mysql` or your chosen database:

```sh
$ create database <Database Name>
```

Create tables and run migrations:

```sh
$ Set Flask_APP = manage.py
$ Flask Shell
$ From auth.models import db
$ db.create_all()
```

### Run the Application

```sh
$ python manage.py runserver
```

Access the application at [http://localhost:5000/](http://localhost:5000/)

> Specify a different port:

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ cd test
$ python test_auth.py #Authentication
$ python test.py      #Microservice to CURD TA
$ python test_config.py # Configuration 
```