""" файл запуска проекта. На него нужно прописывать python main.py """


from app import app
from app import db
from news.blueprint import news
from elgamal.blueprint import elgamal
from view import *


app.register_blueprint(news, url_prefix="/news")
app.register_blueprint(elgamal, url_prefix="/elgamal")


if __name__ == "__main__":
    app.run()
