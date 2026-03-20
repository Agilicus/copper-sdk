from copper_sdk.base import BaseResource


class Users(BaseResource):

    def __init__(self, copper):
        self.copper = copper

    def get(self, id):
        return self.copper.get(f"/users/{id}")

    def list(self, body=None):
        if body is None:
            body = {}

        return self.copper.post('/users/search', body)
