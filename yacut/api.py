from flask import Flask, jsonify, request, render_template
from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.json

    if not data:
        return jsonify({"message": "Отсутствует тело запроса"}), 400

    original_link = data.get('url')
    custom_id = data.get('custom_id')

    if not original_link:
        return jsonify({"message": '"url" является обязательным полем!'}), 400

    if custom_id and URLMap.query.filter_by(short=custom_id).first():
        return jsonify({"message": "Предложенный вариант короткой ссылки уже существует."}), 400

    if not custom_id:
        custom_id = get_unique_short_id()

    url_map = URLMap(original=original_link, short=custom_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({"short_id": custom_id, "url": original_link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if not url_map:
        return jsonify({"message": "Указанный id не найден"}), 404

    return jsonify({"url": url_map.original}), 200



@app.errorhandler(404)
def api_not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({"message": "Resource not found"}), 404
    form = URLMapForm()  # Ensure form is passed to the template
    return render_template('index.html', form=form), 404

@app.errorhandler(500)
def api_internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({"message": "Internal server error"}), 500
    form = URLMapForm()  # Ensure form is passed to the template
    return render_template('index.html', form=form), 500