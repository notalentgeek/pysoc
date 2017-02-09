from check_string import check_client_name as ccn
from check_string import check_db_host     as cdh
from check_string import check_db_name     as cdn
from check_string import check_table_name  as ctn
from database     import check_db          as cd
from database     import check_doc         as cdc
from database     import check_table       as ct
from database     import conn              as c
from database     import create_db         as crd
from database     import create_doc        as crdc
from database     import create_table      as crt
from database     import del_db            as dd
from database     import del_table         as dt
from database     import get_first_doc     as gfd
from docopt       import docopt            as doc
import rethinkdb as r
import sys
import unittest  as ut
import warnings  as warn

class test(ut.TestCase):
    """From `database.py`."""

    def test_conn(self):
        self.assertIsNotNone(c())
        self.assertIsNone(c("!@#InVaLiD_HoSt!@#"))

        try: c()
        except r.errors.ReqlDriverError as e: self.fail()

    def test_check_db(self):
        db_name = sys._getframe().f_code.co_name

        crd(db_name)

        self.assertFalse(cd("database_that_does_not_exist"))
        self.assertTrue(cd(db_name))

        dd(db_name)

    def test_create_db(self):
        db_name = sys._getframe().f_code.co_name

        self.assertIsNotNone(crd(db_name))
        self.assertIsNone(crd(db_name))
        self.assertIsNone(crd("!@#InVaLiD_Db!@#"))

        dd(db_name)

    def test_del_db(self):
        db_name = sys._getframe().f_code.co_name

        crd(db_name)

        self.assertIsNotNone(dd(db_name))
        self.assertIsNone(dd(db_name))

    def test_check_table(self):
        db_name = "{}{}".format(sys._getframe().f_code.co_name, "_db")
        table_name ="{}{}".format(sys._getframe().f_code.co_name, "_table")

        crd(db_name)
        crt(table_name, db_name)

        self.assertFalse(ct("table_that_does_not_exist", db_name))
        self.assertTrue(ct(table_name, db_name))

        try: ct(table_name, db_name)
        except r.errors.ReqlOpFailedError as e: self.fail()

        with self.assertRaises(r.errors.ReqlOpFailedError):
            ct("table_that_does_not_exist", "database_that_does_not_exists")

        dd(db_name)

    def test_create_table(self):
        db_name = "{}{}".format(sys._getframe().f_code.co_name, "_db")
        table_name ="{}{}".format(sys._getframe().f_code.co_name, "_table")

        crd(db_name)

        self.assertIsNotNone(crt(table_name, db_name))
        self.assertIsNone(crt(table_name, db_name))
        self.assertIsNone(crt("!@#InVaLiD_TaBlE!@#"))

        dd(db_name)

    def test_delete_table(self):
        db_name = "{}{}".format(sys._getframe().f_code.co_name, "_db")
        table_name ="{}{}".format(sys._getframe().f_code.co_name, "_table")

        crd(db_name)
        crt(table_name, db_name)

        self.assertIsNotNone(dt(table_name, db_name))
        self.assertIsNone(dt(table_name, db_name))

        dd(db_name)

    def test_check_doc(self):
        db_name = "{}{}".format(sys._getframe().f_code.co_name, "_db")
        table_name ="{}{}".format(sys._getframe().f_code.co_name, "_table")
        document_1 = { "name":"name_1", "job":"manager" }

        crd(db_name)
        crt(table_name, db_name)
        crdc(document_1, table_name, db_name, ["name"])

        #self.assertFalse(cdc("name_1", "column_that_does_not_exists", table_name, db_name))
        #self.assertFalse(cdc("name_that_does_exists", "column_that_does_not_exists", table_name, db_name))
        #self.assertFalse(cdc("name_that_does_not_exists", "name", table_name, db_name))
        #self.assertTrue(cdc("manager", "job", table_name, db_name))
        #self.assertTrue(cdc("name_1", "name", table_name, db_name))

        dd(db_name)

    def test_get_first_doc(self):
        db_name = "{}{}".format(sys._getframe().f_code.co_name, "_db")
        table_name ="{}{}".format(sys._getframe().f_code.co_name, "_table")
        document_1 = { "name":"name_1", "job":"manager" }
        document_2 = { "name":"name_2", "job":"developer" }
        document_3 = { "name":"name_3", "job":"developer" }

        crd(db_name)
        crt(table_name, db_name)
        crdc(document_1, table_name, db_name, ["name"])
        crdc(document_2, table_name, db_name, ["name"])
        crdc(document_3, table_name, db_name, ["name"])

        self.assertEqual(gfd("developer", "job", "name", table_name, db_name), "name_2")
        self.assertEqual(gfd("manager", "job", "name", table_name, db_name), "name_1")
        self.assertIsNone(gfd("job_that_does_not_exist", "job", "name", table_name, db_name))

        dd(db_name)

    """From `check_string.py`."""

    def test_check_client_name(self):
        self.assertFalse(ccn("1client"))
        self.assertFalse(ccn("client!"))
        self.assertFalse(ccn("Client1"))
        self.assertFalse(ccn("client1."))
        self.assertFalse(ccn("client_1"))
        self.assertTrue(ccn("cLiEnT"))
        self.assertTrue(ccn("client"))
        self.assertTrue(ccn("client1"))
        self.assertTrue(ccn("clientAlpha"))
        self.assertTrue(ccn("clientAlphaBeta"))

    def test_check_db_host(self):
        self.assertFalse(cdh("-1.-1.-1.-1"))
        self.assertFalse(cdh("127.  0.0.1"))
        self.assertFalse(cdh("127. 0. 0. 1"))
        self.assertFalse(cdh("127. 0. 0.1"))
        self.assertFalse(cdh("127. 0.0.1"))
        self.assertFalse(cdh("256.256.256.256"))
        self.assertFalse(cdh("https://google.com"))
        self.assertTrue(cdh("0.0.0.0"))
        self.assertTrue(cdh("127.0.0.1"))
        self.assertTrue(cdh("255.255.255.255"))
        self.assertTrue(cdh("http://localhost"))
        self.assertTrue(cdh("http://localhost/"))
        self.assertTrue(cdh("https://localhost"))
        self.assertTrue(cdh("https://localhost/"))
        self.assertTrue(cdh("localhost"))

    def test_check_db_name(self):
        self.assertFalse(cdn(" test db"))
        self.assertFalse(cdn("1_test_db"))
        self.assertFalse(cdn("1test_db"))
        self.assertFalse(cdn("_test_db"))
        self.assertFalse(cdn("test db"))
        self.assertFalse(cdn("TEST DB"))
        self.assertFalse(cdn("test! db!"))
        self.assertFalse(cdn("test.db"))
        self.assertFalse(cdn("tEsT_dB"))
        self.assertFalse(cdn("test_db1"))
        self.assertTrue(cdn("test_db"))
        self.assertTrue(cdn("test_db_1"))
        self.assertTrue(cdn("testdb"))

    def test_check_table_name(self):
        self.assertFalse(ctn("test_Table"))
        self.assertFalse(ctn("TEST_TABLE_1"))
        self.assertFalse(ctn("testTable1"))
        self.assertFalse(ctn("TESTtable_1"))
        self.assertTrue(ctn("test"))
        self.assertTrue(ctn("test_tABLE_1"))
        self.assertTrue(ctn("testTable"))
        self.assertTrue(ctn("testTable_1"))

if __name__ == "__main__": ut.main()