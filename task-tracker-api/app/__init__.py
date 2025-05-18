from flask import Flask
from .extensions import db, migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS # type: ignore

def create_app():
    load_dotenv()  
    
    app = Flask(__name__)
    CORS(app) 

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Task

    from .routes import task_bp
    app.register_blueprint(task_bp, url_prefix="/api/tasks")

    return app
