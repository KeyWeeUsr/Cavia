from cavia.sources import Source


class MangaPanda(Source):
    name = 'MangaPanda'
    url = 'http://www.mangapanda.com'
    list_list = 'http://www.mangapanda.com/alphabetical'

    def __init__(self, *args, **kwargs):
        pass
