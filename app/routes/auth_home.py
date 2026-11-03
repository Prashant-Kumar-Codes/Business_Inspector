from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

home_route = APIRouter()
home_template = Jinja2Templates(directory='app/templates')
    
@home_route.get('/')
def homepage(request: Request):
    return home_template.TemplateResponse(
        request=request,
        name='homepage.html'
    )