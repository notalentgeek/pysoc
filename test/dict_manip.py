"""Collections of function(s) to manipulate dictionary. Usually used to deal with
value returned from RethinkDB query
"""

def take_a_value_from_dict_list(_list:list, _row_target:str,
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
    result = None

    for i in _list:
        if i[_row_target] != None:
            if _ascending: result = min(result, i[_row_target])\
                if not result == None else i[_row_target]
            else: result = max(result, i[_row_target])\
                if not result == None else i[_row_target]

    return result