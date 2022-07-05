import os
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask_httpauth import HTTPBasicAuth
from connect_cloudsql import connect_sql
from connect_firestore import get_firestore_data
from connect_secret_manager import access_secret_version

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route("/")
def index():
    status = get_firestore_data(request.authorization.username, request.authorization.password)
    if request.authorization and status == "0":
        return ('Successfully Logged-in', 200, {
            'WWW-Authenticate': 'Basic realm="User not found"'
        })
    elif request.authorization and status == "1":
        return ('Incorrect Password', 401, {
            'WWW-Authenticate': 'Basic realm="User not found"'
        })
    else:
        return ('User Not Found', 401, {
            'WWW-Authenticate': 'Basic realm="User not found"'
        })


@app.route("/order", methods=["POST"])
def create_order():
    # data = request.get_json()
    # print('Request Data: ' + str(data))
    return jsonify({'msg': 'Order Created Successfully'})


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
