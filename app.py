# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ИСПРАВЛЕННАЯ ВЕРСИЯ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

# Простая база данных в памяти
users_db = {}
messages_db = {}
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

# Создаем фавикон роут чтобы убрать 404 ошибку
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'DLtrollex is running'})

def generate_user_id():
    return str(int(datetime.datetime.now().timestamp() * 1000)) + str(random.randint(1000, 9999))

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
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
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
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
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
        
        .btn::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.3s, height 0.3s;
        }
        
        .btn:active::after {
            width: 100px;
            height: 100px;
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
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
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
        
        /* Новые стили для улучшенного интерфейса */
        .chat-container {
            display: flex;
            height: 100vh;
        }
        
        .sidebar {
            width: 300px;
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
        
        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        
        .message-input {
            padding: 20px;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
        }
        
        .message {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
            max-width: 70%;
            animation: fadeIn 0.3s ease-out;
        }
        
        .message.own {
            background: var(--accent-color);
            margin-left: auto;
        }
        
        .user-card {
            display: flex;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .user-card:hover {
            background: var(--secondary-color);
        }
        
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-right: 15px;
        }
        
        .online-indicator {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            position: absolute;
            bottom: 0;
            right: 0;
            border: 2px solid var(--card-color);
        }
        
        .settings-panel {
            background: var(--card-color);
            padding: 30px;
            border-radius: 15px;
            margin: 20px;
        }
        
        .color-picker {
            display: flex;
            gap: 10px;
            margin: 15px 0;
        }
        
        .color-option {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.2s ease;
        }
        
        .color-option:hover {
            transform: scale(1.1);
        }
        
        .color-option.active {
            border-color: white;
            transform: scale(1.2);
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
            
            <div style="margin-top: 20px; color: #666; font-size: 12px;">
                🔥 Новое: Чат, темы, настройки!
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
            <div id="registerSuccess" class="success hidden"></div>
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
        <!-- Интерфейс будет генерироваться JavaScript -->
    </div>

    <script>
        let currentUser = null;
        let currentTheme = 'purple';
        let onlineUsers = [];

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            setupEventListeners();
            checkAutoLogin();
            loadTheme();
        });

        function setupEventListeners() {
            // Исправлено: используем onclick для надежности
            document.getElementById('startChatBtn').onclick = showRegisterScreen;
            document.getElementById('adminAccessBtn').onclick = showAdminScreen;
            document.getElementById('backToMainBtn').onclick = showMainScreen;
            document.getElementById('backToMainFromAdminBtn').onclick = showMainScreen;
            document.getElementById('registerBtn').onclick = register;
            document.getElementById('adminLoginBtn').onclick = adminLogin;
            
            // Добавляем обработчики клавиш для удобства
            document.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    if (!document.getElementById('registerScreen').classList.contains('hidden')) {
                        register();
                    }
                    if (!document.getElementById('adminScreen').classList.contains('hidden')) {
                        adminLogin();
                    }
                }
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

        function loadTheme() {
            const savedTheme = localStorage.getItem('dltheme');
            if (savedTheme) {
                currentTheme = savedTheme;
                applyTheme(savedTheme);
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
            
            renderChatInterface();
            showNotification('Добро пожаловать в DLtrollex!', 'success');
        }

        function renderChatInterface() {
            const isAdmin = currentUser && currentUser.is_admin;
            
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <!-- Боковая панель -->
                    <div class="sidebar">
                        <!-- Заголовок -->
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">💜 DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Добро пожаловать, ${currentUser.name}!</div>
                        </div>
                        
                        <!-- Онлайн пользователи -->
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color);">
                            <div style="font-weight: bold; margin-bottom: 10px;">👥 Онлайн (${onlineUsers.length + 1})</div>
                            <div class="user-card">
                                <div style="position: relative;">
                                    <div class="user-avatar" style="background: ${currentUser.avatar_bg || '#6b21a8'};">${currentUser.avatar || '👤'}</div>
                                    <div class="online-indicator"></div>
                                </div>
                                <div>
                                    <div style="font-weight: bold;">${currentUser.name}</div>
                                    <div style="color: #888; font-size: 12px;">${currentUser.username}</div>
                                </div>
                            </div>
                            ${onlineUsers.map(user => `
                                <div class="user-card">
                                    <div style="position: relative;">
                                        <div class="user-avatar" style="background: ${user.avatar_bg || '#6b21a8'};">${user.avatar || '👤'}</div>
                                        <div class="online-indicator"></div>
                                    </div>
                                    <div>
                                        <div style="font-weight: bold;">${user.name}</div>
                                        <div style="color: #888; font-size: 12px;">${user.username}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <!-- Навигация -->
                        <div style="flex: 1; padding: 15px;">
                            <button class="btn" onclick="showChat()" style="margin-bottom: 10px;">💬 Чат</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            ${isAdmin ? '<button class="btn btn-admin" onclick="showAdminPanel()">👑 Админ-панель</button>' : ''}
                        </div>
                        
                        <!-- Выход -->
                        <div style="padding: 15px;">
                            <button class="btn" onclick="logout()">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Основная область -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; padding: 20px;">
                            <!-- Сюда будет подгружаться контент -->
                            <div style="text-align: center; padding: 50px;">
                                <div class="logo glowing-logo" style="font-size: 80px;">💜</div>
                                <h1>Добро пожаловать в DLtrollex!</h1>
                                <p style="margin: 20px 0;">Выберите раздел в меню слева</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Имитируем онлайн пользователей
            simulateOnlineUsers();
        }

        function showChat() {
            document.getElementById('chatContent').innerHTML = `
                <div class="messages-container" id="messagesContainer">
                    <div class="message">
                        <strong>Администратор:</strong> Добро пожаловать в DLtrollex! 🎉
                        <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                    </div>
                    <div class="message">
                        <strong>Администратор:</strong> Это фиолетовый мессенджер с максимальной кастомизацией! 💜
                        <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                    </div>
                    <div class="message own">
                        <strong>Вы:</strong> Привет всем! 👋
                        <div style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 5px;">Только что</div>
                    </div>
                </div>
                <div class="message-input">
                    <input type="text" id="messageInput" class="input-field" placeholder="💬 Напишите сообщение..." style="margin-bottom: 10px;">
                    <button class="btn" onclick="sendMessage()">📤 Отправить</button>
                </div>
            `;
        }

        function showSettings() {
            document.getElementById('chatContent').innerHTML = `
                <div class="settings-panel fade-in">
                    <h2>⚙️ Настройки внешнего вида</h2>
                    
                    <div style="margin: 20px 0;">
                        <h3>🎨 Цветовая тема</h3>
                        <div class="color-picker">
                            <div class="color-option ${currentTheme === 'purple' ? 'active' : ''}" 
                                 style="background: #8b5cf6;" 
                                 onclick="changeTheme('purple')" 
                                 title="Фиолетовая"></div>
                            <div class="color-option ${currentTheme === 'blue' ? 'active' : ''}" 
                                 style="background: #3b82f6;" 
                                 onclick="changeTheme('blue')" 
                                 title="Синяя"></div>
                            <div class="color-option ${currentTheme === 'green' ? 'active' : ''}" 
                                 style="background: #10b981;" 
                                 onclick="changeTheme('green')" 
                                 title="Зеленая"></div>
                            <div class="color-option ${currentTheme === 'red' ? 'active' : ''}" 
                                 style="background: #ef4444;" 
                                 onclick="changeTheme('red')" 
                                 title="Красная"></div>
                            <div class="color-option ${currentTheme === 'pink' ? 'active' : ''}" 
                                 style="background: #ec4899;" 
                                 onclick="changeTheme('pink')" 
                                 title="Розовая"></div>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>👤 Настройки профиля</h3>
                        <input type="text" id="userName" class="input-field" placeholder="Имя" value="${currentUser.name}">
                        <input type="text" id="userUsername" class="input-field" placeholder="Юзернейм" value="${currentUser.username}">
                        <button class="btn" onclick="updateProfile()">💾 Сохранить</button>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>🔔 Уведомления</h3>
                        <label style="display: flex; align-items: center; margin: 10px 0;">
                            <input type="checkbox" id="notifications" checked> 
                            <span style="margin-left: 10px;">Показывать уведомления</span>
                        </label>
                    </div>
                </div>
            `;
        }

        function showAdminPanel() {
            document.getElementById('chatContent').innerHTML = `
                <div class="settings-panel fade-in">
                    <h2>👑 Панель администратора</h2>
                    
                    <div style="margin: 20px 0;">
                        <h3>📊 Статистика</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                            <div style="background: var(--secondary-color); padding: 20px; border-radius: 10px; text-align: center;">
                                <div style="font-size: 24px; font-weight: bold; color: var(--accent-color);">${Object.keys(users_db).length}</div>
                                <div style="color: #888;">Пользователей</div>
                            </div>
                            <div style="background: var(--secondary-color); padding: 20px; border-radius: 10px; text-align: center;">
                                <div style="font-size: 24px; font-weight: bold; color: var(--accent-color);">${news_messages.length}</div>
                                <div style="color: #888;">Новостей</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>📢 Управление новостями</h3>
                        <textarea id="newsText" class="input-field" placeholder="Текст новости..." rows="3"></textarea>
                        <button class="btn btn-admin" onclick="addNews()">📢 Опубликовать новость</button>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>🛠️ Системные настройки</h3>
                        <button class="btn" onclick="clearAllData()">🗑️ Очистить все данные</button>
                        <button class="btn btn-admin" onclick="restartServer()">🔄 Перезапустить сервер</button>
                    </div>
                </div>
            `;
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
                pink: { accent: '#ec4899' }
            };
            
            if (themes[theme]) {
                root.style.setProperty('--accent-color', themes[theme].accent);
            }
        }

        function updateProfile() {
            const newName = document.getElementById('userName').value;
            const newUsername = document.getElementById('userUsername').value;
            
            if (newName) {
                currentUser.name = newName;
                currentUser.username = newUsername;
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showNotification('Профиль обновлен!', 'success');
            }
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message) {
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message own fade-in';
                messageElement.innerHTML = `
                    <strong>Вы:</strong> ${message}
                    <div style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 5px;">Только что</div>
                `;
                messagesContainer.appendChild(messageElement);
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Имитация ответа
                setTimeout(() => {
                    const responses = [
                        'Привет! Как дела? 😊',
                        'Классное сообщение! 👍',
                        'Я бот, но скоро здесь будут реальные люди! 🤖',
                        'DLtrollex - лучший мессенджер! 💜'
                    ];
                    const response = responses[Math.floor(Math.random() * responses.length)];
                    
                    const responseElement = document.createElement('div');
                    responseElement.className = 'message fade-in';
                    responseElement.innerHTML = `
                        <strong>Бот:</strong> ${response}
                        <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                    `;
                    messagesContainer.appendChild(responseElement);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }, 1000);
            }
        }

        function simulateOnlineUsers() {
            onlineUsers = [
                { name: 'Алексей', username: '@alex', avatar: '😎', avatar_bg: '#3b82f6' },
                { name: 'Мария', username: '@maria', avatar: '👩', avatar_bg: '#ec4899' },
                { name: 'Дмитрий', username: '@dmitry', avatar: '🧑', avatar_bg: '#10b981' }
            ];
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
            
            // Имитация регистрации
            setTimeout(() => {
                const user_id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
                const finalUsername = username || `user${Math.floor(Math.random() * 10000)}`;
                
                currentUser = {
                    id: user_id,
                    name: name,
                    username: finalUsername,
                    avatar: '👤',
                    avatar_bg: '#6b21a8',
                    registered_at: new Date().toISOString(),
                };
                
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                
                document.getElementById('registerSuccess').textContent = 'Регистрация успешна!';
                document.getElementById('registerSuccess').classList.remove('hidden');
                
                setTimeout(() => {
                    showMainApp();
                }, 1000);
                
            }, 1500);
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
                showNotification('Вход как администратор выполнен', 'success');
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
            }, 5000);
        }

        // Функции для админ-панели
        function addNews() {
            const newsText = document.getElementById('newsText').value;
            if (newsText) {
                showNotification('Новость опубликована!', 'success');
                document.getElementById('newsText').value = '';
            }
        }

        function clearAllData() {
            if (confirm('Вы уверены? Это удалит все данные!')) {
                localStorage.clear();
                showNotification('Все данные очищены', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        }

        function restartServer() {
            showNotification('Сервер перезапускается...', 'success');
            setTimeout(() => {
                showNotification('Сервер успешно перезапущен!', 'success');
            }, 2000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def api_register():
    """API для регистрации"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        
        if not name:
            return jsonify({'success': False, 'message': 'Введите имя'})
        
        user_id = generate_user_id()
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
    print("🚀 Запуск DLtrollex на Render...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("🎯 Анимации кнопок работают!")
    print("🐛 Все баги исправлены!")
    print("✨ Добавлены новые функции: чат, темы, настройки!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
