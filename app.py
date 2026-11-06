
import os
import uuid

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from config import Config
from models import db, Report
from image_utils import validate_image, generate_image_filename
def classify_hazard(description, hazard_type):
    text = description.lower()

    keywords = {
        "pothole": ["deep", "large", "dangerous", "accident", "road damage"],
        "garbage": ["overflowing", "rotten", "waste", "dumping", "smell"],
        "open manhole": ["open", "uncovered", "broken", "dangerous"],
        "waterlogging": ["flood", "standing water", "overflow", "blocked"],
        "broken streetlight": ["dark", "not working", "broken", "no light"]
    }

    matched = sum(
        1 for word in keywords.get(hazard_type, [])
        if word in text
    )

    if matched >= 2:
        return "Critical"
    elif matched == 1:
        return "High"
    else:
        return "Medium"


def generate_complaint_letter(report):
    return f"""
To,
The Municipal Commissioner,
Greater Visakhapatnam Municipal Corporation.

Subject: Complaint regarding {report.hazard_type}

Respected Sir/Madam,

I would like to report a civic infrastructure issue involving
{report.hazard_type}.

Description: {report.description}
Location: {report.address or "Location not provided"}
Severity: {report.severity}
Complaint ID: {report.complaint_id}

I request the concerned department to inspect this issue
and take appropriate action as soon as possible.

Thank you.
Citizen
"""

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5174", "http://localhost:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5173"]}})

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance"),
        exist_ok=True
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "success": True,
            "message": "Civic Hazard Reporting API is running!",
            "project": "Civic Infrastructure Hazard Reporting Pipeline",
            "version": "1.0",
            "database": "SQLite"
        })

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "success": True,
            "status": "healthy",
            "database": "connected"
        })

    # SUBMIT COMPLAINT
    @app.route("/api/reports", methods=["POST"])
    def create_report():

        if request.content_type and request.content_type.startswith(
            "multipart/form-data"
        ):
            data = request.form.to_dict()
        else:
            data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "error": "Invalid request data."
            }), 400

        hazard_type = data.get("hazard_type")
        description = data.get("description")

        if not isinstance(hazard_type, str) or not hazard_type.strip():
            return jsonify({
                "success": False,
                "error": "Hazard type is required."
            }), 400

        if not isinstance(description, str) or not description.strip():
            return jsonify({
                "success": False,
                "error": "Description is required."
            }), 400

        hazard_type = hazard_type.strip().lower()
        description = description.strip()

        if len(description) > 5000:
            return jsonify({
                "success": False,
                "error": "Description is too long."
            }), 400

        allowed_hazards = [
            "pothole",
            "garbage",
            "open manhole",
            "waterlogging",
            "broken streetlight"
        ]

        if hazard_type not in allowed_hazards:
            return jsonify({
                "success": False,
                "error": "Invalid hazard type.",
                "allowed_types": allowed_hazards
            }), 400

        # Validate location
        try:
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude not in (None, ""):
                latitude = float(latitude)
                if not -90 <= latitude <= 90:
                    raise ValueError()

            else:
                latitude = None

            if longitude not in (None, ""):
                longitude = float(longitude)
                if not -180 <= longitude <= 180:
                    raise ValueError()

            else:
                longitude = None

            if (latitude is None) != (longitude is None):
                return jsonify({
                    "success": False,
                    "error": "Latitude and longitude must be provided together."
                }), 400

        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "Invalid GPS coordinates."
            }), 400

        address = data.get("address") or None

        if address is not None:
            address = address.strip()

            if len(address) > 300:
                return jsonify({
                    "success": False,
                    "error": "Address cannot exceed 300 characters."
                }), 400

        # IMAGE UPLOAD
        image_file = request.files.get("image")
        image_filename = None
        saved_image_path = None

        if image_file and image_file.filename:

            valid, result = validate_image(image_file)

            if not valid:
                return jsonify({
                    "success": False,
                    "error": result
                }), 400

            image_filename = generate_image_filename(result)

            saved_image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                image_filename
            )

        try:

            if saved_image_path:
                image_file.save(saved_image_path)

            report = Report(
                complaint_id="TEMP-" + uuid.uuid4().hex,
                hazard_type=hazard_type,
                description=description,
                latitude=latitude,
                longitude=longitude,
                address=address,
                image_filename=image_filename,
                severity=classify_hazard(description, hazard_type),
                status="Pending"
            )

            db.session.add(report)
            db.session.flush()

            report.complaint_id = f"CE{report.id:03d}"
            report.complaint_letter = generate_complaint_letter(report)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Complaint submitted successfully!",
                "report": report.to_dict()
            }), 201

        except Exception:
            db.session.rollback()

            if saved_image_path and os.path.exists(saved_image_path):
                os.remove(saved_image_path)

            app.logger.exception("Complaint submission failed")

            return jsonify({
                "success": False,
                "error": "Unable to save complaint."
            }), 500

	    # GET ALL COMPLAINTS
    @app.route("/api/reports", methods=["GET"])
    def get_reports():

        reports = Report.query.order_by(
            Report.created_at.desc()
        ).all()

        return jsonify({
            "success": True,
            "total_reports": len(reports),
            "reports": [report.to_dict() for report in reports]
        }), 200
      # GET COMPLAINT BY ID
    @app.route("/api/reports/<complaint_id>", methods=["GET"])
    def get_report(complaint_id):

        report = Report.query.filter_by(
            complaint_id=complaint_id
        ).first()

        if not report:
            return jsonify({
                "success": False,
                "error": "Complaint not found."
            }), 404

        return jsonify({
            "success": True,
            "report": report.to_dict()
        }), 200
        # UPDATE COMPLAINT STATUS
    @app.route("/api/reports/<complaint_id>/status", methods=["PATCH"])
    def update_status(complaint_id):

        report = Report.query.filter_by(
            complaint_id=complaint_id
        ).first()

        if not report:
            return jsonify({
                "success": False,
                "error": "Complaint not found."
            }), 404

        data = request.get_json(silent=True) or {}
        new_status = data.get("status")

        allowed_statuses = [
            "Pending",
            "In Progress",
            "Resolved",
            "Rejected"
        ]

        if new_status not in allowed_statuses:
            return jsonify({
                "success": False,
                "error": "Invalid status.",
                "allowed_statuses": allowed_statuses
            }), 400

        report.status = new_status
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Complaint status updated.",
            "report": report.to_dict()
        }), 200
        # DASHBOARD STATISTICS
    @app.route("/api/stats", methods=["GET"])
    def get_stats():

        total = Report.query.count()

        pending = Report.query.filter_by(status="Pending").count()

        in_progress = Report.query.filter_by(status="In Progress").count()

        resolved = Report.query.filter_by(status="Resolved").count()

        rejected = Report.query.filter_by(status="Rejected").count()

        return jsonify({
            "success": True,
            "statistics": {
                "total_reports": total,
                "pending": pending,
                "in_progress": in_progress,
                "resolved": resolved,
                "rejected": rejected
            }
        }), 200

    @app.route("/uploads/<filename>", methods=["GET"])
    def get_uploaded_image(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
