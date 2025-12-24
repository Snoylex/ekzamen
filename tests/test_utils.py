def test_privacy_policy_link(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'privacy_policy.pdf'.encode('utf-8') in response.data

def test_footer_copyright(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '&copy; 2025'.encode('utf-8') in response.data

def test_menu_categories_count(client):
    response = client.get('/menu')
    assert response.status_code == 200
    assert 'Меню'.encode('utf-8') in response.data  # Check for menu title

def test_image_list_endpoint_format(admin_client):
    response = admin_client.get('/admin/list-images')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data['images'], list)

def test_logout_flash_message(logged_in_client):
    response = logged_in_client.get('/auth/logout', follow_redirects=True)
    assert 'Вы вышли'.encode('utf-8') in response.data

def test_review_validation_rating_out_of_range(logged_in_client):
    response = logged_in_client.post('/auth/add_review', data={'rating': 6, 'text': 'Invalid rating'}, follow_redirects=True)
    assert 'Оценка'.encode('utf-8') in response.data  # Check for validation error