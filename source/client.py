from pymongo import MongoClient


class Client:
    def __init__(self):
        self.host = "localhost:27017"
        self.db = None

    def set_db(self) -> None:
        client = MongoClient(self.host)
        self.db = client["DB"]

    def insert(self, data: dict, word: str):
        post = {word: data}
        self.db.insert(post)
