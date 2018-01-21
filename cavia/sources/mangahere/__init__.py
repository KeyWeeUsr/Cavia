from cavia.sources import Source

from os.path import dirname, join
from ast import literal_eval


class MangaHere(Source):
    name = 'mangahere'
    url = 'http://www.mangahere.cc'
    content_url = 'http://www.mangahere.cc/mangalist/'
    language = 'en'
    extension = '.jpg'

    def fetch_list(self):
        '''Use Source.fetch_list to download page content and parse it per
        separate Source file.
        '''
        super(MangaHere, self).fetch_list()

        cache_list = self.cache_list()
        with open(cache_list, 'rb') as f:
            cache_items = f.read()

        if cache_items:
            return literal_eval(cache_items.decode('utf-8'))

        parsed = self.parsed
        items = {}

        i = 0
        for lists in parsed.body.find_all('div', 'list_manga'):
            for results in lists.find_all('ul'):
                for result in results.find_all('li'):
                    for res in result.find_all('a'):
                        i += 1

                        # clean messed up URL
                        res_url = res.get('href')
                        bad_url = '//' + self.url[7:]
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
        super(MangaHere, self).fetch_item(item_name)

        cache_item = self.cache_item_list(item_name)
        with open(cache_item, 'rb') as f:
            cache_item = f.read()

        if cache_item:
            return literal_eval(cache_item.decode('utf-8'))

        parsed = self.parsed_item
        items = {}

        i = 0
        for results in parsed.body.find_all('div', 'detail_list'):
            for result in results.find_all('ul', {'class': None}):
                for res in reversed(result.find_all('li')):
                    i += 1

                    a_tag = res.find('a')
                    text = str(res.find('span', 'left').contents[-1])
                    text = '' if '<span' in text else text

                    # strip 'NAME ' from the number
                    key = a_tag.text.strip(item_name + ' ')
                    item_url = a_tag.get('href')

                    bad_url = '//' + self.url[7:]
                    if item_url.startswith(bad_url):
                        item_url = item_url.replace(bad_url, '')

                    items[str(i)] = {
                        'i': i, 'url': self.url + item_url, 'text': text
                    }

        self.write_cache_item_list(
            item_name,
            str(items).encode('utf-8')
        )
        return items
