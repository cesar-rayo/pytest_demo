# PYTEST COMMANDS

Allows to show print statements
```
$ pytest -v -s tests/test_setup_teardown.py
2025-05-20 10:07:35 [    INFO] Executing test 1 (test_setup_teardown.py:23)
Something here
PASSED
```

Set pytest log level
```
$ pytest -v --log_cli_level INFO
```
We can also set `log_cli_format`, `log_cli_date_format`, see `pytest.ini`. The `log_cli = 1` Enables live logging to the console/terminal during test runs
```
$ pytest test_transformers.py
2025-05-22 10:42:42 [    INFO] out: [0.1  1.1  1.21] (test_transformers.py:47)
2025-05-22 10:42:42 [    INFO] expected: [0.1  1.1  1.21] (test_transformers.py:49)
PASSED    
```

Run tests on demand
```
$ pytest -v -s tests
# All files in tests directory

$ pytest -v -s tests/test_assertions.py
# Whole file

$ pytest -v -s tests/test_assertions.py::test_ArrayAssert
# Specific Test

$ pytest -v -s -k "test_ArrayAssert"
tests/test_assertions.py::test_ArrayAssert PASSED

$ pytest -v -s -k "test_D" 
tests/test_assertions.py::test_DictAssert PASSED

$ pytest -v -s -k "test_D or test_ArrayAssert"
tests/test_assertions.py::test_ArrayAssert PASSED
tests/test_assertions.py::test_DictAssert PASSED

$ pytest -v -s -m "smoke"
2025-05-20 11:56:15 [    INFO] 0.30000000000000004 (test_assertions.py:22)
PASSED

$ pytest -v -s -m "regression"
tests/test_assertions.py::test_ArrayAssert PASSED
tests/test_assertions.py::test_DictAssert PASSED

$ pytest -v -s -m "not regression"
```

# Test Coverage
This also takes into account the conditional paths exercised during tests
```
$ pytest --cov tests
Name                                                               Stmts   Miss  Cover
--------------------------------------------------------------------------------------
/Users/crayo/Documents/work/personal/pytest_demo/checkout.py          41      1    98%
/Users/crayo/Documents/work/personal/pytest_demo/files_reader.py      32      2    94%
/Users/crayo/Documents/work/personal/pytest_demo/fizzbuzz.py          10      0   100%
/Users/crayo/Documents/work/personal/pytest_demo/linereader.py         7      0   100%
/Users/crayo/Documents/work/personal/pytest_demo/main.py              28      5    82%
/Users/crayo/Documents/work/personal/pytest_demo/service.py           16      4    75%
conftest.py                                                            5      0   100%
conftest_files.py                                                     18      1    94%
test_assertions.py                                                    26      0   100%
test_checkout.py                                                      38      2    95%
test_conftest.py                                                      21      0   100%
test_csv_reader.py                                                    79      2    97%
test_fixtures.py                                                      33      0   100%
test_fizzbuzz.py                                                      23      0   100%
test_main.py                                                          27      0   100%
test_mocks.py                                                         62      4    94%
test_service.py                                                       14      0   100%
test_setup_teardown.py                                                24      2    92%
test_setup_teardown_2.py                                              27      2    93%
--------------------------------------------------------------------------------------
TOTAL                                                                531     25    95%
```