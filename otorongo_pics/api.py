from . import twitter


class Bot(object):
    """
    Main class for otorongo_pics, only point of entry for users.

    """
    def __init__(self):
        pass

    def get_pic(self):
        memes = twitter.search_in_twitter(keywords)
        print(memes)
