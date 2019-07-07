from urllib.parse import urlparse

from pyramid.config import Configurator
from pyramid.response import Response
from pymongo import MongoClient


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.add_route('new_video', '/new_video')
    config.add_route('evaluate', '/evaluate')
    config.add_route('trending', '/trending')
    config.add_static_view(name='static', path='app:static')
    config.scan('.views')

    db_url = urlparse(settings['mongo_uri'])

    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    config.add_request_method(add_db, 'db', reify=True)

    return config.make_wsgi_app()
