import sys

import app.dbconfig
from app.queries_and_prompts  import *
from app.dbconfig import *


menu = [
    (1, "Search by Keyword", search_by_keyword),
    (2, "Search by Year and Genre", search_by_year_and_genre),
    (3, "Show Most Popular Filter", show_most_popular_filter),
    (4, "Search by Genre", search_by_genre),
    (5, "Search by Year", search_by_year),
    (0, "Exit", None)  # None means no function to call, just exit
]

def get_valid_input(prompt: str, valid_options: list) -> int:
    """Get numeric input from user, ensuring it's a valid menu option."""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:  # Handle empty input
                print("❌ Please enter a number.")
                continue
            choice = int(user_input)
            if choice in valid_options:
                return choice
            print("❌ Please choose a valid option from the menu.")
        except ValueError:
            print("❌ Please enter a number.")

def main():
    """Run the main menu loop for the film search application."""
    print("\n🎥 Welcome to the Film Search App! 🎥")
    print("Choose an option from the menu to search films or view popular filters.")

    while True:
        print("\n🗒 === Menu === 🗒")
        for option_num, option_name, _ in menu:
            print(f"{option_num}. {option_name}")

        valid_options = [item[0] for item in menu]
        choice = get_valid_input("⤴️ Choose an option: ", valid_options)

        if choice == 0:
            print("🌸 Thank you for using our application. Goodbye! 🌸")
            break

        for option_num, _, func in menu:            # find the function for the chosen option
            if option_num == choice and func is not None:
                result = func(cursorR)
                if result is None:
                    print("🔙 Returning to main menu...")
                break

if __name__ == '__main__':
    try:
        connR, cursorR = app.dbconfig.connect_read()

    except mysql.connector.Error as e:
        print(f"Error connecting to SQL database: {e}")
        sys.exit(1)

    try:
        main()
    except KeyboardInterrupt:
        print("\n🌸 Application terminated by user. Goodbye! 🌸")
    finally:
        app.dbconfig.close_connections()
        print("Database connections closed")
