import requests

customer = {
    "contract": "two_year",
    "tenure": 1,
    "monthlycharges": 10
}

customer2 = {
    "contract": "two_year",
    "tenure": 12,
    "monthlycharges": 10
}

url = 'http://localhost:9696/predict'

resp = requests.post(url, json=customer).json()

print(f'The customer will churn: {resp["churn"]}.' +
 f'The probability the customer is churning is {resp["churn_probability"]:.4f}')