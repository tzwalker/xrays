def build_dict(samp_dictionary, key, item_or_items):
    samp_dictionary.setdefault(key, item_or_items)
    samp_dictionary[key] = item_or_items
    return