def test_admin_access_dishes(admin_client):
    response = admin_client.get('/admin/dishes')
    assert response.status_code == 200

def test_add_dish(admin_client):
    admin_client.post('/admin/category/add', data={'name': 'Тест'}, follow_redirects=True)
    response = admin_client.post('/admin/dish/add', data={
        'name': 'Тестовое блюдо',
        'price': '500',
        'image_path': 'images/test.jpg',
        'category_id': '1',
        'description': 'Вкусно'
    }, follow_redirects=True)
    assert 'Блюдо добавлено'.encode('utf-8') in response.data

def test_list_images_endpoint(admin_client):
    response = admin_client.get('/admin/list-images')
    assert response.status_code == 200
    data = response.get_json()
    assert 'images' in data