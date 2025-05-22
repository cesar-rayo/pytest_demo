import pytest
import logging


@pytest.fixture()
def setup():
    logging.info("Executing fixture 1")
    yield "Fixture 1 answer"
    logging.info("Finish fixture 1")


def teardown_a():
    logging.info("Teardown A")


def teardown_b():
    logging.info("Teardown B")


# scope = [session, module, class, function]
@pytest.fixture(scope="module", autouse=True)
def setup2(request):
    logging.info("Executing fixture 2")
    yield "Fixture 2 answer"
    logging.info("Finish fixture 2")
    request.addfinalizer(teardown_a)
    request.addfinalizer(teardown_b)


@pytest.fixture(params=[1, 2, 3])
def setup3(request):
    parameter = request.param
    logging.info(f"Setup3 Fixture: {parameter}")
    return parameter


def test1(setup):
    logging.info(f"{setup} test 1")
    assert True


def test2(setup, setup2):
    logging.info(f"{setup} test 2")
    logging.info(f"{setup2} test 2")
    assert True


def test3(setup3):
    logging.info(f"Test 3 : {setup3}")
    assert True
