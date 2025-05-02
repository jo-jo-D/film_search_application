# import os
# from pathlib import Path
# import mysql.connector
# import dotenv
# import functools
# import itertools
# from tabulate import tabulate
# import types
#
#
# dotenv.load_dotenv(Path('.env'))
#
# db_config_r = {
#     'host': os.environ.get('host_r'),
#     'user': os.environ.get('user_r'),
#     'password': os.environ.get('password_r'),
#     'database': 'sakila'
# }
#
#
# db_config_e = {
#     'host': os.environ.get('host_e'),
#     'user': os.environ.get('user_e'),
#     'password': os.environ.get('password_e'),
#     'database': 'Trotskaya_111124'
# }
#
#
# connR = mysql.connector.connect(**db_config_r)
# cursorR = connR.cursor()
# connE = mysql.connector.connect(**db_config_e)
# cursorE = connE.cursor()
#
# def check_connection(conn):
#     """Check if the database connection is alive."""
#     try:
#         conn.ping(reconnect=False)
#         return True
#     except mysql.connector.Error:
#         return False
#
# def reconnect(config, max_retries=3):
#     """Try to reconnect to the database if the connection is down."""
#     for attempt in range(max_retries):
#         try:
#             conn = mysql.connector.connect(**config)
#             print(f"Reconnected to database on attempt {attempt + 1}")
#             return conn
#         except mysql.connector.Error as e:
#             print(f"Reconnection attempt {attempt + 1} failed: {e}")
#             time.sleep(2)
#     print("Failed to reconnect to database. Please try again later.")
#     return None
#
# def calling_next_10(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         if result:
#             rows, cursor = result
#             step = 10
#
#             def generator():
#                 for i in range(0, len(rows), step):
#                     yield rows[i:i + step]
#             return generator(), cursor
#     return wrapper
#
#
# def beautiful_output(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         if result is None:
#             return None
#
#         function, cursor = result
#         if cursor is None:
#             return None
#
#         column_names = [desc[0] for desc in cursor.description]
#
#         if isinstance(function, types.GeneratorType):
#             while True:
#                 try:
#                     batch = next(function)
#                     table_data = []
#
#                     for idx, row in batch:
#                         row_dict = {'Film #': idx}
#                         row_dict.update({col: val for col, val in zip(column_names, row)})
#                         table_data.append(row_dict)
#
#                     print(tabulate(table_data, headers='keys', tablefmt='fancy_grid'))
#
#
#                     check_leftover = next(function)
#                     generator = itertools.chain([check_leftover], function)
#                     function = generator
#
#                     next_or_exit = input("\n--- Press Enter to see next 10 rows or 0 to quit --- ")
#                     if next_or_exit.strip() == '0':
#                         return None
#
#                 except StopIteration:
#                     print("No more items.")
#                     break
#         else:
#             if isinstance(function, list):
#                 for idx, film_data in function:
#                     print(f"\nMost popular request #{idx}:")
#                     for col, val in zip(column_names, film_data):
#                         print(f"  {col}: {val}")
#             else:
#                 print("Returned result is not a generator or list of rows.")
#
#         return None
#     return wrapper
#
# def existing(kw):
#     """Check if a filter exists in the database."""
#     global connE, cursorE
#     if not check_connection(connE):
#         print("Write database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_e)
#         if new_conn:
#             connE = new_conn
#             cursorE = connE.cursor()
#         else:
#             return False
#     try:
#         cursorE.execute("SELECT 1 FROM filter_counter WHERE filter_text = %s", (kw,))
#         return cursorE.fetchone() is not None
#     except mysql.connector.Error as e:
#         print(f"Error checking filter: {e}")
#         return False
#
# def insert_or_update(kw, search_type):
#     """Insert or update filter count in the database."""
#     global connE, cursorE
#     if not check_connection(connE):
#         print("Write database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_e)
#         if new_conn:
#             connE = new_conn
#             cursorE = connE.cursor()
#         else:
#             return
#     try:
#         if existing(kw):
#             cursorE.execute("UPDATE filter_counter SET filter_count = filter_count + 1 WHERE filter_text = %s", (kw,))
#         else:
#             cursorE.execute('''
#                 INSERT INTO filter_counter (filter_text, filter_type, filter_count)
#                 VALUES (%s, %s, %s)
#                 ON DUPLICATE KEY UPDATE filter_count = filter_count + 1
#             ''', (kw, search_type, 1))
#         connE.commit()
#     except mysql.connector.Error as e:
#         print(f"Error updating filter: {e}")
#         connE.rollback()
#
# def choose_genre():
#     """Prompt user to choose a genre."""
#     global connR, cursorR
#     if not check_connection(connR):
#         print("Read database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_r)
#         if new_conn:
#             connR = new_conn
#             cursorR = connR.cursor()
#         else:
#             return False
#     try:
#         cursorR.execute("SELECT DISTINCT name FROM category")
#         genres_list = [row[0] for row in cursorR.fetchall()]
#     except mysql.connector.Error as e:
#         print(f"Error fetching genres: {e}")
#         return False
#     while True:
#         for num, genre in enumerate(genres_list, start=1):
#             print(f"{num:2}. {genre}")
#         try:
#             index = input("Choose a genre by number (or press Enter to exit to main menu): ")
#             if index == '':
#                 return False
#             index = int(index)
#             if 1 <= index <= len(genres_list):
#                 return genres_list[index - 1]
#             else:
#                 print("Please choose a valid number from the list.\n")
#         except ValueError:
#             print("Please enter a number.\n")
#             continue
#
# def choose_year():
#     """Prompt user to choose a year."""
#     global connR, cursorR
#     if not check_connection(connR):
#         print("Read database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_r)
#         if new_conn:
#             connR = new_conn
#             cursorR = connR.cursor()
#         else:
#             return False
#     try:
#         cursorR.execute("SELECT DISTINCT release_year FROM film")
#         yrs = [row[0] for row in cursorR.fetchall()]
#     except mysql.connector.Error as e:
#         print(f"Error fetching years: {e}")
#         return False
#     while True:
#         try:
#             choice = input("Choose a year (or press Enter to exit to main menu): ").strip()
#             if choice == '':
#                 return False
#             choice = int(choice)
#             if choice in yrs:
#                 return choice
#             else:
#                 print("No movies for the selected year.\n")
#                 return None
#         except ValueError:
#             print("Please enter a number.\n")
#             continue
#
# @beautiful_output
# @calling_next_10
# def search_by_keyword():
#     """Search films by keyword."""
#     global connR, cursorR
#     if not check_connection(connR):
#         print("Read database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_r)
#         if new_conn:
#             connR = new_conn
#             cursorR = connR.cursor()
#         else:
#             return None
#     try:
#         keyword = input('Enter keyword: ').strip()
#         if not keyword:
#             print("The keyword cannot be empty.")
#             return None
#     except Exception as e:
#         print(f"Error with input: {e}")
#         return None
#     try:
#         cursorR.execute("""
#             SELECT title, release_year, length, rating
#             FROM film
#             WHERE LOWER(description) LIKE %s OR LOWER(title) LIKE %s
#         """, ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%'))
#         result = cursorR.fetchall()
#         if not result:
#             print('No results by chosen keyword')
#             return None
#         else:
#             insert_or_update(keyword, 'keyword')
#             return list(enumerate(result, start=1)), cursorR
#     except mysql.connector.Error as e:
#         print(f"Database error: {e}")
#         return None
#
# @beautiful_output
# @calling_next_10
# def search_by_year_and_genre():
#     """Search films by year and genre."""
#     global connR, cursorR
#     if not check_connection(connR):
#         print("Read database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_r)
#         if new_conn:
#             connR = new_conn
#             cursorR = connR.cursor()
#         else:
#             return None
#     genre = choose_genre()
#     if genre:
#         year = choose_year()
#         if genre and year:
#             try:
#                 cursorR.execute("""
#                     SELECT title, ct.name, release_year, length, rating
#                     FROM film AS fl
#                     LEFT JOIN film_category AS fct ON fl.film_id = fct.film_id
#                     LEFT JOIN category AS ct ON fct.category_id = ct.category_id
#                     WHERE fl.release_year = %s AND ct.name = %s
#                 """, (year, genre))
#                 result = cursorR.fetchall()
#                 if not result:
#                     print('No results by chosen year')
#                     return None
#                 else:
#                     insert_or_update(f"{year}, {genre}", "year and genre")
#                     return list(enumerate(result, start=1)), cursorR
#             except mysql.connector.Error as e:
#                 print(f"Database error: {e}")
#                 return None
#         return None
#     return None
#
# @beautiful_output
# @calling_next_10
# def search_by_genre():
#     """Search films by genre."""
#     global connR, cursorR
#     if not check_connection(connR):
#         print("Read database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_r)
#         if new_conn:
#             connR = new_conn
#             cursorR = connR.cursor()
#         else:
#             return None
#     genre = choose_genre()
#     if genre:       # аппендикс так как
#         try:
#             cursorR.execute("""
#                 SELECT fl.title,ct.name, fl.release_year, fl.length, fl.rating
#                 FROM film AS fl
#                 LEFT JOIN film_category AS fct ON fl.film_id = fct.film_id
#                 LEFT JOIN category AS ct ON fct.category_id = ct.category_id
#                 WHERE ct.name = %s
#             """, (genre,))
#             result = cursorR.fetchall()
#             if result is None:
#                 print('No results by chosen genre')
#                 return None
#             else:
#                 insert_or_update(genre, "genre")
#                 return list(enumerate(result, start=1)), cursorR
#
#         except mysql.connector.Error as e:
#             print(f"Database error: {e}")
#             return None
#
#
# @beautiful_output
# @calling_next_10
# def search_by_year():
#     """Search films by year."""
#     global connR, cursorR
#     if not check_connection(connR):
#         print("Read database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_r)
#         if new_conn:
#             connR = new_conn
#             cursorR = connR.cursor()
#         else:
#             return None
#     year = choose_year()
#     if year and year is not None:
#         try:
#             cursorR.execute("""
#                 SELECT fl.title,ct.name, fl.release_year, fl.length, fl.rating
#                 FROM film AS fl
#                 LEFT JOIN film_category AS fct ON fl.film_id = fct.film_id
#                 LEFT JOIN category AS ct ON fct.category_id = ct.category_id
#                 WHERE fl.release_year = %s
#             """, (year,))
#             result = cursorR.fetchall()
#             if result is None:
#                 print('No results by chosen genre')
#                 return None
#             else:
#                 insert_or_update(year, "year")
#                 return list(enumerate(result, start=1)), cursorR
#
#         except mysql.connector.Error as e:
#             print(f"Database error: {e}")
#             return None
#
#
# @beautiful_output
# def show_most_popular_filter():
#     """Show the most popular filter."""
#     global connE, cursorE
#     if not check_connection(connE):
#         print("Write database connection lost. Trying to reconnect...")
#         new_conn = reconnect(db_config_e)
#         if new_conn:
#             connE = new_conn
#             cursorE = connE.cursor()
#         else:
#             return None
#     try:
#         cursorE.execute("""
#             SELECT filter_text, filter_type, filter_count
#             FROM filter_counter
#             WHERE filter_count = (
#                 SELECT MAX(filter_count)
#                 FROM filter_counter
#             )
#         """)
#         return list(enumerate(cursorE.fetchall(), start=1)), cursorE
#     except mysql.connector.Error as e:
#         print(f"Database error: {e}")
#         return None
#
#
# menu = [
#     (1, "Search by Keyword", search_by_keyword),
#     (2, "Search by Year and Genre", search_by_year_and_genre),
#     (3, "Show Most Popular Filter", show_most_popular_filter),
#     (4, "Search by Genre", search_by_genre),
#     (5, "Search by Year", search_by_year),
#     (0, "Exit", None)  # None means no function to call, just exit
# ]
#
# def get_valid_input(prompt: str, valid_options: list) -> int:
#     """Get numeric input from user, ensuring it's a valid menu option."""
#     while True:
#         try:
#             user_input = input(prompt).strip()
#             if not user_input:  # Handle empty input
#                 print("❌ Please enter a number.")
#                 continue
#             choice = int(user_input)
#             if choice in valid_options:
#                 return choice
#             print("❌ Please choose a valid option from the menu.")
#         except ValueError:
#             print("❌ Please enter a number.")
#
# def main():
#     """Run the main menu loop for the film search application."""
#     print("\n🎥 Welcome to the Film Search App! 🎥")
#     print("Choose an option from the menu to search films or view popular filters.")
#
#     while True:
#         print("\n🗒 === Menu === 🗒")
#         for option_num, option_name, _ in menu:
#             print(f"{option_num}. {option_name}")
#
#         valid_options = [item[0] for item in menu]
#         choice = get_valid_input("⤴️ Choose an option: ", valid_options)
#
#         if choice == 0:
#             print("🌸 Thank you for using our application. Goodbye! 🌸")
#             break
#
#         for option_num, _, func in menu:            # find the function for the chosen option
#             if option_num == choice and func is not None:
#                 result = func()
#                 if result is None:
#                     print("🔙 Returning to main menu...")
#                 break
#
# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n🌸 Application terminated by user. Goodbye! 🌸")
#     finally:
#         if connR.is_connected():
#             connR.close()
#         if connE.is_connected():
#             connE.close()
#         print("Database connections closed")