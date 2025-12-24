import pytest
from app import create_app
from app import mysql as flask_mysql
from werkzeug.security import generate_password_hash
import MySQLdb
from config import Config

@pytest.fixture(scope='session')
def test_db():
    config = {
        'host': Config.MYSQL_HOST,
        'user': Config.MYSQL_USER,
        'password': Config.MYSQL_PASSWORD
    }
    
    conn = MySQLdb.connect(**config)
    cur = conn.cursor()
    
    cur.execute("CREATE DATABASE IF NOT EXISTS georgian_restaurant_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("USE georgian_restaurant_test")
    
    tables_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_admin TINYINT(1) DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
        text TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS dishes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        description TEXT,
        image_path VARCHAR(255),
        category_id INT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    );
    """
    for statement in tables_sql.split(';'):
        if statement.strip():
            cur.execute(statement)
    
    conn.commit()
    
    yield
    
    try:
        cur.execute("DROP DATABASE IF EXISTS georgian_restaurant_test")
        conn.commit()
    except:
        pass
    finally:
        cur.close()
        conn.close()

@pytest.fixture
def app(test_db):
    app = create_app()
    app.config.update({
        'TESTING': True,
        'MYSQL_DB': 'georgian_restaurant_test',
        'SECRET_KEY': 'test_secret',
        'WTF_CSRF_ENABLED': False
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Фикстура для обычного пользователя — без вложенного client
@pytest.fixture
def logged_in_client(client, app):
    with app.app_context():
        cur = flask_mysql.connection.cursor()
        cur.execute("INSERT IGNORE INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    ('testuser', 'test@example.com', generate_password_hash('testpass')))
        flask_mysql.connection.commit()
        cur.close()

    # Логинимся через переданный client
    rv = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert 'Вы успешно вошли'.encode('utf-8') in rv.data

    return client  # Возвращаем тот же client — сессия сохранена

# Фикстура для админа — аналогично
@pytest.fixture
def admin_client(client, app):
    with app.app_context():
        cur = flask_mysql.connection.cursor()
        cur.execute("INSERT IGNORE INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                    ('admin', 'admin@test.com', generate_password_hash('adminpass'), 1))
        flask_mysql.connection.commit()
        cur.close()

    rv = client.post('/auth/login', data={
        'email': 'admin@test.com',
        'password': 'adminpass'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert 'Вы успешно вошли'.encode('utf-8') in rv.data

    return client