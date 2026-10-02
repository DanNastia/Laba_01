from .errors import convector_Error

measurements = {
    'lenghts':{'mm' : 0.001, 'cm' : 0.01,'m' : 1.0,'km' : 1000.0},

    'weights': {'g' : 1.0, 'kg' : 1000.0},

    'temputure': {'c','k','f'}
}


def convector(value, input_unit, output_unit):
    input_unit = input_unit.lower() #приведение всех единиц измерения к нижнему регистру для упрощения далнейшего алгоритма
    output_unit = output_unit.lower()

    try: #проверка входящих числовых значений
        value = float(value)
    except (ValueError, TypeError):
        raise convector_Error(f"Недопустимое числовое значение: '{value}'")

#инициализация категорий
    input_category = None
    output_category = None

#определяем категорию единиц измерения
    if input_unit in measurements['lenghts']:
        input_category = 'lenghts'
    elif input_unit in measurements['weights']:
        input_category = 'weights'
    elif input_unit in measurements['temputure']:
        input_category = 'temputure'

    if output_unit in measurements['lenghts']:
        output_category = 'lenghts'
    elif output_unit in measurements['weights']:
        output_category = 'weights'
    elif output_unit in measurements['temputure']:
        output_category = 'temputure'


# проверка полученной категории измерения
    if input_category is None or output_category is None:
        raise convector_Error(f"Недопустимая единица измерения")

    if input_category != output_category:
        raise convector_Error(f"Невозможно конвертировать разные категории единиц измерения")


# начало работы конвертации из один единиц измерения в другие

# конвертация для длинн
    if input_category == 'lenghts':
        base_value = measurements[input_category][input_unit]
        expected_value = measurements[output_category][output_unit]
        return float(value * base_value / expected_value)

#конвертация для веса
    if input_category == 'weights':
            base_value = measurements[input_category][input_unit]
            expected_value = measurements[output_category][output_unit]
            return float(value * base_value / expected_value)

    if input_category == 'temputure':

#проверка на совпадение величин(то есть конверсия не должна происходить)
        if input_unit == output_unit:
            return float(value)


#перевод для цельсия и проверка для абсолютного нуля
        if input_unit == 'c':
            if value >= -273:
                if output_unit == 'k':
                    return float(value + 273)
                elif output_unit == 'f':
                    return float(value * 1.8 + 32)
            else:
                raise convector_Error(f"Температура в цельсиях ниже абсолютного нуля")

#перевод для кельвинов и проверка для абсолютного нуля
        if input_unit == 'k':
            if value >= 0:
                if output_unit == 'c':
                    return float(value - 273)
                elif output_unit == 'f':
                    return float((value - 273) * 1.8 + 32)
            else:
                raise convector_Error(f"Температура в кельвинах ниже абсолютного нуля")

#перевод для фаренгейта и проверка для абсолютного нуля
        if input_unit == 'f':
            if value >= -460:
                if output_unit == 'c':
                    return float((value - 32) / 1.8)
                elif output_unit == 'k':
                    return float((value - 32) / 1.8 + 273)
            else:
                raise convector_Error(f"Температура в фаренгейтах ниже абсолютного нуля")
