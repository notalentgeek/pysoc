""" Database connection and content. """

from check_string import check_db_host    as cdh
from check_string import check_db_name    as cdn
from check_string import check_table_name as ctn
import rethinkdb as r
import warnings  as warn

"""PENDING: Change these variables with real realtime value."""
rtm_cfg_db_host = "127.0.0.1" # Run time configuration for db host.
rtm_cfg_db_name = "test"      # Run time configuration for db name.

"""PENDING: No unit test for this function just yet!"""
def format_dict(_dict:dict): return json.loads(json.dumps(_dict))

def conn(_db_host:str=rtm_cfg_db_host):
    if not cdh(_db_host): return None

    """Surpress resource warning for unit testing."""
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
    return r.db(_db_name).table_list().contains(_table_name).run(conn())

def create_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if not ctn(_table_name): return None

    if not check_table(_table_name, _db_name):
        return r.db(_db_name).table_create(_table_name).run(conn())
    else: return None

def del_table(_table_name:str, _db_name:str=rtm_cfg_db_name):
    if check_table(_table_name, _db_name):
        return r.db(_db_name).table_drop(_table_name).run(conn())
    else: return None

"""PENDING: Use `coun()`!"""
def check_doc(_value:str, _row:str): pass

def get_first_doc(_value:str, _row_value:str, _row_target:str,
    _table_name:str, _db_name:str=rtm_cfg_db_name):
    try:
        j = r.db(_db_name).table(_table_name).filter({ _row_value: _value })\
            .nth(0).to_json().run(conn())
        d = json.loads(j)
        return d[_row_target]
    except IndexError as e: return None

def insert_doc(_dict:dict): pass