from app import db

from datetime import datetime
from random import randint, choice
from string import ascii_lowercase, digits

from slugify import slugify


article_tabs = db.Table(
    'article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True)
    title = db.Column(db.String(140), nullable=False)
    synopsis = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'<Article id: {self.id}, title: {self.title}>'

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(140), unique=True)
    articles = db.relationship(
        'Article',
        secondary=article_tabs,
        backref='tags')

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'<Tag id: {self.id}, name: {self.name}'

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(140), unique=True)
    posts = db.relationship(
        'Article',
        backref='category',
        cascade='all,delete-orphan')

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return f'<Category id: {self.id}, name: {self.name}'

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)


class EncryptedResult(db.Model):
    __tablename__ = 'encryptedResult'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True)
    public_keys = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(140), nullable=False)
    data = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(EncryptedResult, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        while True:
            slug = ''.join([
                choice(ascii_lowercase+digits)
                for _ in range(randint(25, 99))])
            in_db = EncryptedResult.query.filter_by(slug=slug).first() is not None
            if not in_db:
                self.slug = slug
                break


class DecryptedResult(db.Model):
    __tablename__ = 'decryptedResult'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True)
    private_keys = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(140), nullable=False)
    data = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(DecryptedResult, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        while True:
            slug = ''.join([
                choice(ascii_lowercase+digits)
                for _ in range(randint(25, 99))])
            in_db = DecryptedResult.query.filter_by(slug=slug).first() is not None
            if not in_db:
                self.slug = slug
                break