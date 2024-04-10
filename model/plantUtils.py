from statistics import mean, stdev
import math

# ПО контроль позиционных ограничений
def pos_control(a, b):
    def f(x):
        if a <= x <= b:
            return [x, True]
        else:
            return [x, False]
    return f


# КС - контроль стабильности величины X в кадре
def const_control(x):
    if max(x) == min(x):
        return [x, True]
    else:
        return [x, False]


# НИ - нормирование измерений
def normalize_measure(b1, b2):
    def f(x):
        return [(x - b1)/b2, True]
    return f


# РФ - расчет заданной функции от измеренных значений F(X1,X2,...).
def get_new_x(x):
    return [abs(x-20)**0.5 + 35, True]

def get_rf(x):
    return [abs(x-20)**0.5 + 35, True]


# СД - расчет среднего значения и оценки дисперсии по повторным измерениям
def get_std(x):
    return [stdev(x), True]


def get_mean(x):
    return [mean(x), True]


channels = {
    1: "",
    2: normalize_measure(770, 20),
    3: "",
    4: pos_control(0, 1),
    6: [get_mean, 4],
    7: [const_control, 2],
    14: "",
    44: "",
    54: get_rf,
    65: normalize_measure(100, 300),
    74: [const_control, 3]
}

def get_data_from_model(plant, channels_list = channels):
    def f():
        measures = []
        errors = []
        for channel, prop in channels_list.items():
            measure = plant.measure(channel)
            if callable(prop):
                result = prop(measure)
                if result[1]:
                    measure = result[0]
                else:
                    # Проброс сообщения об ошибке
                    errors.append('Измерение с канала ' + str(channel) + ' выходит из интервала позиционных ограничений')

            if type(prop) == list:
                added_measures = plant.get_measures_from_channel(channel, prop[1]-1)
                added_measures.append(measure)
                result = prop[0](added_measures)

                if channel == 7 or channel == 74:
                    if not result[1]:
                        # Сброс опроса
                        print(result, channel)
                        return []

                if channel == 5:
                    measure = result[0]
                    measures.append(measure)
                    added_measures = plant.get_measures_from_channel(channel, 5)
                    added_measures.append(measure)
                    result = get_std(added_measures)
                    measure = result[0]

            if not (channel == 7 or channel == 74):
                measures.append(measure)

        return measures, errors
    return f



#channels = {
#    1: pos_control(-35, 30),
#    2: pos_control(740, 765),
#    3: pos_control(50, 100),
#    4: pos_control(0, 1),
#    5: [get_mean, 4],
#    6: '',
#    8: [const_control, 3],
#    18: '',
#    47: '',
#    55: get_new_x,
#    83: [const_control, 3]
#}

# channels = {
#     1: "",
#     2: "",
#     3: "",
#     4: pos_control(0, 1),
#     6: normalize_measure(0.5, 0.5),
#     7: [const_control, 3],
#     17: [get_mean, 10],
#     47: "",
#     57: get_rf,
#     75: [const_control, 2],
#     93: pos_control(0, 30)
# }

