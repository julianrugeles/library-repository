from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# URLs internas de los servicios (Docker Compose network)
USER_SERVICE_URL = "http://user_service:13000"
EQUIPMENT_SERVICE_URL = "http://equipment_service:13002"
LOAN_SERVICE_URL = "http://loan_service:13003"

# -------------------------------
# USERS
# -------------------------------
@app.route("/api/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        res = requests.get(f"{USER_SERVICE_URL}/users")
    else:
        res = requests.post(f"{USER_SERVICE_URL}/users", json=request.json)
    return jsonify(res.json()), res.status_code


@app.route("/api/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user_detail(user_id):
    url = f"{USER_SERVICE_URL}/users/{user_id}"
    if request.method == "GET":
        res = requests.get(url)
    elif request.method == "PUT":
        res = requests.put(url, json=request.json)
    else:
        res = requests.delete(url)
    return jsonify(res.json()), res.status_code


# -------------------------------
# EQUIPMENT
# -------------------------------
@app.route("/api/equipment", methods=["GET", "POST"])
def equipment():
    if request.method == "GET":
        res = requests.get(f"{EQUIPMENT_SERVICE_URL}/equipment")
    else:
        res = requests.post(f"{EQUIPMENT_SERVICE_URL}/equipment", json=request.json)
    return jsonify(res.json()), res.status_code


@app.route("/api/equipment/<int:equipment_id>", methods=["GET", "PUT", "DELETE"])
def equipment_detail(equipment_id):
    url = f"{EQUIPMENT_SERVICE_URL}/equipment/{equipment_id}"
    if request.method == "GET":
        res = requests.get(url)
    elif request.method == "PUT":
        res = requests.put(url, json=request.json)
    else:
        res = requests.delete(url)
    return jsonify(res.json()), res.status_code


# -------------------------------
# LOANS
# -------------------------------
@app.route("/api/loans", methods=["GET", "POST"])
def loans():
    if request.method == "GET":
        res = requests.get(f"{LOAN_SERVICE_URL}/loans")
    else:
        res = requests.post(f"{LOAN_SERVICE_URL}/loans", json=request.json)
    return jsonify(res.json()), res.status_code


@app.route("/api/loans/<int:loan_id>", methods=["GET", "PUT", "DELETE"])
def loan_detail(loan_id):
    url = f"{LOAN_SERVICE_URL}/loans/{loan_id}"
    if request.method == "GET":
        res = requests.get(url)
    elif request.method == "PUT":
        res = requests.put(url, json=request.json)
    else:
        res = requests.delete(url)
    return jsonify(res.json()), res.status_code


@app.route("/")
def index():
    return jsonify({"message": "Gateway activo y funcionando 🚀"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13005)
