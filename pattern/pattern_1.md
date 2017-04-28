checking existence procedure

database check  :           no check
database create : not database check
database delete :     database check
table    check  :     database check
table    create : not table    check
table    delete :     table    check
doc      check  :     doc      get
doc      create : not doc      check : no check if _unique_column_list is empty
doc      delete :     doc      check
doc      get    :     table    check

checking name procedure
every function that has db_name and table_name as parameter

testing procedure

test_database_check  : test True  , test False    , test warnings
test_database_create : test None  , test not None
test_database_delete : test None  , test not None
test_table   _check  : test True  , test False
test_table   _create : test None  , test not None
test_table   _delete : test None  , test not None
test_doc     _check  : test True  , test False
test_doc     _create : test None  , test not None
test_doc     _delete : test None  , test not None
test_doc     _get    : test Equal

procedure

delete all current checking name      functions
add    all new     checking name      functions   
delete all current checking existence functions
add    all new     checking existence functions