from cavia.sources import Source


class MangaStream(Source):
    name = 'mangastream'
    url = 'http://readms.net'
    content_url = 'http://readms.net/manga/'
    language = 'en'
    extension = '.jpg'
