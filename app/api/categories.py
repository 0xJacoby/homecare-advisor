from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from .. import db, config
from ..models.categories import Categories
from ..category import Category

bp = Blueprint("categories", __name__)


@bp.route("/", methods=["POST"])
def add_category():
    data = request.get_json()
    name = data.get("name", "")
    if not name:
        return "Bad format for POST request", 400

    category = Categories(name)

    try:
        db.session.add(category)
        db.session.commit()
        config.add_category(name)
    except IntegrityError:
        return jsonify({"error": "Category name already exists"}), 409

    try:
        for param in data.get("parameters", []):
            config.add_parameter(name, param["name"], param["weight"])

            return jsonify(data)
    except (KeyError, TypeError):
        return "Bad format for POST request", 400


@bp.route("/", methods=["GET"])
def get_categories():
    categories = Categories.get_all()
    return jsonify([Category.from_name(c.name).to_dict() for c in categories])


@bp.route("/", methods=["DELETE"])
def del_categories():
    name = request.args.name
