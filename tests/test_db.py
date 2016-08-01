import pytest

@pytest.fixture
def app():
    from PhoenixNow.config import Config
    from PhoenixNow import create_app

    class TestingConfig(Config):
        TESTING = True

    return create_app(TestingConfig)

def test_db_add(app):
    from PhoenixNow.model import db, User

    with app.app_context():
        user = User(name='John Smith', password='password123',
                email='johnsmith@gmail.com')

        db.session.add(user)
        db.session.commit()

        # User.id will change when successfully stored in db
        assert user.id > 0

        db.session.delete(user)
        db.session.commit()

        assert len(User.query.all()) == 0
