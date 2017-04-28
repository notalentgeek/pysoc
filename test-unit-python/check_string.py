""" String checking. """
from IPy import IP as ip

def check_client_name(_string:str):
    """Function to check a string if it is a legitimate client name.

    Example:
        Correct example "client1".
        Correct example "client1Alpha".
        Correct example "clientAlpha".
        Correct example "clientAlpha1Beta".
        Correct example "clientAlphaBeta".
        Correct example "clientAlphabeta".
        Wrong   example "client 1".
        Wrong   example "Client1".
        Wrong   example "client1alpha".
        Wrong   example "client_1".
        Wrong   example "Client_1".
        Wrong   example "ClientAlpha".
    """

    if not _string[:1].islower():
        return False

    if not _string[-1:].isalnum():
        return False

    for i in _string:
        if i.islower() or i.isupper():
            pass
        elif i.isdigit():
            if _string.index(i) < len(_string) - 2:
                if not _string[_string.index(i) + 1].isupper() and\
                   not _string[_string.index(i) + 1].isdigit():
                    return False
        else:
            return False

    return True

def check_db_host(_string:str, _fix:bool=True):
    """Function to check a string if it is a legitimate db host.

    Example:
    Correct example "123.123.123.123".
    Correct example "127.0.0.1".
    Correct example "255.255.255.255".
    Correct example "http://localhost".
    Correct example "https://localhost".
    Wrong   example "-1.0.0.0".
    Wrong   example "127.  0.0.1".
    Wrong   example "127. 0. 0. 1".
    Wrong   example "127. 0. 0.1".
    Wrong   example "127. 0.0.1".
    Wrong   example "2555.255.255.255".
    Wrong   example "http://localhost/"  can be fixed into
    "http://localhost"  with `_fix=True`.
    Wrong   example "https://localhost/" can be fixed into
    "https://localhost" with `_fix=True`.
    """

    localhost = [
        "http://localhost",
        "https://localhost",
        "localhost"
    ]

    if _fix and (_string[-1:] == "/" or _string[-1:] == "\\"):
        _string = _string[:-1]

    for i in localhost:
        if i == _string:
            return True

    try:
        ip(_string)
    except ValueError:
        return False

    return True

def check_db_name(_string:str):
    """Function to check a string if it is a legitimate db name.

    Example:
        Correct example "test".
        Correct example "test_1_database".
        Correct example "test_database".
        Correct example "test_database_1".
        Wrong   example "test_".
        Wrong   example "test_database1".
        Wrong   example "testDatabase1".
        Wrong   example "testdatabase1".
    """

    if not _string[:1].islower():
        return False

    if not _string[-1:].isdigit() and not _string[-1:].islower():
        return False

    for i in _string:
        if i.islower():
            pass
        elif i.isdigit():
            if _string.index(i) > 0:
                if not _string[_string.index(i) - 1].isdigit() and\
                   not _string[_string.index(i) - 1] == "_":
                    return False

            if _string.index(i) < len(_string) - 2:
                if not _string[_string.index(i) + 1].isdigit() and\
                   not _string[_string.index(i) + 1] == "_":
                    return False

        elif i == "_":
            if _string.index(i) > 0:
                if not _string[_string.index(i) - 1].isdigit() and\
                   not _string[_string.index(i) - 1].islower():
                    return False

            if _string.index(i) < len(_string) - 2:
                if not _string[_string.index(i) + 1].isdigit() and\
                   not _string[_string.index(i) + 1].islower():
                    return False

        else:
            return False

    return True

def check_table_name(_string:str):
    """Function to check a string if it is a ligitimate db table.

    Example:
        Correct example "table_1".
        Correct example "table_test".
        Correct example "table_test_1".
        Correct example "tableTest".
        Correct example "tableTest_1".
        Wrong   example "test_".
        Wrong   example "test_database1".
        Wrong   example "testDatabase1".
        Wrong   example "testdatabase1".
    """

    if not _string[:1].islower():
        return False

    if not _string[-1:].isalnum():
        return False

    for i in _string:
        if i.islower():
            pass
        elif i.isupper():
            if _string.index(i) > 0:
                if not _string[_string.index(i) - 1].isalpha():
                    return False

            if _string.index(i) < len(_string) - 2:
                if not _string[_string.index(i) + 1].isalpha() and\
                   not _string[_string.index(i) + 1] == "_":
                    return False

        elif i.isdigit():
            if _string.index(i) > 0:
                if not _string[_string.index(i) - 1].isdigit() and\
                   not _string[_string.index(i) - 1] == "_":
                    return False

            if _string.index(i) < len(_string) - 2:
                if not _string[_string.index(i) + 1].isdigit() and\
                   not _string[_string.index(i) + 1] == "_":
                    return False

        elif i == "_":
            if _string.index(i) > 0:
                if not _string[_string.index(i) - 1].islower() and\
                   not _string[_string.index(i) - 1].isdigit():
                    return False

            if _string.index(i) < len(_string) - 2:
                if not _string[_string.index(i) + 1].islower() and\
                   not _string[_string.index(i) + 1].isdigit():
                    return False

        else:
            return False

    return True