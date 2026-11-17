from pydantic import BaseModel

# შევქმენი კლასი და ქვეკლასი, მემკვიდრეობითობის საჩვენებლად.
# რადგან პაიდენტიკიდან ბეიზმოდელს ვაიმპორტებ, ინიციალიზაცია აღარ არის საჭირო
class Content(BaseModel):
    category: str


class Joke(Content):
    type: str
    joke: str

    def display_info(self):
        return (f"Category: {self.category}\n"
                f"Type: {self.type}\n"
                f"Joke: {self.joke}")