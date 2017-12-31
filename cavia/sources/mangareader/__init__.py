from cavia.sources.mangapanda import MangaPanda


class MangaReader(MangaPanda):
    # same structure like MangaPanda website
    name = 'mangareader'
    url = 'http://www.mangareader.net'
    content_url = 'http://www.mangareader.net/alphabetical'
    language = 'en'
    extension = '.jpg'
