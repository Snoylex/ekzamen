def test_privacy_policy_link_in_footer(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'privacy_policy.pdf'.encode('utf-8') in response.data
    assert 'Согласие на обработку персональных данных'.encode('utf-8') in response.data

def test_edit_dish(admin_client):
    # Сначала добавляем категорию и блюдо
    admin_client.post('/admin/category/add', data={'name': 'Тестовая'}, follow_redirects=True)
    admin_client.post('/admin/dish/add', data={
        'name': 'Старое блюдо',
        'price': '100',
        'image_path': 'images/old.jpg',
        'category_id': '1',
        'description': 'Старое описание'
    }, follow_redirects=True)
    
    # Получаем страницу блюд и находим ID последнего блюда (упрощённо проверяем наличие)
    response = admin_client.get('/admin/dishes')
    assert 'Старое блюдо'.encode('utf-8') in response.data
    
    # Редактируем (предполагаем, что ID = 1 — в тестовой БД он будет первым)
    response = admin_client.post('/admin/dish/edit/1', data={
        'name': 'Новое блюдо',
        'price': '200',
        'image_path': 'images/new.jpg',
        'category_id': '1',
        'description': 'Новое описание'
    }, follow_redirects=True)
    
    assert 'Блюдо обновлено'.encode('utf-8') in response.data
    assert 'Новое блюдо'.encode('utf-8') in response.data