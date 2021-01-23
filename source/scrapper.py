from utils.scrapper_utils import get_data
from nltk.corpus import wordnet as wn


import concurrent.futures
from source.data_types.scrapped_data import DataCollection
from contextlib import suppress


class Scrapper:
    def __init__(self, phrase: str):
        self.phrase = phrase.capitalize()
        self.url = "https://en.wikipedia.org/wiki/"
        self.similar_words = None
        self.scrapped = []

    def get_similar_words(self) -> None:

        concepts = wn.synsets(self.phrase)
        similar_words = [concept.lemma_names() for concept in concepts]

        if not similar_words:
            raise Exception("No similar words found")
        else:
            self.similar_words = set(sum(similar_words, []))

    def scrap_raw_data(self) -> None:

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = []
            for word in self.similar_words:
                futures.append(executor.submit(get_data, self.url, word))

            for future in concurrent.futures.as_completed(futures):
                with suppress(TypeError):
                    future = future.result()
                    text, word, url = future[0], future[1], future[2]
                    prepared_data = DataCollection(parsed_data=text, phrase=word, source=url)

                    self.scrapped.append(prepared_data)
