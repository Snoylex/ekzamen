def test_admin_access_categories(admin_client):
    response = admin_client.get('/admin/categories')
    assert response.status_code == 200
    assert 'Категории меню'.encode('utf-8') in response.data

def test_user_cannot_access_admin(client):
    response = client.get('/admin/categories')
    assert response.status_code in [302, 403]

def test_add_category(admin_client):
    response = admin_client.post('/admin/category/add', data={'name': 'Тестовая категория'}, follow_redirects=True)
    assert 'Категория добавлена'.encode('utf-8') in response.data