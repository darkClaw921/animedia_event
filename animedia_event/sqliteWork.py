import sqlite3

# Создание базы данных и подключение к ней
conn = sqlite3.connect('users_links.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
)
''')

# Создание таблицы ссылок
cursor.execute('''
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    url TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Функция для создания пользователя с проверкой существования
def create_user(user_id,username):
    cursor=conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = ? OR username = ?', (user_id, username))
    user = cursor.fetchone()
    if user:
        print(f'User with id {user_id} or username "{username}" already exists.')
        # conn.close()
        return user[0]  # Возвращаем id существующего пользователя
    else:
        cursor.execute('INSERT INTO users (id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        # conn.close()
        return user_id  # Возвращаем id нового пользователя
    

# Функция для добавления ссылки пользователю
def add_link(user_id, url):
    cursor=conn.cursor()
    cursor.execute('INSERT INTO links (user_id, url) VALUES (?, ?)', (user_id, url,))
    conn.commit()
    # conn.close()

# Функция для получения всех ссылок пользователя
def get_user_links(user_id):
    cursor=conn.cursor()
    cursor.execute('SELECT url FROM links WHERE user_id = ?', (user_id,))
    links = cursor.fetchall()
    conn.close()
    return [link[0] for link in links]

# Пример использования функций
# alice_id = create_user('Alice')
# bob_id = create_user('Bob')

# # Добавление ссылок пользователю Alice
# add_link(alice_id, 'https://example.com/1')
# add_link(alice_id, 'https://example.com/2')

# # Добавление ссылок пользователю Bob
# add_link(bob_id, 'https://example.com/3')
# add_link(bob_id, 'https://example.com/4')

# # Получение всех ссылок пользователя Alice
# alice_links = get_user_links(alice_id)
# print('Links for Alice:', alice_links)

# Получение всех ссылок пользователя Bob
# bob_links = get_user_links(bob_id)
# print('Links for Bob:', bob_links)

# Закрытие соединения с базой данных
# conn.close()
