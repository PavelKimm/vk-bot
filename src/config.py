import os

DATABASE = {
        'NAME': 'vk_bot_db',
        'USER': 'postgres',
        'PASSWORD': 'postgresql123',
        'HOST': 'localhost'
}


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['NAME']}"


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

rasa_url = "https://bdbc5610.ngrok.io"
