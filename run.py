import sys
import os

# Add the parent directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=9909)