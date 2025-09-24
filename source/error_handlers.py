from flask import jsonify

def register_error_handlers(app):
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
            "message": str(error),
            "type": type(error).__name__
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Invalid url",
            "message": str(error),
            "type": type(error).__name__
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad request",
            "message": str(error),
            "type": type(error).__name__
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "Unauthorized",
            "message": str(error),
            "type": type(error).__name__
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "error": "Forbidden",
            "message": str(error),
            "type": type(error).__name__
        }), 403

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed",
            "message": str(error),
            "type": type(error).__name__
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "error": "Unprocessable entity",
            "message": str(error),
            "type": type(error).__name__
        }), 422
    