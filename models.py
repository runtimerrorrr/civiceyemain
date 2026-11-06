from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Report(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    hazard_type = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    latitude = db.Column(db.Float, nullable=True)

    longitude = db.Column(db.Float, nullable=True)

    address = db.Column(db.String(300), nullable=True)

    image_filename = db.Column(db.String(255), nullable=True)

    severity = db.Column(db.String(50), nullable=True)

    status = db.Column(db.String(50), default="Pending")

    complaint_letter = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            "complaint_id": self.complaint_id,
            "hazard_type": self.hazard_type,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "image_filename": self.image_filename,
            "severity": self.severity,
            "status": self.status,
            "complaint_letter": self.complaint_letter,
            "created_at": self.created_at.isoformat()
        }