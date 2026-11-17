# app/errors.py
"""Central error handlers returning a uniform JSON body:
{"error": {"code": str, "message": str, "details": list}}
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException

from app import app


class ApiError(Exception):
    def __init__(self, status, code, message, details=None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details or []


def error_response(status, code, message, details=None):
    body = {"error": {"code": code, "message": message, "details": details or []}}
    return jsonify(body), status


@app.errorhandler(ApiError)
def handle_api_error(exc):
    return error_response(exc.status, exc.code, exc.message, exc.details)


_HTTP_CODES = {
    404: "not_found",
    405: "method_not_allowed",
    415: "unsupported_media_type",
}


@app.errorhandler(HTTPException)
def handle_http_exception(exc):
    status = exc.code or 500
    code = _HTTP_CODES.get(status, "bad_request" if status == 400 else "http_error")
    return error_response(status, code, exc.description or exc.name)


@app.errorhandler(Exception)
def handle_unexpected(exc):
    app.logger.exception("Unhandled error")
    return error_response(500, "internal_error", "Internal server error")
