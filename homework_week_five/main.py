from flask import Flask
from flask import request

app = Flask('ping')

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)