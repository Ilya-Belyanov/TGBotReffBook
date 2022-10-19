from data.keyspace import Separators


def parseForData(data: str, index: int = 1, sep: str = Separators.KEY_DATA):
    data_list = data.split(sep)
    if len(data_list) > index:
        return data_list[index]
    else:
        return data
