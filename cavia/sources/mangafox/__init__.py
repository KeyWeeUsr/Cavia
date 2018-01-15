from cavia.sources import Source

from os.path import dirname, join
from ast import literal_eval

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import zlib


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
        super(MangaFox, self).download_item(item_name, start, end)
        all_urls = []

        for part, chap in self.downloading:
            cache_download = self.cache_download_list(item_name, part)
            with open(cache_download, 'rb') as f:
                cache_download = f.read()

            if not cache_download:
                url_base = chap.find_all('a', {'id': 'comments'})[0]
                url_base = url_base.get('href')
                bad_url = '//' + self.url[11:]
                if url_base.startswith(bad_url):
                    url_base = url_base.replace(bad_url, '')


                pagination = chap.find_all('select', 'm')[0]
                links = []
                for opt in pagination.find_all('option'):
                    # Comments section
                    if opt.attrs['value'] == '0':
                        continue

                    request = Request(
                        self.url + url_base + opt.attrs['value'] + '.html',
                        headers={
                            'User-Agent' : (
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
                    encoding = website.info().get('Content-Encoding')
                    if encoding == 'gzip':
                        content = zlib.decompress(
                            website.read(), 16 + zlib.MAX_WBITS
                        )
                    else:
                        content = website.read()
                    content = BeautifulSoup(
                        content.decode('utf-8'), 'html.parser'
                    )
                    found = content.find_all('img', {'id': 'image'})[0]
                    links.append(found['src'])
                self.write_cache_download_list(
                    item_name, part,
                    str(links).encode('utf-8')
                )
            else:
                links = literal_eval(cache_download.decode('utf-8'))
            all_urls.append([part, links])
        self.download_files(self.download_folder, all_urls)
