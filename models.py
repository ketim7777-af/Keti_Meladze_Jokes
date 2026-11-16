from pydantic import BaseModel


class Content(BaseModel):
    category: str


class Joke(Content):
    type: str
    joke: str

    def display_info(self):
        return (f"Category: {self.category}\n Type: {self.type}\n Joke: {self.joke}")