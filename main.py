import asyncio

from joke_manager import JokeManager


categories = {
    "1": "Any",
    "2": "Programming",
    "3": "Misc",
    "4": "Pun",
    "5": "Spooky",
    "6": "Christmas"
}


def show_jokes(jokes):
    if not jokes:
        print("\nNo jokes found.")
        return

    for number, joke in enumerate(jokes, start=1):
        print(f"\n{number}.")
        print(joke.display_info())
        print("--------------------")


def choose_category():
    while True:
        print("\nChoose a category from 1 to 6: ")

        for number, category in categories.items():
            print(f"{number}. {category}")

        choice = input("Your choice: ").strip()

        category = categories.get(choice)

        if category is not None:
            return category
        else:
            print("Invalid choice. Please choose a number from 1 to 6.")


def get_joke_count():
    while True:
        try:
            count = int(input("How many jokes? (1-10): ").strip())
        except ValueError:
            print("Please enter a whole number.")
            continue

        if not 1 <= count <= 10:
            print("Please enter a number from 1 to 10.")
            continue

        return count


def get_search_text():
    while True:
        search_text = input("Enter a word to search for: ").strip()

        if search_text:
            return search_text

        print("Search text cannot be empty. Please try again.")


def get_delete_number(joke_count):
    while True:
        try:
            number = int(input("Enter the number of the joke to delete: ").strip())
        except ValueError:
            print("Please enter a whole number.")
            continue

        if not 1 <= number <= joke_count:
            print(f"Please enter a number from 1 to {joke_count}.")
            continue

        return number


async def main():
    manager = JokeManager()

    while True:
        print("\n=== Joke Collector ===")
        print("1. Get new jokes")
        print("2. View joke history")
        print("3. Filter jokes by category")
        print("4. Search jokes by text")
        print("5. Delete a joke")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            category = choose_category()
            count = get_joke_count()

            jokes = await manager.get_new_jokes(category, count)
            show_jokes(jokes)

        elif choice == "2":
            show_jokes(manager.get_all_jokes())

        elif choice == "3":
            category = choose_category()
            jokes = manager.filter_jokes(category=category)
            show_jokes(jokes)

        elif choice == "4":
            search_text = get_search_text()
            jokes = manager.search_jokes(search_text)
            show_jokes(jokes)

        elif choice == "5":
            all_jokes = manager.get_all_jokes()
            show_jokes(all_jokes)

            if all_jokes:
                number = get_delete_number(len(all_jokes))

                if manager.delete_joke(number):
                    print("Joke deleted.")
                else:
                    print("Could not delete the joke.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    asyncio.run(main())