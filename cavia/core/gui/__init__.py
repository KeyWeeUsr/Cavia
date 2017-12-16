class GUI(object):
    def __init__(self, **kwargs):
        self.parameters = kwargs

    def run(self, *args, **kwargs):
        print('GUI', args, kwargs)
