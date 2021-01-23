from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DataCollection:
    parsed_data: str
    phrase: str
    source: str
    current_date: Any = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @property
    def get_description(self) -> dict:
        data = {"date": self.current_date,
                "content": self.parsed_data,
                "from": self.source,
                "key-phrase": self.phrase}

        return data
