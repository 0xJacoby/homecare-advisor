from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.categories import Categories

bp = Blueprint("categories", __name__)


@bp.route("/", methods=["PUT"])
def add_category():
    name = request.form.get("name")

    category = Categories(name)

    try:
        db.session.add(category)
        db.session.commit()

        return jsonify(category.to_dict()), 201
    except IntegrityError:
        return jsonify({"error": "Category name already exists"}), 409

@bp.route("/", methods=["GET"])
def get_categories():
    categories = Categories.get_all()
    return jsonify([c.to_dict() for c in categories]), 200
