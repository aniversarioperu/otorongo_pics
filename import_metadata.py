"""
Save metadata into a postgreSQL database.
"""
import os
import json
import sys

import sqlalchemy
import dataset


if os.path.isfile("config.json"):
    with open("config.json", "r") as f:
        secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        print(error_msg)
        sys.exit()


def create_database():
    db = dataset.connect('postgresql://' + DB_USER + ':' + DB_PASS + '@' +
                         DB_HOST + ':' + DB_PORT + '/' + DB_NAME)
    table = db['otorongo_pics']

    table.create_column('foto_imagen', sqlalchemy.String(length=100))
    table.create_column('foto_descripcion', sqlalchemy.String(length=1000))
    table.create_column('foto_codigo', sqlalchemy.String(length=200))
    table.create_column('foto_evento', sqlalchemy.String(length=200))
    table.create_column('foto_fecha', sqlalchemy.String(length=10))
    table.create_column('foto_lugar', sqlalchemy.String(length=200))
    table.create_column('foto_ambiente', sqlalchemy.String(length=200))
    table.create_column('foto_fotografo', sqlalchemy.String(length=200))
    table.create_column('foto_origen', sqlalchemy.String(length=200))
    table.create_column('foto_periodo', sqlalchemy.String(length=200))
    table.create_column('foto_congresistas', sqlalchemy.String(length=200))
    table.create_column('foto_personajes', sqlalchemy.String(length=200))
    table.create_column('foto_pagina', sqlalchemy.String(length=200))
    table.create_column('posted', sqlalchemy.String(length=10))
    return db

DB_USER = get_secret('DB_USER')
DB_PASS = get_secret('DB_PASS')
DB_NAME = get_secret('DB_NAME')
DB_PORT = get_secret('DB_PORT')
DB_HOST = get_secret('DB_HOST')

with open("fotos.csv", "r") as handle:
    fotos = handle.readlines()

items = []
for line in fotos:
    line = line.strip()
    fields = line.split('||')
    item = {
        'foto_imagen': fields[1],
        'foto_descripcion': fields[2],
        'foto_codigo': fields[3],
        'foto_evento': fields[4],
        'foto_fecha': fields[5],
        'foto_lugar': fields[6],
        'foto_ambiente': fields[7],
        'foto_fotografo': fields[8],
        'foto_origen': fields[9],
        'foto_periodo': fields[10],
        'foto_congresistas': fields[11],
        'foto_personajes': fields[12],
        'foto_pagina': fields[13],
    }
    items.append(item)

db = create_database()
table = db[DB_NAME]
table.insert_many(items)
