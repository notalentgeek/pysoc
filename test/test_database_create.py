from database          import conn                    as c
from database          import create_db               as crd
from database          import create_doc              as crdoc
from database          import create_table            as crt
from database          import del_db                  as dd
from exception_warning import CreationDeletionWarning as CDW
import rethinkdb as r
import sys
import unittest  as ut

class test(ut.TestCase):
    ILLEGAL_BY_RDB          = "!LLEGAL"
    ILLEGAL_BY_THIS_PROGRAM = "1LLEGAL"

    """From `database.py`."""

    def test_create_db(self):
        """Test `crd()` of `create_db()` in `database.py`.

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
        


    def test_create_table(self):
        """Test `crt()` of `create_table()` in `database.py`.

        Test 1: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 2: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 3: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 4: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 5: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 6: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 7: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 8: Assert warning for `CDW` of `CreationDeletionWarning`.
        Test 9: Assert not none for valid `crt()` object.
        Test 10: Assert none for counterfeit `crt()` object.
        Test 11: Assert none for counterfeit `crt()` object.
        Test 12: Assert none for counterfeit `crt()` object.
        Test 13: Assert none for counterfeit `crt()` object.
        Test 14: Assert none for counterfeit `crt()` object.
        Test 15: Assert none for counterfeit `crt()` object.
        Test 16: Assert none for counterfeit `crt()` object.
        Test 17: Assert none for counterfeit `crt()` object.
        Test 18: Assert none for counterfeit `crt()` object.
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
        table_name = "{}_{}".format(function_name, "table")
        table_name_illegal_by_rdb = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_RDB
        )
        table_name_illegal_by_this_program = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )

        test_list_1 = [
            db_name,
            table_name,
            None,
            None
        ]
        test_list_2 = [
            db_name,
            table_name_illegal_by_rdb,
            None
        ]
        test_list_3 = [
            db_name,
            table_name_illegal_by_this_program,
            None
        ]
        test_list_4 = [
            db_name_illegal_by_rdb,
            table_name,
            None
        ]
        test_list_5 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_rdb,
            None
        ]
        test_list_6 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_this_program,
            None
        ]
        test_list_7 = [
            db_name_illegal_by_this_program,
            table_name,
            None
        ]
        test_list_8 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_rdb,
            None
        ]
        test_list_9 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_this_program,
            None
        ]

        crd(test_list_1[0])
        test_list_1[len(test_list_1) - 1] = crt(test_list_1[1], test_list_1[0])
        test_list_1[len(test_list_1) - 2] = crt(test_list_1[1], test_list_1[0])
        dd(test_list_1[0])

        crd(test_list_2[0])
        """Test 1."""
        with self.assertWarns(CDW):
            test_list_2[len(test_list_2) - 1] = crt(
                test_list_2[1],
                test_list_2[0]
            )
        dd(test_list_2[0])

        crd(test_list_3[0])
        """Test 2."""
        with self.assertWarns(CDW):
            test_list_3[len(test_list_3) - 1] = crt(
                test_list_3[1],
                test_list_3[0]
            )
        dd(test_list_3[0])

        """Test 3."""
        with self.assertWarns(CDW):
            test_list_4[len(test_list_4) - 1] = crt(
                test_list_4[1],
                test_list_4[0]
            )

        """Test 4."""
        with self.assertWarns(CDW):
            test_list_5[len(test_list_5) - 1] = crt(
                test_list_5[1],
                test_list_5[0]
            )

        """Test 5."""
        with self.assertWarns(CDW):
            test_list_6[len(test_list_6) - 1] = crt(
                test_list_6[1],
                test_list_6[0]
            )

        r.db_create(test_list_7[0]).run(c())
        """Test 6."""
        with self.assertWarns(CDW):
            test_list_7[len(test_list_7) - 1] = crt(
                test_list_7[1],
                test_list_7[0]
            )
        r.db_drop(test_list_7[0]).run(c())

        r.db_create(test_list_8[0]).run(c())
        """Test 7."""
        with self.assertWarns(CDW):
            test_list_8[len(test_list_8) - 1] = crt(
                test_list_8[1],
                test_list_8[0]
            )
        r.db_drop(test_list_8[0]).run(c())

        r.db_create(test_list_9[0]).run(c())
        """Test 8."""
        with self.assertWarns(CDW):
            test_list_9[len(test_list_9) - 1] = crt(
                test_list_9[1],
                test_list_9[0]
            )
        r.db_drop(test_list_9[0]).run(c())

        self.assertIsNotNone(test_list_1[len(test_list_1) - 1]) # Test 9.
        self.assertIsNone(test_list_1[len(test_list_1) - 2])    # Test 10.
        self.assertIsNone(test_list_2[len(test_list_2) - 1])    # Test 11.
        self.assertIsNone(test_list_3[len(test_list_3) - 1])    # Test 12.
        self.assertIsNone(test_list_4[len(test_list_4) - 1])    # Test 13.
        self.assertIsNone(test_list_5[len(test_list_5) - 1])    # Test 14.
        self.assertIsNone(test_list_6[len(test_list_6) - 1])    # Test 15.
        self.assertIsNone(test_list_7[len(test_list_7) - 1])    # Test 16.
        self.assertIsNone(test_list_8[len(test_list_8) - 1])    # Test 17.
        self.assertIsNone(test_list_9[len(test_list_9) - 1])    # Test 18.



    def test_create_doc(self):
        """Test `crdoc()` of `create_doc()` in `database.py`.

        Test 1: Assert not none for valid `crt()` object.
        Test 2: Assert none for counterfeit `crt()` object.
        Test 3: Assert not none for valid `crt()` object.
        Test 4: Assert none for counterfeit `crt()` object.
        Test 5: Assert not none for valid `crt()` object.

        DONE: Create assert warning for invalid database and table.
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
        table_name = "{}_{}".format(function_name, "table")
        table_name_illegal_by_rdb = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_RDB
        )
        table_name_illegal_by_this_program = "{}_{}".format(
            table_name,
            self.ILLEGAL_BY_THIS_PROGRAM
        )
        doc_1 = {"name": "alpha", "no":"1"}
        doc_2 = {"name": "beta", "no":"2"}
        doc_3 = {"name": "charlie", "no":"1"}
        doc_4 = {"name": "charlie", "no":"3"}

        test_list_1 = [
            db_name,
            table_name,
            doc_1,
            ["no"],
            None,
            None
        ]
        test_list_2 = [
            test_list_1[0],
            test_list_1[1],
            doc_2,
            ["no"],
            None
        ]
        test_list_3 = [
            test_list_1[0],
            test_list_1[1],
            doc_3,
            ["no"],
            None
        ]
        test_list_4 = [
            test_list_1[0],
            test_list_1[1],
            doc_4,
            ["name", "no"],
            None
        ]
        test_list_5 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_rdb,
            doc_1,
            None
        ]
        test_list_6 = [
            db_name_illegal_by_rdb,
            table_name_illegal_by_this_program,
            doc_1,
            None
        ]
        test_list_7 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_rdb,
            doc_1,
            None
        ]
        test_list_8 = [
            db_name_illegal_by_this_program,
            table_name_illegal_by_this_program,
            doc_1,
            None
        ]

        crd(test_list_1[0])
        crt(test_list_1[1], test_list_1[0])
        test_list_1[len(test_list_2) - 1] = crdoc(
            test_list_1[2],
            test_list_1[1],
            test_list_1[0]
        )
        test_list_1[len(test_list_2) - 2] = crdoc(
            test_list_1[2],
            test_list_1[1],
            test_list_1[0],
            test_list_1[3]
        )
        test_list_2[len(test_list_2) - 1] = crdoc(
            test_list_2[2],
            test_list_2[1],
            test_list_2[0],
            test_list_2[3]
        )
        crt(test_list_3[1], test_list_3[0])
        test_list_3[len(test_list_3) - 1] = crdoc(
            test_list_3[2],
            test_list_3[1],
            test_list_3[0],
            test_list_3[3]
        )
        test_list_4[len(test_list_4) - 1] = crdoc(
            test_list_4[2],
            test_list_4[1],
            test_list_4[0],
            test_list_4[3]
        )
        dd(test_list_1[0])

        """Test 1."""
        with self.assertWarns(CDW):
            test_list_5[len(test_list_5) - 1] = crdoc(
                test_list_5[2],
                test_list_5[1],
                test_list_5[0]
            )

        """Test 2."""
        with self.assertWarns(CDW):
            test_list_6[len(test_list_6) - 1] = crdoc(
                test_list_6[2],
                test_list_6[1],
                test_list_6[0]
            )

        r.db_create(test_list_7[0]).run(c())
        """Test 3."""
        with self.assertWarns(CDW):
            test_list_7[len(test_list_7) - 1] = crdoc(
                test_list_7[2],
                test_list_7[1],
                test_list_7[0]
            )
        r.db_drop(test_list_7[0]).run(c())

        r.db_create(test_list_8[0]).run(c())
        r.db(test_list_8[0]).table_create(test_list_8[0]).run(c())
        """Test 4."""
        with self.assertWarns(CDW):
            test_list_8[len(test_list_8) - 1] = crdoc(
                test_list_8[2],
                test_list_8[1],
                test_list_8[0]
            )
        r.db_drop(test_list_8[0]).run(c())

        self.assertIsNotNone(test_list_1[len(test_list_2) - 1]) # Test 5.
        self.assertIsNone(test_list_1[len(test_list_2) - 2])    # Test 6.
        self.assertIsNotNone(test_list_2[len(test_list_2) - 1]) # Test 7.
        self.assertIsNone(test_list_3[len(test_list_3) - 1])    # Test 8.
        self.assertIsNotNone(test_list_4[len(test_list_4) - 1]) # Test 9.
        self.assertIsNone(test_list_5[len(test_list_5) - 1])    # Test 10.
        self.assertIsNone(test_list_6[len(test_list_6) - 1])    # Test 11.
        self.assertIsNone(test_list_7[len(test_list_7) - 1])    # Test 12.
        self.assertIsNone(test_list_8[len(test_list_8) - 1])    # Test 13.

if __name__ == "__main__":
    ut.main()