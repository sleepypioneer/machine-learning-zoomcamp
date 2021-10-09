# Deploying a model

## Saving and loading a model

We will save the model from the notebook to a pickle file which we can then import in our web service. Pickle is a built in for saving python objects.
First we create, train and evaluate our churn prediction model from previous weeks, then using the outcomes train out final model.

#### Saving the model

```python
import pickle

output_file = f'model_C={C}.bin'

with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out) # we write out also the dict vectorizer
    # file will be closed when we leave the with statement.
```

#### Loading the model

```python
import pickle 
# we dont have to import sklearn but we do need it installed on the machine where we are running this!!

with open(model_file, 'rb') as f_in:
   (dv, model) = pickle.load(f_in )
```

#### Using the model

```python
customer = {
    'gender': 'female',
    'partner': 'yes',
    ...
}

X = dv.transform([customer])

churn_prediction = model.predict_probab(X)[0, 1]
```

Normally the loading and using part we will not do in a notebook but rather in a python script as part of our a webserver/ application we want to use it in. We can also move the training code out to a python script. Jupyter Notebook allows us to do this easily as an export, which then requires minimum cleaning up. Perhaps we also want to add logging into this training script so we are aware of it's progress.


## Building webserver using flask

```python
app = Flask('ping')

@app.route('/ping', methods=['GET])
def ping():
    return 'pong'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
```

### Creating churn service

Building on our flask webserver we will now add the routes and functions to integrate our predict script using our model.


```python
# in predict.py
from flask import Flask
from flask import request

app = Flask('churn-prediction')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0,1]
    churn = y_pred >= 0.5

    result = {
        'churn_probability' : float(y_pred),
        'churn': bool(churn)
        # bool_ is coming from numpy which our service doesn't know how to turn into text so we need to wrap it!
        # similary we do this for y_pred by making it a float
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
    
```

### Calling our service from another service

```python
import requests

customer = {
    'gender': 'female',
    ...
}

requests.post(url, json=customer).json()
# returns python dictionary of response
```

### Production use server

This is a development server so we cannot use it in production. We need to use a wsig server, for example gunicorn.

```sh
gunicorn --bind 0.0.0.0:9696 predict:app
```

** Note that gunicorn does not work on windows! You could instead use waitress. **

## Virtual environment to keep our service isolated

- useful if different services want to use different versions of dependencies
- keeps the service isolated when running on dev machine
- options include virtual env, conda, pipenv, poetry

## Deployment Management with Docker

- lets us isolate even further
- each service runs in its own container

### Running a docker image

```sh
docker run -it --rm --entrypoint=bash python:3.8.12-slim
# enters bash console inside container using python image
```

### Creating our own container image

```dockerfile
from python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "model_C=1.0.bin", "./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]

```
 
```sh
docker run -p 9696:9696 -it <image-id> --bind 0.0.0.0
```

## Deploying to the cloud using AWS Elastic Beanstalk

- install eb cli (inside virtual environment)
- requires creating an account

`eb init -p docker -r eu-central-1 churn-serving`

creates project for elastic beanstalk. Now we can run the docker container on eb locally to test it.

`eb creat churn-serving-env`

- elastic beanstalk doesn't need the port
- in predict-test (file for calling our churn service) we should change the url to use the eb host

** Note this creates an open public endpoint which anyone can access on the web **

### Shut down your ec instance

`eb terminate churn-serving-env`

## Going further

### Things to try

- a different frame work (ie fastapi)
- 






