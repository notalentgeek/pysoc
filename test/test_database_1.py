from database          import check_db                as cd
from database          import conn                    as c
from database          import create_db               as crd
from database          import del_db                  as dd
from exception_warning import ConventionWarning       as CW
from exception_warning import CreationDeletionWarning as CDW
import rethinkdb as r
import sys
import unittest  as ut
import warnings  as warn 

class test(ut.TestCase):
    ANY_STRING              = "any"         # LOL Mikael pls.
    ILLEGAL_BY_RDB          = "!LLEGAL"
    ILLEGAL_BY_THIS_PROGRAM = "1LLEGAL"
    NOT_EXIST               = "NOT_EXISTs"

    """From `database.py`."""

    def test_conn(self):
        """Test `c()` of `conn()` in `database.py`.

        Test 1: Assert warning for `CW` of `ConventionWarning`.
        Test 2: Assert warning for `CW` of `ConventionWarning`.
        Test 3: Assert not none for valid `c()` object.
        Test 4: Assert none for counterfeit `c()` object.
        Test 5: Assert none for counterfeit `c()` object.
        """
        function_name = sys._getframe().f_code.co_name
        db_host = "{}_{}".format(function_name, "host")
        db_host_illegal_by_rdb = "{}_{}".format(
            db_host,
            self.ILLEGAL_BY_RDB
        )
        db_host_illegal_by_this_program = "{}_{}".format(
            db_host,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = None
        test_list_2 = [db_host_illegal_by_rdb, None]
        test_list_3 = [db_host_illegal_by_this_program, None]

        test_list_1 = c()

        """Test 1."""
        with self.assertWarns(CW):
                test_list_2[len(test_list_2) - 1] = c(db_host_illegal_by_rdb)

        """Test 2."""
        with self.assertWarns(CW):
                test_list_3[len(test_list_3) - 1] = c(
                    db_host_illegal_by_this_program
                )

        self.assertIsNotNone(test_list_1)                    # Test 3.
        self.assertIsNone(test_list_2[len(test_list_2) - 1]) # Test 4.
        self.assertIsNone(test_list_3[len(test_list_3) - 1]) # Test 5.



    def test_check_db(self):
        """Test `cd()` of `check_db()` in `database.py`.

        Test 1: Assert warning for `CW` of `ConventionWarning`.
        Test 2: Assert true for database exists.
        Test 3: Assert false for database does not exists.
        Test 4: Assert true for database exist.
        Test 5: Assert falase for database does not exists.
        """
        function_name = sys._getframe().f_code.co_name
        db_name = "{}_{}".format(function_name, "db")
        db_name_illegal_by_rdb = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_RDB
        )
        db_name_illegal_by_this_program = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )
        db_name_not_exists = "{}_{}".format(
            db_name,
            self.NOT_EXIST
        )

        test_list_1 = [db_name, False]
        test_list_2 = [db_name_illegal_by_rdb, False]
        test_list_3 = [db_name_illegal_by_this_program, False]
        test_list_4 = [db_name_not_exists, False]

        crd(test_list_1[0])
        test_list_1[len(test_list_1) - 1] = cd(test_list_1[0])
        dd(test_list_1[0])

        test_list_2[len(test_list_2) - 1] = cd(test_list_2[0])

        r.db_create(test_list_3[0]).run(c())
        """Test 1."""
        with self.assertWarns(CW):
            test_list_3[len(test_list_3) - 1] = cd(test_list_3[0])
        r.db_drop(test_list_3[0]).run(c())

        test_list_4[len(test_list_4) - 1] = cd(test_list_4[0])

        self.assertTrue(test_list_1[len(test_list_1) - 1])  # Test 2.
        self.assertFalse(test_list_2[len(test_list_2) - 1]) # Test 3.
        self.assertTrue(test_list_3[len(test_list_3) - 1])  # Test 4.
        self.assertFalse(test_list_4[len(test_list_4) - 1]) # Test 5.



    def test_create_db(self):
        """Test `cd()` of `check_db()` in `database.py`.

        Test 1: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 2: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 3: Assert not none for valid `crd()` object.
        Test 4: Assert none for counterfeit `crd()` object.
        Test 5: Assert none for counterfeit `crd()` object.
        Test 6: Assert none for counterfeit `crd()` object.
        """
        function_name = sys._getframe().f_code.co_name
        db_name = "{}_{}".format(function_name, "db")
        db_name_illegal_by_rdb = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_RDB
        )
        db_name_illegal_by_this_program = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = [db_name, None, None]
        test_list_2 = [db_name_illegal_by_rdb, None]
        test_list_3 = [db_name_illegal_by_this_program, None]

        test_list_1[len(test_list_1) - 1] = crd(test_list_1[0])
        test_list_1[len(test_list_1) - 2] = crd(test_list_1[0])
        dd(test_list_1[0])

        """Test 1."""
        with self.assertWarns(CDW):
            test_list_2[len(test_list_2) - 1] = crd(test_list_2[0])

        """Test 2."""
        with self.assertWarns(CDW):
            test_list_3[len(test_list_3) - 1] = crd(test_list_3[0])

        self.assertIsNotNone(test_list_1[len(test_list_1) - 1]) # Test 3.
        self.assertIsNone(test_list_1[len(test_list_1) - 2])    # Test 4.
        self.assertIsNone(test_list_2[len(test_list_2) - 1])    # Test 5.
        self.assertIsNone(test_list_3[len(test_list_3) - 1])    # Test 6.



    def test_del_db(self):
        """Test `dd()` of `del_db()` in `database.py`."""
        function_name = sys._getframe().f_code.co_name
        db_name = "{}_{}".format(function_name, "db")
        db_name_illegal_by_rdb = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_RDB
        )
        db_name_illegal_by_this_program = "{}_{}".format(
            db_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = [db_name, None, None]
        test_list_2 = [db_name_illegal_by_rdb, None]
        test_list_3 = [db_name_illegal_by_this_program, None]

        crd(test_list_1[0])
        test_list_1[len(test_list_1) - 1] = dd(test_list_1[0])
        test_list_1[len(test_list_1) - 2] = dd(test_list_1[0])

        """Test 1."""
        with self.assertWarns(CDW):
            test_list_2[len(test_list_2) - 1] = dd(test_list_2[0])

        """Test 2."""
        with self.assertWarns(CDW):
            test_list_3[len(test_list_3) - 1] = dd(test_list_3[0])

        self.assertIsNotNone(test_list_1[len(test_list_1) - 1]) # Test 3.
        self.assertIsNone(test_list_1[len(test_list_1) - 2])    # Test 4.
        self.assertIsNone(test_list_2[len(test_list_2) - 1])    # Test 5.
        self.assertIsNone(test_list_3[len(test_list_3) - 1])    # Test 6.

if __name__ == "__main__":
    ut.main()