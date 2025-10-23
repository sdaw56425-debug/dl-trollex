# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ХЕЛЛОУИН 2025 + РЕАЛЬНЫЕ ПОЛЬЗОВАТЕЛИ + STAFF)
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
            --staff-color: #f59e0b;
            --premium-color: #fbbf24;
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
            display: flex;
            align-items: center;
            justify-content: center;
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
        
        .btn-staff {
            background: linear-gradient(135deg, var(--staff-color), #d97706);
        }
        
        .btn-staff:hover, .btn-staff:active {
            box-shadow: 0 10px 25px rgba(245, 158, 11, 0.4);
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
            pointer-events: none;
        }
        
        .chat-container {
            display: flex;
            height: 100vh;
            width: 100%;
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
            user-select: none;
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
            align-items: center;
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
        }
        
        .theme-option.active {
            border-color: white;
            transform: scale(1.1);
        }
        
        .user-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: bold;
            margin-left: 8px;
        }
        
        .badge-staff {
            background: var(--staff-color);
            color: black;
        }
        
        .badge-premium {
            background: var(--premium-color);
            color: black;
        }
        
        .badge-admin {
            background: #dc2626;
            color: white;
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

        /* Новые стили для оптимизации */
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
        }
        
        .feature-card:hover, .feature-card:active {
            transform: translateY(-5px);
            border-color: var(--accent-color);
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
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #888;
            font-style: italic;
            padding: 10px;
        }
        
        .typing-dots {
            display: flex;
            gap: 2px;
        }
        
        .typing-dot {
            width: 4px;
            height: 4px;
            background: var(--accent-color);
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
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
            <div class="subtitle">Хеллоуин 2025 Edition! + STAFF система</div>
            
            <button class="btn pulse" onclick="showScreen('screen2')">
                <span>🚀 Продолжить</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                🔒 Ваши данные хранятся локально • ⭐ STAFF доступ
            </div>
        </div>
    </div>

    <!-- ВТОРАЯ СТРАНИЦА - ПРОДОЛЖИТЬ -->
    <div id="screen2" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Выберите способ входа</div>
            
            <button class="btn pulse" onclick="showRegisterScreen()">
                <span>🚀 Обычный пользователь</span>
            </button>
            
            <button class="btn btn-staff pulse" onclick="showStaffScreen()">
                <span>⭐ STAFF вход</span>
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

    <!-- Экран STAFF -->
    <div id="staffScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">⭐ DLtrollex STAFF</div>
            <div class="subtitle">Вход для сотрудников</div>
            
            <input type="text" id="staffUsername" class="input-field" placeholder="👤 STAFF логин" required>
            <input type="password" id="staffPassword" class="input-field" placeholder="🔒 STAFF пароль" required>
            
            <button class="btn btn-staff pulse" onclick="staffLogin()">
                <span>⭐ Войти как STAFF</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen2')">
                <span>← Назад</span>
            </button>
            
            <div style="margin-top: 15px; font-size: 12px; color: #888;">
                Тестовые аккаунты: staff2025 / staff2025
            </div>
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

        // STAFF аккаунты
        const STAFF_ACCOUNTS = {
            "staff2025": "staff2025",
            "moderator": "moderator123", 
            "support": "support2025"
        };

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🎃 DLtrollex Хеллоуин 2025 + STAFF загружен!");
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

        function showStaffScreen() {
            showScreen('staffScreen');
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
            showNotification(`Добро пожаловать в DLtrollex${currentUser.staff ? ' как STAFF! ⭐' : ''}${isHalloweenTheme ? ' 🎃' : ''}!`, 'success');
            
            // Запускаем отслеживание времени
            startTimeTracking();
        }

        // STAFF логин
        function staffLogin() {
            const username = document.getElementById('staffUsername').value;
            const password = document.getElementById('staffPassword').value;
            
            if (STAFF_ACCOUNTS[username] && STAFF_ACCOUNTS[username] === password) {
                currentUser = {
                    id: 'staff_' + Date.now(),
                    name: `STAFF ${username}`,
                    username: `@${username}`,
                    staff: true,
                    staffRole: username.toUpperCase(),
                    avatar: '⭐',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: `Сотрудник DLtrollex - ${username}`,
                    registered: new Date().toISOString(),
                    features: {
                        encryptedChats: true,
                        broadcastMessages: true,
                        userManagement: true,
                        analytics: true,
                        premiumThemes: true
                    }
                };
                
                // Добавляем в общий список пользователей
                allUsers.push(currentUser);
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                
                userStats.logins++;
                saveUserStats();
                
                showMainApp();
            } else {
                alert('Неверные STAFF данные! Попробуйте: staff2025 / staff2025');
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
                registered: new Date().toISOString(),
                staff: false,
                features: {
                    encryptedChats: false,
                    broadcastMessages: false,
                    userManagement: false,
                    analytics: false,
                    premiumThemes: false
                }
            };
            
            // Добавляем в общий список пользователей
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            saveUserStats();
            
            showMainApp();
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
                    registered: new Date().toISOString(),
                    staff: true,
                    staffRole: 'ADMIN'
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
                    <!-- Боковая панель с чатами -->
                    <div class="sidebar">
                        <!-- Заголовок -->
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">
                                ${isHalloweenTheme ? '🎃' : '💜'} DLtrollex
                                ${currentUser.staff ? '<span class="user-badge badge-staff">STAFF</span>' : ''}
                                ${currentUser.is_admin ? '<span class="user-badge badge-admin">ADMIN</span>' : ''}
                            </div>
                            <div style="color: #888; font-size: 12px;">
                                Привет, ${currentUser.name}!
                                ${currentUser.staff ? `<br><span style="color: var(--staff-color);">⭐ ${currentUser.staffRole}</span>` : ''}
                            </div>
                            
                            <!-- Статистика -->
                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div style="font-size: 20px; color: var(--accent-color);">${userStats.messagesSent}</div>
                                    <div style="font-size: 10px; color: #888;">Сообщения</div>
                                </div>
                                <div class="stat-card">
                                    <div style="font-size: 20px; color: var(--accent-color);">${userStats.chatsCreated}</div>
                                    <div style="font-size: 10px; color: #888;">Чаты</div>
                                </div>
                                <div class="stat-card">
                                    <div style="font-size: 20px; color: var(--accent-color);">${Math.floor(userStats.timeSpent / 60)}</div>
                                    <div style="font-size: 10px; color: #888;">Минут</div>
                                </div>
                            </div>
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
                            ${currentUser.staff ? `
                                <button class="btn btn-staff" onclick="showStaffPanel()" style="margin-bottom: 10px;">
                                    ⭐ STAFF Панель
                                </button>
                            ` : ''}
                            <button class="btn" onclick="showNewChatModal()" style="margin-bottom: 10px;">➕ Новый чат</button>
                            <button class="btn" onclick="showAllUsers()" style="margin-bottom: 10px;">👥 Все пользователи</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px;">
                                ${isHalloweenTheme ? '👻 Выкл.Хеллоуин' : '🎃 Вкл.Хеллоуин'}
                            </button>
                            <button class="btn" onclick="logout()" style="margin-top: 10px; background: #dc2626;">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Область чата -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div class="logo glowing-logo ${isHalloweenTheme ? 'spooky' : ''}" style="font-size: 80px;">
                                ${currentUser.staff ? '⭐' : isHalloweenTheme ? '🎃' : '💜'}
                            </div>
                            <h2>Добро пожаловать в чаты!</h2>
                            <p style="color: #888; margin: 10px 0 20px 0; text-align: center;">
                                ${currentUser.staff ? 
                                    '⭐ Вы вошли как сотрудник. Доступны расширенные функции!' : 
                                    isHalloweenTheme ? '🎃 Найди новых друзей в хеллоуинском стиле! 👻' : 'Найди новых друзей и начни общение!'
                                }
                            </p>
                            <button class="btn" onclick="showNewChatModal()">💬 Начать новый чат</button>
                            ${currentUser.staff ? `
                                <div style="margin-top: 15px;">
                                    <button class="btn btn-staff" onclick="showStaffPanel()" style="width: auto; padding: 10px 20px;">
                                        ⭐ STAFF функции
                                    </button>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
        }

        // STAFF ПАНЕЛЬ
        function showStaffPanel() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>⭐ STAFF Панель</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div class="feature-grid">
                        <div class="feature-card" onclick="broadcastMessage()">
                            <div style="font-size: 32px;">📢</div>
                            <div>Рассылка</div>
                            <div style="font-size: 12px; color: #888;">Отправить всем</div>
                        </div>
                        <div class="feature-card" onclick="showAnalytics()">
                            <div style="font-size: 32px;">📊</div>
                            <div>Аналитика</div>
                            <div style="font-size: 12px; color: #888;">Статистика</div>
                        </div>
                        <div class="feature-card" onclick="showUserManagement()">
                            <div style="font-size: 32px;">👥</div>
                            <div>Пользователи</div>
                            <div style="font-size: 12px; color: #888;">Управление</div>
                        </div>
                        <div class="feature-card" onclick="showModTools()">
                            <div style="font-size: 32px;">🛠️</div>
                            <div>Модерация</div>
                            <div style="font-size: 12px; color: #888;">Инструменты</div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-top: 20px;">
                        <h3 style="margin-bottom: 15px;">📈 Статистика системы</h3>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div style="font-size: 24px; color: var(--accent-color);">${allUsers.length}</div>
                                <div style="font-size: 12px; color: #888;">Всего пользователей</div>
                            </div>
                            <div class="stat-card">
                                <div style="font-size: 24px; color: var(--accent-color);">${allUsers.filter(u => u.isOnline).length}</div>
                                <div style="font-size: 12px; color: #888;">Онлайн сейчас</div>
                            </div>
                            <div class="stat-card">
                                <div style="font-size: 24px; color: var(--accent-color);">${allUsers.filter(u => u.staff).length}</div>
                                <div style="font-size: 12px; color: #888;">STAFF</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // НОВЫЕ STAFF ФУНКЦИИ
        function broadcastMessage() {
            const message = prompt('Введите сообщение для рассылки всем пользователям:');
            if (message) {
                showNotification(`📢 Сообщение отправлено ${allUsers.length} пользователям!`, 'success');
            }
        }

        function showAnalytics() {
            const onlineUsers = allUsers.filter(u => u.isOnline).length;
            const staffUsers = allUsers.filter(u => u.staff).length;
            const regularUsers = allUsers.length - staffUsers;
            
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>📊 Аналитика системы</h2>
                        <button class="btn" onclick="showStaffPanel()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="margin-bottom: 15px;">Общая статистика</h3>
                        <div>Всего пользователей: <strong>${allUsers.length}</strong></div>
                        <div>Онлайн: <strong style="color: #10b981;">${onlineUsers}</strong></div>
                        <div>STAFF: <strong style="color: var(--staff-color);">${staffUsers}</strong></div>
                        <div>Обычные пользователи: <strong>${regularUsers}</strong></div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">Активность</h3>
                        <div>Сообщений отправлено: <strong>${userStats.messagesSent}</strong></div>
                        <div>Чатов создано: <strong>${userStats.chatsCreated}</strong></div>
                        <div>Время в системе: <strong>${Math.floor(userStats.timeSpent / 60)} минут</strong></div>
                    </div>
                </div>
            `;
        }

        function showUserManagement() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>👥 Управление пользователями</h2>
                        <button class="btn" onclick="showStaffPanel()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">Список пользователей (${allUsers.length})</h3>
                        <div style="max-height: 400px; overflow-y: auto;">
                            ${allUsers.map(user => `
                                <div style="display: flex; align-items: center; padding: 10px; border-bottom: 1px solid var(--border-color);">
                                    <div class="chat-avatar" style="width: 40px; height: 40px; font-size: 16px;">${user.avatar}</div>
                                    <div style="flex: 1; margin-left: 15px;">
                                        <div style="font-weight: bold;">
                                            ${user.name}
                                            ${user.staff ? '<span class="user-badge badge-staff">STAFF</span>' : ''}
                                            ${user.is_admin ? '<span class="user-badge badge-admin">ADMIN</span>' : ''}
                                        </div>
                                        <div style="color: #888; font-size: 12px;">${user.username}</div>
                                    </div>
                                    <div style="color: #888; font-size: 12px;">
                                        ${user.isOnline ? '<span style="color: #10b981;">● онлайн</span>' : 'офлайн'}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }

        function showModTools() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>🛠️ Инструменты модерации</h2>
                        <button class="btn" onclick="showStaffPanel()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">Быстрые действия</h3>
                        <button class="btn" onclick="clearAllChats()" style="margin-bottom: 10px;">🗑️ Очистить все чаты</button>
                        <button class="btn" onclick="resetUserStats()" style="margin-bottom: 10px;">📊 Сбросить статистику</button>
                        <button class="btn" onclick="createTestData()" style="margin-bottom: 10px;">🧪 Создать тестовые данные</button>
                    </div>
                </div>
            `;
        }

        function clearAllChats() {
            if (confirm('Очистить ВСЕ чаты? Это действие нельзя отменить!')) {
                chats = [];
                localStorage.setItem('dlchats', JSON.stringify(chats));
                showNotification('Все чаты очищены!', 'success');
            }
        }

        function resetUserStats() {
            if (confirm('Сбросить всю статистику?')) {
                userStats = { messagesSent: 0, chatsCreated: 0, logins: 0, timeSpent: 0 };
                saveUserStats();
                showNotification('Статистика сброшена!', 'success');
                showStaffPanel();
            }
        }

        function createTestData() {
            const testUsers = [
                {
                    id: 'test1',
                    name: 'Тест Пользователь 1',
                    username: '@test1',
                    avatar: '🧪',
                    isOnline: true,
                    bio: 'Тестовый аккаунт'
                },
                {
                    id: 'test2',
                    name: 'Тест Пользователь 2', 
                    username: '@test2',
                    avatar: '🔬',
                    isOnline: false,
                    bio: 'Еще один тестовый аккаунт'
                }
            ];
            
            allUsers.push(...testUsers);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            showNotification('Тестовые пользователи созданы!', 'success');
            showUserManagement();
        }

        // ОПТИМИЗАЦИИ
        function startTimeTracking() {
            setInterval(() => {
                if (currentUser) {
                    userStats.timeSpent++;
                    saveUserStats();
                }
            }, 60000);
        }

        // Остальные существующие функции остаются без изменений
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

        // Заглушки для остальных функций (оставлены без изменений)
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

        function searchUsers(query) {}
        function showNewChatModal() { alert('Функция в разработке'); }
        function showAllUsers() { alert('Функция в разработке'); }
        function showSettings() { alert('Функция в разработке'); }
        function formatTime(timestamp) { return 'только что'; }
        function formatLastSeen(timestamp) { return 'только что'; }
        function formatDate(timestamp) { return new Date(timestamp).toLocaleDateString('ru-RU'); }

        // Обработка Enter в формах
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                if (!document.getElementById('registerScreen').classList.contains('hidden')) {
                    registerUser();
                }
                if (!document.getElementById('adminScreen').classList.contains('hidden')) {
                    adminLogin();
                }
                if (!document.getElementById('staffScreen').classList.contains('hidden')) {
                    staffLogin();
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
    print("🎃 DLtrollex Хеллоуин 2025 + STAFF запущен!")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("🎃 Хеллоуин тема активна!")
    print("⭐ STAFF система: staff2025 / staff2025")
    print("📱 Оптимизировано для телефонов и ПК")
    
    app.run(host='0.0.0.0', port=port, debug=False)
