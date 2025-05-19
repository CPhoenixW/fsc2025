import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'database.sqlite'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# 创建 audios 表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS audios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        file_path TEXT NOT NULL,
        prompt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        voice_name TEXT NOT NULL,
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
    )
''')

# 插入一个测试用户（用户名：testuser，密码：testpassword）
username = 'admin'
password = '12345'
hashed_password = generate_password_hash(password)
role = 'admin'

cursor.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)',
               (username, hashed_password, role))

conn.commit()
conn.close()

print("数据库创建成功，测试用户已添加。")
