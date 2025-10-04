# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ С ЗВОНКАМИ (УЛУЧШЕННЫЙ)
from flask import Flask, render_template_string, request, send_from_directory
from flask_socketio import SocketIO, emit
import datetime
import random
import os
import base64
import time
import json
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'
app.config['UPLOAD_FOLDER'] = 'user_avatars'
app.config['DATA_FOLDER'] = 'user_data'
socketio = SocketIO(app, cors_allowed_origins="*")

# Создаем папки
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# База данных
users_db = {}
messages_db = {}  # Структура: {user_id: {target_user_id: [messages]}}
user_sessions = {}
news_messages = []
user_settings = {}
favorites_db = {}
groups_db = {}
message_reactions = {}
active_calls = {}
moderation_db = {
    'banned_users': [],
    'muted_users': [],
    'deleted_messages': [],
    'moderators': []
}
unread_messages = {}  # Новое: непрочитанные сообщения {user_id: {chat_id: count}}

# Админ
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "dltrollex123"

# Стандартные аватарки
DEFAULT_AVATARS = [
    {"emoji": "👻", "bg": "#6b21a8"}, {"emoji": "😊", "bg": "#7e22ce"},
    {"emoji": "😎", "bg": "#9333ea"}, {"emoji": "🤠", "bg": "#a855f7"},
    {"emoji": "🧑", "bg": "#c084fc"}, {"emoji": "👨", "bg": "#6b21a8"},
    {"emoji": "👩", "bg": "#7e22ce"}, {"emoji": "🦊", "bg": "#9333ea"},
    {"emoji": "🐱", "bg": "#a855f7"}, {"emoji": "🐶", "bg": "#c084fc"}
]

# Функции для сохранения/загрузки данных
def save_user_data():
    """Сохраняет все данные пользователей"""
    data = {
        'users_db': users_db,
        'messages_db': messages_db,
        'news_messages': news_messages,
        'user_settings': user_settings,
        'favorites_db': favorites_db,
        'groups_db': groups_db,
        'message_reactions': message_reactions,
        'moderation_db': moderation_db,
        'unread_messages': unread_messages
    }
    try:
        with open(os.path.join(app.config['DATA_FOLDER'], 'data.pkl'), 'wb') as f:
            pickle.dump(data, f)
        print("💾 Данные сохранены")
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

def load_user_data():
    """Загружает данные пользователей"""
    global users_db, messages_db, news_messages, user_settings, favorites_db, groups_db, message_reactions, moderation_db, unread_messages
    try:
        with open(os.path.join(app.config['DATA_FOLDER'], 'data.pkl'), 'rb') as f:
            data = pickle.load(f)
            users_db = data.get('users_db', {})
            messages_db = data.get('messages_db', {})
            news_messages = data.get('news_messages', [])
            user_settings = data.get('user_settings', {})
            favorites_db = data.get('favorites_db', {})
            groups_db = data.get('groups_db', {})
            message_reactions = data.get('message_reactions', {})
            moderation_db = data.get('moderation_db', {
                'banned_users': [],
                'muted_users': [],
                'deleted_messages': [],
                'moderators': []
            })
            unread_messages = data.get('unread_messages', {})
        print("📂 Данные загружены")
    except FileNotFoundError:
        print("📂 Файл данных не найден, создаем новую базу")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")

# Загружаем данные при запуске
load_user_data()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Ваши стили остаются без изменений */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        :root {
            --bg-color: #0f0f0f;
            --card-color: #1a1a1a;
            --accent-color: #8b5cf6;
            --text-color: #ffffff;
            --secondary-color: #2d2d2d;
            --border-color: #3d3d3d;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        /* ... остальные стили без изменений ... */
    </style>
</head>
<body>
    <!-- HTML структура остается без изменений -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Фиолетовый чат с максимальной кастомизацией</div>
            
            <button class="btn pulse" id="startChatBtn">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-admin" id="adminAccessBtn">
                <span>👑 Войти как администратор</span>
            </button>
        </div>
    </div>

    <!-- Экран регистрации -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Создание аккаунта</div>
            
            <input type="text" id="regName" class="input-field" placeholder="💁 Ваше имя" required>
            <input type="text" id="regUsername" class="input-field" placeholder="👤 @username (не обязательно)">
            <div class="optional">✨ Юзернейм не обязателен. Если не указать, будет сгенерирован автоматически</div>
            
            <button class="btn" id="registerBtn">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" id="backToMainBtn">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
            <div id="registerSuccess" class="success"></div>
        </div>
    </div>

    <!-- ... остальная HTML структура без изменений ... -->

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        // УПРОЩЕННАЯ ВЕРСИЯ JAVASCRIPT ДЛЯ ИСПРАВЛЕНИЯ РЕГИСТРАЦИИ
        
        let socket = null;
        let currentUser = null;

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            setupEventListeners();
            connectSocket();
        });

        function setupEventListeners() {
            // Главный экран
            document.getElementById('startChatBtn').addEventListener('click', showRegisterScreen);
            document.getElementById('adminAccessBtn').addEventListener('click', showAdminScreen);
            
            // Кнопки навигации
            document.getElementById('backToMainBtn').addEventListener('click', showMainScreen);
            document.getElementById('backToMainFromAdminBtn').addEventListener('click', showMainScreen);
            
            // Кнопки авторизации
            document.getElementById('registerBtn').addEventListener('click', register);
            document.getElementById('adminLoginBtn').addEventListener('click', adminLogin);
        }

        function connectSocket() {
            socket = io();
            
            socket.on('connect', function() {
                console.log("✅ Подключено к серверу");
            });
            
            socket.on('registration_success', function(user) {
                console.log("✅ Регистрация успешна:", user);
                currentUser = user;
                localStorage.setItem('dlcurrentUser', JSON.stringify(user));
                showMainApp();
            });
            
            socket.on('registration_error', function(data) {
                document.getElementById('registerError').textContent = data.message;
                document.getElementById('registerBtn').disabled = false;
                document.getElementById('registerBtn').innerHTML = '<span>🚀 Начать общение</span>';
            });
            
            socket.on('disconnect', function() {
                console.log("❌ Отключено от сервера");
            });
        }

        function showMainScreen() {
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
        }

        function showRegisterScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            // Простая инициализация интерфейса
            if (currentUser) {
                document.getElementById('userName').textContent = currentUser.name;
                document.getElementById('userUsername').textContent = currentUser.username;
                document.getElementById('userAvatar').textContent = '👤';
            }
        }

        function register() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            document.getElementById('registerBtn').disabled = true;
            document.getElementById('registerBtn').innerHTML = '<span>⏳ Регистрация...</span>';
            document.getElementById('registerError').textContent = '';
            
            console.log("📝 Регистрация:", { name, username });
            
            socket.emit('register', {
                name: name,
                username: username || undefined
            });
        }

        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    is_admin: true
                };
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/user_avatars/<filename>')
def serve_avatar(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def generate_user_id():
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

def generate_message_id():
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

@socketio.on('connect')
def handle_connect():
    print(f"✅ Клиент подключен: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = user_sessions.get(request.sid)
    if user_id:
        print(f"❌ Пользователь отключен: {user_id}")
        del user_sessions[request.sid]

@socketio.on('register')
def handle_register(data):
    """Регистрация нового пользователя - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    try:
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        
        print(f"📝 Попытка регистрации: name={name}, username={username}")
        
        if not name:
            emit('registration_error', {'message': 'Введите имя'})
            return
        
        # Генерируем user_id
        user_id = generate_user_id()
        
        # Если username не указан, генерируем автоматически
        if not username:
            username = f"user{random.randint(10000, 99999)}"
        else:
            # Проверяем уникальность username
            for user in users_db.values():
                if user.get('username') == username:
                    emit('registration_error', {'message': 'Этот юзернейм уже занят'})
                    return
        
        # Создаем пользователя
        user_data = {
            'id': user_id,
            'name': name,
            'username': username,
            'avatar': '👤',
            'avatar_bg': '#6b21a8',
            'registered_at': datetime.datetime.now().isoformat(),
            'is_banned': False,
            'is_muted': False,
            'is_moderator': False
        }
        
        # Сохраняем в базу
        users_db[user_id] = user_data
        user_sessions[request.sid] = user_id
        
        # Инициализируем непрочитанные сообщения
        unread_messages[user_id] = {}
        
        # Сохраняем данные
        save_user_data()
        
        print(f"👤 Новый пользователь: {name} (@{username})")
        
        # Отправляем успешный ответ
        emit('registration_success', user_data)
        
        # Уведомляем всех о новом пользователе онлайн
        emit('user_online', {
            'user_id': user_id, 
            'username': name
        }, broadcast=True)
        
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")
        emit('registration_error', {'message': 'Ошибка сервера при регистрации'})

@socketio.on('send_private_message')
def handle_send_private_message(data):
    """Отправка приватного сообщения"""
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    text = data.get('text', '').strip()
    target_id = data.get('chat_id')
    
    if not text or not target_id:
        return
    
    # Создаем сообщение
    message_id = generate_message_id()
    sender_name = users_db[user_id]['name'] if user_id in users_db else 'Неизвестный'
    
    message = {
        'id': message_id,
        'text': text,
        'sender_id': user_id,
        'sender_name': sender_name,
        'timestamp': datetime.datetime.now().isoformat(),
        'edited': False,
        'reactions': {}
    }
    
    # Сохраняем сообщение для отправителя
    if user_id not in messages_db:
        messages_db[user_id] = {}
    if target_id not in messages_db[user_id]:
        messages_db[user_id][target_id] = []
    messages_db[user_id][target_id].append(message)
    
    # Сохраняем сообщение для получателя (если это не админ)
    if target_id != 'admin' and target_id in users_db:
        if target_id not in messages_db:
            messages_db[target_id] = {}
        if user_id not in messages_db[target_id]:
            messages_db[target_id][user_id] = []
        messages_db[target_id][user_id].append(message)
    
    save_user_data()
    
    # Отправляем сообщение отправителю
    emit('private_message', {**message, 'chat_id': target_id})
    
    # Отправляем получателю, если он онлайн
    for sid, uid in user_sessions.items():
        if uid == target_id:
            emit('private_message', {**message, 'chat_id': user_id}, room=sid)
    
    print(f"📨 Сообщение от {user_id} к {target_id}")

@socketio.on('get_all_users')
def handle_get_all_users():
    """Получение списка всех пользователей"""
    users_list = []
    
    # Добавляем обычных пользователей
    for user_id, user_data in users_db.items():
        if user_id != 'admin':
            users_list.append(user_data)
    
    # Добавляем админа
    users_list.append({
        'id': 'admin',
        'name': 'Администратор',
        'username': '@admin',
        'avatar': '👑',
        'avatar_bg': '#dc2626',
        'is_admin': True
    })
    
    emit('all_users', users_list)

@socketio.on('get_chat_messages')
def handle_get_chat_messages(data):
    """Получение сообщений чата"""
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    target_id = data.get('target_user_id')
    if not target_id:
        return
    
    messages = []
    
    # Ищем сообщения в базе
    if user_id in messages_db and target_id in messages_db[user_id]:
        messages = messages_db[user_id][target_id]
    
    emit('chat_messages', messages)

@socketio.on('get_news_messages')
def handle_get_news_messages():
    """Получение новостей"""
    emit('all_news_messages', news_messages)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Запуск DLtrollex с исправленной регистрацией...")
    print(f"💜 Доступно по адресу: http://localhost:{port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
