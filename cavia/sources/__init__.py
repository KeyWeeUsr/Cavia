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
        return self.sources[sources.index(name)]()


class Source(object):
    name = 'Source'
    language = ''

    def __str__(self, *args, **kwargs):
        return self.name

    def fetch_list(self, *args, **kwargs):
        '''Download and cache the result return cached the next time.
        '''
        print(self.url)
        print(self.item_url)

    def reload_list(self, *args, **kwargs):
        # redownload and cache the result
        pass
