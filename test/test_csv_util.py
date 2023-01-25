import unittest
from datetime import datetime

import numpy.testing
from locate import this_dir
from numpy import nan

from aa_py_csv import query_csv

data_dir = this_dir().parent.joinpath("test_data", "csv_util")


class TestQueryCsv(unittest.TestCase):
    def test_escape_formulas_true(self) -> None:
        path = data_dir.joinpath("test_escape_formulas.csv")
        df = query_csv(
            input_file_path=path,
            pandas_kwargs={},
            sql_query=None,
            escape_formulas=True,
        )
        self.assertEqual(
            [
                ["foo", "bar", "baz"],
                ["asdf", "'=nope", True],
                ["'=[what]", "qwerty", nan],
            ],
            [list(df.columns), *df.values.tolist()],
        )

    def test_escape_formulas_false(self) -> None:
        path = data_dir.joinpath("test_escape_formulas.csv")
        df = query_csv(
            input_file_path=path,
            pandas_kwargs={},
            sql_query=None,
            escape_formulas=False,
        )
        self.assertEqual(
            [
                ["foo", "bar", "baz"],
                ["asdf", "=nope", True],
                ["=[what]", "qwerty", nan],
            ],
            [list(df.columns), *df.values.tolist()],
        )

    def test_sql_query_full(self) -> None:
        path = data_dir.joinpath("test_sql_query.csv")
        df = query_csv(
            input_file_path=path,
            pandas_kwargs={},
            sql_query="SELECT a,b FROM df WHERE c>3",
            escape_formulas=False,
        )
        self.assertEqual(
            [["a", "b"], [2, 3], [3, 4]],
            [list(df.columns), *df.values.tolist()],
        )

    def test_pandas_kwargs_baseline(self) -> None:
        path = data_dir.joinpath("test_pandas_kwargs.csv")
        df = query_csv(
            input_file_path=path,
            pandas_kwargs={},
            sql_query=None,
            escape_formulas=False,
        )
        self.assertEqual(
            [
                ["a", "b", "c"],
                [1, "20221003T182105", True],
                [2, "20221003T182106", False],
                [3, "20221003T182107", nan],
            ],
            [list(df.columns), *df.values.tolist()],
        )

    def test_pandas_kwargs_parse_dates(self) -> None:
        path = data_dir.joinpath("test_pandas_kwargs.csv")
        df = query_csv(
            input_file_path=path,
            pandas_kwargs={"parse_dates": ["b"]},
            sql_query=None,
            escape_formulas=False,
        )
        self.assertEqual(
            [
                ["a", "b", "c"],
                [1, datetime(2022, 10, 3, 18, 21, 5), True],
                [2, datetime(2022, 10, 3, 18, 21, 6), False],
                [3, datetime(2022, 10, 3, 18, 21, 7), nan],
            ],
            [list(df.columns), *df.values.tolist()],
        )

    def test_extra_commas(self) -> None:
        # The default should be `index_col=False`, even when we supply no `pandas_kwargs`.
        path = data_dir.joinpath("test_extra_commas.csv")
        df = query_csv(
            input_file_path=path,
            pandas_kwargs={},
            sql_query=None,
            escape_formulas=True,
        )
        self.assertEqual(
            [["a", "b", "c"], [1, 2, 3], [2, 3, 4], [3, 4, 5]],
            [list(df.columns), *df.values.tolist()],
        )

        # We can still set `index_col=None` if we really wanted to, although that is very unlikely.
        file_path = data_dir.joinpath("test_extra_commas.csv")
        df1 = query_csv(
            input_file_path=file_path,
            pandas_kwargs={"index_col": None},
            sql_query=None,
            escape_formulas=True,
        )
        numpy.testing.assert_equal(
            actual=[list(df1.columns), *df1.values.tolist()],
            desired=[
                ["a", "b", "c"],
                [3.0, nan, nan],
                [4.0, nan, nan],
                [5.0, nan, nan],
            ],
        )

    def test_encoding(self) -> None:
        path_latin = data_dir.joinpath("test_latin1.csv")
        path_utf8 = data_dir.joinpath("test_utf8.csv")

        with self.subTest("Read latin1 file with latin1 encoding"):

            df = query_csv(
                input_file_path=path_latin,
                pandas_kwargs={"encoding": "latin1"},
                sql_query=None,
                escape_formulas=False,
            )
            self.assertEqual(
                [["a", "b"], [1, "þ"], [2, "ß"], [3, "æ"]],
                [list(df.columns), *df.values.tolist()],
            )

        with self.subTest("Read latin1 file with utf-8 encoding"):
            with self.assertRaisesRegex(
                UnicodeDecodeError,
                r"'utf-8' codec can't decode byte (.*) in position (\d+): invalid start byte",
            ):
                query_csv(
                    input_file_path=path_latin,
                    pandas_kwargs={"encoding": "utf-8"},
                    sql_query=None,
                    escape_formulas=False,
                )

        with self.subTest("Read latin1 file with auto encoding"):
            df = query_csv(
                input_file_path=path_latin,
                pandas_kwargs={"encoding": "auto"},
                sql_query=None,
                escape_formulas=False,
            )
            self.assertEqual(
                [["a", "b"], [1, "þ"], [2, "ß"], [3, "æ"]],
                [list(df.columns), *df.values.tolist()],
            )

        with self.subTest("Read utf-8 file with auto encoding"):
            df = query_csv(
                input_file_path=path_utf8,
                pandas_kwargs={"encoding": "auto"},
                sql_query=None,
                escape_formulas=False,
            )

            self.assertEqual(
                [["a", "b"], [1, "þ"], [2, "ß"], [3, "æ"]],
                [list(df.columns), *df.values.tolist()],
            )

        with self.subTest("Read utf-8 file with latin encoding"):
            df = query_csv(
                input_file_path=path_utf8,
                pandas_kwargs={"encoding": "latin-1"},
                sql_query=None,
                escape_formulas=False,
            )

            # Mojibake result
            self.assertEqual(
                [["a", "b"], [1, "Ã¾"], [2, "Ã\x9f"], [3, "Ã¦"]],
                [list(df.columns), *df.values.tolist()],
            )


if __name__ == "__main__":
    unittest.main(
        failfast=True,
    )
