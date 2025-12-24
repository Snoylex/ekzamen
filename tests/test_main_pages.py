def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Кущай вкусно'.encode('utf-8') in response.data

def test_menu_page(client):
    response = client.get('/menu')
    assert response.status_code == 200