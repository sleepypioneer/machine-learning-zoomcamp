from PIL import Image

import numpy as np
from tflite_runtime import tflite


def import_data(file_path, target_size):
    with Image.open(file_path) as img:
        img = img.resize(target_size, Image.NEAREST)
        
    return img


def preprocess_input(x):
    x /= 127.5
    x -= 1.
    return x


def preprocess(img):
    x = np.array(img, dtype="float32")
    X = np.array([x])
    
    X = preprocess_input(X)
    return X


def get_predictions(interpreter, classes, X):
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]
    
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    
    return dict(zip(classes, preds[0]))


def predict(url, target_size=(299,299)):
    img = import_data(url, target_size)

    img = import_data(img)
    X = preprocess(img)
    interpreter = tflite.Interpreter(model_path="data/clothing-model.tflite")
    interpreter.allocate_tensors() 
    predictions = get_predictions(interpreter, classes, X)
    predictions
