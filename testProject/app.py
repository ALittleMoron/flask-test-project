from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from models import Article, Tag, Category


admin= Admin(app)
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Category, db.session))