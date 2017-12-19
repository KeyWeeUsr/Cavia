from cavia.sources import Source


class MangaPanda(Source):
    name = 'MangaPanda'
    url = 'http://www.mangapanda.com'
    item_url = 'http://www.mangapanda.com/alphabetical'
    item_tags = ['series_col']
    language = 'en'

    def fetch_list(self):
        super(MangaPanda, self).fetch_list()

        parsed = self.parsed
        items = []
        for tag in self.item_tags:
            print(parsed.find_all(tag))
