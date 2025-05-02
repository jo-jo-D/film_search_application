import mysql.connector

from app.dbconfig import *
from app.decorators import *


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

def existing(kw, cursorE):
    """Check if a filter exists in the database."""

    try:
        cursorE.execute("SELECT 1 FROM filter_counter WHERE filter_text = %s", (kw,))
        return cursorE.fetchone() is not None
    except mysql.connector.Error as e:
        print(f"Error checking filter: {e}")
        return False

def insert_or_update(kw, search_type):
    """Insert or update filter count in the database."""
    connE, cursorE = connect_write()

    try:
        if existing(kw, cursorE):
            cursorE.execute("UPDATE filter_counter SET filter_count = filter_count + 1 WHERE filter_text = %s", (kw,))
        else:
            cursorE.execute('''
                INSERT INTO filter_counter (filter_text, filter_type, filter_count)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE filter_count = filter_count + 1
            ''', (kw, search_type, 1))
        connE.commit()
    except mysql.connector.Error as e:
        print(f"Error updating filter: {e}")
        connE.rollback()


@beautiful_output
@calling_next_10
def search_by_keyword(cursorR):
    """Search films by keyword."""

    try:
        keyword = input('Enter keyword: ').strip()
        if not keyword:
            print("The keyword cannot be empty.")
            return None
    except Exception as e:
        print(f"Error with input: {e}")
        return None
    try:
        cursorR.execute("""
            SELECT title, release_year, length, rating
            FROM film
            WHERE LOWER(description) LIKE %s OR LOWER(title) LIKE %s
        """, ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%'))
        result = cursorR.fetchall()
        if not result:
            print('No results by chosen keyword')
            return None
        else:
            insert_or_update(keyword, 'keyword')
            return list(enumerate(result, start=1)), cursorR
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None


@beautiful_output
@calling_next_10
def search_by_year_and_genre(cursorR):
    """Search films by year and genre."""

    genre = choose_genre(cursorR)
    if genre:
        year = choose_year(cursorR)
        if genre and year:
            try:
                cursorR.execute("""
                    SELECT title, ct.name, release_year, length, rating
                    FROM film AS fl
                    LEFT JOIN film_category AS fct ON fl.film_id = fct.film_id
                    LEFT JOIN category AS ct ON fct.category_id = ct.category_id
                    WHERE fl.release_year = %s AND ct.name = %s
                """, (year, genre))
                result = cursorR.fetchall()
                if not result:
                    print('No results by chosen year')
                    return None
                else:
                    insert_or_update(f"{year}, {genre}", "year and genre")
                    return list(enumerate(result, start=1)), cursorR
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
                return None
        return None
    return None

@beautiful_output
@calling_next_10
def search_by_genre(cursorR):
    """Search films by genre."""

    genre = choose_genre(cursorR)
    if genre:
        try:
            cursorR.execute("""
                SELECT fl.title,ct.name, fl.release_year, fl.length, fl.rating
                FROM film AS fl
                LEFT JOIN film_category AS fct ON fl.film_id = fct.film_id
                LEFT JOIN category AS ct ON fct.category_id = ct.category_id
                WHERE ct.name = %s
            """, (genre,))
            result = cursorR.fetchall()
            if result is None:
                print('No results by chosen genre')
                return None
            else:
                insert_or_update(genre, "genre")
                return list(enumerate(result, start=1)), cursorR

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None


@beautiful_output
@calling_next_10
def search_by_year(cursorR):
    """Search films by year."""

    year = choose_year(cursorR)
    if year and year is not None:
        try:
            cursorR.execute("""
                SELECT fl.title,ct.name, fl.release_year, fl.length, fl.rating
                FROM film AS fl
                LEFT JOIN film_category AS fct ON fl.film_id = fct.film_id
                LEFT JOIN category AS ct ON fct.category_id = ct.category_id
                WHERE fl.release_year = %s
            """, (year,))
            result = cursorR.fetchall()
            if result is None:
                print('No results by chosen genre')
                return None
            else:
                insert_or_update(year, "year")
                return list(enumerate(result, start=1)), cursorR

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None


@beautiful_output
def show_most_popular_filter(cursorE):
    """Show the most popular filter."""
    connE, cursorE = connect_write()
    try:
        cursorE.execute("""
            SELECT filter_text, filter_type, filter_count
            FROM filter_counter
            WHERE filter_count = (
                SELECT MAX(filter_count)
                FROM filter_counter
            )
        """)
        return list(enumerate(cursorE.fetchall(), start=1)), cursorE
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None


def choose_year(cursorR):
    """Prompt user to choose a year."""
    try:
        cursorR.execute("SELECT DISTINCT release_year FROM film")
        yrs = [row[0] for row in cursorR.fetchall()]
    except mysql.connector.Error as e:
        print(f"Error fetching years: {e}")
        return False
    while True:
        try:
            choice = input("Choose a year (or press Enter to exit to main menu): ").strip()
            if choice == '':
                return False
            choice = int(choice)
            if choice in yrs:
                return choice
            else:
                print("No movies for the selected year.\n")
                return None
        except ValueError:
            print("Please enter a number.\n")
            continue


def choose_genre(cursorR):
    """Prompt user to choose a genre."""

    try:
        cursorR.execute("SELECT DISTINCT name FROM category")
        genres_list = [row[0] for row in cursorR.fetchall()]
    except mysql.connector.Error as e:
        print(f"Error fetching genres: {e}")
        return False
    while True:
        for num, genre in enumerate(genres_list, start=1):
            print(f"{num:2}. {genre}")
        try:
            index = input("Choose a genre by number (or press Enter to exit to main menu): ")
            if index == '':
                return False
            index = int(index)
            if 1 <= index <= len(genres_list):
                return genres_list[index - 1]
            else:
                print("Please choose a valid number from the list.\n")
        except ValueError:
            print("Please enter a number.\n")
            continue

