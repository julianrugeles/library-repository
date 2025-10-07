import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Loan
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 🔗 Conexión a PostgreSQL (misma base "poli")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///users.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear tabla al iniciar el servicio
with app.app_context():
    db.create_all()

# --- ENDPOINTS ---

@app.route("/loans", methods=["GET"])
def get_loans():
    loans = Loan.query.all()
    return jsonify([l.to_dict() for l in loans]), 200

@app.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Préstamo no encontrado"}), 404
    return jsonify(loan.to_dict()), 200

@app.route("/loans", methods=["POST"])
def create_loan():
    data = request.get_json()
    if not data or "user_id" not in data or "equipment_id" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    # Validación mínima (podrías luego hacer peticiones a otros servicios)
    loan = Loan(
        user_id=data["user_id"],
        equipment_id=data["equipment_id"],
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d") if "end_date" in data else None
    )
    db.session.add(loan)
    db.session.commit()
    return jsonify(loan.to_dict()), 201

@app.route("/loans/<int:loan_id>/return", methods=["PUT"])
def return_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Préstamo no encontrado"}), 404

    loan.returned = True
    loan.status = "returned"
    loan.end_date = datetime.utcnow()
    db.session.commit()
    return jsonify(loan.to_dict()), 200

@app.route("/loans/user/<int:user_id>", methods=["GET"])
def get_loans_by_user(user_id):
    loans = Loan.query.filter_by(user_id=user_id).all()
    return jsonify([l.to_dict() for l in loans]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13003)
