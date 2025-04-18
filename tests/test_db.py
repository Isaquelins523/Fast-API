from sqlalchemy import select

from fast_api.models import User


def test_create_user(session):
    user = User(
        username='testuser', email='testemail', password='testpassword'
    )
    session.add(user)
    session.commit()

    session.scalar(select(User).where(User.username == 'testuser'))

    assert user.id == 1
    assert user.username == 'testuser'
    assert user.email == 'testemail'
    assert user.password == 'testpassword'
