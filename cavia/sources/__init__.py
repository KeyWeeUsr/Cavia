class Index(object):
    _sources = []
    _language = ['en']


    def __init__(self, *args, **kwargs):
        from cavia.sources.mangapanda import MangaPanda
        self._sources.append(MangaPanda)

    @property
    def list(self, *args, **kwargs):
        return sorted([src.name for src in self._sources])

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


class Source(object):
    name = 'Source'

    def __str__(self, *args, **kwargs):
        return self.name

    def fetch_list(self, url, tag):
        # download and cache the result
        # return cached the next time
        pass

    def reload_list(self, *args, **kwargs):
        # redownload and cache the result
        pass
