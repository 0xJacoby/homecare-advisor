from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from .. import db, config
from ..models.categories import Categories
from ..category import Category
from ..models.patient import Patient

bp = Blueprint("categories", __name__)


@bp.route("/", methods=["POST"])
def add_category():
    data = request.get_json()
    name = data.get("name", "")
    parameters = data.get("parameters", [])
    if not name:
        return "Bad format for POST request", 400

    if name in config.categories:
        return jsonify({"error": "Category already exists in config"}), 409
    if Categories.get_by_name(name):
        return jsonify({"error": "Category already exists in central database"}), 409

    config.add_category(name, parameters)
    category = Categories(name)
    db.session.add(category)
    db.session.commit()
    return "Added", 201


@bp.route("/", methods=["GET"])
def get_categories():
    ssn = request.args.get("ssn")

    if ssn:
        if Patient.from_ssn(ssn):
            categories = list(Categories.all_from_ssn(ssn))

            return jsonify([c.to_dict() for c in categories])
        else:
            return "user not found", 404

    return config.all_categories()


@bp.route("/", methods=["DELETE"])
def del_categories():
    name = request.args.get("name", "")

    if not name:
        return "Bad format for POST request", 400

    config.remove_category(name)
    Categories.del_from_name(name)
    return "Removed", 200


@bp.route("/", methods=["PATCH"])
def upt_categories():
    data = request.get_json()
    name = data.get("name", "")
    if not name:
        return "Bad format for POST request", 400

    try:
        updated_params = data.get("parameters", [])

        config.set_parameters(name, updated_params)

        return data
    except (KeyError, TypeError):
        return "Bad format for POST request", 400
