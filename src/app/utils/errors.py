from starlette.requests import Request
from starlette.responses import JSONResponse


def app_error_handler(_: Request | None, exc: Exception):
    if isinstance(exc, TypeError) and str(exc) == 'No constructor defined':
        return JSONResponse('Your password should be secure(big and small letters, special characters, numbers)')
    return JSONResponse(str(exc))
