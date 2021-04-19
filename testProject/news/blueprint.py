from flask import Blueprint, render_template

from models import Article

news = Blueprint('news', __name__, template_folder='templates',
                 static_folder='static')


@news.route('/')
def news_page():
    news = Article.query.all()
    return render_template('news/news.html', news=news)


@news.route('/<slug>')
def detail_article(slug):
    article = Article.query.filter(Article.slug==slug)
    return render_template('news/detail_article.html', article=article)


@news.route('/add-article')
def add_article():
    return render_template('news/add_article.html')
