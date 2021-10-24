class Cache:

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data

    def get_data(self):
        return self.data
