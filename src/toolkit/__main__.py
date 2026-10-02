import sys

from toolkit.errors import toolkit_Error
from toolkit.calculator import tokenization, validation, polik_notation, calculation
from toolkit.convecter import convector

# функция вывода поддержки
def print_help():

    help_information = (
        "Лабораторная работа 01"
        "Возможные команды:\n"
        "  python -m toolkit calc \"EXPRESSION\""
        "  python -m toolkit convert VALUE --from UNIT --to UNIT"
        "  python -m toolkit --help"
    )
    print(help_information)


def action_calc(expression: str):

    input_tokens = tokenization(expression)

    validation(input_tokens)

    polik_tokens = polik_notation(input_tokens)

    result_stack = calculation(polik_tokens)

    return result_stack

# основная функция кода
def main():

# отделяем операнды и числа из командной строки
    arguments = sys.argv[1:]

# Проверка отсутствия аргументов
    if not arguments or '--help' in arguments:
        print_help()
        sys.exit(0)

    command = arguments[0]

    try:
        #блок калькулятора
        if command == 'calc':
            if len(arguments) < 2:
                raise toolkit_Error(f"Было переданно пустое выражение")

            expression = arguments[1]
            result = action_calc(expression)

            print(result)
            sys.exit(0)

        #блок конвертора
        elif command == 'convert':
            #проверка на то, что для корректной работы команды потребуется минимум 6 операндов и чисел
            if len(arguments) < 6 or arguments[2] != '--from' or arguments[4] != '--to':
                raise toolkit_Error(f"Неверный формат ввода команды")

            value = arguments[1]
            input_unit = arguments[3]
            output_unit = arguments[5]


            result = convector(value, input_unit, output_unit)

            print(result)
            sys.exit(0)

        else:
            raise toolkit_Error(f"Была полученна неизвестная команда: {command}")

    except toolkit_Error as anexpected:

        sys.stderr.write(f"Ошибка: {str(anexpected)}\n")
        sys.exit(2)



if __name__ == '__main__':
    main()