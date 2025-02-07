import os

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('CONTENT_PG_ENGINE'),
        'NAME': os.environ.get('CONTENT_POSTGRES_DB_NAME'),
        'USER': os.environ.get('CONTENT_POSTGRES_USER'),
        'PASSWORD': os.environ.get('CONTENT_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('CONTENT_POSTGRES_HOST'),
        'PORT': os.environ.get('CONTENT_POSTGRES_PORT'),
    }
}