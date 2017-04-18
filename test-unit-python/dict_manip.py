"""Collections of function(s) to manipulate dictionary. Usually used to deal with
value returned from RethinkDB query
"""

def sort_dict_list(_list:list, _column_target:str, _ascending:bool=True):
    """PENDING: This function is not yet unit tested!"""

    if _ascending:
        l = sorted(_list, key=lambda k : k[_column_target])
    else:
        l = sorted(_list, key=lambda k : k[_column_target], reverse=True)

    return l



def take_a_dict_from_dict_list(_list:list, _column_target:str,
    _ascending:bool=True):
    """PENDING: This function is not yet unit tested!"""

    try:
        return sort_dict_list(_list, _column_target, _ascending)[0]
    except IndexError:
        return []



def take_a_value_from_dict_list(_list:list, _column_target:str,
    _ascending:bool=True):
    """Function to take a value from dictionaries in a list. The value can
    be the first or the least in alphabetical order.

    For example there are these two dictionaries/documents in a list,
    `test_list = [{ "name":"name_1" }, document_2 = { "name":"name_2" }`.

    `take_a_value_from_dict_list(test_list, "name")` will return `"name_1"`.
    `take_a_value_from_dict_list(test_list, "name", False)` will return
    `"name_2"`.

    PENDING: This function is not yet unit tested!
    """

    try:
        return sort_dict_list(_list, _column_target, _ascending)[0]\
            [_column_target]
    except IndexError:
        return []