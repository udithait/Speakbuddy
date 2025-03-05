class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = 'Database connection established'
        return self.connection