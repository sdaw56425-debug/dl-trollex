# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ С ЗВОНКАМИ (ДЛЯ RENDER)
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

# Правильные настройки для Render
socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='eventlet',
                   logger=False,
                   engineio_logger=False)

# Создаем папки
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# База данных
users_db = {}
messages_db = {}
user_sessions = {}
news_messages = []

# Админ
ADMIN_PASSWORD = "dltrollex123"

# Функции для сохранения/загрузки данных
def save_user_data():
    """Сохраняет все данные пользователей"""
    try:
        data = {
            'users_db': users_db,
            'messages_db': messages_db,
            'news_messages': news_messages,
        }
        with open(os.path.join(app.config['DATA_FOLDER'], 'data.pkl'), 'wb') as f:
            pickle.dump(data, f)
        print("💾 Данные сохранены")
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

def load_user_data():
    """Загружает данные пользователей"""
    global users_db, messages_db, news_messages
    try:
        with open(os.path.join(app.config['DATA_FOLDER'], 'data.pkl'), 'rb') as f:
            data = pickle.load(f)
            users_db = data.get('users_db', {})
            messages_db = data.get('messages_db', {})
            news_messages = data.get('news_messages', [])
        print("📂 Данные загружены")
    except FileNotFoundError:
        print("📂 Файл данных не найден, создаем новую базу")
        # Создаем тестовые данные
        news_messages.extend([
            {
                'id': '1',
                'text': 'Добро пожаловать в DLtrollex! 🎉',
                'sender_id': 'admin',
                'sender_name': 'Администратор',
                'timestamp': datetime.datetime.now().isoformat(),
                'edited': False
            },
            {
                'id': '2', 
                'text': 'Это фиолетовый мессенджер с максимальной кастомизацией! 💜',
                'sender_id': 'admin',
                'sender_name': 'Администратор', 
                'timestamp': datetime.datetime.now().isoformat(),
                'edited': False
            }
        ])
        save_user_data()
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")

# Загружаем данные при запуске
load_user_data()

# Создаем фавикон роут чтобы убрать 404 ошибку
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'DLtrollex is running'}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💜</text></svg>">
    <style>
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
        
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 10px var(--accent-color), 0 0 20px var(--accent-color);
            }
            50% {
                text-shadow: 0 0 20px var(--accent-color), 0 0 30px var(--accent-color), 0 0 40px var(--accent-color);
            }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .glowing-logo {
            animation: glow 3s ease-in-out infinite;
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        .screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--bg-color) 0%, var(--card-color) 100%);
            z-index: 1000;
        }
        
        .auth-box {
            background: var(--card-color);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 2px solid var(--accent-color);
            width: 450px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .auth-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, var(--accent-color), transparent);
            animation: shine 3s linear infinite;
            opacity: 0.1;
        }
        
        @keyframes shine {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .logo {
            font-size: 48px;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 15px;
        }
        
        .subtitle {
            color: #888;
            margin-bottom: 40px;
            font-size: 16px;
        }
        
        .input-field {
            width: 100%;
            padding: 18px;
            margin-bottom: 20px;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-color);
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .input-field:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
            transform: translateY(-2px);
        }
        
        .optional {
            color: #888;
            font-size: 12px;
            margin-top: -15px;
            margin-bottom: 20px;
            text-align: left;
        }
        
        .btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn-admin {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        
        .btn-admin:hover {
            box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4);
        }
        
        .error {
            color: #ef4444;
            margin-top: 15px;
            padding: 10px;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
            border: 1px solid #ef4444;
        }
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
        }
        
        .notification-toast {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            z-index: 3000;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: var(--accent-color);
        }
    </style>
</head>
<body>
    <!-- Главный экран выбора -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Фиолетовый чат с максимальной кастомизацией</div>
            
            <button class="btn pulse" id="startChatBtn">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-admin pulse" id="adminAccessBtn">
                <span>👑 Войти как администратор</span>
            </button>
            
            <div id="loading" class="loading hidden">
                <p>Подключение к серверу...</p>
            </div>
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
            
            <button class="btn pulse" id="registerBtn">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" id="backToMainBtn">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
        </div>
    </div>

    <!-- Экран входа админа -->
    <div id="adminScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Панель администратора</div>
            
            <input type="password" id="adminPass" class="input-field" placeholder="🔒 Введите пароль администратора">
            
            <button class="btn btn-admin pulse" id="adminLoginBtn">⚡ Войти</button>
            
            <button class="btn" id="backToMainFromAdminBtn">
                <span>← Назад</span>
            </button>
            
            <div id="adminError" class="error"></div>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <div style="text-align: center; padding: 100px;">
            <div class="logo glowing-logo" style="font-size: 64px;">💜</div>
            <h1>DLtrollex</h1>
            <p>Мессенджер загружается...</p>
            <p style="color: #888; margin-top: 20px;">Если загрузка занимает много времени, проверьте подключение к интернету</p>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        let socket = null;
        let currentUser = null;

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            setupEventListeners();
            connectSocket();
            checkAutoLogin();
        });

        function setupEventListeners() {
            document.getElementById('startChatBtn').addEventListener('click', showRegisterScreen);
            document.getElementById('adminAccessBtn').addEventListener('click', showAdminScreen);
            document.getElementById('backToMainBtn').addEventListener('click', showMainScreen);
            document.getElementById('backToMainFromAdminBtn').addEventListener('click', showMainScreen);
            document.getElementById('registerBtn').addEventListener('click', register);
            document.getElementById('adminLoginBtn').addEventListener('click', adminLogin);
        }

        function connectSocket() {
            console.log("🔗 Подключаемся к серверу...");
            document.getElementById('loading').classList.remove('hidden');
            
            socket = io({
                transports: ['websocket', 'polling'],
                reconnection: true,
                reconnectionAttempts: 10,
                reconnectionDelay: 1000,
                timeout: 10000
            });
            
            socket.on('connect', function() {
                console.log("✅ Подключено к серверу");
                document.getElementById('loading').classList.add('hidden');
                showNotification('Соединение установлено', 'success');
            });
            
            socket.on('registration_success', function(user) {
                console.log("✅ Регистрация успешна:", user);
                currentUser = user;
                localStorage.setItem('dlcurrentUser', JSON.stringify(user));
                showMainApp();
                showNotification('Регистрация успешна!', 'success');
            });
            
            socket.on('registration_error', function(data) {
                console.log("❌ Ошибка регистрации:", data.message);
                document.getElementById('registerError').textContent = data.message;
                document.getElementById('registerBtn').disabled = false;
                document.getElementById('registerBtn').innerHTML = '<span>🚀 Начать общение</span>';
            });
            
            socket.on('disconnect', function() {
                console.log("❌ Отключено от сервера");
                showNotification('Потеряно соединение', 'error');
            });
            
            socket.on('connect_error', function(error) {
                console.log("❌ Ошибка подключения:", error);
                document.getElementById('loading').classList.add('hidden');
                showNotification('Ошибка подключения к серверу. Попробуйте обновить страницу.', 'error');
            });
            
            // Таймаут подключения
            setTimeout(function() {
                if (!socket.connected) {
                    document.getElementById('loading').classList.add('hidden');
                    showNotification('Не удалось подключиться к серверу. Проверьте интернет соединение.', 'error');
                }
            }, 10000);
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    console.log("🔑 Автоматический вход:", currentUser);
                    showMainApp();
                } catch (e) {
                    console.log("❌ Ошибка автоматического входа:", e);
                    localStorage.removeItem('dlcurrentUser');
                }
            }
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
            
            // Простая версия интерфейса
            document.getElementById('mainApp').innerHTML = `
                <div style="padding: 50px; text-align: center;">
                    <div class="logo glowing-logo" style="font-size: 80px;">💜</div>
                    <h1>Добро пожаловать в DLtrollex!</h1>
                    <p style="margin: 20px 0; font-size: 18px;">Вы успешно вошли как <strong>${currentUser.name}</strong></p>
                    <p style="color: #888;">Полная версия мессенджера скоро будет доступна</p>
                    <button class="btn" onclick="logout()" style="margin-top: 30px;">
                        <span>🚪 Выйти</span>
                    </button>
                </div>
            `;
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
            
            console.log("📝 Отправка регистрации:", { name, username });
            
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
                showNotification('Вход как администратор', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        function logout() {
            currentUser = null;
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification-toast';
            notification.style.background = type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : 'var(--accent-color)';
            notification.innerHTML = `
                <div style="font-size: 20px;">${type === 'error' ? '❌' : type === 'success' ? '✅' : '💡'}</div>
                <div>${message}</div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

def generate_user_id():
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

@socketio.on('connect')
def handle_connect():
    print(f"✅ Клиент подключен: {request.sid}")
    emit('connected', {'message': 'Connected to DLtrollex server'})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = user_sessions.get(request.sid)
    if user_id:
        print(f"❌ Пользователь отключен: {user_id}")
        del user_sessions[request.sid]

@socketio.on('register')
def handle_register(data):
    """Регистрация нового пользователя"""
    try:
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        
        print(f"📝 Регистрация: name='{name}', username='{username}'")
        
        if not name:
            emit('registration_error', {'message': 'Введите имя'})
            return
        
        # Генерируем user_id
        user_id = generate_user_id()
        
        # Если username не указан, генерируем автоматически
        if not username:
            username = f"user{random.randint(10000, 99999)}"
        
        # Создаем пользователя
        user_data = {
            'id': user_id,
            'name': name,
            'username': username,
            'avatar': '👤',
            'avatar_bg': '#6b21a8',
            'registered_at': datetime.datetime.now().isoformat(),
        }
        
        # Сохраняем в базу
        users_db[user_id] = user_data
        user_sessions[request.sid] = user_id
        
        # Сохраняем данные
        save_user_data()
        
        print(f"👤 Новый пользователь: {name} (@{username}) ID: {user_id}")
        
        # Отправляем успешный ответ
        emit('registration_success', user_data)
        
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")
        emit('registration_error', {'message': 'Ошибка сервера при регистрации'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🚀 Запуск DLtrollex на Render...")
    print("💜 Сервер запускается...")
    print("🔗 Ожидание подключений...")
    
    # Для Render используем eventlet
    import eventlet
    eventlet.monkey_patch()
    
    socketio.run(app, 
                host='0.0.0.0', 
                port=port, 
                debug=False, 
                log_output=True,
                use_reloader=False)
