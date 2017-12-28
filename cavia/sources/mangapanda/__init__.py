from cavia.sources import Source

from os.path import dirname, join
from ast import literal_eval


class MangaPanda(Source):
    name = 'mangapanda'
    url = 'http://www.mangapanda.com'
    content_url = 'http://www.mangapanda.com/alphabetical'
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

    def fetch_item(self, item_name):
        '''Use Source.fetch_item to download item content and parse it.
        '''
        super(MangaPanda, self).fetch_item(item_name)

        cache_item = self.cache_item_list(item_name)
        with open(cache_item, 'rb') as f:
            cache_item = f.read()

        if cache_item:
            return literal_eval(cache_item.decode('utf-8'))

        parsed = self.parsed_item
        items = {}

        i = 0
        for results in parsed.body.find_all('div', {'id': 'chapterlist'}):
            for result in results.find_all('table', {'id': 'listing'}):
                for res in result.find_all('tr', {'class': ''}):
                    i += 1
                    res = res.find('td')
                    a_tag = res.find('a')

                    # strip 'NAME ' from the number
                    key = a_tag.text.strip(item_name + ' ')
                    item_url = a_tag.get('href')
                    assert str(i) == key

                    # MP separator for URL + chapter name
                    assert ' : ' == res.contents[-1][:3]
                    text = res.contents[-1][3:]
                    items[key] = {
                        'i': i, 'url': self.url + item_url, 'text': text
                    }

        self.write_cache_item_list(
            item_name,
            str(items).encode('utf-8')
        )
        return items
