import unittest
from unittest import mock

from cavia.sources import Index
from cavia.sources.mangafox import MangaFox
from urllib.request import Request
from os.path import abspath, dirname, join
from io import BytesIO

SAMPLES = join(dirname(abspath(__file__)), 'samples')
PATHS = {
    MangaFox.content_url: join(SAMPLES, 'mangafox', 'content.html')
}

TREE = {
    MangaFox.content_url: {
        '-Title 1-': {},
        ':TiTlE 2': {},
        '...Title 3': {},
        '.Ti//4tle': {},
        '"Title" 5 quot.': {},
        '~Title 6~': {},
        'Ti\'tle? 7': {},
        'Title 8%': {},
        'Title 9': {},
        'Title? 10': {}
    }
}


def mocked_urlopen(url, *args, **kwargs):
    if isinstance(url, Request):
        url = url.get_full_url()
    with open(PATHS[url], 'rb') as f:
        return BytesIO(f.read())


@mock.patch(
    # Source.fetch_list
    'cavia.sources.urlopen',
    mocked_urlopen
)
class MangaFoxTestCase(unittest.TestCase):
    def test_content_parse(self):
        index = Index()
        source = index.source('mangafox')
        items = source.fetch_list()

        self.assertEqual(source.content_url, MangaFox.content_url)
        self.assertEqual(len(items), len(TREE[MangaFox.content_url]))
        for item in items:
            self.assertIn(item, TREE[MangaFox.content_url])


if __name__ == '__main__':
    unittest.main()
