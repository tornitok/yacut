from datetime import datetime, timezone

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now(timezone.utc)
    )