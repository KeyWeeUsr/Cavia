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


if __name__ == '__main__':
    unittest.main()
