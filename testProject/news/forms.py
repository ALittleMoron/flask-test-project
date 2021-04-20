from wtforms import Form, StringField, TextAreaField


class ArticleForm(Form):
    title = StringField('Название')
    synopsis = StringField('Краткое содержание')
    text = TextAreaField('Текст новости')