from .errors import divide_by_Zero_Error, validation_Error, toolkit_Error


def tokenization(expression: str):
    tokens = [] # хранилище чисел и операндов
    current_char_in_string = 0 # текущий символ строки
    length_of_the_expression = len(expression)

    while current_char_in_string < length_of_the_expression:
        char = expression[current_char_in_string]

        if char == ' ':
            current_char_in_string += 1
            continue

        if char.isdigit() or char == '.':
                number_str = ""
                # Собираем все цифры и точки, которые идут подряд
                while current_char_in_string < length_of_the_expression and (expression[current_char_in_string].isdigit() or expression[current_char_in_string] == '.'):
                    number_str += expression[current_char_in_string]
                    current_char_in_string += 1
                tokens.append(number_str)
                continue

# отдельно сохраняем все операции и скобочк
        if char in '+-*/()':
            tokens.append(char)
            current_char_in_string += 1
            continue


        raise toolkit_Error(f"Недопустимый символ в выражении: {char}")

    return tokens # возращаем обработаную строку



# функция должна принимать в работу результат выполнения программы tokenization
def validation(tokens: list):

    if not tokens:
        raise validation_Error(f"Выражение не может быть пустым")

    binared_operators = ['+', '-', '*', '/'] # поддерживаемые операторы для счёта
    number_of_brackets = 0

    for i in range(len(tokens)):
        current_char = tokens[i]

        if current_char == '(':
            number_of_brackets += 1
    # проверка на пустоту скобок
            if i + 1 < len(tokens) and tokens[i+1] == ')':
                raise validation_Error(f"Обнаружены пустые скобки")

        elif current_char == ')':
            number_of_brackets -= 1
    #проверка на количество скобок
            if number_of_brackets < 0:
                raise validation_Error(f"Закрывающая скобка идет раньше открывающей скобки")

        if current_char in binared_operators:

    # проверка на то унарный + и - или нет
                    unary_operands = (current_char in ['+', '-']) and (i == 0 or tokens[i-1] in binared_operators or tokens[i-1] == '(')

    # обработка унарных знаков
                    if unary_operands:

                        if i == len(tokens) - 1:
                            raise validation_Error(f"Выражение не может заканчиваться унарным знаком")

                        if tokens[i+1] == ')':
                            raise validation_Error(f"Знак операции не может стоять перед закрывающей скобкой")

                        if tokens[i+1] in binared_operators:
                            raise validation_Error(f"Есть ошибка:или пропущен операнд или два оператора подряд")
                        continue


    # обработка оставшихся операндов
                    if i == 0 and current_char in ['*', '/']:
                        raise validation_Error(f"Выражение не может начинаться с умножения или деления")

                    # проверка на нахождение опранда в конце строки
                    if i == len(tokens) - 1:
                        raise validation_Error(f"Выражение не может заканчиваться знаком операции")

                    next_char = tokens[i+1]

                    if next_char in binared_operators:
                            raise validation_Error(f"Два знака операции не могут стоять рядом")


                    if next_char == ')':
                        raise validation_Error(f"Знак операции не может стоять перед закрывающей скобкой")

                    if i > 0 and tokens[i-1] == '(':
                        if current_char in ['*', '/']:
                            raise validation_Error(f"Пропущен операнд перед бинарным оператором")

    if number_of_brackets != 0:
        raise validation_Error(f"В выражени есть незакрытые скобки")

    return True



# функция перевода выражения в обратнуюю польскую нотацию
def polik_notation(tokens):

    priorities = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_string = []  # Список для консольной строки
    stack = []  # Стек для хранения операторов
    possible_unary__tokens = []

    for i in range(len(tokens)):
        token = tokens[i]

        if token in ['+', '-']:
            unary_check = (i == 0 or tokens[i-1] == '(')
            if unary_check:
                possible_unary__tokens.append('0')
        possible_unary__tokens.append(token)


    for token in possible_unary__tokens:
# проверка на то символ - число или операнд
        if token not in priorities and token not in ['(',')']:
            output_string.append(float(token))

#обработка скобочек
        elif token == '(':
            stack.append(token)
        elif token == ')':
        #пока не встретили закрывающуюся скобку, выталкиваем все из стэка
            while stack and stack[-1] != '(':
                output_string.append(stack.pop())

            stack.pop()# удаляем саму открывающую скобку из стэка

# основной алгоритм обратной польской нотации
        elif token in priorities:
            while (stack and stack[-1] in priorities and priorities[stack[-1]] >= priorities[token]):
                output_string.append(stack.pop())

            # Кладем текущий оператор в стек
            stack.append(token)

    # когда токены закончились, выталкиваем все оставшиеся операторы из стека в очередь
    while stack:
        output_string.append(stack.pop())

    return output_string



# основная программа калькулятора
def calculation(polik_tokens):

    stack = []

    for token in polik_tokens:
    # если число, то кладываем в стэк
        if type(token) is float:
            stack.append(token)

        elif token in '+-*/':

    # из стека первым достается правый операнд, а вторым — левый (сверху вниз как тарелочки)
            right_num = stack.pop()
            left_num = stack.pop()


            if token == '+':
                result_of_calc = left_num + right_num
            elif token == '-':
                result_of_calc = left_num - right_num
            elif token == '*':
                result_of_calc = left_num * right_num
            elif token == '/':

                if right_num == 0.0:
                    raise divide_by_Zero_Error(f"Деление на ноль запрещено")
                result_of_calc = left_num / right_num

    # возращаем вычисленное значение в стэк
            stack.append(result_of_calc)

    return stack[0]
