from flask import Blueprint, request, jsonify
from .. import db
from ..models.journal_entry import JournalEntry

bp = Blueprint("journals", __name__)


@bp.route("/", methods=["PUT"])
def add_entry():
    pass
    # TODO


@bp.route("/", methods=["GET"])
def get_entries():
    pass
    # TODO
