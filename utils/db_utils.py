import os.path


def check_number_of_collections(data: list) -> None:
    if len(data) == 0:
        raise Exception("DB is empty.")


def create_path(directory: str) -> str:
    if os.path.exists(directory):
        df_path = os.path.join(directory, "db.xlsx")
        return df_path
