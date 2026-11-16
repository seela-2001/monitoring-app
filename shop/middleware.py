import logging
import time

logger = logging.getLogger("access")
SKIP = ("/metrics", "/api/health")


class RequestLogMiddleware:
    """Structured access log (JSON) -> بيتقري في Loki"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        if request.path not in SKIP:
            level = logging.ERROR if response.status_code >= 500 else logging.INFO
            logger.log(
                level,
                "request",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "status": response.status_code,
                    "duration_ms": round((time.perf_counter() - start) * 1000, 1),
                },
            )
        return response
