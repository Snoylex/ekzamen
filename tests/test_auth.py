def test_register(client):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'pass123',
        'confirm': 'pass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Регистрация успешна'.encode('utf-8') in response.data

def test_register_invalid_password(client):
    response = client.post('/auth/register', data={
        'username': 'invalid',
        'email': 'invalid@example.com',
        'password': 'short',  # Short password to trigger validation error
        'confirm': 'short'
    })
    assert 'Пароль'.encode('utf-8') in response.data  # Check for password error message in form
def test_login_wrong_password(client):
    client.post('/auth/register', data={'username': 'wrong', 'email': 'wrong@example.com', 'password': 'correct', 'confirm': 'correct'})
    response = client.post('/auth/login', data={'email': 'wrong@example.com', 'password': 'wrong'})
    assert 'Неверный email или пароль'.encode('utf-8') in response.data

def test_logout(logged_in_client):
    response = logged_in_client.get('/auth/logout', follow_redirects=True)
    assert 'Вы вышли'.encode('utf-8') in response.data

def test_access_protected_without_login(client):
    response = client.get('/auth/add_review')
    assert response.status_code == 302