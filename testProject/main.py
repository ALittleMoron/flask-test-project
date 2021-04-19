""" файл запуска проекта. На него нужно прописывать python main.py """


from app import app
from app import db
from news.blueprint import news
from view import *

app.register_blueprint(news, url_prefix="/news")


if __name__ == "__main__":
    app.run()
