class Console(object):
    logo = [
        '                                    ',
        '                         d8b        ',
        '                         Y8P        ',
        '                                    ',
        '  .d8888b 8888b. 888  888888 8888b. ',
        ' d88P"       "88b888  888888    "88b',
        ' 888     .d888888Y88  88P888.d888888',
        ' Y88b.   888  888 Y8bd8P 888 88  888',
        '  "Y8888P"Y888888  Y88P  888 "888888',
        '                                    '
    ]

    def __init__(self, **kwargs):
        self.parameters = kwargs

    def run(self, *args, **kwargs):
        print('\n'.join(self.logo))
        print("Use '-h' or '--help' for more instructions.")
