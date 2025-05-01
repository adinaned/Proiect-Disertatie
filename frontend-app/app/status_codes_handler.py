from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, RedirectResponse
from fastapi import HTTPException


class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if response.status_code == 200:
            response.body = b'{"message": "Operation was successful!"}'
            response.headers['X-Custom-Header'] = 'Custom Header for 200 OK'

        elif 300 <= response.status_code < 400:
            response.headers['X-Redirect-Info'] = 'This is a redirect response'

        elif 400 <= response.status_code < 500:
            if response.status_code == 400:
                response.body = b'{"message": "Bad request - Invalid input!"}'
            elif response.status_code == 404:
                response.body = b'{"message": "Resource not found!"}'
            elif response.status_code == 401:
                response.body = b'{"message": "Unauthorized!"}'

        elif 500 <= response.status_code < 600:
            response.body = b'{"message": "Internal server error!"}'

        return response


app.add_middleware(ResponseMiddleware)


@app.get("/success")
def success():
    return JSONResponse(status_code=200, content={"message": "Operation was successful!"})


@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/new-location", status_code=302)


@app.get("/error")
def error():
    raise HTTPException(status_code=400, detail="This is a bad request")


@app.get("/server-error")
def server_error():
    raise HTTPException(status_code=500, detail="Internal server error")
