from flask import Blueprint, render_template, request, redirect, url_for

from models import Article, Tag, Category
from app import db
from .forms import ArticleForm


news = Blueprint('news', __name__, template_folder='templates',
                 static_folder='static')


@news.route('/add-article', methods=['POST', 'GET'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        synopsis = request.form['synopsis']
        text = request.form['text']
        
        try:
            article = Article(title=title, synopsis=synopsis, text=text)
            
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            print('Something went wrong...')
            print(e)
        return redirect(url_for('news.news_page'))
    else:
        form = ArticleForm()
    return render_template('news/add_article.html', article=article, form=form)


@news.route('/update-article/<slug>', methods=["POST", "GET"])
def update_article(slug):
    article = Article.query.filter(Article.slug==slug).first()

    if request.method == 'POST':
        form = ArticleForm(formdata=request.form, obj=article)
        form.populate_obj(article)
        db.session.commit()
        return redirect(url_for('news.detail_article', slug=article.slug))
    else:
        form = ArticleForm(obj=article)
        return render_template('news/edit.html', article=article, form=form)


@news.route('/')
def news_page():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        news = Article.query.filter(Article.title.contains(q) | Article.text.contains(q))
    else:
        news = Article.query.order_by(Article.created_at.desc())
    pages = news.paginate(page=page, per_page=5)
    
    return render_template('news/news.html', news=news, pages=pages)


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
