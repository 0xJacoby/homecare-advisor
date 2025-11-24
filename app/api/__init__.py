from .patients import bp as patients
from .journals import bp as journals
from .categories import bp as categories

__all__ = ["patients", "journals", "categories"]


def register_routes(app):
    # API routes
    app.register_blueprint(patients, url_prefix="/api/patients")
    app.register_blueprint(journals, url_prefix="/api/journals")
    app.register_blueprint(categories, url_prefix="/api/categories")
