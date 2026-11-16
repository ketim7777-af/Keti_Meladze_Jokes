import json
import logging

from pydantic import ValidationError

from models import Joke


class JsonStorage:
    def __init__(self, filename="jokes.json"):
        self._filename = filename

    def load_jokes(self):
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                jokes_data = json.load(file)

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            logging.error("The jokes file has an incorrect JSON format.")
            return []

        if not isinstance(jokes_data, list):
            logging.error("The jokes file must contain a list.")
            return []

        jokes = []

        for joke_data in jokes_data:
            try:
                joke = Joke.model_validate(joke_data)
                jokes.append(joke)
            except ValidationError:
                logging.exception("Could not load a joke from the file.")

        return jokes

    def save_jokes(self, jokes):
        jokes_data = [joke.model_dump() for joke in jokes]

        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(jokes_data, file, indent=4, ensure_ascii=False)