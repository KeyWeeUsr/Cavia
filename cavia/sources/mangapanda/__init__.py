from cavia.sources import Source

from os.path import dirname, join
from ast import literal_eval


class MangaPanda(Source):
    name = 'mangapanda'
    url = 'http://www.mangapanda.com'
    item_url = 'http://www.mangapanda.com/alphabetical'
    language = 'en'

    def fetch_list(self):
        '''Use Source.fetch_list to download page content and parse it per
        separate Source file.
        '''
        super(MangaPanda, self).fetch_list()

        cache_list = self.cache_list()
        with open(cache_list, 'rb') as f:
            cache_items = f.read()

        if cache_items:
            return literal_eval(cache_items.decode('utf-8'))

        parsed = self.parsed
        items = {}

        i = 0
        for results in parsed.body.find_all('ul', 'series_alpha'):
            for result in results.find_all('li'):
                for res in result.find_all('a'):
                    i += 1
                    items[res.text] = {
                        'i': i, 'url': self.url + res.get('href')
                    }

        self.write_cache_list(str(items).encode('utf-8'))
        return items
