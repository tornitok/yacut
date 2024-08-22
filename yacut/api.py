from flask import jsonify, request

from . import app, db
from .errors import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


def is_valid_custom_id(custom_id):
    return custom_id.isalnum() and 3 <= len(custom_id) <= 16


@app.route('/api/id/', methods=['POST'])
def create_id():
    if not request.is_json:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)

    data = request.get_json()
    original_link = data.get('url')
    custom_id = data.get('custom_id')

    if not original_link:
        raise InvalidAPIUsage('url является обязательным полем!', 400)

    if custom_id and not is_valid_custom_id(custom_id):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки', 400
        )

    if custom_id and URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.', 400
        )

    custom_id = custom_id or get_unique_short_id()
    url_map = URLMap(original=original_link, short=custom_id)
    db.session.add(url_map)
    db.session.commit()
    short_link = f'http://localhost/{custom_id}'
    return jsonify({"short_link": short_link, "url": original_link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({"message": "ID not found"}), 404
    return jsonify({"url": url_map.original}), 200
