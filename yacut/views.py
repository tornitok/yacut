from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data or get_unique_short_id()
        if len(custom_id) > 16:
            flash('Ваша ссылка привышает допустимое колличество символов.')
        elif URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
        else:
            url_map = URLMap(original=original_link, short=custom_id)
            db.session.add(url_map)
            db.session.commit()
            return render_template(
                'index.html',
                form=form,
                short_url=custom_id
            )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)