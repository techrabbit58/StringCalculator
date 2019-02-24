"""Test the simple string calculator class."""

import random
from typing import List

import pytest

import simple


@pytest.fixture
def sc():
    return simple.StringCalculator()


# --- requirement 1 -----------------------------------------------

def test_add_method_gives_0_on_empty_string(sc):
    assert 0 == sc.add('')


def test_add_accepts_one_number_in_expression(sc):
    assert 1 == sc.add('1')


def test_add_accepts_two_numbers_in_expression(sc):
    assert 3 == sc.add('1,2')


# --- requirement 2 -----------------------------------------------

def test_add_handles_many_positive_numbers_correctly(sc):
    numbers: List[int] = [
        random.randint(1, 100)
        for _ in range(random.randint(3, 100))
    ]
    result: int = sum(numbers)
    expression: str = ','.join(str(n) for n in numbers)
    assert result == sc.add(expression)


# --- requirement 3 -----------------------------------------------

def test_add_accepts_newline_and_comma_as_separators(sc):
    assert 6 == sc.add('1\n2,3')


def test_add_does_not_allow_repeated_separators(sc):
    with pytest.raises(ValueError):
        assert 1 == sc.add('\n,1')


# --- requirement 4 -----------------------------------------------

def test_add_accepts_a_prefix_to_set_arbitrary_delimiters(sc):
    assert 3 == sc.add('//;\n1;2')
    assert 10 == sc.add('//. <\n1.2 3<4')
    assert 15 == sc.add('1,2,3,4,5')


# --- requirement 5 -----------------------------------------------

def test_negatives_not_allowed_throw_exception(sc):
    with pytest.raises(ValueError):
        assert 7 == sc.add('-1,3,5')


def test_add_exception_on_negatives_must_show_negatives_list(sc):
    with pytest.raises(ValueError) as ex:
        sc.add('2,-2,1,-1')
        assert '[-1, -2]' in ex.value


# --- requirement 6 -----------------------------------------------

def test_add_accepts_numbers_up_to_1000(sc):
    assert 1002 == sc.add('1000,2')


def test_add_ignores_numbers_bigger_than_1000(sc):
    assert 2 == sc.add('1001,2')


# --- requirement 7 -----------------------------------------------

def test_add_accepts_bracketed_prefixes_for_multichar_delimiters(sc):
    assert 6 == sc.add('//[***]\n1***2***3')


# --- requirement 8 -----------------------------------------------

def test_add_accepts_multiple_bracketed_singlechar_delimiters(sc):
    assert 6 == sc.add('//[*][%]\n1*2%3')


# --- requirement 9 -----------------------------------------------

def test_add_accepts_multiple_bracketed_multichar_delimiters(sc):
    assert 10 == sc.add('//[*][%%][...]\n1*2%%3...4')

# last line of code
