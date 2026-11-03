from fastapi import Request, Response, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates

from .fuc_inspect import fig_to_base64
from ml.rfm.main import main
import io
import base64
import os


inspect_route = APIRouter()
inspect_template = Jinja2Templates(directory='templates')

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    
@inspect_route.get('/inspect')
def inspect(request: Request):
    if not session['username'] and session['email']:
        return inspect_template.TEmplateResponse(
            'homepage.html',
            {request: Response}
        )
    return TemplateResponse(
        'inspect.html',
        {request:Response}
    )

@inspect_route.post('/inspect/upload_dataset')
def upload_dataset(request: Response):
    if request.method == 'POST':
        # check for the file present in request
        if 'dataset' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        file = request.files['dataset']
        
        # if no file selected
        if file.filename == '':
            raise HTTPException(status_code=400, detials='No selected file')
        
        # secure the file with werkzeug to prevent directory traversal vulnerabilities
        filename = secure_filename(file.filename)
        
        # create a full path on the server
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        # save file to the disk
        file.save(file_path)
        
        # store file path in session for the analysis route
        session['uploaded_file_path'] = file_path
        
        return {'status': 'success', 'message': 'File uploaded successfully'}

@inspect_route.post('/inspect/analyse_dataset')
def analyse_dataset():
    file_path = session.get('uploaded_file_path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail='No uploaded file found. Please upload a file first.')
        
    try:
        rfm_segment_df, rfm_summary_df, pie_plot, bar_plot = main(file_path)

        pie_base64 = fig_to_base64(pie_plot)
        bar_base64 = fig_to_base64(bar_plot)
        
        # Convert DataFrames to HTML tables
        summary_table_html = rfm_summary_df.to_html(classes='table table-striped table-hover', index=False)
        segment_table_html = rfm_segment_df.to_html(classes='table table-striped table-hover', index=True)
        
        return {
            'status': 'success',
            'message': 'Analysis complete',
            'segment_table': segment_table_html,
            'summary_table': summary_table_html,
            'pie_chart': pie_base64,
            'bar_chart': bar_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Analysis failed: {str(e)}')


