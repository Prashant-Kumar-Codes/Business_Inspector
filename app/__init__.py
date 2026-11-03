import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from app.config.config import Config
from app.config.config import STATIC_FILES_DIR, settings

load_dotenv()

def create_app():
    # create fastapi application (fastapi app object)
    app = FastAPI()
    
    # configure static files
    app.mount('/static',
              StaticFiles(directory=STATIC_FILES_DIR),
              name='static' )

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        same_site='lax',
        https_only=os.getenv('FASTAPI_ENV') == 'production',
    )
    
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
    from app.routes.login_signup.auth_login import login_route
    
    app.include_router(home_route)
    app.include_router(inspect_route)
    app.include_router(login_route)
    
    return app