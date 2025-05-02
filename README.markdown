# Film Search Application

## Overview
The Film Search Application is a Python-based command-line tool that allows users to search for films in a MySQL database (using the Sakila sample database) based on various criteria such as keywords, genres, years, or a combination of year and genre. It also tracks the popularity of search filters and displays the most frequently used ones. The application features a user-friendly menu, paginated search results, and a tabulated output for better readability.

## Features
- **Search by Keyword**: Find films by entering a keyword that matches the film's title or description.
- **Search by Genre**: Filter films by selecting a genre from a list.
- **Search by Year**: Retrieve films released in a specific year.
- **Search by Year and Genre**: Combine year and genre for more precise filtering.
- **Most Popular Filter**: View the most frequently used search filter.
- **Paginated Results**: Display search results in batches of 10 films, with the option to continue or exit.
- **Tabulated Output**: Present results in a clean, formatted table using the `tabulate` library.
- **Database Connection Management**: Handles read and write connections to MySQL databases with reconnection logic.

## Prerequisites
- Python 3.8 or higher
- MySQL Server with the Sakila sample database installed
- A secondary MySQL database (`Trotskaya_111124`) for storing filter counts
- Environment variables configured in a `.env` file

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/film-search-app.git
   cd film-search-app
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root with the following structure:
   ```env
   host_r=your_read_host
   user_r=your_read_user
   password_r=your_read_password
   host_e=your_write_host
   user_e=your_write_user
   password_e=your_write_password
   ```
   Replace `your_read_host`, `your_read_user`, etc., with the appropriate MySQL connection details.

5. **Set Up Databases**:
   - Ensure the Sakila database is available for read operations.
   - Create a table in the `Trotskaya_111124` database for storing filter counts:
     ```sql
     CREATE TABLE filter_counter (
         filter_text VARCHAR(255) PRIMARY KEY,
         filter_type VARCHAR(50),
         filter_count INT DEFAULT 1
     );
     ```

## Usage
1. Run the application:
   ```bash
   python main.py
   ```

2. Follow the interactive menu to:
   - Select a search option (e.g., Search by Keyword, Search by Genre).
   - Enter required inputs (e.g., keyword, year, or genre).
   - View results in a tabulated format.
   - Navigate paginated results by pressing Enter or exit by typing `0`.

3. To exit the application, select `0` from the main menu.

## Project Structure
- `main.py`: Entry point of the application, handles the main menu loop.
- `dbconfig.py`: Manages MySQL database connections and reconnection logic.
- `queries_and_prompts.py`: Contains search functions and helper methods for user input.
- `decorators.py`: Provides decorators for paginating results and formatting output.
- `requirements.txt`: Lists project dependencies.
- `.env`: Stores environment variables (not included in the repository).

## Dependencies
- `mysql-connector-python~=9.2.0`: For MySQL database connectivity.
- `python-dotenv==1.1.0`: For loading environment variables from `.env`.
- `tabulate~=0.9.0`: For formatting search results in a table.

## Notes
- The application uses two database connections: one for reading from the Sakila database and another for writing filter counts to the `Trotskaya_111124` database.
- Ensure both databases are accessible and properly configured before running the application.
- The Sakila database must include the `film`, `film_category`, and `category` tables.
- Error handling is implemented for database connections, user input, and query execution.

## License

This project is licensed under the MIT License. See the LICENSE file for details.




