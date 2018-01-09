from cavia.sources import Source

from os.path import dirname, join
from ast import literal_eval

from urllib.request import urlopen
from bs4 import BeautifulSoup


class MangaFox(Source):
    name = 'mangafox'
    url = 'http://www.mangafox.la'
    content_url = 'http://www.mangafox.la/manga/'
    language = 'en'
    extension = '.jpg'

    def fetch_list(self):
        '''Use Source.fetch_list to download page content and parse it per
        separate Source file.
        '''
        super(MangaFox, self).fetch_list()

        cache_list = self.cache_list()
        with open(cache_list, 'rb') as f:
            cache_items = f.read()

        if cache_items:
            return literal_eval(cache_items.decode('utf-8'))

        parsed = self.parsed
        items = {}

        i = 0
        for lists in parsed.body.find_all('div', 'manga_list'):
            for results in lists.find_all('ul'):
                for result in results.find_all('li'):
                    for res in result.find_all('a'):
                        i += 1

                        # clean messed up URL
                        res_url = res.get('href')
                        bad_url = '//' + self.url[11:]
                        if res_url.startswith(bad_url):
                            res_url = res_url.replace(bad_url, '')

                        items[res.text] = {
                            'i': i,
                            'url': self.url + res_url
                        }

        self.write_cache_list(str(items).encode('utf-8'))
        return items

    def fetch_item(self, item_name):
        '''Use Source.fetch_item to download item content and parse it.
        '''
        super(MangaFox, self).fetch_item(item_name)

        cache_item = self.cache_item_list(item_name)
        with open(cache_item, 'rb') as f:
            cache_item = f.read()

        if cache_item:
            return literal_eval(cache_item.decode('utf-8'))

        parsed = self.parsed_item
        items = {}

        i = 0
        for results in parsed.body.find_all('div', {'id': 'chapters'}):
            for result in reversed(results.find_all('ul', 'chlist')):
                for res in reversed(result.find_all('li')):
                    i += 1

                    a_tag = res.find('a', 'tips')
                    title = res.find('span', 'title')
                    text = title.text if title else ''

                    # strip 'NAME ' from the number
                    key = a_tag.text.strip(item_name + ' ')
                    item_url = a_tag.get('href')

                    bad_url = '//' + self.url[11:]
                    if item_url.startswith(bad_url):
                        item_url = item_url.replace(bad_url, '')

                    items[key] = {
                        'i': i, 'url': self.url + item_url, 'text': text
                    }

        self.write_cache_item_list(
            item_name,
            str(items).encode('utf-8')
        )
        return items
