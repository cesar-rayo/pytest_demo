import sqlite3
from unittest.mock import MagicMock


def db_connect(dns):
    conn = sqlite3.connect(dns, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


class DBClient:
    def __init__(self, dns):
        self.conn = db_connect(dns)

    def metrics(self, start_time, end_time):
        params = {"start": start_time, "end": end_time}
        sql_query = "SELECT * FROM metrics where time >= :start AND time <= :end"
        return self.conn.execute(sql_query, params)


data = [
    {"time": "2021-07-13T14:36:52.380Z", "metric": "mem", "value": 227551548.0},
    {"time": "2021-07-13T14:36:52.380Z", "metric": "cpu", "value": 30.04},
    {"time": "2021-07-13T14:36:53.337Z", "metric": "mem", "value": 227567864.0},
    {"time": "2021-07-13T14:36:53.337Z", "metric": "cpu", "value": 30.93},
    {"time": "2021-07-13T14:36:54.294Z", "metric": "mem", "value": 227574696.0},
    {"time": "2021-07-13T14:36:54.294Z", "metric": "cpu", "value": 32.61},
    {"time": "2021-07-13T14:36:55.251Z", "metric": "mem", "value": 227567135.0},
    {"time": "2021-07-13T14:36:55.251Z", "metric": "cpu", "value": 32.24},
    {"time": "2021-07-13T14:36:56.208Z", "metric": "mem", "value": 227561333.0},
    {"time": "2021-07-13T14:36:56.208Z", "metric": "cpu", "value": 31.27},
    {"time": "2021-07-13T14:36:57.165Z", "metric": "cpu", "value": 31.33},
    {"time": "2021-07-13T14:36:57.165Z", "metric": "mem", "value": 227586440.0},
]


class TestDBClient:
    def test_metrics_monkeypatch(self, monkeypatch):
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_conn
        mock_conn.execute.return_value = data
        # Import the method we want to mock 'test_mock_db.db_connect' so it returns 'mock_conn'
        # similar to 'def test_mock_db.db_connect(dns): return mock_conn'
        monkeypatch.setattr('test_mock_db.db_connect', lambda dns: mock_conn)

        client = DBClient('random_path')
        rows = client.metrics('2021-07-13', '2021-07-14')
        assert mock_conn.execute.called
        assert len(rows) == len(data)
