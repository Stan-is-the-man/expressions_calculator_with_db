import re
import time
import psycopg2


def factorial(any_integer):
    the_result = 1
    for num in range(1, any_integer + 1):
        the_result *= num
    return the_result


def calculate_execution_time_in_milliseconds(func, *args):
    start_time = time.perf_counter()
    func(*args)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return execution_time


def data_to_db(the_operands, the_result, the_total_time, the_operators):
    connection = psycopg2.connect(
        host='localhost',
        database='expressions_calculator_with_db',
        user='postgres',
        password='1123QwER'
    )
    cursor_object = connection.cursor()
    cursor_object.execute(
        """CREATE TABLE IF NOT EXISTS calculator_statistics (
        operands VARCHAR(200),
        results FLOAT,
        execution_time FLOAT,
        operators VARCHAR(100)
    )"""
    )

    cursor_object.execute(
        """INSERT INTO calculator_statistics(operands, results, execution_time,operators)
        VALUES(%s, %s, %s, %s)
    """, (the_operands, the_result, the_total_time, the_operators))
    connection.commit()


def symbol_count(the_expression):
    count = 0
    for char in the_expression:
        if not char.isspace():
            count += 1
    if count <= 128:
        return True


while True:
    expression = input("Enter a mathematical expression to be calculated or '!' for factorial. "
                       "Type 'exit' to quit:\n")
    if expression == 'exit':
        break
    if expression == "!":
        try:
            the_number = int(input("Please enter just ONE INTEGER number:\n"))
            res = factorial(the_number)
            exec_time = calculate_execution_time_in_milliseconds(factorial, the_number)
            data_to_db(the_number, res, exec_time, expression)
            print(res)
        except ValueError:
            print("The entered number should be an integer !!!\n")

    else:
        try:
            result = eval(expression)
            if symbol_count(expression):
                exec_time = calculate_execution_time_in_milliseconds(eval, expression)
                all_operands = ', '.join(re.findall(r'\d+(?:\.\d+)?', expression))
                all_operators = ', '.join(re.findall(r'[+\-*/^%]+', expression))
                data_to_db(all_operands, result, exec_time, all_operators)

                print(result)
            else:
                print('Up to 128 symbols accepted, please try again')

        except Exception as e:
            print(f"Error in {e}\n")
