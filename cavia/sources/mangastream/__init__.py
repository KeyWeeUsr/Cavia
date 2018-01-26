from cavia.sources import Source

from ast import literal_eval


class MangaStream(Source):
    name = 'mangastream'
    url = 'http://readms.net'
    content_url = 'http://readms.net/manga/'
    language = 'en'
    extension = '.jpg'

    def fetch_list(self):
        '''Use Source.fetch_list to download page content and parse it per
        separate Source file.
        '''
        super(MangaStream, self).fetch_list()

        cache_list = self.cache_list()
        with open(cache_list, 'rb') as f:
            cache_items = f.read()

        if cache_items:
            return literal_eval(cache_items.decode('utf-8'))

        parsed = self.parsed
        items = {}

        i = 0
        for lists in parsed.body.find_all('table', 'table'):
            for results in lists.find_all('tr'):
                for result in results.find_all('td'):
                    for res in result.find_all('a', {'class': None}):
                        i += 1

                        # clean messed up URL
                        res_url = res.get('href')

                        items[res.text] = {
                            'i': i,
                            'url': self.url + res_url
                        }

        self.write_cache_list(str(items).encode('utf-8'))
        return items

    def fetch_item(self, item_name):
        '''Use Source.fetch_item to download item content and parse it.
        '''
        super(MangaStream, self).fetch_item(item_name)

        cache_item = self.cache_item_list(item_name)
        with open(cache_item, 'rb') as f:
            cache_item = f.read()

        if cache_item:
            return literal_eval(cache_item.decode('utf-8'))

        parsed = self.parsed_item
        items = {}

        i = 0
        for results in parsed.body.find_all('table', 'table'):
            for result in reversed(results.find_all('td')):
                for res in result.find_all('a'):
                    i += 1

                    item_url = res.get('href')
                    text = res.contents[0]

                    items[str(i)] = {
                        'i': i, 'url': self.url + item_url, 'text': text
                    }

        self.write_cache_item_list(
            item_name,
            str(items).encode('utf-8')
        )
        return items
