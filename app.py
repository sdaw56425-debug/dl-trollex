# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (БЫСТРАЯ РЕГИСТРАЦИЯ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

# База данных в памяти
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
            animation: fadeIn 0.3s ease-out;
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
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .message-input {
            padding: 20px;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 10px;
        }
        
        .message {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 15px;
            max-width: 70%;
            animation: fadeIn 0.3s ease-out;
            word-wrap: break-word;
        }
        
        .message.own {
            background: var(--accent-color);
            align-self: flex-end;
        }
        
        .message.system {
            background: #374151;
            align-self: center;
            max-width: 90%;
            text-align: center;
            font-style: italic;
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
            background: var(--accent-color);
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
            flex-wrap: wrap;
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
        
        .admin-stats {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: var(--secondary-color);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #888;
            font-size: 12px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        
        .feature-card {
            background: var(--secondary-color);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .quick-actions {
            display: flex;
            gap: 10px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        
        .quick-btn {
            padding: 10px 15px;
            background: var(--secondary-color);
            border: none;
            border-radius: 8px;
            color: var(--text-color);
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .quick-btn:hover {
            background: var(--accent-color);
            transform: translateY(-2px);
        }
        
        .typing-indicator {
            color: #888;
            font-style: italic;
            padding: 10px;
            display: none;
        }
        
        .message-time {
            font-size: 11px;
            color: rgba(255,255,255,0.6);
            margin-top: 5px;
            text-align: right;
        }
    </style>
</head>
<body>
    <!-- Главный экран выбора -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Ультра-быстрый чат с моментальной регистрацией!</div>
            
            <button class="btn pulse" id="startChatBtn">
                <span>⚡ Мгновенная регистрация</span>
            </button>
            
            <button class="btn btn-admin pulse" id="adminAccessBtn">
                <span>👑 Войти как администратор</span>
            </button>
            
            <div style="margin-top: 20px; color: #666; font-size: 12px;">
                🚀 Новое: Мгновенная регистрация, голосовые сообщения, реакции!
            </div>
        </div>
    </div>

    <!-- Экран регистрации -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Мгновенная регистрация</div>
            
            <input type="text" id="regName" class="input-field" placeholder="💁 Ваше имя" required autofocus>
            <input type="text" id="regUsername" class="input-field" placeholder="👤 @username (не обязательно)">
            <div class="optional">✨ Юзернейм не обязателен. Будет сгенерирован автоматически</div>
            
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
            
            <input type="password" id="adminPass" class="input-field" placeholder="🔒 Введите пароль администратора" autofocus>
            
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
        let chatMessages = [];
        let isTyping = false;

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            setupEventListeners();
            checkAutoLogin();
            loadTheme();
            loadChatHistory();
        });

        function setupEventListeners() {
            document.getElementById('startChatBtn').onclick = showRegisterScreen;
            document.getElementById('adminAccessBtn').onclick = showAdminScreen;
            document.getElementById('backToMainBtn').onclick = showMainScreen;
            document.getElementById('backToMainFromAdminBtn').onclick = showMainScreen;
            document.getElementById('registerBtn').onclick = register;
            document.getElementById('adminLoginBtn').onclick = adminLogin;
            
            // Быстрая регистрация по Enter
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

        function loadChatHistory() {
            const savedMessages = localStorage.getItem('dlchatMessages');
            if (savedMessages) {
                chatMessages = JSON.parse(savedMessages);
            }
        }

        function saveChatHistory() {
            localStorage.setItem('dlchatMessages', JSON.stringify(chatMessages));
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
            document.getElementById('regName').focus();
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
            document.getElementById('adminPass').focus();
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            renderChatInterface();
            showNotification(`Добро пожаловать, ${currentUser.name}! 🎉`, 'success');
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
                            <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                            <div style="color: #10b981; font-size: 10px; margin-top: 5px;">● Онлайн</div>
                        </div>
                        
                        <!-- Быстрые действия -->
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color);">
                            <div style="font-weight: bold; margin-bottom: 10px;">⚡ Быстрые действия</div>
                            <div class="quick-actions">
                                <button class="quick-btn" onclick="showChat()" title="Чат">💬</button>
                                <button class="quick-btn" onclick="showSettings()" title="Настройки">⚙️</button>
                                <button class="quick-btn" onclick="showThemes()" title="Темы">🎨</button>
                                <button class="quick-btn" onclick="showGames()" title="Игры">🎮</button>
                                ${isAdmin ? '<button class="quick-btn" onclick="showAdminPanel()" title="Админ">👑</button>' : ''}
                            </div>
                        </div>
                        
                        <!-- Онлайн пользователи -->
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color); flex: 1;">
                            <div style="font-weight: bold; margin-bottom: 10px;">👥 Онлайн (${onlineUsers.length + 1})</div>
                            <div class="user-card">
                                <div style="position: relative;">
                                    <div class="user-avatar">${getUserAvatar(currentUser.name)}</div>
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
                                        <div class="user-avatar">${getUserAvatar(user.name)}</div>
                                        <div class="online-indicator"></div>
                                    </div>
                                    <div>
                                        <div style="font-weight: bold;">${user.name}</div>
                                        <div style="color: #888; font-size: 12px;">${user.username}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <!-- Выход -->
                        <div style="padding: 15px;">
                            <button class="btn" onclick="logout()">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Основная область -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; flex-direction: column;">
                            <!-- Заглушка будет заменена контентом -->
                            <div style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                                <div class="logo glowing-logo" style="font-size: 80px;">💜</div>
                                <h1>Добро пожаловать в DLtrollex!</h1>
                                <p style="margin: 20px 0; color: #888;">Выберите действие в меню слева</p>
                                <div class="feature-grid">
                                    <div class="feature-card" onclick="showChat()">
                                        <div style="font-size: 24px; margin-bottom: 10px;">💬</div>
                                        <div>Чат</div>
                                    </div>
                                    <div class="feature-card" onclick="showSettings()">
                                        <div style="font-size: 24px; margin-bottom: 10px;">⚙️</div>
                                        <div>Настройки</div>
                                    </div>
                                    <div class="feature-card" onclick="showThemes()">
                                        <div style="font-size: 24px; margin-bottom: 10px;">🎨</div>
                                        <div>Темы</div>
                                    </div>
                                    <div class="feature-card" onclick="showGames()">
                                        <div style="font-size: 24px; margin-bottom: 10px;">🎮</div>
                                        <div>Игры</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            simulateOnlineUsers();
        }

        function getUserAvatar(name) {
            const avatars = ['😊', '😎', '🤩', '👻', '🐱', '🦊', '🐶', '🐼'];
            let hash = 0;
            for (let i = 0; i < name.length; i++) {
                hash = name.charCodeAt(i) + ((hash << 5) - hash);
            }
            return avatars[Math.abs(hash) % avatars.length];
        }

        function showChat() {
            document.getElementById('chatContent').innerHTML = `
                <div class="messages-container" id="messagesContainer">
                    ${chatMessages.map(msg => `
                        <div class="message ${msg.sender_id === currentUser.id ? 'own' : ''} ${msg.type === 'system' ? 'system' : ''}">
                            <strong>${msg.sender_name}:</strong> ${msg.text}
                            ${msg.reaction ? `<div style="margin-top: 5px;">${msg.reaction}</div>` : ''}
                            <div class="message-time">${formatTime(msg.timestamp)}</div>
                        </div>
                    `).join('')}
                </div>
                <div class="typing-indicator" id="typingIndicator">Кто-то печатает...</div>
                <div class="message-input">
                    <input type="text" id="messageInput" class="input-field" placeholder="💬 Напишите сообщение..." style="flex: 1;">
                    <button class="btn" onclick="sendMessage()">📤</button>
                    <button class="btn" onclick="showReactions()" style="padding: 10px;">😊</button>
                    <button class="btn" onclick="sendVoiceMessage()" style="padding: 10px;">🎤</button>
                </div>
            `;
            
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Фокус на поле ввода
            document.getElementById('messageInput').focus();
        }

        function showSettings() {
            document.getElementById('chatContent').innerHTML = `
                <div class="settings-panel fade-in">
                    <h2>⚙️ Настройки</h2>
                    
                    <div style="margin: 20px 0;">
                        <h3>👤 Профиль</h3>
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
                        <label style="display: flex; align-items: center; margin: 10px 0;">
                            <input type="checkbox" id="sounds" checked> 
                            <span style="margin-left: 10px;">Звуки уведомлений</span>
                        </label>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>💾 Данные</h3>
                        <button class="btn" onclick="exportData()">📤 Экспорт данных</button>
                        <button class="btn" onclick="importData()">📥 Импорт данных</button>
                        <button class="btn" onclick="clearChat()" style="background: #dc2626;">🗑️ Очистить чат</button>
                    </div>
                </div>
            `;
        }

        function showThemes() {
            document.getElementById('chatContent').innerHTML = `
                <div class="settings-panel fade-in">
                    <h2>🎨 Темы оформления</h2>
                    
                    <div style="margin: 20px 0;">
                        <h3>🌈 Цветовые схемы</h3>
                        <div class="color-picker">
                            <div class="color-option ${currentTheme === 'purple' ? 'active' : ''}" style="background: #8b5cf6;" onclick="changeTheme('purple')" title="Фиолетовая"></div>
                            <div class="color-option ${currentTheme === 'blue' ? 'active' : ''}" style="background: #3b82f6;" onclick="changeTheme('blue')" title="Синяя"></div>
                            <div class="color-option ${currentTheme === 'green' ? 'active' : ''}" style="background: #10b981;" onclick="changeTheme('green')" title="Зеленая"></div>
                            <div class="color-option ${currentTheme === 'red' ? 'active' : ''}" style="background: #ef4444;" onclick="changeTheme('red')" title="Красная"></div>
                            <div class="color-option ${currentTheme === 'pink' ? 'active' : ''}" style="background: #ec4899;" onclick="changeTheme('pink')" title="Розовая"></div>
                            <div class="color-option ${currentTheme === 'orange' ? 'active' : ''}" style="background: #f97316;" onclick="changeTheme('orange')" title="Оранжевая"></div>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>🌙 Ночной режим</h3>
                        <label style="display: flex; align-items: center; margin: 10px 0;">
                            <input type="checkbox" id="darkMode" checked> 
                            <span style="margin-left: 10px;">Темная тема</span>
                        </label>
                    </div>
                </div>
            `;
        }

        function showGames() {
            document.getElementById('chatContent').innerHTML = `
                <div class="settings-panel fade-in">
                    <h2>🎮 Игры и развлечения</h2>
                    
                    <div class="feature-grid">
                        <div class="feature-card" onclick="startGame('emoji')">
                            <div style="font-size: 24px; margin-bottom: 10px;">😀</div>
                            <div>Угадай эмодзи</div>
                        </div>
                        <div class="feature-card" onclick="startGame('quiz')">
                            <div style="font-size: 24px; margin-bottom: 10px;">❓</div>
                            <div>Викторина</div>
                        </div>
                        <div class="feature-card" onclick="startGame('tic-tac-toe')">
                            <div style="font-size: 24px; margin-bottom: 10px;">⭕</div>
                            <div>Крестики-нолики</div>
                        </div>
                        <div class="feature-card" onclick="showJokes()">
                            <div style="font-size: 24px; margin-bottom: 10px;">😂</div>
                            <div>Шутки</div>
                        </div>
                    </div>
                </div>
            `;
        }

        function showAdminPanel() {
            const userCount = Object.keys(users_db).length;
            const messageCount = chatMessages.length;
            
            document.getElementById('chatContent').innerHTML = `
                <div class="settings-panel fade-in">
                    <h2>👑 Панель администратора</h2>
                    
                    <div class="admin-stats">
                        <div class="stat-card">
                            <div class="stat-number">${userCount}</div>
                            <div class="stat-label">Пользователей</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${messageCount}</div>
                            <div class="stat-label">Сообщений</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${onlineUsers.length}</div>
                            <div class="stat-label">Онлайн</div>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>👥 Управление пользователями</h3>
                        <button class="btn" onclick="createTestUsers()">➕ Создать тестовых пользователей</button>
                        <button class="btn" onclick="showAllUsers()">📋 Список пользователей</button>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>📢 Системные сообщения</h3>
                        <textarea id="systemMessage" class="input-field" placeholder="Системное сообщение..." rows="3"></textarea>
                        <button class="btn btn-admin" onclick="sendSystemMessage()">📢 Отправить</button>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3>🛠️ Система</h3>
                        <button class="btn" onclick="clearAllData()">🗑️ Очистить все данные</button>
                        <button class="btn btn-admin" onclick="restartServer()">🔄 Перезапустить</button>
                    </div>
                </div>
            `;
        }

        // 🔥 ИСПРАВЛЕННАЯ РЕГИСТРАЦИЯ - БЕЗ ЗАДЕРЖЕК!
        function register() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            // МГНОВЕННАЯ регистрация
            const user_id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
            const finalUsername = username || `user${Math.floor(Math.random() * 10000)}`;
            
            currentUser = {
                id: user_id,
                name: name,
                username: finalUsername,
                avatar: getUserAvatar(name),
                registered_at: new Date().toISOString(),
            };
            
            // Сохраняем пользователя
            users_db[user_id] = currentUser;
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            // Мгновенный переход
            showMainApp();
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

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message) {
                const newMessage = {
                    id: Date.now().toString(),
                    text: message,
                    sender_id: currentUser.id,
                    sender_name: currentUser.name,
                    timestamp: new Date().toISOString(),
                    type: 'message'
                };
                
                chatMessages.push(newMessage);
                saveChatHistory();
                
                // Обновляем чат
                showChat();
                
                // Очищаем поле ввода
                input.value = '';
                
                // Имитация ответа
                simulateResponse();
            }
        }

        function simulateResponse() {
            setTimeout(() => {
                const responses = [
                    'Привет! Как дела? 😊',
                    'Интересное сообщение! 👍',
                    'Я бот DLtrollex! 🤖',
                    'Отличный мессенджер, правда? 💜',
                    'Скоро здесь будет много людей! 🚀'
                ];
                
                const response = responses[Math.floor(Math.random() * responses.length)];
                const botMessage = {
                    id: Date.now().toString(),
                    text: response,
                    sender_id: 'bot',
                    sender_name: 'Бот DLtrollex',
                    timestamp: new Date().toISOString(),
                    type: 'message'
                };
                
                chatMessages.push(botMessage);
                saveChatHistory();
                
                if (document.getElementById('messagesContainer')) {
                    showChat();
                }
            }, 1000);
        }

        function formatTime(timestamp) {
            return new Date(timestamp).toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }

        function simulateOnlineUsers() {
            onlineUsers = [
                { name: 'Алексей', username: '@alex' },
                { name: 'Мария', username: '@maria' },
                { name: 'Дмитрий', username: '@dmitry' },
                { name: 'Елена', username: '@elena' }
            ];
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
                pink: { accent: '#ec4899' },
                orange: { accent: '#f97316' }
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
                renderChatInterface();
            }
        }

        // Новые функции
        function showReactions() {
            const reactions = ['😀', '😍', '😂', '😮', '😢', '😡', '👍', '❤️', '🎉', '🔥'];
            const reactionPicker = document.createElement('div');
            reactionPicker.style.cssText = `
                position: fixed;
                background: var(--card-color);
                border: 2px solid var(--accent-color);
                border-radius: 15px;
                padding: 10px;
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 5px;
                z-index: 10000;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            `;
            
            reactions.forEach(reaction => {
                const btn = document.createElement('button');
                btn.textContent = reaction;
                btn.style.cssText = `
                    background: none;
                    border: none;
                    font-size: 20px;
                    cursor: pointer;
                    padding: 5px;
                    border-radius: 5px;
                    transition: background 0.2s;
                `;
                btn.onmouseover = () => btn.style.background = 'var(--secondary-color)';
                btn.onclick = () => {
                    sendReaction(reaction);
                    document.body.removeChild(reactionPicker);
                };
                reactionPicker.appendChild(btn);
            });
            
            document.body.appendChild(reactionPicker);
            
            // Позиционирование
            const input = document.getElementById('messageInput');
            const rect = input.getBoundingClientRect();
            reactionPicker.style.top = (rect.top - 60) + 'px';
            reactionPicker.style.left = (rect.left) + 'px';
        }

        function sendReaction(reaction) {
            const reactionMessage = {
                id: Date.now().toString(),
                text: reaction,
                sender_id: currentUser.id,
                sender_name: currentUser.name,
                timestamp: new Date().toISOString(),
                type: 'reaction'
            };
            
            chatMessages.push(reactionMessage);
            saveChatHistory();
            showChat();
        }

        function sendVoiceMessage() {
            showNotification('🎤 Функция голосовых сообщений скоро будет доступна!', 'info');
        }

        function createTestUsers() {
            const testUsers = [
                { name: 'Тестовый пользователь 1', username: '@test1' },
                { name: 'Тестовый пользователь 2', username: '@test2' },
                { name: 'Тестовый пользователь 3', username: '@test3' }
            ];
            
            testUsers.forEach(user => {
                const user_id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
                users_db[user_id] = {
                    id: user_id,
                    name: user.name,
                    username: user.username,
                    avatar: getUserAvatar(user.name),
                    registered_at: new Date().toISOString(),
                };
            });
            
            showNotification('Тестовые пользователи созданы!', 'success');
            showAdminPanel();
        }

        function showAllUsers() {
            const allUsers = Object.values(users_db);
            let usersHTML = '<h3>📋 Все пользователи</h3>';
            
            allUsers.forEach(user => {
                usersHTML += `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; margin: 5px 0; background: var(--secondary-color); border-radius: 8px;">
                        <div>
                            <strong>${user.name}</strong>
                            <div style="color: #888; font-size: 12px;">${user.username}</div>
                        </div>
                        <div style="font-size: 20px;">${user.avatar}</div>
                    </div>
                `;
            });
            
            document.querySelector('.settings-panel').innerHTML += usersHTML;
        }

        function sendSystemMessage() {
            const message = document.getElementById('systemMessage').value;
            if (message) {
                const systemMessage = {
                    id: Date.now().toString(),
                    text: message,
                    sender_id: 'system',
                    sender_name: 'Система',
                    timestamp: new Date().toISOString(),
                    type: 'system'
                };
                
                chatMessages.push(systemMessage);
                saveChatHistory();
                showNotification('Системное сообщение отправлено!', 'success');
                document.getElementById('systemMessage').value = '';
            }
        }

        function clearChat() {
            if (confirm('Очистить всю историю чата?')) {
                chatMessages = [];
                saveChatHistory();
                showNotification('Чат очищен!', 'success');
                showChat();
            }
        }

        function clearAllData() {
            if (confirm('Удалить ВСЕ данные? Это действие нельзя отменить!')) {
                localStorage.clear();
                Object.keys(users_db).forEach(key => delete users_db[key]);
                chatMessages = [];
                showNotification('Все данные очищены!', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        }

        function startGame(game) {
            showNotification(`Игра "${game}" запускается...`, 'info');
            // Здесь можно добавить логику игр
        }

        function showJokes() {
            const jokes = [
                "Почему программисты путают Хеллоуин и Рождество? Потому что Oct 31 == Dec 25!",
                "Какой у программиста любимый напиток? Java!",
                "Почему Python стал таким популярным? Потому что у него нет лишних скобок!",
                "Что сказал один бит другому? До скорой встречи!"
            ];
            
            const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
            const jokeMessage = {
                id: Date.now().toString(),
                text: randomJoke,
                sender_id: 'joke-bot',
                sender_name: 'Шутник',
                timestamp: new Date().toISOString(),
                type: 'system'
            };
            
            chatMessages.push(jokeMessage);
            saveChatHistory();
            showChat();
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
            }, 3000);
        }

        function restartServer() {
            showNotification('Сервер перезапускается...', 'success');
            setTimeout(() => {
                showNotification('Сервер успешно перезапущен!', 'success');
            }, 1500);
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
    print("🚀 Запуск DLtrollex с мгновенной регистрацией...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("⚡ Регистрация теперь мгновенная!")
    print("🎮 Добавлены игры и реакции!")
    print("👑 Улучшена админ-панель!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
