import sys
import unittest
from unittest.mock import patch, MagicMock

from cavia import __main__ as cavia_main


class MainTestCase(unittest.TestCase):
    def test_import(self):
        with patch('cavia.__main__.Parser') as parser:
            # run_main is called, but only returns
            self.assertIsNone(cavia_main.run_main('import'))

            # the first parser configuration isn't called
            parser.set_defaults.assert_not_called()

    def test_main(self):
        # backup old console args, set new ones
        old_args = sys.argv[:]
        sys.argv = ['cavia']

        # set main_parser.type value to 'main',
        # so that new Mock isn't created instead
        parser = MagicMock(**{'parse_args.return_value.type': 'main'})

        with patch(target='cavia.__main__.Parser', new=parser):
            # mocked Parser with type == 'main' doesn't have
            # the Client defined, only prints help and exits
            with self.assertRaises(SystemExit) as cavia_exit:
                cavia_main.run_main('__main__')

        # revert to previous args
        sys.argv = old_args

        # default parser type is set to 'main'
        parser.set_defaults.assert_called_once_with(type='main')

        # subparsers are different types user when selected
        # from the console i.e. 'cavia console' instead of 'cavia'
        parser.console_parser.set_defaults.assert_called_once_with(
            type='console'
        )
        parser.gui_parser.set_defaults.assert_called_once_with(type='gui')

        # parsing args from console
        parser.parse_args.assert_called_once_with()

        # main parser type is set to 'main' via 'cavia' only args
        self.assertEqual(parser.parse_args.return_value.type, 'main')

        # help page is printed out
        parser.print_help.assert_called_once_with()

        # console is exited with zero/None exit code
        self.assertIsNone(cavia_exit.exception.code)

    def test_console(self):
        # backup old console args, set new ones
        old_args = sys.argv[:]
        sys.argv = ['cavia']

        # set main_parser.type value to 'console',
        # so that new Mock isn't created instead
        parser = MagicMock(**{'parse_args.return_value.type': 'console'})

        with patch(target='cavia.__main__.Parser', new=parser):
            with patch(target='cavia.core.console.Console') as client:
                cavia_main.run_main('__main__')

        # revert to previous args
        sys.argv = old_args

        # default parser type is set to 'main'
        parser.set_defaults.assert_called_once_with(type='main')

        # subparsers are different types user when selected
        # from the console i.e. 'cavia console' instead of 'cavia'
        parser.console_parser.set_defaults.assert_called_once_with(
            type='console'
        )
        parser.gui_parser.set_defaults.assert_called_once_with(type='gui')

        # parsing args from console
        parser.parse_args.assert_called_once_with()

        # main parser type is set to 'console' via 'cavia console' only args
        self.assertEqual(parser.parse_args.return_value.type, 'console')

        # help page is not printed out
        parser.print_help.assert_not_called()

        # Client class is instantiated and run() is called
        client.assert_called_once_with(**vars(
            parser.parse_args.return_value
        ))
        client.return_value.run.assert_called_once_with()

    def test_gui(self):
        # backup old console args, set new ones
        old_args = sys.argv[:]
        sys.argv = ['cavia']

        # set main_parser.type value to 'gui',
        # so that new Mock isn't created instead
        parser = MagicMock(**{'parse_args.return_value.type': 'gui'})

        with patch(target='cavia.__main__.Parser', new=parser):
            with patch(target='cavia.core.gui.GUI') as client:
                cavia_main.run_main('__main__')

        # revert to previous args
        sys.argv = old_args

        # default parser type is set to 'main'
        parser.set_defaults.assert_called_once_with(type='main')

        # subparsers are different types user when selected
        # from the console i.e. 'cavia console' instead of 'cavia'
        parser.console_parser.set_defaults.assert_called_once_with(
            type='console'
        )
        parser.gui_parser.set_defaults.assert_called_once_with(type='gui')

        # parsing args from console
        parser.parse_args.assert_called_once_with()

        # main parser type is set to 'gui' via 'cavia gui' only args
        self.assertEqual(parser.parse_args.return_value.type, 'gui')

        # help page is not printed out
        parser.print_help.assert_not_called()

        # Client class is instantiated and run() is called
        client.assert_called_once_with(**vars(
            parser.parse_args.return_value
        ))
        client.return_value.run.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
