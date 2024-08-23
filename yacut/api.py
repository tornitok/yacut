from flask import jsonify, request, url_for

from . import app, db
from .errors import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from .validator import is_valid_custom_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    original_link = data.get('url')
    custom_id = data.get('custom_id')

    if not original_link:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.', 400
            )
        if not is_valid_custom_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400
            )
    custom_id = custom_id or get_unique_short_id()
    url_map = URLMap(original=original_link, short=custom_id)
    db.session.add(url_map)
    db.session.commit()
    short_link = url_for(
        'redirect_to_original',
        short_id=custom_id,
        _external=True
    )
    return jsonify({'short_link': short_link, 'url': original_link}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({"url": url_map.original}), 200