import uvicorn
from app.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('run:app', host='localhost', port=9999, reload=True)