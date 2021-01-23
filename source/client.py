import click
import pandas as pd
from pymongo import MongoClient

from utils.db_utils import check_number_of_collections
from utils.db_utils import create_path


class Client:
    def __init__(self):
        self.host = "mongodb://localhost:27017/"
        self.db = None

    def set_db(self) -> None:

        client = MongoClient(self.host)
        self.db = client["DB"]

    def insert(self, data: list, collection: str) -> None:

        cursor = self.db[collection]
        for result in data:
            post = result.get_description
            cursor.insert(post)

    def collections(self) -> list:

        collections = self.db.list_collection_names()
        check_number_of_collections(collections)

        collections_available = " ".join(collections)
        click.echo(click.style(f"Available collections: {collections_available}", bold=True))

        return collections

    def fetch_documents(self, collections: list) -> dict:

        docs = {}
        for collection in collections:
            cursor = self.db[collection]
            documents_in_collection = list(cursor.find({}))
            docs.update({collection: documents_in_collection})

        return docs

    def delete_collection(self, collection_name: str) -> None:
        collections = self.db.list_collection_names()

        if collection_name not in collections:
            raise Exception(f"Collection: {collection_name} not found.")
        else:
            self.db[collection_name].drop()


    @staticmethod
    def convert_to_df(docs: dict) -> pd.DataFrame:

        all_docs = []
        for collection, documents in docs.items():
            df = pd.DataFrame(documents).set_index("_id")
            df["Collection"] = collection
            all_docs.append(df)

        return pd.concat(all_docs, axis=0, sort=False)

    @staticmethod
    def export_to_csv(df: pd.DataFrame, directory: str) -> None:
        path = create_path(directory)
        print(df.head())
        df.to_excel(path, encoding='utf-8')
