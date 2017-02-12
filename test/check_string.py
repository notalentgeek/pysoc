""" String checking. """

import sys
sys.path.append("./python-ipy")

from IPy import IP as ip

def check_client_name(_client_name:str):
    """Function to check client name.

    Args:
        _client_name: The client name.
                      The client name can have number(s).
                      The client name can have upper case.
                      The client name should start in lower case.
                      Right example "client1".
                      Right example "clientAlpha".
                      Right example "clientAlphaBeta".
                      Wrong example "1client".
                      Wrong example "client 1".
                      Wrong example "Client1".
                      Wrong example "client_1".

    Returns:
        This function will return `True` if all conditions `True`.
        This function will return `False` if one conditions `False`.
    """

    if not _client_name[:1].islower(): return False
    for i in _client_name:
        if not i.isalnum(): return False
    return True 

def check_db_host(_db_host:str, _fix:bool=True):
    """Function to check host name. Host name is an address to the RethinkDB
    database. Usually (and what is coded now) RethinkDB server and web server
    are in the same ip address (host). They each just located in different
    ports.

    Args:
        _db_host: The host address for both database server and web server.
                  The host address will follow convention from IPy module.
                  The host address can be "http://localhost".
                  The host address can be "https://localhost".
                  The host address can be "localhost".
                  Right example "123.123.123.123".
                  Right example "127.0.0.1".
                  Right example "255.255.255.255".
                  Right example "http://localhost".
                  Right example "https://localhost".
                  Wrong example "-1.0.0.0".
                  Wrong example "127.  0.0.1".
                  Wrong example "127. 0. 0. 1".
                  Wrong example "127. 0. 0.1".
                  Wrong example "127. 0.0.1".
                  Wrong example "2555.255.255.255".
                  Wrong example "http://localhost/" can be fixed into
                  "http://localhost".
                  Wrong example "https://localhost/" can be fixed into
                  "https://localhost".
    Returns:
        This function will return `True` if all conditions `True`.
        This function will return `False` if one conditions `False`.
    """

    if _fix and _db_host[-1:] == "/": _db_host = _db_host[:-1]

    if   _db_host == "http://localhost" : return True
    elif _db_host == "https://localhost": return True
    elif _db_host == "localhost"        : return True
    else:
        try: ip(_db_host)
        except ValueError as e: return False
    return True

def check_db_name(_db_name:str):
    """Function to check database name.

    Args:
        _dn_name: The database name.
                  The database name can have number(s) but right after
                  underscore.
                  The database name can have underscore ("_").
                  The database name cannot have upper case.
                  The database name should start with lower case.
                  Right example "test".
                  Right example "test_database".
                  Right example "test_database_1".
                  Wrong example "test_database1".
    Returns:
        This function will return `True` if all conditions `True`.
        This function will return `False` if one conditions `False`.
    """

    if not _db_name[:1].islower(): return False
    for i in _db_name:
        #print("{} {}".format(i, i.isupper()))

        """If `i` is a digit then we check the previous index. If the
        previous index is not an `"_"` then `return False`. This is the
        implementation of "The database name can have number(s) but separated
        by underscore.".

        If `not i.islower()` then `return False`. "Why not using
        `i.isupper()` instead?". That is because a `" ".isupper()` (" " as it
        is in space) will return `False` whereas we need it to return `True`
        at the if statement and then `return False` to reject as soon the
        `i == " "`.
        """
        if i == "_": pass
        elif i.islower(): pass
        elif i.isdigit() and _db_name.index(i) - 1 >= 0:
            if not _db_name[_db_name.index(i) - 1] == "_": return False
        elif not i.islower(): return False
        else: return False
    return True

def check_table_name(_table_name:str):
    """Function to check table name.

    Args:
        _table_name: The table name.
                     The table name can have number(s) but followed with
                     underscore ("_") if it is not the last character.
                     The table name can have number(s) but right after
                     underscore ("_").
                     The table name can have underscore ("_").
                     The table name can have upper case(s) but not right
                     after number.
                     The table name can have upper case(s) but not right
                     after underscore ("_").
                     The table name should start with lower case.
                     Right example "table_1".
                     Right example "table_test_1".
                     Right example "tableTEST".
                     Right example "tableTest".
                     Right example "tableTest_1".
                     Wrong example "table1".
                     Wrong example "table_1TEST".
                     Wrong example "table_1test".
                     Wrong example "table_Test".
                     Wrong example "TABLEtest1".

    Returns:
        This function will return `True` if all conditions `True`.
        This function will return `False` if one conditions `False`.
    """

    if _table_name[:1].isupper():
        return False

    for i in _table_name:
        if i == "_":
            pass
        elif i.islower():
            pass
        elif i.isdigit():
            if _table_name.index(i) - 1 >= 0:
                if not _table_name[_table_name.index(i) - 1].isdigit()\
                    and _table_name[_table_name.index(i) - 1] != "_":
                    print("1")
                    return False
            if _table_name.index(i) + 1 <= len(_table_name) - 1:
                if not _table_name[_table_name.index(i) + 1].isdigit()\
                    and _table_name[_table_name.index(i) + 1] != "_":
                    print("2")
                    return False
        elif i.isupper():
            if _table_name.index(i) - 1 >= 0:
                if _table_name[_table_name.index(i) - 1] == "_":
                    print("3")
                    return False
        else:
            return False

    return True