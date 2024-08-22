from flask import jsonify, render_template, request

from . import app


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500


# Обработчики ошибок для API
@app.errorhandler(404)
def api_not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error="Resource not found"), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def api_internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error="Internal server error"), 500
    return render_template('index.html'), 500