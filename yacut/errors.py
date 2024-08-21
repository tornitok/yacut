from flask import render_template, jsonify, request
from . import app


@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500


# Обработчики ошибок для API
@app.errorhandler(404)
def api_not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error="Resource not found"), 404
    return render_template('index.htmll'), 404


@app.errorhandler(500)
def api_internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error="Internal server error"), 500
    return render_template('index.html'), 500