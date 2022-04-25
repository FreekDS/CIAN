import datetime

from analyzer.utils import format_date_str, format_date, merge_dicts


def test_format_date():
    assert format_date(None) == datetime.datetime(1, 1, 1)
    assert format_date("2022-10-05T21:14:17Z") == datetime.datetime(2022, 10, 5, 21, 14, 17)


def test_format_date_str():
    assert "2022-10-05T21:14:17Z" == format_date_str(datetime.datetime(2022, 10, 5, 21, 14, 17))


def test_merge_dicts_list():
    l1 = [1, 2, 3]
    l2 = [4, 5]

    assert merge_dicts(l1, l2) == [1, 2, 3, 4, 5]

    l3 = ['a']
    l4 = ['b', 3]

    assert merge_dicts(l3, l4) == ['a', 'b', 3]
    assert merge_dicts(['a', 'b'], []) == ['a', 'b']


def test_merge_dicts():
    d1 = {
        'not_in_d2': 'some_value',
        'in_both': True,
        'list_in_both': [
            1, 2, 3
        ],
        'dict_in_both': {
            'also_in_d2': 'ha',
            'not_in_d2': 'jep',
            'list': ['a', 'b'],
            'dicte': {
                'more_nesting': False
            }
        }
    }

    d2 = {
        'not_in_d1': 'value',
        'in_both': False,
        'list_in_both': [8, 9, 10],
        'dict_in_both': {
            'also_in_d2': 'ho',
            'not_in_d1': 'jop',
            'list': ['c', 'd'],
            'dicte': {
                'more_nesting': True,
                'a': 'a'
            }
        }
    }

    merged = merge_dicts(d1, d2)

    assert merged.get('not_in_d1') == 'value'
    assert merged.get('not_in_d2') == 'some_value'
    assert merged.get('in_both') is False
    assert merged.get('list_in_both') == [1, 2, 3, 8, 9, 10]
    assert merged.get('dict_in_both', {}).get('also_in_d2') == 'ho'
    assert merged.get('dict_in_both', {}).get('not_in_d2') == 'jep'
    assert merged.get('dict_in_both', {}).get('not_in_d1') == 'jop'
    assert merged.get('dict_in_both', {}).get('list') == ['a','b','c','d']
    assert merged.get('dict_in_both', {}).get('dicte', {}).get('more_nesting') is True
    assert merged.get('dict_in_both', {}).get('dicte', {}).get('a') == 'a'
