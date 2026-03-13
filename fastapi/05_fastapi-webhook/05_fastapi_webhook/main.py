from fastapi import FastAPI,Request,Body
from starlette.middleware import Middleware
from asgi_middleware import ASGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from webhook import WebhookSenderMiddleWare,Event


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"WebHooks_URLS" : set()}



app = FastAPI(
    title="Middleware",
    lifespan = lifespan,
    middleware = [
        Middleware(ASGIMiddleware,parameter="example_parameter")
    ]
)

app.add_middleware(WebhookSenderMiddleWare)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Accepts requests from any domain
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"] # Allows any request header
)

"""
# another middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost"], # Only accepts requests where `Host: localhost`
)

NOTE : These two middlewares work against each other:
    CORS says "anyone from anywhere can call this API"
    TrustedHost says "but only if you're hitting localhost"

So `TrustedHostMiddleware` will block most cross-origin requests because real external callers won't have Host: localhost. 
This makes the wide-open CORS config largely meaningless.
"""

@app.get('/')
async def read_root():
    return {'Hello', 'World'}


@app.post('/register-webhook-url')
async def add_webhooks(request: Request, url: str = Body()):
    if not url.startswith('http'):
        url = f"http://{url}"
    request.state.WebHooks_URLS.add(url)
    return {"url added" : url}

@app.webhooks.post("/fastapi-webhook")
def fastapi_webhook(event: Event):
    """_summary_
    Args:
        event (Event): Received event from webhook
        It contains information about the
        host, path, timestamp and body of the request
    """


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()

