import datetime
import os
import re

import dataset
from twython import Twython

from . import twitter
from . import utils
from . import config


class Bot(object):
    """
    Main class for otorongo_pics, only point of entry for users.

    """
    def __init__(self):
        self.table = config.DB_NAME
        self.pics = None
        self.twitter = Twython(config.key, config.secret, config.token, config.token_secret)

    def get_pics(self):
        db = utils.get_database()
        query = "SELECT * FROM " + self.table + " WHERE random() < 0.01 "
        query += " AND posted IS DISTINCT FROM 'yes' limit 5"
        res = db.query(query)
        print("5 pics where selected")
        self.pics = res

    def post_pics(self):
        for pic in self.pics:
            year = get_date(pic['foto_fecha'])
            print(year)
            if year is not False:
                tuit = year + ': '
                tuit += pic['foto_descripcion'][0:84]
                tuit += ' ' + pic['foto_pagina']

            filename = get_photo(pic['foto_imagen'])
            print(filename)
            if filename is not False:
                photo = open(filename, 'rb')
                print(tuit)
                print(filename)
                self.twitter.update_status_with_media(status=tuit, media=photo)


def get_photo(url):
    photo = re.search('.+/(.+\.jpg)$', url).groups()[0]
    filename = os.path.join('pics', photo)
    if os.path.isfile(filename):
        return filename
    else:
        return False


def get_date(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%d/%m/%Y')
    except ValueError:
        return False

    year = str(date.year)
    return year
