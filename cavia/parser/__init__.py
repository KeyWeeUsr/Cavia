from argparse import ArgumentParser, Action
from cavia import __version__, __name__ as name


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

# add positional arguments for Console
console_subparsers = Parser.console_parser.add_subparsers()
Parser.console_parser.sources = console_subparsers.add_parser('sources')

# add optional arguments for Console.sources
Parser.console_parser.sources.add_argument(
    'list',
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=print,
        func_args=('list', ),
        func_kwargs={}
    )
)
