from flask import Blueprint, request, jsonify
from .. import db, DB
from ..models.patient import Patient
from datetime import datetime

bp = Blueprint("patients", __name__)


@bp.route("/", methods=["PUT"])
def add_patient():
    ssn = request.form.get("ssn")
    firstname = request.form.get("firstname")
    surname = request.form.get("surname")
    date_of_birth = request.form.get("date_of_birth")
    municipality = request.form.get("municipality")
    has_homecare = request.form.get("has_homecare")

    patient = Patient.from_ssn(ssn)

    if patient is None:
        # TODO: Add more validation
        homecare = has_homecare.lower() == "true"
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        patient = Patient(ssn, firstname, surname, dob, municipality)
        db.session.add(patient)
        db.session.commit()

    return jsonify(patient.to_dict()), 201


@bp.route("/", methods=["GET"])
def get_patient():
    ssn = request.args.get("ssn")

    if ssn:
        patient = Patient.from_ssn(ssn)

        if patient:
            return jsonify(patient.to_dict()), 302
        else:
            return "user not found", 404

    return jsonify([patient.to_dict() for patient in Patient.query.all()]), 302
