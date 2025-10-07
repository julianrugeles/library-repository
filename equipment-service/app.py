from flask import Flask, jsonify, request
from models import db, Equipment
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)

# 🔗 Conexión a PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///users.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas al inicio
with app.app_context():
    db.create_all()

# --- ENDPOINTS ---

@app.route("/equipment", methods=["GET"])
def get_equipment():
    equipment = Equipment.query.all()
    return jsonify([e.to_dict() for e in equipment]), 200

@app.route("/equipment/<int:equipment_id>", methods=["GET"])
def get_equipment_by_id(equipment_id):
    eq = Equipment.query.get(equipment_id)
    if not eq:
        return jsonify({"error": "Equipo no encontrado"}), 404
    return jsonify(eq.to_dict()), 200

@app.route("/equipment", methods=["POST"])
def create_equipment():
    data = request.get_json()
    if not data or "name" not in data or "type" not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    eq = Equipment(
        name=data["name"],
        type=data["type"],
        status=data.get("status", "available"),
        description=data.get("description"),
        available=data.get("available", True)
    )
    db.session.add(eq)
    db.session.commit()
    return jsonify(eq.to_dict()), 201

@app.route("/equipment/<int:equipment_id>", methods=["PUT"])
def update_equipment(equipment_id):
    eq = Equipment.query.get(equipment_id)
    if not eq:
        return jsonify({"error": "Equipo no encontrado"}), 404
    data = request.get_json()
    eq.name = data.get("name", eq.name)
    eq.type = data.get("type", eq.type)
    eq.status = data.get("status", eq.status)
    eq.description = data.get("description", eq.description)
    eq.available = data.get("available", eq.available)
    db.session.commit()
    return jsonify(eq.to_dict()), 200

@app.route("/equipment/<int:equipment_id>", methods=["DELETE"])
def delete_equipment(equipment_id):
    eq = Equipment.query.get(equipment_id)
    if not eq:
        return jsonify({"error": "Equipo no encontrado"}), 404
    db.session.delete(eq)
    db.session.commit()
    return jsonify({"message": "Equipo eliminado"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13002)
