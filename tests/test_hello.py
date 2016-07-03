import pytest
import PhoenixNow

@pytest.fixture
def app():
    return PhoenixNow.app.test_client()

def test_hello(app):
    rv = app.get('/')
    assert b"hello" in rv.data
