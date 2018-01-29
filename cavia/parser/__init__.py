from argparse import ArgumentParser, Action
from cavia import __version__, __name__ as name
from cavia.core.console import Console
from cavia.sources import Index


class ExecuteAction(Action):
    '''ArgumentParser action for add_argument(action=...)

    Executes a function and its args + kwargs passed as
    the __init__ arguments:

      * func
      * func_args
      * func_kwargs

    together with argument values inserted into func_kwargs
    as 'arg_values' and exits immediately.
    '''
    def __init__(self, func=None, func_args=(), func_kwargs={}, *a, **kw):
        super(ExecuteAction, self).__init__(*a, **kw)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def __call__(self, parser, namespace, values, option_string=None):
        self.func_kwargs['arg_values'] = values
        self.func(*self.func_args, **self.func_kwargs)
        exit()


class CaviaArgumentParser(ArgumentParser):
    def print_help(self, *args, **kwargs):
        print('\n'.join(Console.logo))
        super(CaviaArgumentParser, self).print_help(*args, **kwargs)


# create main parser
Parser = CaviaArgumentParser(
    prog=name,
    epilog='Epilog',
    add_help=True
)
Parser.add_argument(
    '-V', '--version',
    action='version',
    version='%(prog)s %(ver)s' % {
        'prog': Parser.prog, 'ver': __version__
    }
)

# create subparsers for main parser
subparsers = Parser.add_subparsers()

# add positional argument for main parser
Parser.console_parser = subparsers.add_parser('console')
Parser.gui_parser = subparsers.add_parser('gui')

# add optional arguments for Console.sources
Parser.console_parser.add_argument(
    '-l', '--sources',
    help='show all available sources',
    required=False, nargs=0,
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Index().print_sources()
    )
)

Parser.console_parser.add_argument(
    '-x', '--clear_cache',
    help='clear cache for a source',
    required=False, nargs=1,
    metavar='SOURCE',
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *a, **kw: Index().source(
            kw['arg_values'][0]
        ).purge_cache()
    )
)

Parser.console_parser.add_argument(
    '-X', '--clear_all_cache',
    help='clear cache for all sources',
    required=False, nargs=0,
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *a, **kw: Index().purge_all_cache()
    )
)

Parser.console_parser.add_argument(
    '-c', '--source_content',
    help='list all available content items in a source',
    required=False, nargs=1,
    metavar='SOURCE',
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *a, **kw: Index().source(
            kw['arg_values'][0]
        ).print_items()
    )
)

Parser.console_parser.add_argument(
    '-i', '--source_content_item',
    help='list all available parts of a content item in a source',
    required=False, nargs=2,
    metavar=('SOURCE', 'NAME'),
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *a, **kw: Index().source(
            kw['arg_values'][0]
        ).print_content_item(kw['arg_values'][1])
    )
)

Parser.console_parser.add_argument(
    '-d', '--source_download',
    help='download content from source',
    required=False, nargs=4,
    metavar=('SOURCE', 'NAME', 'START', 'END'),
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *a, **kw: Index().source(
            kw['arg_values'][0]
        ).download_item(
            *kw['arg_values'][1:4]
        )
    )
)

Parser.console_parser.add_argument(
    '-s', '--search',
    help='search all available parts of a source contents',
    required=False, nargs=1,
    metavar='PATTERN',
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *a, **kw: Index().search(
            kw['arg_values'][0]
        )
    )
)
