import dataset

from . import config


DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_NAME = config.DB_NAME


def get_database():
    db = dataset.connect('postgresql://' + DB_USER + ':' + DB_PASS + '@' +
                         DB_HOST + ':' + DB_PORT + '/' + DB_NAME)
    return db
