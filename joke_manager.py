import asyncio
import aiohttp

from api_client import JokeAPIClient
from storage import JsonStorage

# შეიქმნა კლასი, გადაეცა ორი კლასის ობიექტი და ჩამოიტვირთა სთორიჯ სია.
class JokeManager:
    def __init__(self):
        self._api_client = JokeAPIClient()
        self._storage = JsonStorage()
        self._jokes = self._storage.load_jokes()

    # ასინქრონული მეთოდია ახალი ხუმრობების მისაღებად.
    async def get_new_jokes(self, category, count):
        if not 1 <= count <= 10:
            raise ValueError("The number of jokes must be from 1 to 10.")

        # აქ იქმნება სესია, რომლის საშუალებითაც ხდება მოთხოვნის გაგზავნა.
        # გროვდება დავალებები ლისტში.
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self._api_client.get_joke(session, category))
                for _ in range(count)]

            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        new_jokes = []

        for result in results:
            if isinstance(result, Exception):
                print(f"Could not get a joke: {result}")
            elif result is not None:
                new_jokes.append(result)

        if new_jokes:
            self._jokes.extend(new_jokes)
            self._storage.save_jokes(self._jokes)

        return new_jokes

    # მეთოდი – აბრუნებს ყველა ხუმრობას.
    def get_all_jokes(self):
        return self._jokes

    # მეთოდი – ფილტრავს ხუმრობებს კატეგორიის მიხედვით.
    def filter_jokes(self, category=""):
        filtered_jokes = self._jokes
        category = category.strip().lower()

        if category and category != "any":
            filtered_jokes = [joke for joke in filtered_jokes if joke.category.strip().lower() == category]

        return filtered_jokes

    # მეთოდი – ეძებს ხუმრობას ტექსტის მიხედვით.
    def search_jokes(self, search_text):
        search_text = search_text.strip().lower()

        if not search_text:
            return []

        return [joke for joke in self._jokes
            if search_text in joke.joke.lower()]

    # მეთოდი – შლის ხუმრობას.
    def delete_joke(self, number):
        if not isinstance(number, int):
            return False

        if number < 1 or number > len(self._jokes):
            return False

        self._jokes.pop(number - 1)
        self._storage.save_jokes(self._jokes)
        return True