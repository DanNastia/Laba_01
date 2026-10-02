import sys

from toolkit.errors import toolkit_Error
from toolkit.calculator import tokenization, validation, polik_notation, calculation
from toolkit.convecter import convector

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


def main():
#отделяем аргументы командной строки без имени самой строки
    args = sys.argv[1:]

#Проверка отсутствиz аргументов
    if not args or '--help' in args:
        print_help()
        sys.exit(0)

    command = args[0]

    try:

        if command == 'calc':
            if len(args) < 2:
                raise toolkit_Error(f"Было переданно пустое выражение")

            expression = args[1]
            result = action_calc(expression)

            print(result)
            sys.exit(0)


        elif command == 'convert':

            if len(args) < 6 or args[2] != '--from' or args[4] != '--to':
                raise toolkit_Error("Неверный формат ввода команды. Должен быть: convert VALUE --from UNIT --to UNIT")

            value = args[1]
            input_unit = args[3]
            output_unit = args[5]


            result = convector(value, input_unit, output_unit)

            print(result)
            sys.exit(0)

        else:
            raise toolkit_Error(f"Была полученна неизвестная команда: {command}")

    except toolkit_Error as auexpected:

        sys.stderr.write(f"Ошибка: {str(auexpected)}\n")
        sys.exit(2)



if __name__ == '__main__':
    main()