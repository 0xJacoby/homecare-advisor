from flask import Blueprint, request, jsonify
from .. import db
from ..models.patient import Patient

bp = Blueprint("patients", __name__)


@bp.route("/", methods=["PUT"])
def add_patient():
    ssn = request.form.get("ssn")
    firstname = request.form.get("firstname")
    surname = request.form.get("surname")

    patient = Patient.from_ssn(ssn)

    if patient is None:
        patient = Patient(ssn, firstname, surname)
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
