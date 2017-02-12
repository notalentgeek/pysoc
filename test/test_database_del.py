from database          import create_db               as crd
from database          import del_db                  as dd
from exception_warning import CreationDeletionWarning as CDW
import rethinkdb as r
import sys
import unittest  as ut

class test(ut.TestCase):
    ILLEGAL_BY_RDB          = "!LLEGAL"
    ILLEGAL_BY_THIS_PROGRAM = "1LLEGAL"

    """From `database.py`."""

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