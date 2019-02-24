"""Implement the base class of a simple string calculator.

The string calculator adds whole positive numbers in the range
0 ... 1000 from an input string. The numbers shall be separated
by a set of separators. The set of separators can be configured
by a special string calculator prefix in the input string.

Numbers greater than 1000 are simply ignored and do not contribute
to the string calculator result. Negative numbers lead to a value
error.

For a detailed description of the kata, and for instructions to
develop it by TDD, please refer to:

    http://osherove.com/tdd-kata-1/

"""
import re
from typing import List, Tuple


def is_empty(text: str) -> bool:
    return text.isspace() or 0 == len(text)


def insure_positive_numbers(numbers: int) -> None:
    negative_numbers = [n for n in numbers if n < 0]
    if len(negative_numbers) > 0:
        raise ValueError('negatives not allowed: {}'.format(str(negative_numbers)))


def parse_expression_to_numbers(expression: str, delimiter_table: List[str]) -> List[int]:
    table = [re.escape(s) for s in delimiter_table]
    parts = re.compile('(?:' + '|'.join(table) + ')').split(expression)
    if '' in parts:
        raise ValueError('consecutive separators in expression')
    return [int(n) for n in parts]


class StringCalculator:
    """This creates a simple string calculator that can add numbers from a string."""

    newline: str = '\n'
    default_delimiters: List[str] = [',', newline]
    max_value: int = 1000

    def add(self, expression: str) -> int:
        """Method 'add':

        Add up all numbers in the expression string.
        :type expression: str
        """
        if is_empty(expression):
            return 0
        expression, delimiter_table = self.extract_delimiters(expression)
        numbers = parse_expression_to_numbers(expression, delimiter_table)
        insure_positive_numbers(numbers)
        return sum(n for n in numbers if n <= self.max_value)

    def extract_delimiters(self, expression: str) -> Tuple[str, List[str]]:
        """Take an expression, check if it is preceded by a custom delimiter specification.
        If so, parse this delimiter specification and create a custom delimiter table from
        it.

        Custom delimiter specifications can be of one of to forms:

            //[<delimiter_string>][<delimiter_string>]...\n
            //<singechar_delimiter><singlechar_delimiter>...\n

        returns a tuple:

            <expression_without_prefix>, <delimiter_table_to_use_for_this_run>

        where

            <expression...> is the original expression, if no custom delimiters,
                or the tail of the original expression, if the expression had a custom
                delimiter specificatin as its prefix

            <delimiter_table...> is a list of strings, where each string in the list
                represents a valid delimiter, be it from the delimiter default, or from
                the delimiter specification prefix of the expresssion, if any. The newline
                character is always in the table.

        """
        if expression.startswith('//'):
            delimiters, _, expression = expression[2:].partition(self.newline)
            if delimiters.startswith('[') and delimiters.endswith(']'):
                delimiter_table = re.compile(r'(?:\]\[)').split(delimiters[1:-1])
            else:
                delimiter_table = list(delimiters)
            delimiter_table.append(self.newline)
        else:
            delimiter_table = self.default_delimiters
        return expression, delimiter_table

# last line of code
