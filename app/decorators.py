import types
import functools
import itertools
from tabulate import tabulate

def calling_next_10(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            rows, cursor = result
            step = 10

            def generator():
                for i in range(0, len(rows), step):
                    yield rows[i:i + step]
            return generator(), cursor
    return wrapper


def beautiful_output(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return None

        function, cursor = result
        if cursor is None:
            return None

        column_names = [desc[0] for desc in cursor.description]

        if isinstance(function, types.GeneratorType):
            while True:
                try:
                    batch = next(function)
                    table_data = []

                    for idx, row in batch:
                        row_dict = {'Film #': idx}
                        row_dict.update({col: val for col, val in zip(column_names, row)})
                        table_data.append(row_dict)

                    print(tabulate(table_data, headers='keys', tablefmt='fancy_grid'))


                    check_leftover = next(function)
                    generator = itertools.chain([check_leftover], function)
                    function = generator

                    next_or_exit = input("\n--- Press Enter to see next 10 rows or 0 to quit --- ")
                    if next_or_exit.strip() == '0':
                        return None

                except StopIteration:
                    print("No more items.")
                    break
        else:
            if isinstance(function, list):
                for idx, film_data in function:
                    print(f"\nMost popular request #{idx}:")
                    for col, val in zip(column_names, film_data):
                        print(f"  {col}: {val}")
            else:
                print("Returned result is not a generator or list of rows.")

        return None
    return wrapper