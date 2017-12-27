# PYTHONIOENCODING="UTF-8" for printing
from urllib.request import urlopen
from bs4 import BeautifulSoup

from os.path import abspath, dirname, join, exists
from shutil import rmtree
from os import mkdir


class SourceDoesNotExist(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class Index(object):
    def __init__(self, *args, **kwargs):
        # list of all sources as classes
        self._sources = []

        from cavia.sources.mangapanda import MangaPanda
        self._sources.append(MangaPanda)

    @property
    def list(self):
        return sorted([src.name for src in self.sources])

    @property
    def sources(self):
        return self._sources

    def print_sources(self):
        lst = sorted([src.__name__ for src in self.sources])
        lst_max = len(max(lst, key=len))
        for i, source in enumerate(lst):
            if not i % 2:
                print('    {}'.format(source), end='')
            else:
                print('    {0}{1}'.format(
                    ' ' * lst_max,
                    source
                ))

    def source(self, name):
        '''Return a Source instance fetched by the name.'''
        sources = [src.name for src in self.sources]

        name = name.lower()
        if name not in sources:
            raise SourceDoesNotExist(repr(name))

        return self.sources[sources.index(name)]()


class Source(object):
    name = 'source'
    language = ''
    cache_folder = join(
        dirname(abspath(__file__)),
        '__source_cache__'
    )
    connection_timeout = 5  # seconds

    def __str__(self):
        return self.name

    def cache(self):
        name = self.name
        source = Index().source(name)
        assert source is not None, 'Invalid source name!'

        if not exists(self.cache_folder):
            mkdir(self.cache_folder)

        self.source_folder = join(self.cache_folder, name)
        if not exists(self.source_folder):
            mkdir(self.source_folder)

        self.cache_file = join(self.source_folder, name + '.cache')
        if not exists(self.cache_file):
            with open(self.cache_file, 'wb') as f:
                f.write(b'')
        return self.cache_file

    def cache_list(self):
        cache = self.cache()
        self.cache_list_file = join(
            self.source_folder,
            self.name + '_list.cache'
        )
        if not exists(self.cache_list_file):
            with open(self.cache_list_file, 'wb') as f:
                f.write(b'')
        return self.cache_list_file

    def cache_item(self, item_name):
        cache = self.cache_list()
        if not hasattr(self, 'cache_item_files'):
            self.cache_item_files = {}

        path = join(
            self.source_folder,
            self.name + '_item_{}.cache'.format(item_name)
        )
        self.cache_item_files[item_name] = path

        if not exists(path):
            with open(path, 'wb') as f:
                f.write(b'')
        return path

    def cache_item_list(self, item_name):
        cache = self.cache_item(item_name)
        if not hasattr(self, 'cache_item_list_files'):
            self.cache_item_list_files = {}

        path = join(
            self.source_folder,
            self.name + '_item_list_{}.cache'.format(item_name)
        )
        self.cache_item_list_files[item_name] = path

        if not exists(path):
            with open(path, 'wb') as f:
                f.write(b'')
        return path

    def write_cache(self, content):
        cache = self.cache()
        assert '.cache' in cache

        with open(cache, 'wb') as f:
            f.write(content)

    def write_cache_list(self, content):
        cache_list = self.cache_list()
        assert '_list.cache' in cache_list

        with open(cache_list, 'wb') as f:
            f.write(content)

    def write_cache_item(self, item_name, content):
        cache_item = self.cache_item(item_name)
        assert '_item_{}.cache'.format(item_name) in cache_item

        with open(cache_item, 'wb') as f:
            f.write(content)

    def write_cache_item_list(self, item_name, content):
        cache_item_list = self.cache_item_list(item_name)
        assert '_item_list_{}.cache'.format(item_name) in cache_item_list

        with open(cache_item_list, 'wb') as f:
            f.write(content)

    def purge_cache(self):
        rmtree(dirname(self.cache()))

    def fetch_list(self):
        '''Download and cache the result return cache the next time.

        Returns a dictionary of this shape::

            {
                'name1': {'i': 1, 'url': 'URL'},
                'name2': {'i': 2, 'url': 'URL'}
            }
        '''
        name = self.name
        cache = self.cache()
        with open(cache, 'rb') as f:
            cache = f.read()

        if not cache:
            website = urlopen(
                self.content_url,
                timeout=self.connection_timeout
            )
            content = website.read()
            self.write_cache(content)
            cache = content

        self.parsed = BeautifulSoup(
            cache.decode('utf-8'), 'html.parser'
        )

    def fetch_item(self, item_name):
        '''Download and cache the result return cache the next time.
        '''
        name = self.name
        items = self.fetch_list()

        if item_name not in items:
            raise ItemDoesNotExist(repr(item_name))

        cache = self.cache_item(item_name)
        with open(cache, 'rb') as f:
            cache = f.read()

        item_url = items[item_name]['url']
        if not cache:
            website = urlopen(
                item_url,
                timeout=self.connection_timeout
            )
            content = website.read()
            self.write_cache_item(item_name, content)
            cache = content

        self.parsed_item = BeautifulSoup(
            cache.decode('utf-8'), 'html.parser'
        )

    def reload_list(self):
        # redownload and cache the result
        pass

    def print_items(self):
        '''Print items from Source.fetch_list()

        Expects a dictionary of this shape::

            {
                'name1': {'i': 1, 'url': 'URL'},
                'name2': {'i': 2, 'url': 'URL'}
            }
        '''
        fetch_items = self.fetch_list()
        len_items = len(fetch_items)

        # list of sorted dict keys
        sorted_items = sorted(
            fetch_items,
            key=lambda key: fetch_items[key]['i']
        )

        # list of [name, url] lists
        list_items = [
            [item, fetch_items[item]['url']]
            for item in sorted_items
        ]

        items = [
            '{}.\t{}\n\t{}'.format(
                str(i + 1).zfill(len(str(len_items))),
                items[0],  # name
                items[1]   # URL
            )
            for i, items in enumerate(list_items)
        ]
        print('\n\n'.join(items))

    def print_content_item(self, item_name):
        fetch_items = self.fetch_item(item_name)
        len_items = len(fetch_items)

        # list of sorted dict keys
        sorted_items = sorted(
            fetch_items,
            key=lambda key: fetch_items[key]['i']
        )

        # list of [name, url] lists
        list_items = [
            [fetch_items[item]['text'], fetch_items[item]['url']]
            for item in sorted_items
        ]

        items = [
            '{}.\t{}\n\t{}'.format(
                str(i + 1).zfill(len(str(len_items))),
                items[0],  # name
                items[1]   # URL
            )
            for i, items in enumerate(list_items)
        ]
        print('\n\n'.join(items))
