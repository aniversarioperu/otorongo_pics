import datetime
import os
import re

from twython import Twython

from . import utils
from . import config


class Bot(object):
    """
    Main class for otorongo_pics, only point of entry for users.

    """
    def __init__(self):
        self.table_name = config.DB_NAME
        self.table = None
        self.pics = None
        self.twitter = Twython(config.key, config.secret, config.token, config.token_secret)

    def get_pics(self):
        db = utils.get_database()
        query = "SELECT * FROM " + self.table_name + " WHERE random() < 0.001 "
        query += " AND posted IS DISTINCT FROM 'yes' limit 15"
        res = db.query(query)
        print("5 pics where selected")
        self.pics = res
        self.table = db[self.table_name]

    def post_pics(self):
        count = 0
        for pic in self.pics:
            year = get_date(pic['foto_fecha'])
            if year is not False:
                tuit = year + ': '
                tuit += pic['foto_descripcion'][0:84]
                tuit += ' ' + pic['foto_pagina']

            filename = get_photo(pic['foto_imagen'])
            if filename is not False:
                if count == 1:
                    break
                photo = open(filename, 'rb')
                print(tuit)
                print(filename)
                self.twitter.update_status_with_media(status=tuit, media=photo)
                data = dict(id=pic['id'], posted='yes')
                self.table.update(data, ['id'])
                count += 1


def get_photo(url):
    photo = re.search('.+/(.+\.jpg)$', url).groups()[0]
    filename = os.path.join(config.pics_folder, photo)
    if os.path.isfile(filename):
        return filename
    else:
        print("could not find photo %s" % filename)
        return False


def get_date(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%d/%m/%Y')
    except ValueError:
        return False

    year = str(date.year)
    return year
