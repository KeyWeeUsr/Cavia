import unittest
from unittest.mock import patch, MagicMock


class ParserTestCase(unittest.TestCase):
    @staticmethod
    def test_argument_parser():
        lines = ['a', 'b', 'c']
        console_mock = MagicMock(**{'logo': lines})

        # mock Console to inject custom lines for print_help()
        with patch(target='cavia.parser.Console', new=console_mock):
            # mock print() to check the output
            with patch(target='builtins.print') as stdout:
                from cavia.parser import CaviaArgumentParser as CAP
                CAP().print_help()

        # check the print_help() call
        stdout.assert_called_once_with('\n'.join(lines))

    def test_parser_setup(self):
        # pylint: disable=protected-access

        from cavia.parser import Parser, CaviaArgumentParser as CAP
        from cavia import __name__ as name

        # parser output prog name == name from package
        self.assertEqual(Parser.prog, name)
        opts = Parser._option_string_actions

        # the same func for two options in main parser
        self.assertIn('-V', opts)
        self.assertIn('--version', opts)
        self.assertEqual(opts['-V'], opts['--version'])

        # console parser is present in the main parser
        self.assertIn('console_parser', vars(Parser))
        self.assertIsInstance(Parser.console_parser, CAP)
        con_opts = Parser.console_parser._option_string_actions

        # the same func for two options in console parser
        self.assertIn('-l', con_opts)
        self.assertIn('--sources', con_opts)
        self.assertEqual(con_opts['-l'], con_opts['--sources'])

        self.assertIn('-x', con_opts)
        self.assertIn('--clear_cache', con_opts)
        self.assertEqual(con_opts['-x'], con_opts['--clear_cache'])

        self.assertIn('-X', con_opts)
        self.assertIn('--clear_all_cache', con_opts)
        self.assertEqual(con_opts['-X'], con_opts['--clear_all_cache'])

        self.assertIn('-c', con_opts)
        self.assertIn('--source_content', con_opts)
        self.assertEqual(con_opts['-c'], con_opts['--source_content'])

        self.assertIn('-i', con_opts)
        self.assertIn('--source_content_item', con_opts)
        self.assertEqual(con_opts['-i'], con_opts['--source_content_item'])

        self.assertIn('-d', con_opts)
        self.assertIn('--source_download', con_opts)
        self.assertEqual(con_opts['-d'], con_opts['--source_download'])

        self.assertIn('-s', con_opts)
        self.assertIn('--search', con_opts)
        self.assertEqual(con_opts['-s'], con_opts['--search'])

        # gui parser is present in the main parser
        self.assertIn('gui_parser', vars(Parser))
        self.assertIsInstance(Parser.gui_parser, CAP)


if __name__ == '__main__':
    unittest.main()
