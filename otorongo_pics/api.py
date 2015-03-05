import dataset

from . import twitter
from . import utils
from . import config


class Bot(object):
    """
    Main class for otorongo_pics, only point of entry for users.

    """
    def __init__(self):
        pass

    def get_pic(self):
        db = utils.get_database()
        query = "SELECT * FROM " + config.DB_NAME + " WHERE random() < 0.01 "
        query += " AND posted IS DISTINCT FROM 'yes' limit 5"
        res = db.query(query)
        for i in res:
            print(i)
