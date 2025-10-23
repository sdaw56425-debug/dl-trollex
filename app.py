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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_username():
    adjectives = ['Весёлый', 'Серьёзный', 'Смелый', 'Умный', 'Быстрый', 'Креативный', 'Яркий', 'Тайный', 'Фиолетовый', 'Хеллоуинский']
    nouns = ['Единорог', 'Дракон', 'Волк', 'Феникс', 'Тигр', 'Орёл', 'Кот', 'Призрак', 'Тыква', 'Паук']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(100, 999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(12))

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
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
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
        
        @keyframes confetti {
            0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
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
        
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background: var(--accent-color);
            animation: confetti 3s linear forwards;
            z-index: 10000;
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
        
        .btn-success {
            background: linear-gradient(135deg, #10b981, #059669);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f59e0b, #d97706);
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
        
        .warning {
            color: #f59e0b;
            margin-top: 15px;
            padding: 10px;
            background: rgba(245, 158, 11, 0.1);
            border-radius: 8px;
            border: 1px solid #f59e0b;
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
        
        .message.system {
            background: var(--warning-color);
            align-self: center;
            max-width: 90%;
            font-style: italic;
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
        
        .credential-box {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid var(--accent-color);
        }
        
        .credential-field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 8px 0;
        }
        
        .credential-value {
            font-family: monospace;
            background: var(--card-color);
            padding: 5px 10px;
            border-radius: 5px;
            flex: 1;
            margin-left: 10px;
        }
        
        .copy-btn {
            background: var(--accent-color);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
        }
        
        .password-strength {
            height: 5px;
            border-radius: 5px;
            margin-top: 5px;
            transition: all 0.3s ease;
        }
        
        .strength-weak { background: #ef4444; width: 25%; }
        .strength-medium { background: #f59e0b; width: 50%; }
        .strength-strong { background: #10b981; width: 75%; }
        .strength-very-strong { background: #10b981; width: 100%; }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .feature-card {
            background: var(--card-color);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-color);
        }
        
        .feature-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .stat-card {
            background: var(--card-color);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: var(--accent-color);
        }
        
        .stat-label {
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <!-- Хеллоуинские декорации -->
    <div class="halloween-decoration" style="top: 10%; left: 5%;">🎃</div>
    <div class="halloween-decoration" style="top: 20%; right: 10%;">👻</div>
    <div class="halloween-decoration" style="bottom: 30%; left: 15%;">🦇</div>
    <div class="halloween-decoration" style="bottom: 20%; right: 5%;">🕷️</div>

    <!-- Главный экран выбора -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Хеллоуин 2025 Edition! Фиолетовый чат с реальными пользователями</div>
            
            <div class="feature-grid">
                <div class="feature-card" onclick="showRegisterScreen()">
                    <div class="feature-icon">🚀</div>
                    <div>Быстрый старт</div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Начать общение</div>
                </div>
                
                <div class="feature-card" onclick="showQuickRegisterScreen()">
                    <div class="feature-icon">🎲</div>
                    <div>Авто-регистрация</div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Сгенерировать аккаунт</div>
                </div>
            </div>
            
            <button class="btn btn-admin pulse" onclick="showAdminScreen()">
                <span>👑 Войти как администратор</span>
            </button>
            
            <button class="btn btn-halloween pulse" onclick="toggleHalloweenTheme()">
                <span>🎃 Активировать хеллоуин!</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                🔒 Ваши данные хранятся локально
            </div>
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
            <input type="password" id="regPassword" class="input-field" placeholder="🔒 Пароль" oninput="checkPasswordStrength(this.value)">
            <div class="password-strength" id="passwordStrength"></div>
            <div class="optional">✨ Заполните только имя и пароль - остальные поля не обязательны</div>
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Создать аккаунт</span>
            </button>
            
            <button class="btn" onclick="showMainScreen()">
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
            <div class="subtitle">Автоматическая регистрация</div>
            
            <div style="text-align: left; margin-bottom: 20px;">
                <p>Мы сгенерируем для вас:</p>
                <ul style="margin-left: 20px; color: #888;">
                    <li>Уникальное имя пользователя</li>
                    <li>Надежный пароль</li>
                    <li>Случайный аватар</li>
                </ul>
            </div>
            
            <div class="credential-box">
                <div class="credential-field">
                    <span>👤 Имя:</span>
                    <span class="credential-value" id="generatedName">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 Пароль:</span>
                    <span class="credential-value" id="generatedPassword">...</span>
                    <button class="copy-btn" onclick="copyToClipboard('generatedPassword')">📋</button>
                </div>
            </div>
            
            <button class="btn btn-success pulse" onclick="quickRegister()">
                <span>🎲 Сгенерировать и начать!</span>
            </button>
            
            <button class="btn" onclick="generateNewCredentials()">
                <span>🔄 Новые данные</span>
            </button>
            
            <button class="btn" onclick="showMainScreen()">
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
            
            <button class="btn" onclick="showMainScreen()">
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
        let userStats = {
            messagesSent: 0,
            chatsCreated: 0,
            logins: 0,
            timeSpent: 0
        };

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🎃 DLtrollex Хеллоуин 2025 загружен!");
            checkAutoLogin();
            loadHalloweenTheme();
            loadTheme();
            initializeData();
            loadUserStats();
        });

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    userStats.logins++;
                    saveUserStats();
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

        function loadUserStats() {
            const saved = localStorage.getItem('dluserStats');
            if (saved) {
                userStats = {...userStats, ...JSON.parse(saved)};
            }
        }

        function saveUserStats() {
            localStorage.setItem('dluserStats', JSON.stringify(userStats));
        }

        function initializeData() {
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
                        registered: new Date(Date.now() - 86400000).toISOString(),
                        password: 'hashed_password_1'
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
                        registered: new Date(Date.now() - 172800000).toISOString(),
                        password: 'hashed_password_2'
                    }
                ];
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }

            const savedChats = localStorage.getItem('dlchats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
        }

        function showMainScreen() {
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('quickRegisterScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showRegisterScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.remove('hidden');
            document.getElementById('quickRegisterScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showQuickRegisterScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('quickRegisterScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
            generateNewCredentials();
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('quickRegisterScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('quickRegisterScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            renderChatsInterface();
            showNotification(`Добро пожаловать в DLtrollex${isHalloweenTheme ? ' 🎃' : ''}!`, 'success');
            createConfetti();
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
        }

        function generateUsername() {
            const adjectives = ['Весёлый', 'Серьёзный', 'Смелый', 'Умный', 'Быстрый', 'Креативный', 'Яркий', 'Тайный', 'Фиолетовый', 'Хеллоуинский'];
            const nouns = ['Единорог', 'Дракон', 'Волк', 'Феникс', 'Тигр', 'Орёл', 'Кот', 'Призрак', 'Тыква', 'Паук'];
            return `${randomChoice(adjectives)}${randomChoice(nouns)}${Math.floor(Math.random() * 1000)}`;
        }

        function generatePassword() {
            const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
            let password = '';
            for (let i = 0; i < 12; i++) {
                password += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            return password;
        }

        function randomChoice(array) {
            return array[Math.floor(Math.random() * array.length)];
        }

        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Скопировано в буфер обмена! 📋', 'success');
            });
        }

        function checkPasswordStrength(password) {
            const strengthBar = document.getElementById('passwordStrength');
            let strength = 0;
            
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
            if (password.match(/\d/)) strength++;
            if (password.match(/[^a-zA-Z\d]/)) strength++;
            
            strengthBar.className = 'password-strength ';
            if (password.length === 0) {
                strengthBar.style.width = '0%';
            } else if (strength <= 1) {
                strengthBar.classList.add('strength-weak');
            } else if (strength === 2) {
                strengthBar.classList.add('strength-medium');
            } else if (strength === 3) {
                strengthBar.classList.add('strength-strong');
            } else {
                strengthBar.classList.add('strength-very-strong');
            }
        }

        function hashPassword(password) {
            // Простая имитация хеширования (в реальном приложении используйте bcrypt)
            return 'hashed_' + btoa(password).slice(0, 20);
        }

        function createConfetti() {
            const colors = ['#8b5cf6', '#ff7b25', '#10b981', '#3b82f6', '#f59e0b'];
            for (let i = 0; i < 50; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.animationDelay = Math.random() * 2 + 's';
                document.body.appendChild(confetti);
                
                setTimeout(() => confetti.remove(), 3000);
            }
        }

        // Остальные функции (renderChatsInterface, openChat, sendMessage, и т.д.) остаются похожими, 
        // но добавляем новые возможности:

        function renderChatsInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">${isHalloweenTheme ? '🎃' : '💜'} DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                            ${isHalloweenTheme ? '<div style="color: #ff7b25; font-size: 10px; margin-top: 5px;">🎃 Хеллоуин 2025 Активен!</div>' : ''}
                            
                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div class="stat-value">${userStats.messagesSent}</div>
                                    <div class="stat-label">Сообщений</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${userStats.chatsCreated}</div>
                                    <div class="stat-label">Чатов</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${userStats.logins}</div>
                                    <div class="stat-label">Входов</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="search-box">
                            <input type="text" class="search-input" placeholder="🔍 Поиск пользователей..." oninput="searchUsers(this.value)">
                        </div>
                        
                        <div class="chats-list" id="chatsList">
                            ${renderChatsList()}
                        </div>
                        
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            <button class="btn" onclick="showNewChatModal()" style="margin-bottom: 10px;">➕ Новый чат</button>
                            <button class="btn" onclick="showAllUsers()" style="margin-bottom: 10px;">👥 Все пользователи</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            <button class="btn" onclick="showFeatures()" style="margin-bottom: 10px;">🌟 Возможности</button>
                            ${currentUser && currentUser.is_admin ? '<button class="btn btn-admin" onclick="showAdminPanel()">👑 Админ</button>' : ''}
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px;">
                                ${isHalloweenTheme ? '👻 Выкл.Хеллоуин' : '🎃 Вкл.Хеллоуин'}
                            </button>
                            <button class="btn" onclick="logout()" style="margin-top: 10px; background: #dc2626;">🚪 Выйти</button>
                        </div>
                    </div>
                    
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

        function showFeatures() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>🌟 Возможности DLtrollex</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div class="feature-grid">
                        <div class="feature-card">
                            <div class="feature-icon">🔒</div>
                            <div>Безопасность</div>
                            <div style="font-size: 12px; color: #888;">Хеширование паролей</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🎨</div>
                            <div>Кастомизация</div>
                            <div style="font-size: 12px; color: #888;">Темы и настройки</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🎃</div>
                            <div>Хеллоуин тема</div>
                            <div style="font-size: 12px; color: #888;">Сезонный дизайн</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">👥</div>
                            <div>Реальные пользователи</div>
                            <div style="font-size: 12px; color: #888;">Живое общение</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">📊</div>
                            <div>Статистика</div>
                            <div style="font-size: 12px; color: #888;">Отслеживание активности</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🎲</div>
                            <div>Авто-регистрация</div>
                            <div style="font-size: 12px; color: #888;">Быстрый старт</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">🔍</div>
                            <div>Умный поиск</div>
                            <div style="font-size: 12px; color: #888;">Поиск по пользователям</div>
                        </div>
                        <div class="feature-card">
                            <div class="feature-icon">💾</div>
                            <div>Резервные копии</div>
                            <div style="font-size: 12px; color: #888;">Экспорт/импорт данных</div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-top: 20px;">
                        <h3 style="margin-bottom: 15px;">📈 Ваша статистика</h3>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-value">${userStats.messagesSent}</div>
                                <div class="stat-label">Отправлено сообщений</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${userStats.chatsCreated}</div>
                                <div class="stat-label">Создано чатов</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${userStats.logins}</div>
                                <div class="stat-label">Входов в систему</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${Math.floor(userStats.timeSpent / 60)}</div>
                                <div class="stat-label">Минут онлайн</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
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
                        <h3 style="margin-bottom: 15px;">🔒 Безопасность</h3>
                        <input type="password" class="input-field" placeholder="Текущий пароль" id="currentPassword">
                        <input type="password" class="input-field" placeholder="Новый пароль" id="newPassword" oninput="checkPasswordStrength(this.value)">
                        <div class="password-strength" id="passwordStrengthSettings"></div>
                        <input type="password" class="input-field" placeholder="Повторите новый пароль" id="confirmPassword">
                        <button class="btn" onclick="changePassword()">🔐 Сменить пароль</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="margin-bottom: 15px;">🎨 Внешний вид</h3>
                        <div class="theme-selector">
                            <div class="theme-option ${currentTheme === 'purple' ? 'active' : ''}" style="background: #8b5cf6;" onclick="changeTheme('purple')" title="Фиолетовая"></div>
                            <div class="theme-option ${currentTheme === 'blue' ? 'active' : ''}" style="background: #3b82f6;" onclick="changeTheme('blue')" title="Синяя"></div>
                            <div class="theme-option ${currentTheme === 'green' ? 'active' : ''}" style="background: #10b981;" onclick="changeTheme('green')" title="Зеленая"></div>
                            <div class="theme-option ${currentTheme === 'red' ? 'active' : ''}" style="background: #ef4444;" onclick="changeTheme('red')" title="Красная"></div>
                            <div class="theme-option ${currentTheme === 'orange' ? 'active' : ''}" style="background: #f97316;" onclick="changeTheme('orange')" title="Оранжевая"></div>
                            <div class="theme-option ${currentTheme === 'pink' ? 'active' : ''}" style="background: #ec4899;" onclick="changeTheme('pink')" title="Розовая"></div>
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

        function registerUser() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value;
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            if (!password) {
                document.getElementById('registerError').textContent = 'Введите пароль';
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
                registered: new Date().toISOString(),
                password: hashPassword(password)
            };
            
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            saveUserStats();
            
            showMainApp();
        }

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            
            const user_id = 'user_' + Date.now();
            const avatar = getRandomAvatar();
            
            currentUser = {
                id: user_id,
                name: name,
                username: '@' + name.toLowerCase().replace(/\s/g, ''),
                email: '',
                avatar: avatar,
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Авто-сгенерированный пользователь DLtrollex 🎲',
                registered: new Date().toISOString(),
                password: hashPassword(password)
            };
            
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            saveUserStats();
            
            showMainApp();
            showNotification(`Аккаунт создан! Пароль: ${password} - сохраните его!`, 'warning');
        }

        function changePassword() {
            const currentPass = document.getElementById('currentPassword').value;
            const newPass = document.getElementById('newPassword').value;
            const confirmPass = document.getElementById('confirmPassword').value;
            
            if (hashPassword(currentPass) !== currentUser.password) {
                showNotification('Текущий пароль неверен!', 'error');
                return;
            }
            
            if (newPass !== confirmPass) {
                showNotification('Пароли не совпадают!', 'error');
                return;
            }
            
            if (newPass.length < 6) {
                showNotification('Пароль должен быть не менее 6 символов!', 'error');
                return;
            }
            
            currentUser.password = hashPassword(newPass);
            
            const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
            if (userIndex !== -1) {
                allUsers[userIndex].password = currentUser.password;
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }
            
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            document.getElementById('currentPassword').value = '';
            document.getElementById('newPassword').value = '';
            document.getElementById('confirmPassword').value = '';
            
            showNotification('Пароль успешно изменен! 🔐', 'success');
        }

        // Остальные функции (sendMessage, searchUsers, и т.д.) остаются похожими, 
        // но обновляем их для учета статистики:

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
                
                localStorage.setItem('dlchats', JSON.stringify(chats));
                
                openChat(currentChat.id);
                renderChatsList();
                
                input.value = '';
                
                userStats.messagesSent++;
                saveUserStats();
                
                showNotification('Сообщение отправлено!', 'success');
            }
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

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
            
            localStorage.setItem('dlchats', JSON.stringify(chats));
            
            userStats.chatsCreated++;
            saveUserStats();
            
            openChat(newChat.id);
            showNotification(`Чат с ${user.name} начат! 💬`, 'success');
        }

        // ... остальные существующие функции ...

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
                    registered: new Date().toISOString(),
                    password: hashPassword('dltrollex123')
                };
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                
                userStats.logins++;
                saveUserStats();
                
                showMainApp();
                showNotification('Вход как администратор выполнен', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        // Таймер для отслеживания времени онлайн
        setInterval(() => {
            if (currentUser) {
                userStats.timeSpent++;
                saveUserStats();
            }
        }, 60000); // Каждую минуту

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
        password = data.get('password', '')
        
        if not name:
            return jsonify({'success': False, 'message': 'Введите имя'})
        
        if not password:
            return jsonify({'success': False, 'message': 'Введите пароль'})
        
        user_id = str(int(datetime.datetime.now().timestamp() * 1000)) + str(random.randint(1000, 9999))
        final_username = username or f"user{random.randint(10000, 99999)}"
        
        user_data = {
            'id': user_id,
            'name': name,
            'username': final_username,
            'avatar': '👤',
            'avatar_bg': '#6b21a8',
            'registered_at': datetime.datetime.now().isoformat(),
            'password': hash_password(password)
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
    print("🔒 Система паролей!")
    print("🎲 Авто-генерация аккаунтов!")
    print("📊 Статистика пользователя!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
