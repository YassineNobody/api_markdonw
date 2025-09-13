from flask import jsonify
from pydantic import ValidationError as PydanticValidationError


class AppError(Exception):
    """Exception de base pour l'application"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(AppError):
    """Ressource non trouvée"""

    pass


class ConflictError(AppError):
    """Conflit (ex: doublon dans la DB)"""

    pass


class AppValidationError(AppError):
    """Erreur de validation des données"""

    pass


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return jsonify({"error": error.message}), 404

    @app.errorhandler(ConflictError)
    def handle_conflict(error):
        return jsonify({"error": error.message}), 409

    @app.errorhandler(AppValidationError)
    def handle_validation(error):
        return jsonify({"error": error.message}), 422

    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_validation(error):
        return jsonify({"error": "Invalid input", "details": error.errors()}), 422

    @app.errorhandler(404)
    def handle_route_not_found(error):
        return (
            jsonify(
                {"error": "Not Found", "message": "La route demandée n'existe pas."}
            ),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": "La méthode HTTP utilisée n'est pas autorisée pour cette ressource.",
                }
            ),
            405,
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({"error": str(error)}), 500
