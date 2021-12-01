from io import BytesIO
from urllib import request

import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_input(x):
    x *= 1./255
    return x


def preprocess(img):
    x = np.array(img, dtype="float32")
    X = np.array([x])
    
    X = preprocess_input(X)
    return X
    

def predict(url):
    classes = ["cats", "dog"]
    
    img = download_image(url)
    img = prepare_image(img, (150, 150))

    X = preprocess(img)
    
    interpreter = tflite.Interpreter(model_path='cats-dogs-v2.tflite')
    interpreter.allocate_tensors()

    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    float_predictions = preds[0].tolist()

    return dict(zip(classes, float_predictions))


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result