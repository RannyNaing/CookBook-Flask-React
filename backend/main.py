from flask import Flask, jsonify
from flask_restx import Api
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipes import recipe_ns
from auth import auth_ns
from flask_cors import CORS

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    
    CORS(app)

    db.init_app(app)

    migrate = Migrate(app, db)
    JWTManager(app)
    api = Api(app, doc="/docs")
    
    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)
    
    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "Recipe": Recipe, "user": User}
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    # Optionally handle other HTTP errors
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({"error": "Unauthorized", "message": str(error)}), 401
    
    return app

