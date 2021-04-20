""" Конфигурационный файл для flask приложения. """


class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = 'a;lkgsa;lksa;lg jsa;j sa;gs;l;sagks;k;'