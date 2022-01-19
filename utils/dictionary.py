from itertools import *


def group(iterable, key, value=lambda x: x):
    return dict((k, list(map(value, values))) for k, values in groupby(sorted(iterable, key=key), key))
