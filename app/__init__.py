# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
# from app.config.config import Config

# load_dotenv()

# def create_app():
    
# # declare the Flask App:
#     app = Flask(__name__,
#                 static_folder='static',
#                 template_folder='templates'
#             )
# # configure the config file
#     app.config.from_object(Config)

#     CORS(app, origins=[
#         "https://prashantbuilds.in",
#         "https://www.prashantbuilds.in",
#         "https://inspector.prashantbuilds.in"
#     ])
    
#     from app.routes.extensions import mail
#     mail.init_app(app)

# # register blueprints:

#     # add auth_home route
#     from app.routes.auth_home import home_route
#     app.register_blueprint(home_route)
    
#     # add auth_inspect route
#     from app.routes.auth_inspect import inspect_route
#     app.register_blueprint(inspect_route)
    
#     from app.routes.login_signup.auth_login import login_route
#     app.register_blueprint(login_route)
    
    
#     return app


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.config.config import Config
from app.config.config import STATIC_FILES_DIR

load_dotenv()

def create_app():
    # create fastapi application (fastapi app object)
    app = FastAPI()
    
    # configure static files
    app.mount('/static',
              StaticFiles(directory=STATIC_FILES_DIR),
              name='static' )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'https://prashantbuilds.in',
            'https://ww.prashntbuilds.in',
            'https://inspector.prashantbuilds.in',
            'www.inspector.prashantbuilds.in'
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    
    # Register mail
    from app.mail.mail import mail_config
    
    # Register routes
    from app.routes.auth_home import home_route
    from app.routes.auth_inspect import inspect_route
    # from app.routes.login_signup.auth_login import login_route
    
    app.include_router(home_route)
    app.include_router(inspect_route)
    # app.include_route(login_route)
    
    return app