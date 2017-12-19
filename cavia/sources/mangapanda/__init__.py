from cavia.sources import Source


class MangaPanda(Source):
    name = 'MangaPanda'
    url = 'http://www.mangapanda.com'
    item_url = 'http://www.mangapanda.com/alphabetical'
    language = 'en'

    def __init__(self, *args, **kwargs):
        pass
