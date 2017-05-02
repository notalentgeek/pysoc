"""Database connection and content.

PENDING: _expr has not yet unit tested.
PENDING: Please check why `ResourceWarning` happens.
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
from check_string      import check_name_db               as cdn
from check_string      import check_name_table            as ctn
from dict_manip        import take_a_dict_from_dict_list  as t1d
from dict_manip        import take_a_value_from_dict_list as t1v
from exception_warning import c_warning                   as cw
from exception_warning import cd_warning                  as cdw
import json
import rethinkdb as r
import warnings  as warn



"""PENDING: Change these variables with real realtime value."""
rtm_cfg_db_host = "127.0.0.1" # Run time configuration for db host.
rtm_cfg_name_db = "test"      # Run time configuration for db name.



"""Modified warning functions.

`cw_`  is for ConventionWarning.
`cdw_` is for CreationDeletionWarning.
"""
def cw_db_mod(_name_db:str):
    cw("database", _name_db, "check_name_db", "check_string")

def cw_table_mod(_name_table:str):
    cw("table", _name_table, "check_name_table", "check_string")

def cdw_db_creation_mod(_name_db:str):
    cdw("database", _name_db, True, "check_name_db", "check_string")

def cdw_db_deletion_mod(_name_db:str):
    cdw("database", _name_db, False, "check_name_db", "check_string")

def cdw_table_creation_mod(_name_table:str):
    cdw("table", _name_table, True, "check_name_table", "check_string")

def cdw_table_deletion_mod(_name_table:str):
    cdw("table", _name_table, False, "check_name_table", "check_string")

def cdw_prevent_creation_or_deletion_if_string_check_fail(
    _db_or_name_table:str,
    _db_or_table:bool,
    _creation_or_deletion:bool
):
    if _db_or_table and _creation_or_deletion:
        cdw_db_creation_mod(_db_or_name_table)
    elif _db_or_table and not _creation_or_deletion:
        cdw_db_deletion_mod(_db_or_name_table)
    elif not _db_or_table and _creation_or_deletion:
        cdw_table_creation_mod(_db_or_name_table)
    elif not _db_or_table and not _creation_or_deletion:
        cdw_table_deletion_mod(_db_or_name_table)



def conn(_db_host:str=rtm_cfg_db_host):
    if not cdh(_db_host):
        cw("db host", _db_host, "check_db_host", "check_string")
        return None

    """Keep re - trying for Internet connection."""
    p = False
    while True:
        try:
            return r.connect(host=_db_host, timeout=5)
        except r.errors.ReqlDriverError:
            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
                p = True



def check_db(
    _conn    :r.net.DefaultConnection,
    _name_db :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            if r.db_list().contains(_name_db).run(_conn):
                if not cdn(_name_db):
                    cw_db_mod(_name_db)
                return True
            break
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True

    return False



def check_table(
    _conn       :r.net.DefaultConnection,
    _name_table :str,
    _name_db    :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            if check_db(_conn, _name_db):
                if r.db(_name_db).table_list().contains(_name_table).run(_conn):
                    if not ctn(_name_table):
                        cw_table_mod(_name_table)
                    return True
            break
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True

    return False



def check_doc(
    _conn       :r.net.DefaultConnection,
    _value      :str,
    _column     :str,
    _name_table :str,
    _name_db    :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            if check_db(_conn, _name_db):
                if check_table(_conn, _name_table, _name_db):
                    return bool(
                        get_doc_first_value(
                            _conn,
                            _value,
                            _column,
                            _column,
                            _name_table,
                            _name_db
                        )
                    )
            break
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True

    return False


# `_expr` stands for expression. It is used to return RethinkDB query instead
# of object.
def create_db(
    _conn    :r.net.DefaultConnection,
    _name_db :str=rtm_cfg_name_db,
    _expr    :bool=False
):
    p = False
    while True:
        try:
            if not cdn(_name_db):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_db,
                    True,
                    True
                )
                return None

            if check_db(_conn, _name_db):
                return None

            if _expr:
                return r.db_create(_name_db)
            else:
                return r.db_create(_name_db).run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def create_table(
    _conn       :r.net.DefaultConnection,
    _name_table :str,
    _name_db    :str=rtm_cfg_name_db,
    _expr       :bool=False
):
    p = False
    while True:
        try:
            if not cdn(_name_db):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_db,
                    True,
                    True
                )
                return None
            if not ctn(_name_table):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_table,
                    False,
                    True
                )
                return None

            if check_db(_conn, _name_db) and\
               check_table(_conn, _name_table, _name_db):
                return None

            if _expr:
                return r.db(_name_db).table_create(_name_table)
            else:
                return r.db(_name_db).table_create(_name_table).run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def create_doc(
    _conn          :r.net.DefaultConnection,
    _dict          :dict,
    _name_table    :str,
    _name_db       :str=rtm_cfg_name_db,
    _unique_column :list=[],
    _expr          :bool=False
):
    p = False
    while True:
        try:
            if not cdn(_name_db):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_db,
                    True,
                    True
                )
                return None
            if not ctn(_name_table):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_table,
                    False,
                    True
                )
                return None

            """Make sure the document's value is unique based on `_unique_column`."""
            if check_db(_conn, _name_db) and\
               check_table(_conn, _name_table, _name_db):
                for i in _unique_column:
                    if check_doc(_conn, _dict[i], i, _name_table, _name_db):
                        return None

            if _expr:
                return r.db(_name_db).table(_name_table).insert(_dict)
            else:
                return r.db(_name_db).table(_name_table).insert(_dict).run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def del_db(
    _conn    :r.net.DefaultConnection,
    _name_db :str=rtm_cfg_name_db,
    _expr    :bool=False
):
    p = False
    while True:
        try:
            if not cdn(_name_db):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_db,
                    True,
                    False
                )
                return None

            if not check_db(_conn, _name_db):
                return None

            if _expr:
                return r.db_drop(_name_db)
            else:
                return r.db_drop(_name_db).run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def del_table(
    _conn       :r.net.DefaultConnection,
    _name_table :str,
    _name_db    :str=rtm_cfg_name_db,
    _expr       :bool=False
):
    p = False
    while True:
        try:
            if not cdn(_name_db):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_db,
                    True,
                    False
                )
                return None
            if not ctn(_name_table):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_table,
                    False,
                    False
                )
                return None

            if not check_db(_conn, _name_db):
                return None

            if not check_table(_conn, _name_table, _name_db):
                return None

            if _expr:
                return r.db(_name_db).table_drop(_name_table)
            else:
                return r.db(_name_db).table_drop(_name_table).run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def del_doc(
    _conn         :r.net.DefaultConnection,
    _value        :str,
    _name_column :str,
    _name_table   :str,
    _name_db      :str=rtm_cfg_name_db,
    _expr         :bool=False
):
    """ Delete document based on column and its value. If there are more then
    one document has the same value on its column then multiple documents will
    be deleted.
    """
    p = False
    while True:
        try:
            if not cdn(_name_db):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_db,
                    True,
                    False
                )
                return None
            if not ctn(_name_table):
                cdw_prevent_creation_or_deletion_if_string_check_fail(
                    _name_table,
                    False,
                    False
                )
                return None

            if not check_db(_conn, _name_db):
                return None

            if not check_table(_conn, _name_table, _name_db):
                return None

            if not check_doc(_conn, _value, _name_column, _name_table, _name_db):
                return None

            if _expr:
                return r.db(_name_db).table(_name_table)\
                    .filter({ _name_column:_value }).delete()
            else:
                return r.db(_name_db).table(_name_table)\
                    .filter({ _name_column:_value }).delete().run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def get_doc_first(
    _conn               :r.net.DefaultConnection,
    _value              :str,
    _name_column        :str,
    _name_column_target :str,
    _name_table         :str,
    _name_db            :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            l = r.db(_name_db).table(_name_table).filter(
                    { _name_column: _value }).run(_conn)

            return t1d(l, _name_column_target)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def get_doc_first_value(
    _conn               :r.net.DefaultConnection,
    _value              :str,
    _name_column        :str,
    _name_column_target :str,
    _name_table         :str,
    _name_db            :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            """If this function returns a list (instead of just single document)
            value returned is alphabetically sorted (for example, this returns
            `"Alpha"`, when there are `["Alpha", "Beta"]`).
            """
            l = r.db(_name_db).table(_name_table).filter(
                    { _name_column: _value }).run(_conn)

            return t1v(l, _name_column_target)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True


def get_table(
    _conn       :r.net.DefaultConnection,
    _name_table :str,
    _name_db    :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            return r.db(_name_db).table(_name_table).run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True



def get_table_all(
    _conn    :r.net.DefaultConnection,
    _name_db :str=rtm_cfg_name_db
):
    p = False
    while True:
        try:
            return r.db(_name_db).table_list().run(_conn)
        except r.errors.ReqlDriverError:
            _conn.reconnect()

            if not p:
                print("\n{}{}\n{}".format(
                    "there is no database connection and/or there is no ",
                    "internet connection",
                    "re - trying database connection"
                ))
            p = True