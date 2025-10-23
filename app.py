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
            -webkit-tap-highlight-color: transparent;
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
            touch-action: manipulation;
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
            padding: 20px;
        }
        
        .auth-box {
            background: var(--card-color);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 2px solid var(--accent-color);
            width: 100%;
            max-width: 450px;
            text-align: center;
            position: relative;
            overflow: hidden;
            z-index: 1001;
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
            font-size: 42px;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 15px;
        }
        
        .subtitle {
            color: #888;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .input-field {
            width: 100%;
            padding: 16px;
            margin-bottom: 15px;
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
            margin-top: -10px;
            margin-bottom: 20px;
            text-align: left;
        }
        
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            touch-action: manipulation;
            user-select: none;
            min-height: 50px;
            display: flex !important;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1002;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        .btn:hover, .btn:active {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn:active {
            transform: translateY(0px);
        }
        
        .btn-admin {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        
        .btn-admin:hover, .btn-admin:active {
            box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4);
        }
        
        .btn-halloween {
            background: linear-gradient(135deg, #ff7b25, #ff5500);
        }
        
        .btn-halloween:hover, .btn-halloween:active {
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
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
            position: relative;
            z-index: 1000;
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
            pointer-events: none;
        }
        
        .chat-container {
            display: flex;
            height: 100vh;
            width: 100%;
            position: relative;
            z-index: 1000;
        }
        
        .sidebar {
            width: 350px;
            background: var(--card-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 1001;
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 1001;
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
            user-select: none;
            position: relative;
            z-index: 1002;
        }
        
        .chat-item:hover, .chat-item:active {
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
            flex-shrink: 0;
        }
        
        .chat-info {
            flex: 1;
            min-width: 0;
        }
        
        .chat-name {
            font-weight: bold;
            margin-bottom: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
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
            flex-shrink: 0;
            margin-left: 10px;
        }
        
        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            position: relative;
            z-index: 1001;
        }
        
        .message {
            background: var(--secondary-color);
            padding: 12px 15px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
            position: relative;
            z-index: 1002;
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
            align-items: center;
            position: relative;
            z-index: 1001;
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
            min-width: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1002;
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
            transition: all 0.3s ease;
            position: relative;
            z-index: 1002;
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
            position: relative;
            z-index: 1001;
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
            word-break: break-all;
        }
        
        .copy-btn {
            background: var(--accent-color);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
            flex-shrink: 0;
            position: relative;
            z-index: 1002;
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
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
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
            cursor: pointer;
            user-select: none;
            position: relative;
            z-index: 1002;
        }
        
        .feature-card:hover, .feature-card:active {
            transform: translateY(-5px);
            border-color: var(--accent-color);
        }
        
        .feature-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .stat-card {
            background: var(--card-color);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            position: relative;
            z-index: 1001;
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

        /* Мобильные стили */
        @media (max-width: 768px) {
            .auth-box {
                padding: 30px 20px;
                margin: 10px;
            }
            
            .logo {
                font-size: 36px;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
            }
            
            .chat-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: 40vh;
            }
            
            .chat-area {
                height: 60vh;
            }
            
            .btn {
                min-height: 44px;
                padding: 14px;
            }
        }

        /* Гарантированная видимость кнопок */
        .btn {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        .screen {
            display: flex !important;
        }
    </style>
</head>
<body>
    <!-- Хеллоуинские декорации (упрощенные) -->
    <div class="halloween-decoration" style="top: 10%; left: 5%;">🎃</div>
    <div class="halloween-decoration" style="top: 20%; right: 10%;">👻</div>

    <!-- ПЕРВАЯ СТРАНИЦА - ПРОДОЛЖИТЬ -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Хеллоуин 2025 Edition! Фиолетовый чат с реальными пользователями</div>
            
            <button class="btn pulse" onclick="showScreen('screen2')">
                <span>🚀 Продолжить</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                🔒 Ваши данные хранятся локально • 🎲 Авто-генерация • 💬 Реальные чаты
            </div>
        </div>
    </div>

    <!-- ВТОРАЯ СТРАНИЦА - ПРОДОЛЖИТЬ -->
    <div id="screen2" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Выберите способ регистрации</div>
            
            <div class="feature-grid">
                <div class="feature-card" onclick="showRegisterScreen()">
                    <div class="feature-icon">🚀</div>
                    <div>Обычная регистрация</div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Создать аккаунт</div>
                </div>
                
                <div class="feature-card" onclick="showQuickRegisterScreen()">
                    <div class="feature-icon">🎲</div>
                    <div>Быстрая регистрация</div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Сгенерировать аккаунт</div>
                </div>
            </div>
            
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
            <input type="password" id="regPassword" class="input-field" placeholder="🔒 Пароль" oninput="checkPasswordStrength(this.value)">
            <div class="password-strength" id="passwordStrength"></div>
            <div class="optional">✨ Заполните только имя и пароль - остальные поля не обязательны</div>
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Создать аккаунт</span>
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
            
            // Проверка видимости кнопок
            setTimeout(() => {
                const buttons = document.querySelectorAll('.btn');
                console.log(`Найдено кнопок: ${buttons.length}`);
                buttons.forEach((btn, index) => {
                    console.log(`Кнопка ${index}:`, btn.textContent);
                });
            }, 500);
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
                    }
                ];
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }

            const savedChats = localStorage.getItem('dlchats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
        }

        // ПРОСТЫЕ ФУНКЦИИ ДЛЯ СМЕНЫ ЭКРАНОВ
        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById('mainApp').style.display = 'none';
            document.getElementById(screenId).classList.remove('hidden');
        }

        function showRegisterScreen() {
            showScreen('registerScreen');
        }

        function showQuickRegisterScreen() {
            showScreen('quickRegisterScreen');
            generateNewCredentials();
        }

        function showAdminScreen() {
            showScreen('adminScreen');
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById('mainApp').style.display = 'block';
            renderChatsInterface();
            showNotification(`Добро пожаловать в DLtrollex${isHalloweenTheme ? ' 🎃' : ''}!`, 'success');
            startTimeTracking();
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
                registered: new Date().toISOString()
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
                registered: new Date().toISOString()
            };
            
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            saveUserStats();
            
            showMainApp();
            showNotification(`Аккаунт создан! Пароль: ${password} - сохраните его!`, 'warning');
        }

        function getRandomAvatar() {
            const avatars = ['😊', '😎', '🤩', '👻', '🐱', '🦊', '🐶', '🐼', '🐯', '🦁'];
            return avatars[Math.floor(Math.random() * avatars.length)];
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
                
                userStats.logins++;
                saveUserStats();
                
                showMainApp();
                showNotification('Вход как администратор выполнен', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        function renderChatsInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">${isHalloweenTheme ? '🎃' : '💜'} DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                            ${isHalloweenTheme ? '<div style="color: #ff7b25; font-size: 10px; margin-top: 5px;">🎃 Хеллоуин 2025 Активен!</div>' : ''}
                        </div>
                        
                        <div class="search-box">
                            <input type="text" class="search-input" placeholder="🔍 Поиск пользователей..." oninput="searchUsers(this.value)">
                        </div>
                        
                        <div class="chats-list" id="chatsList">
                            ${renderChatsList()}
                        </div>
                        
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            <button class="btn" onclick="showNewChatModal()" style="margin-bottom: 10px;">➕ Новый чат</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            ${currentUser && currentUser.is_admin ? '<button class="btn btn-admin" onclick="showAdminPanel()">👑 Админ</button>' : ''}
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px;">
                                ${isHalloweenTheme ? '👻 Выкл.Хеллоуин' : '🎃 Вкл.Хеллоуин'}
                            </button>
                            <button class="btn" onclick="logout()" style="margin-top: 10px; background: #dc2626;">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div class="logo glowing-logo" style="font-size: 80px;">${isHalloweenTheme ? '🎃' : '💜'}</div>
                            <h2>Добро пожаловать в чаты!</h2>
                            <p style="color: #888; margin: 10px 0 20px 0; text-align: center;">
                                ${isHalloweenTheme ? '🎃 Найди новых друзей в хеллоуинском стиле! 👻' : 'Найди новых друзей и начни общение!'}
                            </p>
                            <button class="btn" onclick="showNewChatModal()">💬 Начать новый чат</button>
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
            return '';
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

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherParticipants = currentChat.participants.filter(p => p !== currentUser.id);
            const chatUser = allUsers.find(u => u.id === otherParticipants[0]);
            if (!chatUser) return;
            
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <div style="position: relative; margin-right: 15px;">
                            <div class="chat-avatar">${chatUser.avatar}</div>
                            ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div>
                            <div style="font-weight: bold; font-size: 16px;">${chatUser.name}</div>
                            <div style="color: #888; font-size: 12px;">
                                ${chatUser.isOnline ? 'online' : `был(а) ${formatLastSeen(chatUser.lastSeen)}`}
                            </div>
                        </div>
                    </div>
                    <div>
                        <button class="btn" onclick="renderChatsInterface()" style="padding: 8px 15px; font-size: 12px;">← Назад</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    ${renderChatMessages()}
                </div>
                
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="💬 Введите сообщение..." id="messageInput" onkeypress="if(event.key=='Enter') sendMessage()">
                    <button class="send-btn" onclick="sendMessage()">📤</button>
                </div>
            `;

            scrollToBottom();
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
                
                localStorage.setItem('dlchats', JSON.stringify(chats));
                
                openChat(currentChat.id);
                renderChatsList();
                
                input.value = '';
                
                userStats.messagesSent++;
                saveUserStats();
                
                showNotification('Сообщение отправлено!', 'success');
            }
        }

        function scrollToBottom() {
            const messagesContainer = document.getElementById('messagesContainer');
            if (messagesContainer) {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        }

        function searchUsers(query) {
            if (!query.trim()) {
                document.getElementById('chatsList').innerHTML = renderChatsList();
                return;
            }
            
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && (
                    user.name.toLowerCase().includes(query.toLowerCase()) ||
                    user.username.toLowerCase().includes(query.toLowerCase())
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
                            <div class="chat-name">${user.name}</div>
                            <div class="chat-last-message">${user.username}</div>
                        </div>
                        <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Чат</button>
                    </div>
                `).join('');
            } else {
                searchHTML = `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">🔍</div>
                        <div>Пользователи не найдены</div>
                    </div>
                `;
            }
            
            document.getElementById('chatsList').innerHTML = searchHTML;
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
                        <button class="btn" onclick="updateProfile()">💾 Сохранить профиль</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="margin-bottom: 15px;">🎨 Внешний вид</h3>
                        <div class="theme-selector">
                            <div class="theme-option ${currentTheme === 'purple' ? 'active' : ''}" style="background: #8b5cf6;" onclick="changeTheme('purple')"></div>
                            <div class="theme-option ${currentTheme === 'blue' ? 'active' : ''}" style="background: #3b82f6;" onclick="changeTheme('blue')"></div>
                            <div class="theme-option ${currentTheme === 'green' ? 'active' : ''}" style="background: #10b981;" onclick="changeTheme('green')"></div>
                        </div>
                        <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px;">
                            ${isHalloweenTheme ? '👻 Выключить хеллоуин' : '🎃 Включить хеллоуин'}
                        </button>
                    </div>
                </div>
            `;
        }

        function updateProfile() {
            const name = document.getElementById('settingsName').value.trim();
            const username = document.getElementById('settingsUsername').value.trim();
            
            if (!name) {
                showNotification('Введите имя!', 'error');
                return;
            }
            
            currentUser.name = name;
            currentUser.username = username;
            
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
            showNotification('🎃 Хеллоуинская тема активирована!', 'success');
            renderChatsInterface();
        }

        function deactivateHalloweenTheme() {
            document.body.classList.remove('halloween-theme');
            isHalloweenTheme = false;
            localStorage.setItem('dlhalloween', 'false');
            showNotification('👻 Хеллоуинская тема деактивирована!', 'info');
            renderChatsInterface();
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
                green: { accent: '#10b981' }
            };
            
            if (themes[theme]) {
                root.style.setProperty('--accent-color', themes[theme].accent);
            }
        }

        function showAdminPanel() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>👑 Панель администратора</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">Статистика</h3>
                        <div>Пользователей: ${allUsers.length}</div>
                        <div>Чатов: ${chats.length}</div>
                        <div>Онлайн: ${allUsers.filter(u => u.isOnline).length}</div>
                    </div>
                </div>
            `;
        }

        function formatTime(timestamp) {
            const date = new Date(timestamp);
            return date.toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
        }

        function formatLastSeen(timestamp) {
            return 'только что';
        }

        function startTimeTracking() {
            setInterval(() => {
                if (currentUser) {
                    userStats.timeSpent++;
                    saveUserStats();
                }
            }, 60000);
        }

        function logout() {
            if (currentUser) {
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
            }, 3000);
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
    print("🎃 DLtrollex Хеллоуин 2025 запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("🚀 Все кнопки теперь видны и работают!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
