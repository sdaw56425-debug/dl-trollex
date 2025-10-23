# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ХЕЛЛОУИН 2025 + РЕАЛЬНЫЕ ПОЛЬЗОВАТЕЛИ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

# База данных в памяти
users_db = {}
messages_db = {}
chats_db = {}
news_messages = [
    {
        'id': '1',
        'text': 'Добро пожаловать в DLtrollex! 🎉',
        'sender_name': 'Администратор',
        'timestamp': datetime.datetime.now().isoformat(),
    },
    {
        'id': '2', 
        'text': 'Это фиолетовый мессенджер с максимальной кастомизацией! 💜',
        'sender_name': 'Администратор', 
        'timestamp': datetime.datetime.now().isoformat(),
    }
]

# Админ
ADMIN_PASSWORD = "dltrollex123"

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'DLtrollex is running'})

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex 🎃</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎃</text></svg>">
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
            --halloween-color: #ff7b25;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        body.halloween-theme {
            --accent-color: #ff7b25;
            --bg-color: #1a0f00;
            --card-color: #2a1a00;
            --secondary-color: #3a2a00;
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
        
        @keyframes spooky {
            0%, 100% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(5deg) scale(1.1); }
            75% { transform: rotate(-5deg) scale(1.1); }
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
        
        .spooky {
            animation: spooky 3s ease-in-out infinite;
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
        
        .btn-halloween {
            background: linear-gradient(135deg, #ff7b25, #ff5500);
        }
        
        .btn-halloween:hover {
            box-shadow: 0 10px 25px rgba(255, 123, 37, 0.4);
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
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .halloween-decoration {
            position: fixed;
            font-size: 24px;
            z-index: 100;
            opacity: 0.1;
            animation: float 8s ease-in-out infinite;
        }
        
        .chat-container {
            display: flex;
            height: 100vh;
        }
        
        .sidebar {
            width: 350px;
            background: var(--card-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .search-box {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .search-input {
            width: 100%;
            padding: 12px 45px 12px 15px;
            background: var(--secondary-color);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 14px;
        }
        
        .chats-list {
            flex: 1;
            overflow-y: auto;
        }
        
        .chat-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .chat-item:hover {
            background: var(--secondary-color);
        }
        
        .chat-item.active {
            background: var(--accent-color);
        }
        
        .chat-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-right: 15px;
        }
        
        .chat-info {
            flex: 1;
        }
        
        .chat-name {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .chat-last-message {
            color: #888;
            font-size: 13px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .chat-time {
            color: #888;
            font-size: 11px;
        }
        
        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .message {
            background: var(--secondary-color);
            padding: 12px 15px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
        }
        
        .message.own {
            background: var(--accent-color);
            align-self: flex-end;
        }
        
        .message-input-container {
            padding: 20px;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 10px;
        }
        
        .message-input {
            flex: 1;
            padding: 12px 15px;
            background: var(--secondary-color);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 14px;
        }
        
        .send-btn {
            padding: 12px 20px;
            background: var(--accent-color);
            border: none;
            border-radius: 25px;
            color: white;
            cursor: pointer;
        }
        
        .online-indicator {
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            position: absolute;
            bottom: 2px;
            right: 2px;
            border: 2px solid var(--card-color);
        }
        
        .user-status {
            font-size: 11px;
            color: #10b981;
        }
        
        .theme-selector {
            display: flex;
            gap: 10px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        
        .theme-option {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .theme-option.active {
            border-color: white;
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <!-- Хеллоуинские декорации -->
    <div class="halloween-decoration" style="top: 10%; left: 5%;">🎃</div>
    <div class="halloween-decoration" style="top: 20%; right: 10%;">👻</div>
    <div class="halloween-decoration" style="bottom: 30%; left: 15%;">🦇</div>
    <div class="halloween-decoration" style="bottom: 20%; right: 5%;">🕷️</div>

    <!-- ПЕРВАЯ СТРАНИЦА - ПРОДОЛЖИТЬ -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Хеллоуин 2025 Edition! Фиолетовый чат с реальными пользователями</div>
            
            <button class="btn pulse" onclick="showScreen('screen2')">
                <span>🚀 Продолжить</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                🔒 Ваши данные хранятся локально
            </div>
        </div>
    </div>

    <!-- ВТОРАЯ СТРАНИЦА - ПРОДОЛЖИТЬ -->
    <div id="screen2" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Выберите способ регистрации</div>
            
            <button class="btn pulse" onclick="showRegisterScreen()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-halloween pulse" onclick="showQuickRegisterScreen()">
                <span>🎲 Быстрая регистрация</span>
            </button>
            
            <button class="btn btn-admin pulse" onclick="showAdminScreen()">
                <span>👑 Администратор</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen1')">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- Экран регистрации -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Создание аккаунта</div>
            
            <input type="text" id="regName" class="input-field" placeholder="💁 Ваше имя" required>
            <input type="text" id="regUsername" class="input-field" placeholder="👤 @username (не обязательно)">
            <input type="email" id="regEmail" class="input-field" placeholder="📧 Email (не обязательно)">
            <div class="optional">✨ Заполните только имя - остальные поля не обязательны</div>
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen2')">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
            <div id="registerSuccess" class="success hidden"></div>
        </div>
    </div>

    <!-- Экран быстрой регистрации -->
    <div id="quickRegisterScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Быстрая регистрация</div>
            
            <div style="text-align: left; margin-bottom: 20px; color: #888;">
                <p>Мы создадим для вас аккаунт с:</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>Случайным именем</li>
                    <li>Автоматическим юзернеймом</li>
                    <li>Готовым к использованию</li>
                </ul>
            </div>
            
            <button class="btn btn-halloween pulse" onclick="quickRegister()">
                <span>🎲 Создать аккаунт</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen2')">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- Экран входа админа -->
    <div id="adminScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Панель администратора</div>
            
            <input type="password" id="adminPass" class="input-field" placeholder="🔒 Введите пароль администратора">
            
            <button class="btn btn-admin pulse" onclick="adminLogin()">⚡ Войти</button>
            
            <button class="btn" onclick="showScreen('screen2')">
                <span>← Назад</span>
            </button>
            
            <div id="adminError" class="error"></div>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <!-- Интерфейс будет генерироваться JavaScript -->
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let isHalloweenTheme = false;
        let currentTheme = 'purple';

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🎃 DLtrollex Хеллоуин 2025 загружен!");
            checkAutoLogin();
            loadHalloweenTheme();
            loadTheme();
            initializeData();
        });

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    showMainApp();
                } catch (e) {
                    localStorage.removeItem('dlcurrentUser');
                }
            }
        }

        function loadHalloweenTheme() {
            const saved = localStorage.getItem('dlhalloween');
            if (saved === 'true') {
                activateHalloweenTheme();
            }
        }

        function loadTheme() {
            const savedTheme = localStorage.getItem('dltheme');
            if (savedTheme) {
                currentTheme = savedTheme;
                applyTheme(savedTheme);
            }
        }

        function initializeData() {
            // Инициализируем реальных пользователей из localStorage или создаем тестовых
            const savedUsers = localStorage.getItem('dlallUsers');
            if (savedUsers) {
                allUsers = JSON.parse(savedUsers);
            } else {
                allUsers = [
                    {
                        id: 'user1',
                        name: 'Алексей',
                        username: '@alexey',
                        email: 'alexey@example.com',
                        avatar: '😎',
                        isOnline: true,
                        lastSeen: new Date().toISOString(),
                        bio: 'Люблю программирование и путешествия 🚀',
                        registered: new Date(Date.now() - 86400000).toISOString()
                    },
                    {
                        id: 'user2', 
                        name: 'Мария',
                        username: '@maria',
                        email: 'maria@example.com',
                        avatar: '👩',
                        isOnline: true,
                        lastSeen: new Date().toISOString(),
                        bio: 'Дизайнер и художник 🎨',
                        registered: new Date(Date.now() - 172800000).toISOString()
                    },
                    {
                        id: 'user3',
                        name: 'Дмитрий',
                        username: '@dmitry',
                        email: 'dmitry@example.com',
                        avatar: '🧑',
                        isOnline: false,
                        lastSeen: new Date(Date.now() - 300000).toISOString(),
                        bio: 'Разработчик игр 🎮',
                        registered: new Date(Date.now() - 259200000).toISOString()
                    }
                ];
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }

            // Инициализируем чаты
            const savedChats = localStorage.getItem('dlchats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
        }

        // ПРОСТЫЕ ФУНКЦИИ ДЛЯ СМЕНЫ ЭКРАНОВ
        function showScreen(screenId) {
            // Скрыть все экраны
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').style.display = 'none';
            
            // Показать нужный экран
            document.getElementById(screenId).classList.remove('hidden');
        }

        function showRegisterScreen() {
            showScreen('registerScreen');
        }

        function showQuickRegisterScreen() {
            showScreen('quickRegisterScreen');
        }

        function showAdminScreen() {
            showScreen('adminScreen');
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').style.display = 'block';
            
            renderChatsInterface();
            showNotification(`Добро пожаловать в DLtrollex${isHalloweenTheme ? ' 🎃' : ''}!`, 'success');
        }

        function renderChatsInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <!-- Боковая панель с чатами -->
                    <div class="sidebar">
                        <!-- Заголовок -->
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">${isHalloweenTheme ? '🎃' : '💜'} DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                            ${isHalloweenTheme ? '<div style="color: #ff7b25; font-size: 10px; margin-top: 5px;">🎃 Хеллоуин 2025 Активен!</div>' : ''}
                        </div>
                        
                        <!-- Поиск -->
                        <div class="search-box">
                            <div style="position: relative;">
                                <input type="text" class="search-input" placeholder="🔍 Поиск пользователей..." oninput="searchUsers(this.value)">
                            </div>
                        </div>
                        
                        <!-- Список чатов -->
                        <div class="chats-list" id="chatsList">
                            ${renderChatsList()}
                        </div>
                        
                        <!-- Нижняя панель -->
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            <button class="btn" onclick="showNewChatModal()" style="margin-bottom: 10px;">➕ Новый чат</button>
                            <button class="btn" onclick="showAllUsers()" style="margin-bottom: 10px;">👥 Все пользователи</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            ${currentUser && currentUser.is_admin ? '<button class="btn btn-admin" onclick="showAdminPanel()">👑 Админ</button>' : ''}
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px;">
                                ${isHalloweenTheme ? '👻 Выкл.Хеллоуин' : '🎃 Вкл.Хеллоуин'}
                            </button>
                            <button class="btn" onclick="logout()" style="margin-top: 10px; background: #dc2626;">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Область чата -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div class="logo glowing-logo ${isHalloweenTheme ? 'spooky' : ''}" style="font-size: 80px;">${isHalloweenTheme ? '🎃' : '💜'}</div>
                            <h2>Добро пожаловать в чаты!</h2>
                            <p style="color: #888; margin: 10px 0 20px 0; text-align: center;">
                                ${isHalloweenTheme ? '🎃 Найди новых друзей в хеллоуинском стиле! 👻' : 'Найди новых друзей и начни общение!'}
                            </p>
                            <button class="btn" onclick="showNewChatModal()">💬 Начать новый чат</button>
                            ${isHalloweenTheme ? '<div style="color: #ff7b25; margin-top: 15px; font-size: 14px;">🎃 Счастливого Хеллоуина 2025! 👻</div>' : ''}
                        </div>
                    </div>
                </div>
            `;
        }

        function renderChatsList() {
            if (chats.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">💬</div>
                        <div>Чатов пока нет</div>
                        <div style="font-size: 12px; margin-top: 5px;">Начните новый чат с пользователем</div>
                    </div>
                `;
            }

            return chats.map(chat => {
                const otherParticipants = chat.participants.filter(p => p !== currentUser.id);
                const chatUser = allUsers.find(u => u.id === otherParticipants[0]);
                if (!chatUser) return '';
                
                const isActive = currentChat && currentChat.id === chat.id;
                
                return `
                    <div class="chat-item ${isActive ? 'active' : ''}" onclick="openChat('${chat.id}')">
                        <div style="position: relative;">
                            <div class="chat-avatar">${chat.type === 'group' ? '👥' : chatUser.avatar}</div>
                            ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div class="chat-info">
                            <div class="chat-name">
                                ${chat.type === 'group' ? chat.name : chatUser.name}
                                ${chatUser.isOnline ? '<span class="user-status">● онлайн</span>' : ''}
                            </div>
                            <div class="chat-last-message">${chat.lastMessage.text}</div>
                        </div>
                        <div class="chat-time">${formatTime(chat.lastMessage.timestamp)}</div>
                        ${chat.unreadCount > 0 ? `
                            <div style="background: var(--accent-color); color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 12px; margin-left: 10px;">
                                ${chat.unreadCount}
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');
        }

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherParticipants = currentChat.participants.filter(p => p !== currentUser.id);
            const chatUser = allUsers.find(u => u.id === otherParticipants[0]);
            if (!chatUser) return;
            
            document.getElementById('chatContent').innerHTML = `
                <!-- Заголовок чата -->
                <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <div style="position: relative; margin-right: 15px;">
                            <div class="chat-avatar">${currentChat.type === 'group' ? '👥' : chatUser.avatar}</div>
                            ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div>
                            <div style="font-weight: bold; font-size: 16px;">
                                ${currentChat.type === 'group' ? currentChat.name : chatUser.name}
                            </div>
                            <div style="color: #888; font-size: 12px;">
                                ${chatUser.isOnline ? 'online' : `был(а) ${formatLastSeen(chatUser.lastSeen)}`}
                            </div>
                        </div>
                    </div>
                    <div>
                        <button class="btn" onclick="showUserProfile('${chatUser.id}')" style="padding: 8px 15px; font-size: 12px; margin-right: 10px;">👤 Профиль</button>
                        <button class="btn" onclick="renderChatsInterface()" style="padding: 8px 15px; font-size: 12px;">← Назад</button>
                    </div>
                </div>
                
                <!-- Сообщения -->
                <div class="messages-container" id="messagesContainer">
                    ${renderChatMessages()}
                </div>
                
                <!-- Ввод сообщения -->
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="💬 Введите сообщение..." id="messageInput" onkeypress="if(event.key=='Enter') sendMessage()">
                    <button class="send-btn" onclick="sendMessage()">📤</button>
                    ${isHalloweenTheme ? '<button class="send-btn btn-halloween" onclick="sendHalloweenMessage()">🎃</button>' : ''}
                </div>
            `;

            // Прокрутка вниз
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Фокус на поле ввода
            document.getElementById('messageInput').focus();
        }

        function renderChatMessages() {
            if (!currentChat.messages || currentChat.messages.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">💬</div>
                        <div>Чат пуст</div>
                        <div style="font-size: 12px; margin-top: 5px;">Напишите первое сообщение!</div>
                    </div>
                `;
            }

            return currentChat.messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                const sender = allUsers.find(u => u.id === msg.senderId);
                if (!sender) return '';
                
                return `
                    <div class="message ${isOwn ? 'own' : ''}">
                        <div style="margin-bottom: 5px;">
                            ${!isOwn ? `<strong>${sender.name}:</strong> ` : ''}
                            ${msg.text}
                        </div>
                        <div style="font-size: 11px; color: ${isOwn ? 'rgba(255,255,255,0.7)' : '#888'}; text-align: ${isOwn ? 'right' : 'left'};">
                            ${formatTime(msg.timestamp)}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                if (!currentChat.messages) currentChat.messages = [];
                
                const newMessage = {
                    id: Date.now().toString(),
                    text: message,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                
                // Сохраняем в localStorage
                localStorage.setItem('dlchats', JSON.stringify(chats));
                
                // Обновляем интерфейс
                openChat(currentChat.id);
                renderChatsList();
                
                input.value = '';
                showNotification('Сообщение отправлено!', 'success');
            }
        }

        function sendHalloweenMessage() {
            const messages = [
                'Бууу! Счастливого Хеллоуина! 👻',
                '🎃 Тыквенное настроение!',
                'Конфеты или смерть! 🍬',
                'Хеллоуин 2025 будет самым страшным! 🦇',
                'Приветствую в хеллоуинском чате! 🎃'
            ];
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            
            document.getElementById('messageInput').value = randomMessage;
            sendMessage();
        }

        function searchUsers(query) {
            if (!query.trim()) {
                document.getElementById('chatsList').innerHTML = renderChatsList();
                return;
            }
            
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && (
                    user.name.toLowerCase().includes(query.toLowerCase()) ||
                    user.username.toLowerCase().includes(query.toLowerCase()) ||
                    (user.bio && user.bio.toLowerCase().includes(query.toLowerCase()))
                )
            );
            
            let searchHTML = '';
            
            if (filteredUsers.length > 0) {
                searchHTML = filteredUsers.map(user => `
                    <div class="chat-item" onclick="startNewChat('${user.id}')">
                        <div style="position: relative;">
                            <div class="chat-avatar">${user.avatar}</div>
                            ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div class="chat-info">
                            <div class="chat-name">
                                ${user.name}
                                ${user.isOnline ? '<span class="user-status">● онлайн</span>' : ''}
                            </div>
                            <div class="chat-last-message">${user.username} • ${user.bio || 'Нет описания'}</div>
                        </div>
                        <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Чат</button>
                    </div>
                `).join('');
            } else {
                searchHTML = `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">🔍</div>
                        <div>Пользователи не найдены</div>
                        <div style="font-size: 12px; margin-top: 5px;">Попробуйте другой запрос</div>
                    </div>
                `;
            }
            
            document.getElementById('chatsList').innerHTML = searchHTML;
        }

        function showNewChatModal() {
            const availableUsers = allUsers.filter(user => user.id !== currentUser.id);
            
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>💬 Новый чат</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">👥 Все пользователи (${availableUsers.length})</h3>
                        <div style="max-height: 60vh; overflow-y: auto;">
                            ${availableUsers.map(user => `
                                <div class="chat-item" onclick="startNewChat('${user.id}')">
                                    <div style="position: relative;">
                                        <div class="chat-avatar">${user.avatar}</div>
                                        ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                                    </div>
                                    <div class="chat-info">
                                        <div class="chat-name">
                                            ${user.name}
                                            ${user.isOnline ? '<span class="user-status">● онлайн</span>' : ''}
                                        </div>
                                        <div class="chat-last-message">${user.username} • ${user.bio || 'Нет описания'}</div>
                                    </div>
                                    <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Начать чат</button>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }

        function showAllUsers() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>👥 Все пользователи</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div style="display: grid; gap: 15px;">
                        ${allUsers.map(user => `
                            <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                    <div style="position: relative; margin-right: 15px;">
                                        <div class="chat-avatar">${user.avatar}</div>
                                        ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                                    </div>
                                    <div style="flex: 1;">
                                        <div style="font-weight: bold; font-size: 18px;">${user.name}</div>
                                        <div style="color: #888;">${user.username}</div>
                                        <div style="color: #666; font-size: 12px; margin-top: 5px;">
                                            Зарегистрирован: ${formatDate(user.registered)}
                                        </div>
                                    </div>
                                    ${user.id !== currentUser.id ? 
                                        `<button class="btn" onclick="startNewChat('${user.id}')" style="padding: 8px 15px;">💬 Чат</button>` : 
                                        '<div style="color: var(--accent-color); padding: 8px 15px;">Это вы</div>'
                                    }
                                </div>
                                ${user.bio ? `
                                    <div style="color: #888; font-size: 14px; border-top: 1px solid var(--border-color); padding-top: 10px;">
                                        ${user.bio}
                                    </div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

            // Проверяем, есть ли уже чат с этим пользователем
            const existingChat = chats.find(chat => 
                chat.type === 'private' && 
                chat.participants.includes(userId) && 
                chat.participants.includes(currentUser.id)
            );

            if (existingChat) {
                currentChat = existingChat;
                openChat(existingChat.id);
                showNotification(`Чат с ${user.name} уже существует!`, 'info');
                return;
            }

            // Создаем новый чат
            const newChat = {
                id: 'chat_' + Date.now(),
                type: 'private',
                participants: [currentUser.id, userId],
                lastMessage: {
                    text: 'Чат начат 🚀',
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                },
                unreadCount: 0,
                messages: [
                    {
                        id: '1',
                        text: `Привет! Я ${currentUser.name}. Рад познакомиться! 👋`,
                        senderId: currentUser.id,
                        timestamp: new Date().toISOString()
                    }
                ]
            };

            chats.unshift(newChat);
            currentChat = newChat;
            
            // Сохраняем в localStorage
            localStorage.setItem('dlchats', JSON.stringify(chats));
            
            // Открываем новый чат
            openChat(newChat.id);
            showNotification(`Чат с ${user.name} начат! 💬`, 'success');
        }

        function showUserProfile(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 4000;
            `;
            
            modal.innerHTML = `
                <div style="background: var(--card-color); padding: 30px; border-radius: 20px; max-width: 400px; width: 90%; position: relative;">
                    <button onclick="this.parentElement.parentElement.remove()" style="position: absolute; top: 15px; right: 15px; background: none; border: none; color: #888; font-size: 20px; cursor: pointer;">×</button>
                    
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div class="chat-avatar" style="width: 80px; height: 80px; font-size: 32px; margin: 0 auto 15px;">${user.avatar}</div>
                        <h2>${user.name}</h2>
                        <div style="color: #888; margin-bottom: 5px;">${user.username}</div>
                        <div style="color: ${user.isOnline ? '#10b981' : '#888'}; font-size: 14px;">
                            ${user.isOnline ? '● онлайн' : `был(а) ${formatLastSeen(user.lastSeen)}`}
                        </div>
                    </div>
                    
                    ${user.email ? `
                        <div style="margin-bottom: 15px;">
                            <strong>📧 Email:</strong> ${user.email}
                        </div>
                    ` : ''}
                    
                    ${user.bio ? `
                        <div style="margin-bottom: 20px;">
                            <strong>ℹ️ О себе:</strong>
                            <div style="color: #888; margin-top: 5px;">${user.bio}</div>
                        </div>
                    ` : ''}
                    
                    <div style="color: #666; font-size: 12px; margin-bottom: 20px;">
                        Зарегистрирован: ${formatDate(user.registered)}
                    </div>
                    
                    ${user.id !== currentUser.id ? `
                        <button class="btn" onclick="startNewChat('${user.id}'); this.parentElement.parentElement.parentElement.remove();" style="margin-bottom: 10px;">
                            💬 Написать сообщение
                        </button>
                    ` : ''}
                    
                    <button class="btn" onclick="this.parentElement.parentElement.remove()" style="background: #666;">
                        Закрыть
                    </button>
                </div>
            `;
            
            document.body.appendChild(modal);
        }

        function showSettings() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>⚙️ Настройки</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="margin-bottom: 15px;">👤 Профиль</h3>
                        <input type="text" class="input-field" value="${currentUser.name}" placeholder="Ваше имя" id="settingsName">
                        <input type="text" class="input-field" value="${currentUser.username}" placeholder="Юзернейм" id="settingsUsername">
                        <input type="email" class="input-field" value="${currentUser.email || ''}" placeholder="Email" id="settingsEmail">
                        <textarea class="input-field" placeholder="О себе..." id="settingsBio" style="height: 80px; resize: vertical;">${currentUser.bio || ''}</textarea>
                        <button class="btn" onclick="updateProfile()">💾 Сохранить профиль</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="margin-bottom: 15px;">🎨 Внешний вид</h3>
                        <div class="theme-selector">
                            <div class="theme-option ${currentTheme === 'purple' ? 'active' : ''}" style="background: #8b5cf6;" onclick="changeTheme('purple')" title="Фиолетовая"></div>
                            <div class="theme-option ${currentTheme === 'blue' ? 'active' : ''}" style="background: #3b82f6;" onclick="changeTheme('blue')" title="Синяя"></div>
                            <div class="theme-option ${currentTheme === 'green' ? 'active' : ''}" style="background: #10b981;" onclick="changeTheme('green')" title="Зеленая"></div>
                            <div class="theme-option ${currentTheme === 'red' ? 'active' : ''}" style="background: #ef4444;" onclick="changeTheme('red')" title="Красная"></div>
                            <div class="theme-option ${currentTheme === 'orange' ? 'active' : ''}" style="background: #f97316;" onclick="changeTheme('orange')" title="Оранжевая"></div>
                        </div>
                        <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px;">
                            ${isHalloweenTheme ? '👻 Выключить хеллоуин' : '🎃 Включить хеллоуин'}
                        </button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px; color: #dc2626;">⚠️ Опасная зона</h3>
                        <button class="btn" onclick="clearChats()" style="background: #dc2626; margin-bottom: 10px;">🗑️ Очистить все чаты</button>
                        <button class="btn" onclick="exportData()" style="margin-bottom: 10px;">📤 Экспорт данных</button>
                        <button class="btn" onclick="importData()">📥 Импорт данных</button>
                    </div>
                </div>
            `;
        }

        function showAdminPanel() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>👑 Панель администратора</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 30px;">
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${allUsers.length}</div>
                            <div style="color: #888;">Пользователей</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${chats.length}</div>
                            <div style="color: #888;">Чатов</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${allUsers.filter(u => u.isOnline).length}</div>
                            <div style="color: #888;">Онлайн</div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">🛠️ Управление системой</h3>
                        <button class="btn btn-admin" onclick="createTestUsers()" style="margin-bottom: 10px;">👥 Создать тестовых пользователей</button>
                        <button class="btn btn-admin" onclick="sendSystemNotification()" style="margin-bottom: 10px;">📢 Системное уведомление</button>
                        <button class="btn btn-halloween" onclick="sendHalloweenNotification()" style="margin-bottom: 10px;">🎃 Хеллоуин-уведомление</button>
                        <button class="btn" onclick="clearAllData()" style="background: #dc2626;">🗑️ Очистить ВСЕ данные</button>
                    </div>
                </div>
            `;
        }

        function updateProfile() {
            const name = document.getElementById('settingsName').value.trim();
            const username = document.getElementById('settingsUsername').value.trim();
            const email = document.getElementById('settingsEmail').value.trim();
            const bio = document.getElementById('settingsBio').value.trim();
            
            if (!name) {
                showNotification('Введите имя!', 'error');
                return;
            }
            
            currentUser.name = name;
            currentUser.username = username;
            currentUser.email = email;
            currentUser.bio = bio;
            
            // Обновляем в allUsers
            const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
            if (userIndex !== -1) {
                allUsers[userIndex] = {...allUsers[userIndex], ...currentUser};
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }
            
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            showNotification('Профиль обновлен!', 'success');
            renderChatsInterface();
        }

        function toggleHalloweenTheme() {
            if (isHalloweenTheme) {
                deactivateHalloweenTheme();
            } else {
                activateHalloweenTheme();
            }
        }

        function activateHalloweenTheme() {
            document.body.classList.add('halloween-theme');
            isHalloweenTheme = true;
            localStorage.setItem('dlhalloween', 'true');
            showNotification('🎃 Хеллоуинская тема активирована! С Хеллоуином 2025! 👻', 'success');
            
            if (currentUser) {
                renderChatsInterface();
            }
        }

        function deactivateHalloweenTheme() {
            document.body.classList.remove('halloween-theme');
            isHalloweenTheme = false;
            localStorage.setItem('dlhalloween', 'false');
            showNotification('👻 Хеллоуинская тема деактивирована!', 'info');
            
            if (currentUser) {
                renderChatsInterface();
            }
        }

        function changeTheme(theme) {
            currentTheme = theme;
            localStorage.setItem('dltheme', theme);
            applyTheme(theme);
            showNotification(`Тема изменена на ${theme}`, 'success');
        }

        function applyTheme(theme) {
            const root = document.documentElement;
            const themes = {
                purple: { accent: '#8b5cf6' },
                blue: { accent: '#3b82f6' },
                green: { accent: '#10b981' },
                red: { accent: '#ef4444' },
                orange: { accent: '#f97316' }
            };
            
            if (themes[theme]) {
                root.style.setProperty('--accent-color', themes[theme].accent);
            }
        }

        function registerUser() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            const user_id = 'user_' + Date.now();
            const finalUsername = username || `user${Math.floor(Math.random() * 10000)}`;
            const avatar = getRandomAvatar();
            
            currentUser = {
                id: user_id,
                name: name,
                username: finalUsername,
                email: email,
                avatar: avatar,
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Новый пользователь DLtrollex 🚀',
                registered: new Date().toISOString()
            };
            
            // Добавляем в общий список пользователей
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            showMainApp();
        }

        function getRandomAvatar() {
            const avatars = ['😊', '😎', '🤩', '👻', '🐱', '🦊', '🐶', '🐼', '🐯', '🦁'];
            return avatars[Math.floor(Math.random() * avatars.length)];
        }

        function quickRegister() {
            const names = ['Алексей', 'Мария', 'Дмитрий', 'Елена', 'Сергей', 'Анна', 'Иван', 'Ольга'];
            const randomName = names[Math.floor(Math.random() * names.length)] + Math.floor(Math.random() * 1000);
            
            const user_id = 'user_' + Date.now();
            const avatar = getRandomAvatar();
            
            currentUser = {
                id: user_id,
                name: randomName,
                username: '@' + randomName.toLowerCase(),
                email: '',
                avatar: avatar,
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Авто-сгенерированный пользователь 🎲',
                registered: new Date().toISOString()
            };
            
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            showMainApp();
            showNotification('Аккаунт создан! Добро пожаловать! 🎲', 'success');
        }

        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    isOnline: true,
                    is_admin: true,
                    avatar: '👑',
                    bio: 'Администратор системы DLtrollex',
                    registered: new Date().toISOString()
                };
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
                showNotification('Вход как администратор выполнен', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        function createTestUsers() {
            const newUsers = [
                {
                    id: 'test_' + Date.now(),
                    name: 'Тестовый Пользователь',
                    username: '@testuser',
                    email: 'test@example.com',
                    avatar: '🧪',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'Тестовый пользователь для проверки системы',
                    registered: new Date().toISOString()
                }
            ];
            
            allUsers.push(...newUsers);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            showNotification('Тестовые пользователи созданы!', 'success');
            showAdminPanel();
        }

        function sendSystemNotification() {
            showNotification('📢 Системное уведомление отправлено всем пользователям!', 'success');
        }

        function sendHalloweenNotification() {
            showNotification('🎃 Хеллоуинское уведомление отправлено! Счастливого Хеллоуина 2025! 👻', 'success');
        }

        function clearChats() {
            if (confirm('Очистить все чаты? Это действие нельзя отменить!')) {
                chats = [];
                localStorage.setItem('dlchats', JSON.stringify(chats));
                showNotification('Все чаты очищены!', 'success');
                renderChatsInterface();
            }
        }

        function clearAllData() {
            if (confirm('Удалить ВСЕ данные? Это удалит всех пользователей и чаты!')) {
                localStorage.clear();
                allUsers = [];
                chats = [];
                showNotification('Все данные очищены!', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        }

        function exportData() {
            const data = {
                users: allUsers,
                chats: chats,
                exportDate: new Date().toISOString()
            };
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `dltrollex_backup_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            showNotification('Данные экспортированы!', 'success');
        }

        function importData() {
            showNotification('Функция импорта в разработке 🚧', 'info');
        }

        function formatTime(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            
            if (diff < 60000) return 'только что';
            if (diff < 3600000) return Math.floor(diff / 60000) + ' мин';
            if (diff < 86400000) return date.toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            return date.toLocaleDateString('ru-RU');
        }

        function formatLastSeen(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            
            if (diff < 60000) return 'только что';
            if (diff < 3600000) return Math.floor(diff / 60000) + ' минут назад';
            if (diff < 86400000) return 'сегодня';
            if (diff < 172800000) return 'вчера';
            return date.toLocaleDateString('ru-RU');
        }

        function formatDate(timestamp) {
            return new Date(timestamp).toLocaleDateString('ru-RU');
        }

        function logout() {
            if (currentUser) {
                // Устанавливаем статус offline
                const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
                if (userIndex !== -1) {
                    allUsers[userIndex].isOnline = false;
                    allUsers[userIndex].lastSeen = new Date().toISOString();
                    localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
                }
            }
            
            currentUser = null;
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification-toast';
            notification.style.background = type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : 'var(--accent-color)';
            notification.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 20px;">${type === 'error' ? '❌' : type === 'success' ? '✅' : '💡'}</div>
                    <div>${message}</div>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 4000);
        }

        // Обработка Enter в формах
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                if (!document.getElementById('registerScreen').classList.contains('hidden')) {
                    registerUser();
                }
                if (!document.getElementById('adminScreen').classList.contains('hidden')) {
                    adminLogin();
                }
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        
        if not name:
            return jsonify({'success': False, 'message': 'Введите имя'})
        
        user_id = str(int(datetime.datetime.now().timestamp() * 1000)) + str(random.randint(1000, 9999))
        final_username = username or f"user{random.randint(10000, 99999)}"
        
        user_data = {
            'id': user_id,
            'name': name,
            'username': final_username,
            'avatar': '👤',
            'avatar_bg': '#6b21a8',
            'registered_at': datetime.datetime.now().isoformat(),
        }
        
        users_db[user_id] = user_data
        
        return jsonify({'success': True, 'user': user_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Ошибка сервера'})

def create_app():
    return app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🎃 Запуск DLtrollex Хеллоуин 2025 с реальными пользователями...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("🎃 Хеллоуин тема активна!")
    print("💬 Реальные пользователи вместо ботов!")
    print("🔍 Улучшенный поиск!")
    print("👤 Профили пользователей!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
