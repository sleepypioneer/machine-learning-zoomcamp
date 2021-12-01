# Serverless

Using AWS lambda to run code at a dedicated end point. We are not required to set up EC2 instances and only get billed when our code is called.

## Creating Lambda function

- go to AWS console and search for lambda
- create function and give it a name, use author from scratch, chose Python3.9 environment and x86_64
- we can get input parameters from the event object in our function ie:

```python
def my_lambda(event, context):
    url = event["url"]
    prediction = predict(url)
    return {
        "prediction": prediction
    }
```

### Testing lamdba function

- click on test to set up a test and save it
- click deploy to deploy current version of code
- click test to run test and see output

## Tensor Flow lite

Tensflow is not ideal for lambda for a few reasons:

- large images require more $$ for storage
- slower initialisation (when first invoking the function) and need to pay for the stack
- slow to import == bigger RAM footprint

Tensorflow is a good approach to getting round this, it is a much smaller package. It can only be used for inference (model.predict), so not for training models.

## Convert notebook to script

```sh
jupyter nbconvert --to script week_nine_serverless.ipynb
```