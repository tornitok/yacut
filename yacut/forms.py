from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 128)],
    )
    custom_id = TextAreaField(
        'Ваш вариант короткой ссылки',
    )
    submit = SubmitField('Создать')
