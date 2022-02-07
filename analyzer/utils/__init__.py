def merge_dicts(dict1, dict2):
    """
    Merge dict 2 into dict 1
    Note: dict1 is overridden
    :return: merged dict 1
    """
    for k, v in dict2.items():
        if k in dict1:
            if isinstance(dict1[k], list):
                dict1[k].extend(v)
            elif isinstance(dict1[k], dict):
                dict1[k] = merge_dicts(dict1[k], v)
        else:
            dict1[k] = v
    return dict1

