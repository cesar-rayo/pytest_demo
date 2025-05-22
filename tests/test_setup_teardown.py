import logging


def setup_module(module):
    logging.info(f">>Setup Module")


def teardown_module(module):
    logging.info(f">>Teardown Module")


def setup_function(function):
    if function == test1:
        logging.info("Setup test 1")
    elif function == test2:
        logging.info("Setup test 2")
    else:
        logging.info("Default test setup")


def teardown_function(function):
    if function == test1:
        logging.info("Teardown test 1")
    elif function == test2:
        logging.info("Teardown test 2")
    else:
        logging.info("Default test teardown")


def test1():
    logging.info("Executing test 1")
    print("Something here")
    assert True


def test2():
    logging.info("Executing test 2")
    assert True
