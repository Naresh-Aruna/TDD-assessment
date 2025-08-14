import pytest

from string_calculator.calculator import StringCalculator


def test_empty_string_returns_zero():
    sc = StringCalculator()
    assert sc.add("") == 0


def test_single_number_returns_value():
    sc = StringCalculator()
    assert sc.add("7") == 7


def test_two_numbers_sum():
    sc = StringCalculator()
    assert sc.add("1,2") == 3


def test_many_numbers_sum():
    sc = StringCalculator()
    assert sc.add("1,2,3,4,5") == 15


def test_newlines_between_numbers():
    sc = StringCalculator()
    assert sc.add("1\n2,3") == 6


def test_custom_single_char_delimiter():
    sc = StringCalculator()
    assert sc.add("//;\n1;2;3") == 6


def test_negatives_raise_with_all_listed():
    sc = StringCalculator()
    with pytest.raises(ValueError) as e:
        sc.add("1,-2,3,-4")
    assert "negatives not allowed" in str(e.value)
    # The message should contain both negatives
    assert "-2" in str(e.value) and "-4" in str(e.value)


def test_get_called_count_tracks_invocations():
    sc = StringCalculator()
    assert sc.get_called_count() == 0
    sc.add("1,2")
    sc.add("3")
    assert sc.get_called_count() == 2


def test_event_fires_after_add():
    sc = StringCalculator()
    seen = []

    def listener(inp, result):
        seen.append((inp, result))

    sc.add_listener(listener)
    total = sc.add("4,6")
    assert total == 10
    assert seen == [("4,6", 10)]


def test_ignore_numbers_greater_than_1000():
    sc = StringCalculator()
    assert sc.add("2,1001") == 2
    assert sc.add("1000,1") == 1001


def test_any_length_delimiter():
    sc = StringCalculator()
    assert sc.add("//[***]\n1***2***3") == 6


def test_multiple_delimiters():
    sc = StringCalculator()
    assert sc.add("//[*][%]\n1*2%3") == 6


def test_multiple_long_delimiters():
    sc = StringCalculator()
    assert sc.add("//[**][%%]\n1**2%%3") == 6
