from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.tests import Tests

bp = Blueprint("tests", __name__)


@bp.route("/", methods=["PUT"])
def add_test():
    name = request.form.get("name")
    test = Tests(name)

    try:
        db.session.add(test)
        db.session.commit()

        return jsonify(test.to_dict()), 201
    except IntegrityError:
        return jsonify({"error": "Test already exists"}), 409

@bp.route("/", methods=["GET"])
def get_tests():
    tests = Tests.get_all()
    return jsonify([t.to_dict() for t in tests]), 200
