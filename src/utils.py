import re

def to_snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def count_percentage(x, y, data):
    return data \
        .groupby(x)[y] \
        .value_counts(normalize=True) \
        .mul(100) \
        .rename('percent') \
        .reset_index()
