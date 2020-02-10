import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/vk_bot_db'  # os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


basedir = os.path.abspath(os.path.dirname(__file__))


token = "acd63c90c7f3963ba4748938ed576b200aff75eda798fba5f46894d4ebfd39939735d584e427949214c09"
confirmation_token = "196e0e88"
access_token = "5aa2df955aa2df955aa2df95955acca5d455aa25aa2df95074ce843d0498ebf417b7aaa"

rasa_url = "https://00e083cf.ngrok.io"

JIRA = {
    "host": "jira.sib-soft.ru/jira",
    "master": ("kimpa", "3010352Qr")
}