from io import BytesIO
from time import time

from fastapi import Request
from fastapi.responses import StreamingResponse
from src.logger import logger


async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = (time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{round(process_time)} ms"
    return response


async def logger_middleware(request: Request, call_next):
    start_time = time()
    log_dict: dict = {
        "url": request.url.path,
        "method": request.method,
    }
    response: StreamingResponse = await call_next(request)
    duration_ms: int = int((time() - start_time) * 1000)
    log_dict["duration_ms"] = duration_ms
    log_dict["status_code"] = response.status_code
    if response.status_code >= 400:
        body = b"".join([segment async for segment in response.body_iterator])
        error_message = body.decode("utf-8")
        log_dict["error_message"] = error_message
        response = StreamingResponse(BytesIO(body), media_type="application/json")
    logger.info(log_dict)
    return response
