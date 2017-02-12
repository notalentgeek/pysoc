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

from check_string      import check_db_host               as cdh
from check_string      import check_db_name               as cdn
from check_string      import check_table_name            as ctn
from dict_manip        import take_a_dict_from_dict_list  as t1d
from dict_manip        import take_a_value_from_dict_list as t1v
from exception_warning import c_warning                   as cw
from exception_warning import cd_warning                  as cdw
import json
import rethinkdb as r
import warnings  as warn



"""PENDING: Change these variables with real realtime value."""
rtm_cfg_db_host = "127.0.0.1" # Run time configuration for db host.
rtm_cfg_db_name = "test"      # Run time configuration for db name.



"""Modified warning functions.

`cw_`  is for ConventionWarning.
`cdw_` is for CreationDeletionWarning.
"""
def cw_db_mod(_db_name:str):
    cw("database", _db_name, "check_db_name", "check_string")

def cw_table_mod(_table_name:str):
    cw("table", _table_name, "check_table_name", "check_string")

def cdw_db_creation_mod(_db_name:str):
    cdw("database", _db_name, True, "check_db_name", "check_string")

def cdw_db_deletion_mod(_db_name:str):
    cdw("database", _db_name, False, "check_db_name", "check_string")

def cdw_table_creation_mod(_table_name:str):
    cdw("table", _table_name, True, "check_table_name", "check_string")

def cdw_table_deletion_mod(_table_name:str):
    cdw("table", _table_name, False, "check_table_name", "check_string")

def cdw_prevent_creation_or_deletion_if_string_check_fail(
    _db_or_table_name:str,
    _db_or_table:bool,
    _creation_or_deletion:bool
):
    if _db_or_table and _creation_or_deletion:
        cdw_db_creation_mod(_db_or_table_name)
    elif _db_or_table and not _creation_or_deletion:
        cdw_db_deletion_mod(_db_or_table_name)
    elif not _db_or_table and _creation_or_deletion:
        cdw_table_creation_mod(_db_or_table_name)
    elif not _db_or_table and not _creation_or_deletion:
        cdw_table_deletion_mod(_db_or_table_name)



def conn(_db_host:str=rtm_cfg_db_host):
    if not cdh(_db_host):
        cw("db host", _db_host, "check_db_host", "check_string")
        return None

    """PENDING: Surpress resource warning for unit testing."""
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=ResourceWarning)

        """Keep re - trying for Internet connection."""
        p = False
        while True:
            try:
                return r.connect(host=_db_host, timeout=5)
            except r.errors.ReqlDriverError as e:
                if not p:
                    print("\n{}{}\n{}".format(
                        "there is no database connection and/or there is no ",
                        "internet connection",
                        "re - trying database connection"
                    ))
                    p = True



def check_db(_db_name:str=rtm_cfg_db_name):
    if r.db_list().contains(_db_name).run(conn()):
        if not cdn(_db_name):
            cw_db_mod(_db_name)
        return True

    return False



def check_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if check_db(_db_name):
        if r.db(_db_name).table_list().contains(_table_name).run(conn()):
            if not ctn(_table_name):
                cw_table_mod(_table_name)
            return True

    return False



def check_doc(_value:str, _column:str, _table_name:str,
    _db_name:str=rtm_cfg_db_name):
    if check_db(_db_name):
        if check_table(_table_name, _db_name):
            return bool(
                get_first_doc(
                    _value,
                    _column,
                    _column,
                    _table_name,
                    _db_name
                )
            )

    return False



def create_db(_db_name:str=rtm_cfg_db_name):
    if not cdn(_db_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _db_name,
            True,
            True
        )
        return None

    if not check_db(_db_name):
        return None

    return r.db_create(_db_name).run(conn())



def create_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if not cdn(_db_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _db_name,
            True,
            True
        )
        return None
    if not ctn(_table_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _table_name,
            False,
            True
        )
        return None

    if check_db(_db_name) and check_table(_table_name, _db_name):
        return None

    return r.db(_db_name).table_create(_table_name).run(conn())



def create_doc(_dict:dict, _table_name:str,
    _db_name:str=rtm_cfg_db_name, _unique_column:list=[]):
    if not cdn(_db_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _db_name,
            True,
            True
        )
        return None
    if not ctn(_table_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _table_name,
            False,
            True
        )
        return None

    """Make sure the document's value is unique based on `_unique_column`."""
    if check_db(_db_name) and check_table(_table_name, _db_name):
        for i in _unique_column:
            if check_doc(_dict[i], i, _table_name, _db_name):
                return None

    return r.db(_db_name).table(_table_name).insert(_dict).run(conn())



def del_db(_db_name:str=rtm_cfg_db_name):
    if not cdn(_db_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _db_name,
            True,
            False
        )
        return None

    if not check_db(_db_name):
        return None

    return r.db_drop(_db_name).run(conn())



def del_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if not cdn(_db_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _db_name,
            True,
            False
        )
        return None
    if not ctn(_table_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _table_name,
            False,
            False
        )
        return None

    if not check_table(_table_name, _db_name):
        return None

    return r.db(_db_name).table_drop(_table_name).run(conn())



def del_doc(_value:str, _column_value:str, _table_name:str,
    _db_name:str=rtm_cfg_db_name):
    """ Delete document based on column and its value. If there are more then
    one document has the same value on its column then multiple documents will
    be deleted.
    """

    if not cdn(_db_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _db_name,
            True,
            False
        )
        return None
    if not ctn(_table_name):
        cdw_prevent_creation_or_deletion_if_string_check_fail(
            _table_name,
            False,
            False
        )
        return None

    if not check_doc(_value, _column_value, _table_name, _db_name):
        return None

    return r.db(_db_name).table(_table_name).filter({ _column_value:_value })\
        .delete().run(conn())



def get_first_doc(_value:str, _column_value:str, _column_target:str,
    _table_name:str, _db_name:str=rtm_cfg_db_name):
    l = r.db(_db_name).table(_table_name).filter(
            { _column_value: _value }).run(conn())

    return t1d(l, _column_target)



def get_first_doc_value(_value:str, _column_value:str, _column_target:str,
    _table_name:str, _db_name:str=rtm_cfg_db_name):
    """If this function returns a list (instead of just single document)
    value returned is alphabetically sorted (for example, this returns
    `"Alpha"`, when there are `["Alpha", "Beta"]`).
    """

    l = r.db(_db_name).table(_table_name).filter(
            { _column_value: _value }).run(conn())

    return t1v(l, _column_target)