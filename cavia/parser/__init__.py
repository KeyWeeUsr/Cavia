from argparse import ArgumentParser, Action
from cavia import __version__, __name__ as name
from cavia.sources import Index


class ExecuteAction(Action):
    '''ArgumentParser action for add_argument(action=...)

    Executes a function and its args + kwargs passed as
    the __init__ arguments:

      * func
      * func_args
      * func_kwargs

    and exits immediately.
    '''
    def __init__(self, func=None, func_args=(), func_kwargs={}, *a, **kw):
        super(ExecuteAction, self).__init__(*a, **kw)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def __call__(self, *args, **kwargs):
        self.func(*self.func_args, **self.func_kwargs)
        exit()


# create main parser
Parser = ArgumentParser(
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
    '-s', '--sources',
    help='show all available sources',
    required=False, nargs=0,
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=Index().print_sources
    )
)
