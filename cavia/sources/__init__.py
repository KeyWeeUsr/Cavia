# PYTHONIOENCODING="UTF-8" for printing
from urllib.request import urlopen
from bs4 import BeautifulSoup

from os.path import abspath, dirname, join, exists
from shutil import rmtree
from os import mkdir


class SourceDoesNotExist(Exception):
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

    def write_cache(self, content):
        cache = self.cache()
        assert '.cache' in cache

        with open(cache, 'wb') as f:
            return f.write(content)

    def write_cache_list(self, content):
        cache_list = self.cache_list()
        assert '_list.cache' in cache_list

        with open(cache_list, 'wb') as f:
            return f.write(content)

    def purge_cache(self):
        rmtree(dirname(self.cache()))

    def fetch_list(self):
        '''Download and cache the result return cache the next time.
        '''
        name = self.name
        cache = self.cache()
        with open(cache, 'rb') as f:
            cache = f.read()

        if not cache:
            website = urlopen(
                self.item_url,
                timeout=self.connection_timeout
            )
            content = website.read()
            self.write_cache(content)
            cache = content

        self.parsed = BeautifulSoup(
            cache.decode('utf-8'), 'html.parser'
        )

    def reload_list(self):
        # redownload and cache the result
        pass

    def print_items(self):
        fetch_items = self.fetch_list()
        len_items = len(fetch_items)

        items = [
            '{}.\t{}\n\t{}'.format(
                str(i + 1).zfill(len(str(len_items))),
                items[0],  # name
                items[1]   # URL
            )
            for i, items in enumerate(fetch_items)
        ]
        print('\n\n'.join(items))
