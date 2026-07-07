from .extensions import *
from .fuc_inspect import fig_to_base64
from ml.rfm.main import main
import io
import base64

inspect_auth = Blueprint('inspect_auth', __name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    
@inspect_auth.route('/inspect', methods=['POST', 'GET'])
def inspect():
    return render_template('auth/inspect.html')

@inspect_auth.route('/inspect/upload_dataset', methods=['POST'])
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

@inspect_auth.route('/inspect/analyse_dataset', methods=['POST'])
def analyse_dataset():
    file_path = session.get('uploaded_file_path')
    if not file_path or not os.path.exists(file_path):
        return jsonify({'status': 'error', 'message': 'No uploaded file found. Please upload a file first.'}), 400
        
    try:
        rfm_segment_df, rfm_summary_df, pie_plot, bar_plot = main(file_path)

        pie_base64 = fig_to_base64(pie_plot)
        bar_base64 = fig_to_base64(bar_plot)
        
        # Convert DataFrames to HTML tables
        summary_table_html = rfm_summary_df.to_html(classes='table table-striped table-hover', index=False)
        segment_table_html = rfm_segment_df.to_html(classes='table table-striped table-hover', index=True)
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis complete',
            'segment_table': segment_table_html,
            'summary_table': summary_table_html,
            'pie_chart': pie_base64,
            'bar_chart': bar_base64
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Analysis failed: {str(e)}'}), 500


