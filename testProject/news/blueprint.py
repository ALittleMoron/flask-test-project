from flask import Blueprint, render_template, request

from models import Article, Tag, Category

news = Blueprint('news', __name__, template_folder='templates',
                 static_folder='static')


@news.route('/')
def news_page():
    q = request.args.get('q')
    print(q)
    if q:
        news = Article.query.filter(Article.title.contains(q) | Article.text.contains(q)).all()
    else:
        news = Article.query.all()
    return render_template('news/news.html', news=news)


@news.route('/<slug>')
def detail_article(slug):
    article = Article.query.filter(Article.slug==slug).first()
    tags = article.tags
    return render_template('news/detail_article.html', article=article, tags=tags)


@news.route('/tag/<slug>')
def news_by_tag(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    news = tag.articles
    return render_template('news/news_by_tag.html', tag=tag, news=news)


@news.route('/add-article')
def add_article():
    return render_template('news/add_article.html')
