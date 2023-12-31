class RepositoryMock:
    _name: str
    _pk: str
    _fields: list

    def __init__(self, data):
        self.data = data

    def entityExists(self, identifier):
        return None

    def fetch(self) -> list:
        return [self.data]

    def getById(self, identity) -> list:
        return self.data

    def delete(self, identity) -> bool:
        return True

    def create(self, data) -> bool:
        return True

    def update(self, data) -> bool:
        return True
