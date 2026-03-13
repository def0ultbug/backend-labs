import logging
from starlette.types import (
    ASGIApp, Scope, Receive, Send
)

import hashlib


logger = logging.getLogger("uvicorn")

class ASGIMiddleware:
    def __init__(self, app:ASGIApp, parameter: str = "default"):
        self.app = app
        self.parameter = parameter

    async def __call__(self,scope: Scope, receive: Receive, send: Send):
        logger.info("Entering ASGI middleware")
        logger.info(f"The parameter is: {self.parameter}")
        logger.info(f"event scope : {scope.get('type')}") # return the type of request "http", "websocket", "lifespan"
        await self.app(scope, receive, send) # Hands off to the next layer
        logger.info("Exiting ASGI middleware") # Runs AFTER your app responds


# another middleware that reads every incoming request body, computes a cryptographic hash of it, then stamps that hash onto the response header before the client ever sees it.
class RequestBodyHashMiddleware:
    def __init__(self, app: ASGIApp, algorithm: str = "sha256"):
        self.app = app
        self.algorithm = algorithm  # e.g. "sha256", "md5", "sha512"

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Only process HTTP requests, pass everything else through
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # ── Step 1: Intercept receive() to capture the request body ──
        body_parts = []

        async def receive_and_capture():
            message = await receive()
            if message["type"] == "http.request":
                body_parts.append(message.get("body", b""))
            return message  # still pass the original message downstream

        # ── Step 2: Wrap send() to inject the hash before responding ──
        async def send_with_hash(message):
            if message["type"] == "http.response.start":

                # Compute hash from the captured body chunks
                full_body = b"".join(body_parts)
                body_hash = hashlib.new(self.algorithm, full_body).hexdigest()

                logger.info(f"[{self.algorithm}] Request body hash: {body_hash}")

                # Inject hash as a custom response header
                headers = list(message.get("headers", []))
                headers.append((b"x-request-body-hash", body_hash.encode()))

                # Rebuild the message with the new headers
                message = {**message, "headers": headers}

            await send(message)  # forward the (possibly modified) message

        # Pass our wrapped callables instead of the originals
        await self.app(scope, receive_and_capture, send_with_hash)