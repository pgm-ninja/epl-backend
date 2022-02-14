from core.settings.__init__ import *
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         "NAME": env("SQL_DATABASE"),
#         "USER": env("SQL_USER"),
#         "PASSWORD": env("SQL_PASSWORD"),
#         "HOST": env("SQL_HOST"),
#         "PORT": env("SQL_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
