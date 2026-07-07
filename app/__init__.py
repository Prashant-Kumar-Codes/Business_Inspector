from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.config.config import Config

load_dotenv()

def create_app():
    
# declare the Flask App:
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates'
            )
# configure the config file
    app.config.from_object(Config)

    CORS(app, origins=[
        "https://prashantbuilds.in",
        "https://www.prashantbuilds.in",
        "https://inspector.prashantbuilds.in"
    ])
    
# register blueprints:

    # add auth_home route
    from app.routes.auth_home import home_auth
    app.register_blueprint(home_auth)
    
    # add auth_inspect route
    from app.routes.auth_inspect import inspect_auth
    app.register_blueprint(inspect_auth)
    
    
    return app