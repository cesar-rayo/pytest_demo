import sys
import os
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from service import UserService, ApiClient


def test_get_username_with_mock(mocker):
    # Mock entire APIClient class
    mock_api_client = mocker.Mock(spec=ApiClient)

    # mock return value for get_user_data method
    mock_api_client.get_user_data.return_value = {"id": 1, "name": "Alice"}

    # create UserService object using mocked class
    service = UserService(mock_api_client)

    # execute get_username method from UserService class
    result = service.get_username(1)
    logging.info(result)

    assert result == "ALICE"
    mock_api_client.get_user_data.assert_called_once_with(1)
