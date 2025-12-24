from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import mysql
from .forms import RegisterForm, LoginForm, ReviewForm
from collections import defaultdict
import os

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Декоратор для проверки админа
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ============================
# Основные страницы
# ============================

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/menu')
def menu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cur.fetchall()

    cur.execute("""
        SELECT d.id, d.name, d.price, d.description, d.image_path, d.category_id
        FROM dishes d JOIN categories c ON d.category_id = c.id
        ORDER BY c.name, d.name
    """)
    dishes = cur.fetchall()
    cur.close()

    dishes_by_category = defaultdict(list)
    for dish in dishes:
        dishes_by_category[dish['category_id']].append(dish)

    return render_template('menu.html', categories=categories, dishes_by_category=dishes_by_category)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/reviews')
def reviews():
    # Получаем параметр сортировки из URL (?sort=date_desc, rating_asc и т.д.)
    sort = request.args.get('sort', 'date_desc')  # По умолчанию — по дате убывание
    
    cur = mysql.connection.cursor()
    
    # Базовый запрос
    base_query = """
        SELECT r.id, r.rating, r.text, r.created_at, u.username, u.id AS user_id
        FROM reviews r 
        JOIN users u ON r.user_id = u.id
    """
    
    # Определяем сортировку
    if sort == 'date_desc':
        order_by = "ORDER BY r.created_at DESC"
    elif sort == 'date_asc':
        order_by = "ORDER BY r.created_at ASC"
    elif sort == 'rating_desc':
        order_by = "ORDER BY r.rating DESC, r.created_at DESC"
    elif sort == 'rating_asc':
        order_by = "ORDER BY r.rating ASC, r.created_at DESC"
    else:
        order_by = "ORDER BY r.created_at DESC"  # fallback
    
    cur.execute(f"{base_query} {order_by}")
    reviews_list = cur.fetchall()
    
    # Средний рейтинг и количество
    cur.execute("SELECT COUNT(*) AS count, AVG(rating) AS avg_rating FROM reviews")
    stats = cur.fetchone()
    cur.close()
    
    total_reviews = stats['count'] or 0
    average_rating = round(stats['avg_rating'], 1) if stats['avg_rating'] else 0.0
    
    return render_template(
        'reviews.html',
        reviews=reviews_list,
        total_reviews=total_reviews,
        average_rating=average_rating,
        current_sort=sort  # Передаём текущую сортировку в шаблон
    )
# ============================
# Аутентификация и отзывы пользователей
# ============================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (form.email.data,))
        if cur.fetchone():
            flash('Этот email уже зарегистрирован.', 'danger')
            cur.close()
            return render_template('auth/register.html', form=form)

        hashed = generate_password_hash(form.password.data)
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (form.username.data, form.email.data, hashed))
        mysql.connection.commit()
        cur.close()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password_hash, is_admin FROM users WHERE email = %s", (form.email.data,))
        user_data = cur.fetchone()
        cur.close()

        if user_data and check_password_hash(user_data['password_hash'], form.password.data):
            from .models import User
            user = User(user_data['id'], user_data['username'], user_data['email'], user_data['is_admin'])
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('main.index'))
        flash('Неверный email или пароль.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews (user_id, rating, text) VALUES (%s, %s, %s)",
                    (current_user.id, form.rating.data, form.text.data))
        mysql.connection.commit()
        cur.close()
        flash('Ваш отзыв добавлен!', 'success')
        return redirect(url_for('main.reviews'))
    return render_template('auth/add_review.html', form=form)

# Редактирование своего отзыва
@auth_bp.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, rating, text FROM reviews WHERE id = %s AND user_id = %s", (review_id, current_user.id))
    review = cur.fetchone()

    if not review:
        flash('Отзыв не найден или не принадлежит вам.', 'danger')
        cur.close()
        return redirect(url_for('main.reviews'))

    form = ReviewForm()
    if form.validate_on_submit():
        cur.execute("UPDATE reviews SET rating = %s, text = %s WHERE id = %s AND user_id = %s",
                    (form.rating.data, form.text.data, review_id, current_user.id))
        mysql.connection.commit()
        cur.close()
        flash('Отзыв обновлён!', 'success')
        return redirect(url_for('main.reviews'))

    if request.method == 'GET':
        form.rating.data = review['rating']
        form.text.data = review['text']

    cur.close()
    return render_template('auth/edit_review.html', form=form)

# Удаление своего отзыва
@auth_bp.route('/delete_review/<int:review_id>')
@login_required
def delete_review_user(review_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM reviews WHERE id = %s AND user_id = %s", (review_id, current_user.id))
    deleted = cur.rowcount > 0
    mysql.connection.commit()
    cur.close()

    if deleted:
        flash('Ваш отзыв удалён.', 'info')
    else:
        flash('Отзыв не найден или не принадлежит вам.', 'danger')
    return redirect(url_for('main.reviews'))

# ============================
# Админ-панель
# ============================

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/categories')
@admin_required
def admin_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cur.fetchall()
    cur.close()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/category/add', methods=['GET', 'POST'])
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name:
            cur = mysql.connection.cursor()
            try:
                cur.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
                mysql.connection.commit()
                flash('Категория добавлена', 'success')
            except:
                flash('Категория уже существует', 'danger')
            cur.close()
        return redirect(url_for('admin.admin_categories'))
    return render_template('admin/category_form.html', title='Добавить категорию')

@admin_bp.route('/category/edit/<int:cat_id>', methods=['GET', 'POST'])
@admin_required
def edit_category(cat_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name:
            cur.execute("UPDATE categories SET name = %s WHERE id = %s", (name, cat_id))
            mysql.connection.commit()
            flash('Категория обновлена', 'success')
        cur.close()
        return redirect(url_for('admin.admin_categories'))

    cur.execute("SELECT * FROM categories WHERE id = %s", (cat_id,))
    category = cur.fetchone()
    cur.close()
    return render_template('admin/category_form.html', title='Редактировать категорию', category=category)

@admin_bp.route('/category/delete/<int:cat_id>')
@admin_required
def delete_category(cat_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM categories WHERE id = %s", (cat_id,))
    mysql.connection.commit()
    cur.close()
    flash('Категория удалена', 'warning')
    return redirect(url_for('admin.admin_categories'))

@admin_bp.route('/dishes')
@admin_required
def admin_dishes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()
    cur.execute("""
        SELECT d.id, d.name, d.price, d.description, d.image_path, c.name as category_name
        FROM dishes d JOIN categories c ON d.category_id = c.id
        ORDER BY c.name, d.name
    """)
    dishes = cur.fetchall()
    cur.close()
    return render_template('admin/dishes.html', dishes=dishes, categories=categories)

@admin_bp.route('/dish/add', methods=['GET', 'POST'])
@admin_required
def add_dish():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form.get('description', '')
        image_path = request.form['image_path']
        category_id = request.form['category_id']
        cur.execute("""
            INSERT INTO dishes (name, price, description, image_path, category_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, price, description, image_path, category_id))
        mysql.connection.commit()
        flash('Блюдо добавлено', 'success')
        cur.close()
        return redirect(url_for('admin.admin_dishes'))
    cur.close()
    return render_template('admin/dish_form.html', title='Добавить блюдо', categories=categories)

@admin_bp.route('/dish/edit/<int:dish_id>', methods=['GET', 'POST'])
@admin_required
def edit_dish(dish_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form.get('description', '')
        image_path = request.form['image_path']
        category_id = request.form['category_id']
        cur.execute("""
            UPDATE dishes SET name=%s, price=%s, description=%s, image_path=%s, category_id=%s
            WHERE id=%s
        """, (name, price, description, image_path, category_id, dish_id))
        mysql.connection.commit()
        flash('Блюдо обновлено', 'success')
        cur.close()
        return redirect(url_for('admin.admin_dishes'))

    cur.execute("SELECT * FROM dishes WHERE id = %s", (dish_id,))
    dish = cur.fetchone()
    cur.close()
    return render_template('admin/dish_form.html', title='Редактировать блюдо', dish=dish, categories=categories)

@admin_bp.route('/dish/delete/<int:dish_id>')
@admin_required
def delete_dish(dish_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dishes WHERE id = %s", (dish_id,))
    mysql.connection.commit()
    cur.close()
    flash('Блюдо удалено', 'warning')
    return redirect(url_for('admin.admin_dishes'))

@admin_bp.route('/reviews')
@admin_required
def list_admin_reviews():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT r.id, r.rating, r.text, r.created_at, u.username
        FROM reviews r JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
    """)
    reviews = cur.fetchall()
    cur.close()
    return render_template('admin/reviews.html', reviews=reviews)

@admin_bp.route('/review/delete/<int:review_id>')
@admin_required
def delete_review(review_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
    mysql.connection.commit()
    cur.close()
    flash('Отзыв удалён', 'warning')
    return redirect(url_for('admin.list_admin_reviews'))

# ============================
# Выбор изображений для админки
# ============================

@admin_bp.route('/list-images')
@admin_required
def list_images():
    static_folder = current_app.static_folder
    images_dir = os.path.join(static_folder, 'images')

    print(f"[DEBUG] Поиск изображений в: {images_dir}")

    if not os.path.exists(images_dir):
        print("[ERROR] Папка static/images/ не найдена")
        return jsonify({'images': [], 'error': 'Папка static/images/ не существует'}), 404

    try:
        files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
        files.sort(key=str.lower)
        print(f"[DEBUG] Найдено файлов: {len(files)} — {files}")
        return jsonify({'images': files})
    except Exception as e:
        print(f"[ERROR] Ошибка чтения папки: {e}")
        return jsonify({'images': [], 'error': 'Ошибка доступа к папке изображений'}), 500