import logging


class TestClass:
    @classmethod
    def setup_class(cls):
        logging.info("Setup Class")

    @classmethod
    def teardown_class(cls):
        logging.info("Teardown Class")

    def setup_method(self, method):
        if method == self.test1:
            logging.info("Setup Test 1")
        elif method == self.test2:
            logging.info("Setup Test 2")
        else:
            logging.info("Default setup")

    def teardown_method(self, method):
        if method == self.test1:
            logging.info("Teardown Test 1")
        elif method == self.test2:
            logging.info("Teardown Test 2")
        else:
            logging.info("Default teardown")

    def test1(self):
        logging.info("Executing test 1")
        print("Something here")
        assert True

    def test2(self):
        logging.info("Executing test 2")
        assert True
