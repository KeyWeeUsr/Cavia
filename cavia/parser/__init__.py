from argparse import ArgumentParser
from cavia import __version__, __name__ as name


Parser = ArgumentParser(prog=name, epilog='Epilog', add_help=True)
Parser.add_argument(
    '-V', '--version',
    action='version',
    version='%(prog)s %(ver)s' % {
        'prog': Parser.prog, 'ver': __version__
    }
)
subparsers = Parser.add_subparsers()

# add positional argument for Console
Parser.console_parser = subparsers.add_parser('console')

# add positional argument for GUI
Parser.gui_parser = subparsers.add_parser('gui')
