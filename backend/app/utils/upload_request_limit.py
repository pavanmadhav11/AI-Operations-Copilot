import json


class UploadRequestLimitMiddleware:
    def __init__(self, app, max_bytes: int, upload_paths: set[str]):
        self.app = app
        self.max_bytes = max_bytes
        self.upload_paths = upload_paths

    async def send_too_large(self, send):
        body = json.dumps({"detail": "Uploads must be 10 MB or smaller."}).encode()
        await send({
            "type": "http.response.start",
            "status": 413,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
            ],
        })
        await send({"type": "http.response.body", "body": body})

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("method") != "POST" or scope.get("path") not in self.upload_paths:
            await self.app(scope, receive, send)
            return

        content_length = next(
            (value for name, value in scope.get("headers", []) if name.lower() == b"content-length"),
            None,
        )
        if content_length is not None:
            try:
                if int(content_length) > self.max_bytes:
                    await self.send_too_large(send)
                    return
            except ValueError:
                body = b'{"detail":"Invalid Content-Length header."}'
                await send({
                    "type": "http.response.start",
                    "status": 400,
                    "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
                })
                await send({"type": "http.response.body", "body": body})
                return

        received_bytes = 0
        request_too_large = False

        async def limited_receive():
            nonlocal received_bytes, request_too_large
            message = await receive()
            if message["type"] == "http.request":
                received_bytes += len(message.get("body", b""))
                if received_bytes > self.max_bytes:
                    request_too_large = True
                    await self.send_too_large(send)
                    return {"type": "http.disconnect"}
            return message

        async def limited_send(message):
            if not request_too_large:
                await send(message)

        await self.app(scope, limited_receive, limited_send)
