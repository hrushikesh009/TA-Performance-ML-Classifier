# Flask JWT Auth

[![Build Status](https://travis-ci.org/realpython/flask-jwt-auth.svg?branch=master)](https://travis-ci.org/realpython/flask-jwt-auth)

## Want to learn how to build this project?

The initiative is centered on assessing the Teaching Assistant's performance using the Teaching Assistant Evaluation Dataset. The information is comprised of assessments of teaching effectiveness from three ordinary semesters and two

151 TA engagements throughout the summer semesters at the Statistics Department of Madison's University of Wisconsin. The scores were split into three fairly equal groups. categories ("low", "medium", and "high") ("low", "medium", and "high").

## Machine Learning Model
Around the dataset, I created a machine learning model, which I served and deployed using a Flask microservice.

I built a Machine learning model around the dataset and utilize Flask microservice to serve and deploy the model.

## Teaching Assistant Evalution

### Endpoint:
`
/home
`

visit the home page fill basic form of the feature to evaluate the TA assistant.

If the form is completed and submitted, you will receive a projected score based on your data.

## Backend Services

In the Backend 

`
/predict_score
`
Score prediction endpoint Evulates processes the user-submitted form model's data before feeding it to the model. The model evaluates a projected score, and the result is shown on the output.html page.

### Endpoints
1. /add_TA [POST]

2. /update_ta/<int:id>['PUT']

3. /retrieve_ta/<int:id>,['GET']

4. /delete_ta/<int:id,['DELETE']

Note: The above endpoints are JWT token protected to utilize the service users first need to 

5. register_user/ #Register New User

6. login_user/ #Generate Unique Token for authencation

The microservice is Simple yet elegant.
Minor adjustments. Flask includes a simple microservice where you could add, edit, generate, and alter the TA dataset at any time.

## Want to use this project?

### Basics

1. Fork/Clone
1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *project/server/config.py*, and then run:

```sh
$ set APP_SETTINGS="server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

Create a .env folder and place the secret key inside:

```sh
$ SECRET_KEY="change_me"
```

### Create DB

Create the databases in `mysql` or Database of your Choice:

```sh
$ create database <Database Name>
# \q
```

Create the tables and run the migrations:

```sh
$ Set Flask_APP = manage.py
$ Flask Sheel
$ From auth.models import db
$ db.create_all()
```

### Run the Application

```sh
$ python manage.py runserver
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

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
