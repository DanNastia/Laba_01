import sys
import pytest

from toolkit.calculator import tokenization, validation, polik_notation, calculation
from toolkit.convecter import convector
from toolkit.errors import validation_Error, divide_by_Zero_Error, convector_Error
from toolkit.__main__ import main

# положительные тесты
def test_calc_1():

    tokens = tokenization("2 + 3 * 4")
    assert tokens == ['2', '+', '3', '*', '4']
    assert validation(tokens) is True
    polik = polik_notation(tokens)
    assert polik == [2.0, 3.0, 4.0, '*', '+']
    assert calculation(polik) == 14.0

def test_calc_2():

    tokens = tokenization("2.5 + 1.25")
    assert tokens == ['2.5', '+', '1.25']
    assert validation(tokens) is True
    polik = polik_notation(tokens)
    assert polik == [2.5, 1.25, '+']
    assert calculation(polik) == 3.75

def test_calc_3():

    tokens = tokenization("-5 + 3")
    assert validation(tokens) is True
    polik = polik_notation(tokens)
    assert calculation(polik) == -2.0

def test_convert_4():

    assert convector("1.5", "m", "mm") == 1500.0

def test_convert_5():

    assert convector("500", "g", "kg") == 0.5


def test_cli_6(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["toolkit", "--help"])
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 0
    captured = capsys.readouterr()
    assert "Лабораторная работа 01" in captured.out


# негативные тесты
def test_calc_7():

    tokens = tokenization("")
    with pytest.raises(validation_Error):
        validation(tokens)

def test_calc_8():

    tokens = tokenization("2 ) + ( 3")
    with pytest.raises(validation_Error):
        validation(tokens)

def test_calc_9():

    tokens = tokenization("5 + * 2")
    with pytest.raises(validation_Error):
        validation(tokens)

def test_calc_10():

    tokens = tokenization("10 / 0")
    polik = polik_notation(tokens)
    with pytest.raises(divide_by_Zero_Error):
        calculation(polik)

def test_convert_11():

    with pytest.raises(convector_Error):
        convector("10", "m", "g")


def test_cli_12(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["toolkit", "calc"])
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert "Ошибка:" in captured.err