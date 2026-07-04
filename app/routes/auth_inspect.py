from .extensions import *
from Business_Inspector.ml.rfm.main import main

inspect_auth = Blueprint('inspect_auth', __name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    
@inspect_auth.route('/inspect', methods=['POST', 'GET'])
def inspect():
    return render_template('auth/inspect.html')

@inspect_auth.route('/inspect/upload_dataset', methods=['POST', 'GET'])
def upload_dataset():
    if request.method == 'POST':
        # check for the file present in request
        if 'dataset' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        file = request.files['dataset']
        
        # if no file selected
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        # secure the file with werkzeug to prevent directory traversal vulnerabilities
        filename = secure_filename(file.filename)
        
        # create a full path on the server
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        # save file to the disk
        file.save(file_path)
        
        # store file path in session for the analysis route
        session['uploaded_file_path'] = file_path
        
        return jsonify({'status': 'success', 'message': 'File uploaded successfully'})

@inspect_auth.route('/inspect/analyse_dataset', methods=['POST', 'GET'])
def analyse_dataset():
    file_path = session.get('uploaded_file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({'status': 'error', 'message': 'No uploaded file found. Please upload a file first.'}), 400
        
    try:
        main(file_path)
        return jsonify({'status': 'success', 'message': 'Analysis complete'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Analysis failed: {str(e)}'}), 500

