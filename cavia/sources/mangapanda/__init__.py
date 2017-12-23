from cavia.sources import Source


class MangaPanda(Source):
    name = 'mangapanda'
    url = 'http://www.mangapanda.com'
    item_url = 'http://www.mangapanda.com/alphabetical'
    language = 'en'

    def fetch_list(self):
        super(MangaPanda, self).fetch_list()

        parsed = self.parsed
        items = []

        for results in parsed.body.find_all('ul', 'series_alpha'):
            for result in results.find_all('li'):
                for res in result.find_all('a'):
                    items.append([res.text, self.url + res.get('href')])
        return items
