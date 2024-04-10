from model.plant import Plant
from model.plantUtils import get_data_from_model
from bdUtils import signAndLog, addDataToDB

plant = Plant('model\plant.dll')

conf = {
    "№ Кадра": "cad_num",
    "Канал 1": "ch_1",
    "Канал 2": "ch_2",
    "Канал 3": "ch_3",
    "Канал 4": "ch_4",
    "Канал 6 сред.": "ch6_mean",
    "Канал 6 дисп.": "ch6_disp",
    "Канал 14": "ch_14",
    "Канал 44": "ch_44",
    "Канал 54": "ch_54",
    "Канал 65": "ch_65",
}
def get_data():
    get_data = get_data_from_model(plant)
    result, errors = get_data()
    return {
        'result':result,
        'errors':errors,
        }
