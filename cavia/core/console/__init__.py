class Console(object):
    def __init__(self, **kwargs):
        self.parameters = kwargs

    def run(self, *args, **kwargs):
        print('Console', args, kwargs)
