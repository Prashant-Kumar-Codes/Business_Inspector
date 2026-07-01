from .extensions import *

inspect_auth = Blueprint('inspect_auth', __name__)

@inspect_auth.route('/inspect', methods=['POST', 'GET'])
def inspect():
    return render_template('auth/inspect.html')