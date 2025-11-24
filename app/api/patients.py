from flask import Blueprint, request, jsonify
from .. import db
from ..models.patient import Patient

bp = Blueprint("patients", __name__)


@bp.route("/", methods=["POST"])
def add_patient():
    ssn = request.form.get("ssn")
    firstname = request.form.get("firstname")
    surname = request.form.get("surname")
    municipality = request.form.get("municipality")
    has_homecare = request.form.get("has_homecare")

    patient = Patient.from_ssn(ssn)

    if patient is None:
        # TODO: Add more validation
        if (
            has_homecare.lower() not in ["true", "false"]
            or len(ssn) != 13
            or ssn[8] != "-"
        ):
            return "Invalid values in form fields", 400

        homecare = has_homecare.lower() == "true"
        patient = Patient(ssn, firstname, surname, municipality, homecare)
        db.session.add(patient)
        db.session.commit()

    return jsonify(patient.to_dict()), 201


@bp.route("/", methods=["GET"])
def get_patient():
    ssn = request.args.get("ssn")

    if ssn:
        patient = Patient.from_ssn(ssn)

        if patient:
            return jsonify(patient.to_dict())
        else:
            return "user not found", 404

    return jsonify([patient.to_dict() for patient in Patient.query.all()])
