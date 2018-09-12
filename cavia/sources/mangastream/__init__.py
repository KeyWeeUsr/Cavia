from cavia.sources import Source

from ast import literal_eval

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


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

    def download_item(self, item_name, start, end):
        '''Use Source.download_item to parse download urls
        and retrieve the content.
        '''
        super(MangaStream, self).download_item(item_name, start, end)
        all_urls = []

        for part, chap in self.downloading:
            cache_download = self.cache_download_list(item_name, part)
            with open(cache_download, 'rb') as f:
                cache_download = f.read()

            if not cache_download:
                controls = chap.find_all('div', 'controls')[0]
                pagination = controls.find_all('ul', 'dropdown-menu')[-1]
                links = []
                for page in pagination.find_all('a'):
                    request = Request(
                        self.url + page.get('href'),
                        headers={
                            'User-Agent': (
                                'Mozilla/5.0 '
                                '(Windows NT 6.3; Win64; x64; rv:57.0) '
                                'Gecko/20100101 Firefox/57.0'
                            )
                        }
                    )
                    website = urlopen(
                        request,
                        timeout=self.connection_timeout
                    )
                    content = BeautifulSoup(
                        website.read().decode('utf-8'), 'html.parser'
                    )

                    found = content.find_all('img', {'id': 'manga-page'})[0]
                    src = found['src']
                    if src[:2] == '//':
                        src = src.replace('//', 'http://')
                    links.append(src)
                self.write_cache_download_list(
                    item_name, part,
                    str(links).encode('utf-8')
                )
            else:
                links = literal_eval(cache_download.decode('utf-8'))
            all_urls.append([part, links])
        self.download_files(self.download_folder, all_urls)
