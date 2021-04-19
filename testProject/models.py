from app import db

from datetime import datetime

from slugify import slugify


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True)
    title = db.Column(db.String(140), nullable=False)
    synopsis = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'<Article id: {self.id}, title: {self.title}>'
