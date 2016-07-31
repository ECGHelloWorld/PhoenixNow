import pytest

@pytest.fixture
def app():
    from PhoenixNow.config import Config
    from PhoenixNow import create_app

    class TestingConfig(Config):
        TESTING = True

    return create_app(TestingConfig).test_client()

def test_hello(app):
    rv = app.get('/hello')
    assert b"hello" in rv.data
