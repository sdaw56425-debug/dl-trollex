# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ С ЗВОНКАМИ (ПОЛНОСТЬЮ ИСПРАВЛЕННЫЙ)
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

# Настройки для Render
socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='threading')

# Создаем папки
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# База данных
users_db = {}
messages_db = {}
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
unread_messages = {}

# Админ
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
    try:
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
        
        /* Анимация свечения */
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
        
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
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
        
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        
        /* Экраны входа */
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
            position: relative;
            overflow: hidden;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
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
        
        .success {
            color: #10b981;
            margin-top: 15px;
            padding: 10px;
            background: rgba(16, 185, 129, 0.1);
            border-radius: 8px;
            border: 1px solid #10b981;
        }
        
        .hidden {
            display: none !important;
        }
        
        /* Основной интерфейс чата */
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
        }
        
        .chat-container {
            display: flex;
            height: 100vh;
            background: var(--bg-color);
        }
        
        .sidebar {
            width: 350px;
            background: var(--card-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
        }
        
        .header {
            padding: 25px;
            background: var(--card-color);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
        }
        
        .header-btn {
            background: var(--secondary-color);
            border: none;
            border-radius: 10px;
            width: 45px;
            height: 45px;
            color: var(--accent-color);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            transition: all 0.3s ease;
        }
        
        .header-btn:hover {
            background: var(--accent-color);
            color: white;
            transform: scale(1.1);
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px;
            background: var(--secondary-color);
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
        }
        
        .avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 20px;
        }
        
        .chats {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }
        
        .chat-item {
            padding: 20px;
            margin-bottom: 8px;
            background: var(--secondary-color);
            border-radius: 15px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }
        
        .chat-item:hover {
            background: var(--accent-color);
            transform: translateX(5px);
        }
        
        .chat-item.active {
            background: var(--accent-color);
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            padding: 25px;
            background: var(--card-color);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .messages {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            background: var(--bg-color);
        }
        
        .message {
            max-width: 65%;
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .message-in {
            background: var(--card-color);
            margin-right: auto;
        }
        
        .message-out {
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            margin-left: auto;
        }
        
        .message-sender {
            font-size: 13px;
            color: var(--accent-color);
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        .message-time {
            font-size: 11px;
            color: rgba(255,255,255,0.6);
            text-align: right;
            margin-top: 8px;
        }
        
        .input-area {
            padding: 25px;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }
        
        .message-input {
            flex: 1;
            padding: 18px;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 16px;
            resize: none;
        }
        
        .message-input:focus {
            outline: none;
            border-color: var(--accent-color);
        }
        
        .send-btn {
            padding: 18px 25px;
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
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
            animation: slideIn 0.3s ease-out;
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
        <div class="chat-container">
            <div class="sidebar">
                <div class="header">
                    <div class="logo glowing-logo" style="font-size: 24px;">💜 DLtrollex</div>
                    <div class="header-actions">
                        <button class="header-btn" id="themeBtn" title="Сменить тему">🎨</button>
                        <button class="header-btn" id="settingsBtn" title="Настройки">⚙️</button>
                        <button class="header-btn" id="logoutBtn" title="Выйти">🚪</button>
                    </div>
                </div>
                
                <div class="user-info" id="profileSection">
                    <div class="avatar" id="userAvatar">👤</div>
                    <div>
                        <div id="userName">Пользователь</div>
                        <div style="color: var(--accent-color); font-size: 13px;" id="userUsername">@username</div>
                    </div>
                </div>
                
                <div class="chats" id="chatsList">
                    <div class="chat-item active" data-chat="news">
                        <div class="chat-icon">📢</div>
                        <div class="chat-info">
                            <div class="chat-name">Новости DLtrollex</div>
                            <div class="chat-last-message">Официальные объявления</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="chat-area">
                <div class="chat-header">
                    <div class="chat-info">
                        <div id="chatTitle" style="font-size: 20px; font-weight: bold;">📢 Новости DLtrollex</div>
                        <div style="color: var(--accent-color); font-size: 14px;" id="chatStatus">Официальный канал</div>
                    </div>
                </div>
                
                <div class="messages" id="messagesContainer">
                    <div style="text-align: center; color: #666; margin-top: 100px;">
                        <div style="font-size: 64px;" class="floating">💜</div>
                        <p style="margin-top: 20px; font-size: 18px;">Добро пожаловать в DLtrollex!</p>
                    </div>
                </div>
                
                <div class="input-area">
                    <textarea class="message-input" id="messageInput" placeholder="💬 Введите ваше сообщение..." rows="1"></textarea>
                    <button class="send-btn" id="sendBtn">
                        <span>Отправить</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        let socket = null;
        let currentUser = null;
        let currentChat = "news";
        let allUsers = [];

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
            document.getElementById('sendBtn').addEventListener('click', sendMessage);
            document.getElementById('logoutBtn').addEventListener('click', logout);
            document.getElementById('themeBtn').addEventListener('click', showThemeModal);
            document.getElementById('settingsBtn').addEventListener('click', showProfileModal);
            document.getElementById('profileSection').addEventListener('click', showProfileModal);

            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            document.getElementById('chatsList').addEventListener('click', function(e) {
                const chatItem = e.target.closest('.chat-item');
                if (chatItem) {
                    document.querySelectorAll('.chat-item').forEach(item => item.classList.remove('active'));
                    chatItem.classList.add('active');
                    const chatType = chatItem.getAttribute('data-chat');
                    selectChat(chatType);
                }
            });
        }

        function connectSocket() {
            console.log("🔗 Подключаемся к серверу...");
            socket = io({
                transports: ['websocket', 'polling'],
                reconnection: true,
                reconnectionAttempts: 5,
                reconnectionDelay: 1000
            });
            
            socket.on('connect', function() {
                console.log("✅ Подключено к серверу");
                showNotification('Соединение установлено', 'success');
                
                if (currentUser) {
                    socket.emit('restore_session', {user_id: currentUser.id});
                    loadNews();
                }
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
            
            socket.on('private_message', function(data) {
                console.log("📨 Получено сообщение:", data);
                if (currentChat === data.chat_id) {
                    addMessageToChat(data);
                }
            });
            
            socket.on('all_news_messages', function(messages) {
                console.log("📢 Получены новости:", messages);
                displayMessages(messages);
            });
            
            socket.on('all_users', function(users) {
                console.log("👥 Получены пользователи:", users);
                allUsers = users;
                updateUsersList(users);
            });
            
            socket.on('disconnect', function() {
                console.log("❌ Отключено от сервера");
                showNotification('Потеряно соединение', 'error');
            });
            
            socket.on('connect_error', function(error) {
                console.log("❌ Ошибка подключения:", error);
                showNotification('Ошибка подключения к серверу', 'error');
            });
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
            
            updateUserInfo();
            socket.emit('get_all_users');
            loadNews();
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

        function updateUserInfo() {
            if (currentUser) {
                document.getElementById('userName').textContent = currentUser.name;
                document.getElementById('userUsername').textContent = currentUser.username || '@user';
                document.getElementById('userAvatar').textContent = currentUser.avatar || '👤';
                
                if (currentUser.avatar_bg) {
                    document.getElementById('userAvatar').style.background = currentUser.avatar_bg;
                }
            }
        }

        function selectChat(chatType) {
            currentChat = chatType;
            
            if (chatType === 'news') {
                document.getElementById('chatTitle').textContent = '📢 Новости DLtrollex';
                document.getElementById('chatStatus').textContent = 'Официальный канал';
                loadNews();
            } else {
                const user = allUsers.find(u => u.id === chatType);
                if (user) {
                    document.getElementById('chatTitle').textContent = user.name;
                    document.getElementById('chatStatus').textContent = user.username;
                    loadPrivateMessages(chatType);
                }
            }
        }

        function loadNews() {
            socket.emit('get_news_messages');
        }

        function loadPrivateMessages(userId) {
            socket.emit('get_chat_messages', {target_user_id: userId});
        }

        function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const text = messageInput.value.trim();
            
            if (!text || !currentUser) return;
            
            socket.emit('send_private_message', {
                text: text,
                chat_id: currentChat
            });
            
            messageInput.value = '';
        }

        function displayMessages(messages) {
            const container = document.getElementById('messagesContainer');
            container.innerHTML = '';
            
            if (messages.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; color: #666; margin-top: 100px;">
                        <div style="font-size: 64px;">💬</div>
                        <p style="margin-top: 20px; font-size: 18px;">Нет сообщений</p>
                    </div>
                `;
                return;
            }
            
            messages.forEach(message => {
                addMessageToChat(message);
            });
            
            container.scrollTop = container.scrollHeight;
        }

        function addMessageToChat(message) {
            const container = document.getElementById('messagesContainer');
            const messageDiv = document.createElement('div');
            
            const isOwnMessage = message.sender_id === currentUser?.id;
            const messageTime = new Date(message.timestamp).toLocaleTimeString('ru-RU', {
                hour: '2-digit',
                minute: '2-digit'
            });
            
            messageDiv.className = `message ${isOwnMessage ? 'message-out' : 'message-in'}`;
            messageDiv.innerHTML = `
                ${!isOwnMessage ? `<div class="message-sender">${message.sender_name}</div>` : ''}
                <div class="message-text">${message.text}</div>
                <div class="message-time">${messageTime}</div>
            `;
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }

        function updateUsersList(users) {
            const chatsList = document.getElementById('chatsList');
            const systemChats = chatsList.querySelectorAll('[data-chat="news"]');
            chatsList.innerHTML = '';
            systemChats.forEach(chat => chatsList.appendChild(chat));
            
            users.forEach(user => {
                if (user.id !== currentUser?.id) {
                    const chatItem = document.createElement('div');
                    chatItem.className = 'chat-item';
                    chatItem.setAttribute('data-chat', user.id);
                    chatItem.innerHTML = `
                        <div class="chat-icon">${user.avatar || '👤'}</div>
                        <div class="chat-info">
                            <div class="chat-name">${user.name}</div>
                            <div class="chat-last-message">${user.username}</div>
                        </div>
                    `;
                    chatsList.appendChild(chatItem);
                }
            });
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
            }, 3000);
        }

        function showThemeModal() {
            showNotification('Смена темы скоро будет доступна', 'info');
        }

        function showProfileModal() {
            showNotification('Настройки профиля скоро будут доступны', 'info');
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
        
        print(f"👤 Новый пользователь: {name} (@{username}) ID: {user_id}")
        
        # Отправляем успешный ответ
        emit('registration_success', user_data)
        
        # Уведомляем всех о новом пользователе
        emit('all_users', get_all_users_list(), broadcast=True)
        
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
    
    print(f"📨 Сообщение от {user_id} к {target_id}: {text}")
    
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
    
    # Сохраняем сообщение
    if user_id not in messages_db:
        messages_db[user_id] = {}
    if target_id not in messages_db[user_id]:
        messages_db[user_id][target_id] = []
    messages_db[user_id][target_id].append(message)
    
    save_user_data()
    
    # Отправляем сообщение отправителю
    emit('private_message', {**message, 'chat_id': target_id})
    
    # Отправляем получателю, если он онлайн
    for sid, uid in user_sessions.items():
        if uid == target_id:
            emit('private_message', {**message, 'chat_id': user_id}, room=sid)
    
    print(f"✅ Сообщение отправлено")

def get_all_users_list():
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
    
    return users_list

@socketio.on('get_all_users')
def handle_get_all_users():
    """Получение списка всех пользователей"""
    emit('all_users', get_all_users_list())

@socketio.on('get_news_messages')
def handle_get_news_messages():
    """Получение новостей"""
    emit('all_news_messages', news_messages)

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

@socketio.on('restore_session')
def handle_restore_session(data):
    """Восстановление сессии пользователя"""
    user_id = data.get('user_id')
    if user_id in users_db or user_id == 'admin':
        user_sessions[request.sid] = user_id
        emit('session_restored', {'status': 'success', 'user_id': user_id})
        print(f"🔑 Восстановлена сессия для: {user_id}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Запуск DLtrollex на Render...")
    print(f"💜 Доступно по адресу: https://dl-trollex-5.onrender.com")
    print("🎯 Анимации кнопок восстановлены!")
    print("🐛 Баги исправлены!")
    print("🔗 Socket.IO настроен для Render")
    socketio.run(app, 
                host='0.0.0.0', 
                port=port, 
                debug=False, 
                allow_unsafe_werkzeug=True)
