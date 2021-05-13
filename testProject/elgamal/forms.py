from wtforms import Form, StringField, TextAreaField


class ElgamalForm(Form):
    keys = StringField('Ключи шифровки/расшифровки')
    message = StringField('Ваше сообщение для шифровки/расшифровки')