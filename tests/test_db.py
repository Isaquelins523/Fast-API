from sqlalchemy import create_engine

from fast_api.models import User, table_registry


def test_create_user():
    engine = create_engine('sqlite:///database.db')

    table_registry.metadata.create_all(engine)

    user = User(
        username='testuser', email='testemail', password='testpassword'
    )

    assert user.username == 'testuser'
    assert user.email == 'testemail'
    assert user.password == 'testpassword'
