from flask import Blueprint, render_template


news = Blueprint('news', __name__, template_folder='templates',
                 static_folder='static')


@news.route('/')
def news_page():
    return render_template('news/news.html')


@news.route('/add-article')
def add_article():
    return render_template('news/add_article.html')
