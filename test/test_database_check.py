from database          import check_db          as cd
from database          import conn              as c
from database          import create_db         as crd
from database          import del_db            as dd
from exception_warning import ConventionWarning as CW
import rethinkdb as r
import sys
import unittest  as ut

class test(ut.TestCase):
    ILLEGAL_BY_RDB          = "!LLEGAL"
    ILLEGAL_BY_THIS_PROGRAM = "1LLEGAL"

    """From `database.py`."""

    def test_check_db(self):
        """Test `cd()` of `check_db()` in `database.py`.

        Test 1: Assert warning for `CW` of `ConventionWarning`.
        Test 2: Assert true for database exists.
        Test 3: Assert false for database does not exists.
        Test 4: Assert true for database exist.
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

        test_list_1 = [db_name, False]
        test_list_2 = [db_name_illegal_by_rdb, False]
        test_list_3 = [db_name_illegal_by_this_program, False]

        crd(test_list_1[0])
        test_list_1[len(test_list_1) - 1] = cd(test_list_1[0])
        dd(test_list_1[0])

        test_list_2[len(test_list_2) - 1] = cd(test_list_2[0])

        r.db_create(test_list_3[0]).run(c())
        """Test 1."""
        with self.assertWarns(CW):
            test_list_3[len(test_list_3) - 1] = cd(test_list_3[0])
        r.db_drop(test_list_3[0]).run(c())

        self.assertTrue(test_list_1[len(test_list_1) - 1])  # Test 2.
        self.assertFalse(test_list_2[len(test_list_2) - 1]) # Test 3.
        self.assertTrue(test_list_3[len(test_list_3) - 1])  # Test 4.

if __name__ == "__main__":
    ut.main()