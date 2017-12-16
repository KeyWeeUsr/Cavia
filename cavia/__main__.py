from cavia.parser import Parser


if __name__ == '__main__':
    Parser.set_defaults(type='main')
    Parser.console_parser.set_defaults(type='console')
    Parser.gui_parser.set_defaults(type='gui')
    main_parser = Parser.parse_args()

    if main_parser.type == 'main':
        Parser.print_help()
        exit()
    elif main_parser.type == 'console':
        from cavia.core.console import Console as Client
    elif main_parser.type == 'gui':
        from cavia.core.gui import GUI as Client
    Client(**vars(main_parser)).run()
