import pickle
from flask import Flask, jsonify
from flask import request

app = Flask('churn-prediction')

model_file = open('model2.bin', 'rb')
model = pickle.load(model_file)

dv_file = open('dv.bin', 'rb')
dv = pickle.load(dv_file)

model_file.close()
dv_file.close()

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0,1]
    churn = y_pred >= 0.5

    result = {
        'churn_probability' : float(y_pred),
        'churn': bool(churn)
    }

    return jsonify(result)
