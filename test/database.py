"""Database connection and content.

PENDING: Please check why `ResourceWarning` happens.
         Search for `warn.simplefilter("ignore", category=ResourceWarning)`.
         Here are sample output.

         /usr/local/lib/python3.5/dist-packages/rethinkdb/ast.py:1804:
         ResourceWarning: unclosed <socket.socket fd=4,
         family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6,
         laddr=('127.0.0.1', 40260), raddr=('127.0.0.1', 28015)>
           if any([_ivar_scan(arg) for k, arg in dict_items(query.optargs)]):
         /usr/local/lib/python3.5/dist-packages/rethinkdb/ast.py:1804:
         ResourceWarning: unclosed <socket.socket fd=5,
         family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6,
         laddr=('127.0.0.1', 40262), raddr=('127.0.0.1', 28015)>
           if any([_ivar_scan(arg) for k, arg in dict_items(query.optargs)]):
         /usr/local/lib/python3.5/dist-packages/rethinkdb/ast.py:1804:
         ResourceWarning: unclosed <socket.socket fd=6,
         family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6,
         laddr=('127.0.0.1', 40264), raddr=('127.0.0.1', 28015)>
"""

from check_string import check_db_host               as cdh
from check_string import check_db_name               as cdn
from check_string import check_table_name            as ctn
from dict_manip   import take_a_value_from_dict_list as t1v
import json
import rethinkdb as r
import warnings  as warn

"""PENDING: Change these variables with real realtime value."""
rtm_cfg_db_host = "127.0.0.1" # Run time configuration for db host.
rtm_cfg_db_name = "test"      # Run time configuration for db name.



"""PENDING: No unit test for this function just yet!"""
def format_dict(_dict:dict): return json.loads(json.dumps(_dict))



def conn(_db_host:str=rtm_cfg_db_host):
    if not cdh(_db_host): return None

    """PENDING: Surpress resource warning for unit testing."""
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=ResourceWarning)

        """Keep re - trying for Internet connection."""
        p = False
        while True:
            try: return r.connect(host=_db_host, timeout=5)
            except r.errors.ReqlDriverError as e:
                if not p:
                    print("\n{}{}\n{}".format(
                        "there is no database connection and/or there is no ",
                        "internet connection",
                        "re - trying database connection"
                    ))
                    p = True



def check_db(_db_name:str=rtm_cfg_db_name):
    return r.db_list().contains(_db_name).run(conn())



def create_db(_db_name:str=rtm_cfg_db_name):
    if not cdn(_db_name): return None

    if not check_db(_db_name): return r.db_create(_db_name).run(conn())
    else: return None



def del_db(_db_name:str=rtm_cfg_db_name):
    if check_db(_db_name): return r.db_drop(_db_name).run(conn())
    else: return None



def check_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if check_db(_db_name):
        return r.db(_db_name).table_list().contains(_table_name).run(conn())
    else: return None



def create_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if not ctn(_table_name): return None

    if not check_table(_table_name, _db_name):
        return r.db(_db_name).table_create(_table_name).run(conn())
    else: return None



def del_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if check_table(_table_name, _db_name):
        return r.db(_db_name).table_drop(_table_name).run(conn())
    else: return None



def check_doc(_value:str, _column:str, _table_name:str,
    _db_name:str=rtm_cfg_db_name):
    """This function returns `True` if there is at least an element that
    equal to `_value` from `_column`.
    """
    if not check_table(_table_name, _db_name): return None

    """PENDING: Surpress resource warning for unit testing."""
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=ResourceWarning)
        return bool(get_first_doc(_value, _column, _column, _table_name,
            _db_name))



def create_doc(_dict:dict, _table_name:str,
    _db_name:str=rtm_cfg_db_name, _unique_column:list=[]):
    """Function to insert value into database.
    
    DONE: Add function to check if the `_unique_column` value is really one
          of its kind, if not `return None`. Make this as separate function.
    DONE: Add unit test if database does not exist.
    DONE: Add unit test if table does not exist.
    DONE: Add unit test if there is same document with uniques name exists.
          In the case of `client` table the column `client_name` should be
          unique.
    
    Make sure there is no document in column name in `_unique_column`
    are the same.
    """
    for i in _unique_column:
        """PENDING: Surpress resource warning for unit testing."""
        with warn.catch_warnings():
            warn.simplefilter("ignore", category=ResourceWarning)
            #print("_dict[i]: {}, i: {}, _table_name: {}, _db_name: {}"\
            #    .format(_dict[i], i, _table_name, _db_name))
            if check_doc(_dict[i], i, _table_name, _db_name): return None

    return r.db(_db_name).table(_table_name).insert(_dict).run(conn())



"""PENDING."""
def del_doc(_value:str, _column_value:str, _table_name:str,
    _db_name:str=rtm_cfg_db_name):
    if not check_db(_db_name): return None
    elif not check_table(_table_name, _db_name): return None

    return r.db(_db_name).table(_table_name).filter({ _column_value:_value })\
        .delete().run(conn())



def get_first_doc(_value:str, _column_value:str, _column_target:str,
    _table_name:str, _db_name:str=rtm_cfg_db_name):
    """If this function returns a list (instead of just single document)
    value returned is alphabetically sorted (for example, this returns
    `"Alpha"`, when there are `["Alpha", "Beta"]`).
    
    PENDING: Surpress resource warning for unit testing.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=ResourceWarning)

        """This will return a list."""
        l = r.db(_db_name).table(_table_name).filter(
            { _column_value: _value }).run(conn())

    return t1v(l, _column_target)