def test_add_review(logged_in_client):
    response = logged_in_client.post('/auth/add_review', data={'rating': 5, 'text': 'Отличный ресторан!'}, follow_redirects=True)
    assert 'Ваш отзыв добавлен'.encode('utf-8') in response.data

def test_add_review_unauthorized(client):
    response = client.post('/auth/add_review', follow_redirects=True)
    assert 'Пожалуйста, войдите'.encode('utf-8') in response.data

def test_edit_own_review(logged_in_client):
    logged_in_client.post('/auth/add_review', data={'rating': 4, 'text': 'Хорошо'})
    response = logged_in_client.get('/reviews')
    assert 'Изменить'.encode('utf-8') in response.data

def test_delete_own_review(logged_in_client):
    logged_in_client.post('/auth/add_review', data={'rating': 5, 'text': 'Буду удалять'})
    response = logged_in_client.get('/reviews')
    assert 'Удалить'.encode('utf-8') in response.data
