# PYTHONIOENCODING="UTF-8" for printing
from urllib.request import urlopen
from bs4 import BeautifulSoup

from os.path import abspath, dirname, join, exists
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
    def list(self, *args, **kwargs):
        return sorted([src.name for src in self._sources])

    @property
    def sources(self):
        return self._sources

    def print_sources(self, *args, **kwargs):
        lst = self.list
        lst_max = len(max(lst, key=len))
        for i, source in enumerate(lst):
            if not i % 2:
                print('    {}'.format(source), end='')
            else:
                print('    {0}{1}'.format(
                    ' ' * lst_max,
                    source
                ))

    def get_source(self, name):
        '''Return a Source instance fetched by the name.'''
        sources = [src.__name__.lower() for src in self.sources]

        if name not in sources:
            raise SourceDoesNotExist(repr(name))

        return self.sources[sources.index(name)]()


class Source(object):
    name = 'Source'
    language = ''
    cache_folder = join(
        dirname(abspath(__file__)),
        '__source_cache__'
    )
    connection_timeout = 5  # seconds

    def __str__(self, *args, **kwargs):
        return self.name

    def cache(self, name):
        name = name.lower()
        source = Index().get_source(name)
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

    def write_cache(self, name, content):
        cache = self.cache(name)
        assert '.cache' in cache

        with open(cache, 'wb') as f:
            return f.write(content)

    def fetch_list(self, *args, **kwargs):
        '''Download and cache the result return cache the next time.
        '''
        name = self.name.lower()
        cache = self.cache(name)
        with open(cache, 'rb') as f:
            cache = f.read()

        if not cache:
            website = urlopen(
                self.item_url,
                timeout=self.connection_timeout
            )
            content = website.read()
            self.write_cache(name, content)
            cache = content

        self.parsed = BeautifulSoup(
            cache.decode('utf-8'), 'html.parser'
        )

    def reload_list(self, *args, **kwargs):
        # redownload and cache the result
        pass
