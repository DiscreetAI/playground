import os
import connexion

from services.dbinterfacer import DBInterfacer

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver


def configure(binder: Binder):
    binder.bind(DBInterfacer, DBInterfacer('some_host', 'some_port'))
    return binder


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('indexer.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run(port=5000)
