from fastapi import Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import status

def _is_json_request(request: Request) -> bool:
    return request.headers.get('content-type', '').lower().startswith('application/json')

async def _request_data(request: Request):
    if _is_json_request(request):
        try:
            data = await request.json()
        except ValueError:
            return {}
        return data if isinstance(data, dict) else {}
    return await request.form()


def _respond(
    request: Request,
    payload: dict,
    status_code: int = status.HTTP_200_OK,
    redirect_url: str = '/login',
    flash_category: str | None = None,
):
    if _is_json_request(request):
        return JSONResponse(payload, status_code=status_code)

    if flash_category:
        request.session.setdefault('flash_messages', []).append({
            'category': flash_category,
            'message': payload['message'],
        })
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)