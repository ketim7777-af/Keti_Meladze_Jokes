import asyncio
import aiohttp
from pydantic import ValidationError

from models import Joke


BASE_URL = "https://v2.jokeapi.dev/joke"

# შევქმენი კლასი, ვიყენებ ასინქრონულ მეთოდს. 
# გარედან შექმნილი სესიის გამოყენებით კონკრეტული URL–ის მოთხოვნა იგზავნება.
# ჯეისონიდან პითონის ფორმატში აბრუნებს.
class JokeAPIClient:
    async def fetch_data(self, session, url):
        try:
            timeout = aiohttp.ClientTimeout(total=10)

            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                return await response.json()

        # მოწმდება ერორები.
        except aiohttp.ContentTypeError as error:
            print(f"Invalid response format: {error}")

        except aiohttp.ClientResponseError as error:
            print(f"API response error: {error}")

        except aiohttp.ClientConnectionError as error:
            print(f"Connection error: {error}")

        except asyncio.TimeoutError:
            print("The request timed out.")

        except Exception as error:
            print(f"Unexpected error: {error}")

    # ახალი ხუმრობები, კატეგორიის არჩევით.
    async def get_joke(self, session, category):
        url = f"{BASE_URL}/{category}" 

        data = await self.fetch_data(session, url)

        try:
            return Joke.model_validate(data)

        except ValidationError as error:
            print("Pydantic validation error:")
            print(error)