from check_string      import check_client_name                                     as ccn
from check_string      import check_db_host                                         as cdh
from check_string      import check_db_name                                         as cdn
from check_string      import check_table_name                                      as ctn
from database          import cdw_database_creation_mod                             as cdw_dcm
from database          import cdw_database_deletion_mod                             as cdw_ddm
from database          import cdw_table_creation_mod                                as cdw_tcm
from database          import cdw_table_deletion_mod                                as cdw_tdm
from database          import check_db                                              as cd
from database          import check_doc                                             as cdc
from database          import check_table                                           as ct
from database          import conn                                                  as c
from database          import create_db                                             as crd
from database          import create_doc                                            as crdc
from database          import create_table                                          as crt
from database          import cw_database_mod                                       as cwdm
from database          import cw_table_mod                                          as cwtm
from database          import del_db                                                as dd
from database          import del_table                                             as dt
from database          import get_first_doc                                         as gfd
from database          import cdw_prevent_creation_or_deletion_if_string_check_fail as prevent_creation_deletion
from docopt            import docopt                                                as doc
from exception_warning import ConventionWarning                                     as CW
from exception_warning import CreationDeletionWarning                               as CDW
from exception_warning import TestWarning                                           as TW
import rethinkdb as r
import sys
import unittest  as ut
import warnings  as warn

class test(ut.TestCase):
    """From `database.py`."""

    def test_conn(self):
        """This is a test function to test `c()` of `conn()` in `database.py`.

        Test 1: Assert not none if `c()` returns an object.
        Test 2: Assert none if `c()` returns none.
        Test 3: Assert true if `CW` of `ConventionWarning` happens.
        """
        db_host = "{}_{}".format(sys._getframe().f_code.co_name, "_host")
        db_host_invalid = "{}_{}".format(db_host, "INVALID")

        """Test 1."""
        self.assertIsNotNone(c())

        test_CW = False
        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CW)
            try:
                """Test 2."""
                self.assertIsNone(c(db_host_invalid))
            except CW as w:
                test_CW = True
        """Test 3."""
        self.assertTrue(test_CW)



    def test_check_db(self):
        """This is a test function to test `cd()` of `check_database()` in
        `database.py`.

        Test 1: Assert true if database is exist.
        Test 2: Assert true if database is not exist. 
        Test 3: Assert true if database is exist.
        Test 4: Assert true if `CW` of `ConventionWarning` happens.
        """
        db_name = "{}_{}".format(sys._getframe().f_code.co_name, "db")
        db_name_invalid = "{}_{}".format(db_name, "INVALID")
        db_name_not_exists = "{}_{}".format(db_name, "not_exists")

        """Test 1."""
        crd(db_name)
        self.assertTrue(cd(db_name))
        dd(db_name)

        """Test 2."""
        self.assertFalse(cd(db_name_not_exists))

        test_CW = False
        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CW)
            try:
                if not cd(db_name_invalid):
                    r.db_create(db_name_invalid).run(c())
                """Test 3."""
                self.assertTrue(cd(db_name_invalid))
            except CW as w:
                test_CW = True 
        """Test 4."""               
        self.assertTrue(test_CW)
        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CDW)
            try:
                r.db_drop(db_name_invalid).run(c())
            except r.errors.ReqlOpFailedError as e:
                pass




    def test_create_db(self):
        """This is a test function to test `crd()` of `create_db()` in
        `database.py`.

        Test 1: Assert not none if database is created.
        Test 2: Assert none if database is not created.
        Test 3: Assert none if database is not created.
        Test 4: Assert true if `CDW` of `CreationDeletionWarning` happens.
        """
        db_name = "{}_{}".format(sys._getframe().f_code.co_name, "db")
        db_name_invalid = "{}_{}".format(db_name, "INVALID")

        """Test 1."""
        self.assertIsNotNone(crd(db_name))

        """Test 2."""
        self.assertIsNone(crd(db_name))
        dd(db_name)

        test_CDW = False
        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CDW)
            try:
                """Test 3."""
                self.assertIsNone(crd(db_name_invalid))
            except CDW as w:
                test_CDW = True
        """Test 4."""
        self.assertTrue(test_CDW)




    def test_del_db(self):
        """This is a test function to test `dd()`of `delete_db()` in
        `database.py`.

        Test 1: Assert not none if database is deleted.
        Test 2: Assert none if database is not deleted.
        Test 3: Assert none if database is not created.
        Test 4: Assert true if `CDW` of `CreationDeletionWarning` happens.
        """
        db_name = "{}_{}".format(sys._getframe().f_code.co_name, "db")
        db_name_invalid = "{}_{}".format(db_name, "INVALID")

        """Test 1."""
        crd(db_name)
        self.assertIsNotNone(dd(db_name))

        """Test 2."""
        self.assertIsNone(dd(db_name))

        test_CDW = False
        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CDW)
            try:
                """Test 3."""
                self.assertIsNone(dd(db_name_invalid))
            except CDW as w:
                test_CDW = True
        """Test 4."""
        self.assertTrue(test_CDW)



    def test_check_table(self):
        db_name = "{}_{}".format(sys._getframe().f_code.co_name, "db")
        db_name_not_exists = "{}_{}".format(db_name, "not_exists")
        db_name_invalid = "{}_{}".format(db_name, "INVALID")

        table_name = "{}_{}".format(sys._getframe().f_code.co_name, "table")
        table_name_not_exists = "{}_{}".format(db_name, "not_exists")
        table_name_invalid = "{}_{}".format(db_name, "INVALID")

        crd(db_name)
        crt(table_name, db_name)
        """Test 1."""
        self.assertTrue(ct(table_name, db_name))
        """Test 2."""
        self.assertFalse(ct(table_name_not_exists, db_name))
        dd(db_name)

        """Test 3."""
        self.assertFalse(ct(table_name, db_name_not_exists))

        """Test 4."""
        self.assertFalse(ct(table_name_not_exists, db_name_not_exists))

        test_CW_1 = False
        test_CW_2 = False
        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CW)
            try:
                if not cd(db_name_invalid):
                    r.db_create(db_name_invalid).run(c())
                    if not ct(table_name_not_exists, db_name_invalid):
                        r.db(db_name_invalid).table_create(table_name_not_exists).run(c())
                """Test 5."""
                self.assertTrue(cd(db_name_invalid))
                """Test 6."""
                self.assertTrue(ct(table_name_not_exists, db_name_invalid))
                r.db_drop(db_name_invalid).run(c())
            except CW as w:
                test_CW_1 = True

            try:
                if not ct(table_name_invalid, db_name_invalid):
                    r.db(db_name_invalid).table_create(table_name_invalid).run(c())
                """Test 7."""
                self.assertTrue(cd(db_name_invalid))
                """Test 8."""
                self.assertTrue(ct(table_name_invalid, db_name_invalid))
            except CW as w:
                test_CW_2 = True

        r.db_drop(db_name_invalid).run(c())

        """Test 9."""
        self.assertTrue(test_CW_1)

        """Test 10."""
        self.assertTrue(test_CW_2)



    def test_create_table(self):
        db_name = "{}_{}".format(sys._getframe().f_code.co_name, "db")
        db_name_invalid = "{}_{}".format(db_name, "INVALID")

        table_name = "{}_{}".format(sys._getframe().f_code.co_name, "table")
        table_name_invalid = "{}_{}".format(db_name, "!NVALID")

        crd(db_name)
        self.assertIsNotNone(crt(table_name, db_name))
        self.assertIsNone(crt(table_name, db_name))
        dd(db_name)

        with warn.catch_warnings(record=False):
            warn.simplefilter("error", category=CDW)

            try:
                self.assertIsNone(crt(db_name_invalid))
            except CDW as w:
                pass


    """
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
    """

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