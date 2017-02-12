from check_string      import check_client_name as ccn
from check_string      import check_db_host     as cdh
from check_string      import check_db_name     as cdn
from check_string      import check_table_name  as ctn
from exception_warning import ConventionWarning as CW
import unittest as ut

class test(ut.TestCase):

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
        self.assertFalse(ctn("TEST_TABLE_!"))
        self.assertFalse(ctn("TEST_TABLE_!NVALID"))
        self.assertFalse(ctn("test_table_!NVALID"))
        self.assertFalse(ctn("TEST_TABLE_1"))
        self.assertFalse(ctn("testTable1"))
        self.assertFalse(ctn("TESTtable_1"))
        self.assertTrue(ctn("test"))
        self.assertTrue(ctn("test_tABLE_1"))
        self.assertTrue(ctn("testTable"))
        self.assertTrue(ctn("testTable_1"))

if __name__ == "__main__": ut.main()