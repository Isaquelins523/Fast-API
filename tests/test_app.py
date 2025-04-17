from http import HTTPStatus


def test_root_deve_retornar_ok_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user_deve_criar_um_novo_usuario(client):
    response = client.post(
        '/users',
        json={
            'username': 'testeusername',
            'email': 'teste@example.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'email': 'teste@example.com',
        'id': 1,
        'username': 'testeusername',
    }


def test_read_users_deve_listar_usuarios(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'teste@example.com',
                'id': 1,
                'username': 'testeusername',
            }
        ]
    }


def test_read_user_deve_listar_um_usuario(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'teste@example.com',
        'id': 1,
        'username': 'testeusername',
    }


def test_read_user_deve_retornar_not_found(client):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User with id 2 not found'}


def test_update_user_deve_atualizar_um_usuario(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste2',
            'email': 'teste@example.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'teste@example.com',
        'id': 1,
        'username': 'teste2',
    }


def test_update_user_deve_retornar_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'teste2',
            'email': 'teste@example.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User with id 2 not found'}


def test_delete_user_deve_deletar_um_usuario(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User with id 1 deleted'}


def test_delete_user_deve_retornar_not_found(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User with id 2 not found'}
