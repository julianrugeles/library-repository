from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    equipment_id = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    returned = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default="active")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "equipment_id": self.equipment_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "returned": self.returned,
            "status": self.status
        }
