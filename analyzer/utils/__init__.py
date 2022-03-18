import datetime


def merge_dicts(dict1, dict2):
    """
    Merge dict 2 into dict 1
    Note: dict1 is overridden
    :return: merged dict 1
    """
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    for k, v in dict2.items():
        if k in dict1:
            if isinstance(dict1[k], list):
                dict1[k].extend(v)
            elif isinstance(dict1[k], dict):
                dict1[k] = merge_dicts(dict1[k], v)
        else:
            dict1[k] = v
    return dict1


def format_date(date):
    if not date:
        return datetime.datetime(1, 1, 1)
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')


def format_date_str(date: datetime.date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')
