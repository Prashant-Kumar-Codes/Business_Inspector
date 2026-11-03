import os
from fastapi import Request, APIRouter, HTTPException, status
from fastapi.templating import Jinja2Templates
from werkzeug.utils import secure_filename
from app.routes.helper.request_type_and_respond import _respond
from .fuc_inspect import fig_to_base64
from ml.rfm.main import main
from app.logger.logger import logger

'''
return _respond(request, {
    'success': False,
    'message': 'Session expired or email missing. Please sign up again.',
}, status.HTTP_400_BAD_REQUEST, flash_category='error')

'''


inspect_route = APIRouter()
inspect_template = Jinja2Templates(directory='app/templates')

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    
@inspect_route.get('/inspect')
def inspect(request: Request):
    if not request.session.get('username') and not request.session.get('user_email'):
        return inspect_template.TemplateResponse(
            request=request,
            name='homepage.html',
        )
    return inspect_template.TemplateResponse(
        request=request,
        name='inspect.html',
    )

@inspect_route.post('/inspect/upload_dataset')
async def upload_dataset(request: Request):
    form = await request.form()
    uploaded_file = form.get('dataset')
    if uploaded_file is None or not hasattr(uploaded_file, 'filename'):
        return _respond(request, {
            'success': False,
            'message': 'No file part'
        }, status.HTTP_400_BAD_REQUEST, flash_category='error')

    if not uploaded_file.filename:
        raise HTTPException(status_code=400, detail='No selected file')
    
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(file_path, 'wb') as destination:
        destination.write(await uploaded_file.read())

    request.session['uploaded_file_path'] = file_path
    
    logger.success(f'File uploaded successfully: {file_path}')
    return {'status': 'success', 'message': 'File uploaded successfully'}

@inspect_route.post('/inspect/analyse_dataset')
def analyse_dataset(request: Request):
    file_path = request.session.get('uploaded_file_path')
    if not file_path or not os.path.exists(file_path):
        logger.error('No uploaded file found in session or file does not exist.')
        raise HTTPException(status_code=400, detail='No uploaded file found. Please upload a file first.')
        
    try:
        rfm_segment_df, rfm_summary_df, pie_plot, bar_plot = main(file_path)

        pie_base64 = fig_to_base64(pie_plot)
        bar_base64 = fig_to_base64(bar_plot)
        
        # Convert DataFrames to HTML tables
        summary_table_html = rfm_summary_df.to_html(classes='table table-striped table-hover', index=False)
        segment_table_html = rfm_segment_df.to_html(classes='table table-striped table-hover', index=True)
        
        logger.success('Successfully generate the output files and charts')
        
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


