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

# Админ
ADMIN_PASSWORD = "dltrollex123"

# STAFF пользователи
STAFF_USERS = {
    "staff2025": "staff_pass_2025",
    "moderator": "mod_pass_123",
    "support": "support_2025"
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
            --success-color: #10b981;
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
        
        /* Анимации */
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px var(--accent-color), 0 0 20px var(--accent-color); }
            50% { text-shadow: 0 0 20px var(--accent-color), 0 0 30px var(--accent-color), 0 0 40px var(--accent-color); }
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
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .glowing-logo { animation: glow 3s ease-in-out infinite; }
        .floating { animation: float 6s ease-in-out infinite; }
        .pulse { animation: pulse 2s ease-in-out infinite; }
        .slide-in { animation: slideIn 0.3s ease-out; }
        .fade-in { animation: fadeIn 0.5s ease-out; }
        
        /* Основные стили */
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
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn-staff {
            background: linear-gradient(135deg, var(--staff-color), #d97706);
        }
        
        .btn-staff:hover {
            box-shadow: 0 10px 25px rgba(245, 158, 11, 0.4);
        }
        
        .btn-premium {
            background: linear-gradient(135deg, var(--premium-color), #f59e0b);
        }
        
        .btn-premium:hover {
            box-shadow: 0 10px 25px rgba(251, 191, 36, 0.4);
        }
        
        .btn-admin {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        
        .btn-halloween {
            background: linear-gradient(135deg, #ff7b25, #ff5500);
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
        }
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
        }
        
        /* Стили для чата */
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
        
        /* Улучшения для мобильных устройств */
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
            
            .user-badge {
                font-size: 8px;
                padding: 1px 6px;
            }
        }
        
        @media (min-width: 1200px) {
            .chat-container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .sidebar {
                width: 400px;
            }
        }
        
        /* Дополнительные стили */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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
        }
        
        .feature-card:hover {
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
        
        .online-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }
        
        .message.encrypted::before {
            content: '🔒 ';
            font-size: 12px;
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
    <!-- Декорации -->
    <div class="halloween-decoration" style="top: 10%; left: 5%;">🎃</div>
    <div class="halloween-decoration" style="top: 20%; right: 10%;">👻</div>

    <!-- ПЕРВАЯ СТРАНИЦА -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Хеллоуин 2025 Edition + STAFF</div>
            
            <button class="btn pulse" onclick="showScreen('screen2')">
                <span>🚀 Продолжить</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                🔒 Безопасность • 🎨 Кастомизация • 👥 Реальные пользователи
            </div>
        </div>
    </div>

    <!-- ВТОРАЯ СТРАНИЦА -->
    <div id="screen2" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Выберите тип аккаунта</div>
            
            <div class="feature-grid">
                <div class="feature-card" onclick="showRegisterScreen()">
                    <div style="font-size: 32px; margin-bottom: 10px;">🚀</div>
                    <div>Обычный</div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Базовые функции</div>
                </div>
                
                <div class="feature-card" onclick="showStaffScreen()">
                    <div style="font-size: 32px; margin-bottom: 10px;">⭐</div>
                    <div>STAFF</div>
                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Расширенные возможности</div>
                </div>
            </div>
            
            <button class="btn" onclick="showScreen('screen1')">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- Обычная регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Создание обычного аккаунта</div>
            
            <input type="text" id="regName" class="input-field" placeholder="💁 Ваше имя" required>
            <input type="text" id="regUsername" class="input-field" placeholder="👤 Юзернейм">
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Создать аккаунт</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen2')">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- STAFF вход -->
    <div id="staffScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">⭐ DLtrollex STAFF</div>
            <div class="subtitle">Вход для сотрудников</div>
            
            <input type="text" id="staffUsername" class="input-field" placeholder="👤 STAFF логин">
            <input type="password" id="staffPassword" class="input-field" placeholder="🔒 STAFF пароль">
            
            <button class="btn btn-staff pulse" onclick="staffLogin()">
                <span>⭐ Войти как STAFF</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen2')">
                <span>← Назад</span>
            </button>
            
            <div style="margin-top: 15px; font-size: 12px; color: #888;">
                Доступно: staff2025, moderator, support
            </div>
        </div>
    </div>

    <!-- Основной интерфейс -->
    <div id="mainApp" class="app"></div>

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
            timeSpent: 0,
            lastLogin: null
        };

        // STAFF данные
        const STAFF_ACCOUNTS = {
            "staff2025": { password: "staff_pass_2025", role: "STAFF" },
            "moderator": { password: "mod_pass_123", role: "MODERATOR" },
            "support": { password: "support_2025", role: "SUPPORT" }
        };

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            initializeApp();
        });

        function initializeApp() {
            checkAutoLogin();
            loadHalloweenTheme();
            loadTheme();
            initializeData();
            loadUserStats();
            setupServiceWorker();
        }

        // Простые функции навигации
        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById('mainApp').style.display = 'none';
            document.getElementById(screenId).classList.remove('hidden');
        }

        function showRegisterScreen() { showScreen('registerScreen'); }
        function showStaffScreen() { showScreen('staffScreen'); }

        function showMainApp() {
            showScreen('mainApp');
            renderChatsInterface();
            showNotification(`Добро пожаловать${currentUser.staff ? ' как STAFF 👑' : ''}!`, 'success');
            startTimeTracking();
        }

        // STAFF логин
        function staffLogin() {
            const username = document.getElementById('staffUsername').value;
            const password = document.getElementById('staffPassword').value;
            
            if (STAFF_ACCOUNTS[username] && STAFF_ACCOUNTS[username].password === password) {
                currentUser = {
                    id: 'staff_' + Date.now(),
                    name: `STAFF ${username}`,
                    username: `@${username}`,
                    staff: true,
                    staffRole: STAFF_ACCOUNTS[username].role,
                    avatar: '⭐',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: `Сотрудник DLtrollex - ${STAFF_ACCOUNTS[username].role}`,
                    registered: new Date().toISOString(),
                    features: {
                        encryptedChats: true,
                        broadcastMessages: true,
                        userManagement: true,
                        analytics: true,
                        premiumThemes: true
                    }
                };
                
                saveUserData();
                showMainApp();
            } else {
                alert('Неверные STAFF данные!');
            }
        }

        // Обычная регистрация
        function registerUser() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            
            if (!name) {
                alert('Введите имя!');
                return;
            }
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: username || '@user' + Math.floor(Math.random() * 10000),
                staff: false,
                avatar: getRandomAvatar(),
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Пользователь DLtrollex 🚀',
                registered: new Date().toISOString(),
                features: {
                    encryptedChats: false,
                    broadcastMessages: false,
                    userManagement: false,
                    analytics: false,
                    premiumThemes: false
                }
            };
            
            saveUserData();
            showMainApp();
        }

        // Сохранение данных
        function saveUserData() {
            const savedUsers = localStorage.getItem('dlallUsers');
            if (savedUsers) {
                allUsers = JSON.parse(savedUsers);
            }
            allUsers.push(currentUser);
            
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            localStorage.setItem('dluserStats', JSON.stringify(userStats));
        }

        // Рендер интерфейса чата
        function renderChatsInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">
                                ${isHalloweenTheme ? '🎃' : '💜'} DLtrollex
                                ${currentUser.staff ? '<span class="user-badge badge-staff">STAFF</span>' : ''}
                            </div>
                            <div style="color: #888; font-size: 12px;">
                                Привет, ${currentUser.name}!
                                ${currentUser.staff ? `<br><span style="color: var(--staff-color);">${currentUser.staffRole}</span>` : ''}
                            </div>
                            
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
                        
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color);">
                            <input type="text" class="input-field" placeholder="🔍 Поиск..." style="margin-bottom: 0;">
                        </div>
                        
                        <div class="chats-list" style="flex: 1; overflow-y: auto;">
                            ${renderChatsList()}
                        </div>
                        
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            ${currentUser.staff ? `
                                <button class="btn btn-staff" onclick="showStaffPanel()" style="margin-bottom: 10px;">
                                    ⭐ STAFF Панель
                                </button>
                            ` : ''}
                            <button class="btn" onclick="showNewChatModal()" style="margin-bottom: 10px;">➕ Новый чат</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            <button class="btn" onclick="showFeatures()" style="margin-bottom: 10px;">🌟 Возможности</button>
                            <button class="btn" onclick="logout()" style="background: #dc2626;">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div class="logo glowing-logo" style="font-size: 80px;">
                                ${currentUser.staff ? '⭐' : isHalloweenTheme ? '🎃' : '💜'}
                            </div>
                            <h2>Добро пожаловать в DLtrollex!</h2>
                            <p style="color: #888; margin: 10px 0 20px 0; text-align: center;">
                                ${currentUser.staff ? 
                                    'Вы вошли как сотрудник. Доступны расширенные функции!' : 
                                    'Начните общение с другими пользователями'
                                }
                            </p>
                            <button class="btn" onclick="showNewChatModal()">💬 Начать общение</button>
                        </div>
                    </div>
                </div>
            `;
        }

        // STAFF панель
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
                        </div>
                        <div class="feature-card" onclick="showAnalytics()">
                            <div style="font-size: 32px;">📊</div>
                            <div>Аналитика</div>
                        </div>
                        <div class="feature-card" onclick="showUserManagement()">
                            <div style="font-size: 32px;">👥</div>
                            <div>Пользователи</div>
                        </div>
                        <div class="feature-card" onclick="showModTools()">
                            <div style="font-size: 32px;">🛠️</div>
                            <div>Модерация</div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px; margin-top: 20px;">
                        <h3 style="margin-bottom: 15px;">Статистика системы</h3>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div style="font-size: 24px; color: var(--accent-color);">${allUsers.length}</div>
                                <div style="font-size: 12px; color: #888;">Пользователей</div>
                            </div>
                            <div class="stat-card">
                                <div style="font-size: 24px; color: var(--accent-color);">${allUsers.filter(u => u.isOnline).length}</div>
                                <div style="font-size: 12px; color: #888;">Онлайн</div>
                            </div>
                            <div class="stat-card">
                                <div style="font-size: 24px; color: var(--accent-color);">${chats.length}</div>
                                <div style="font-size: 12px; color: #888;">Активных чатов</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Новые функции
        function broadcastMessage() {
            const message = prompt('Введите сообщение для рассылки:');
            if (message) {
                showNotification('📢 Сообщение отправлено всем пользователям!', 'success');
            }
        }

        function showAnalytics() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <h2>📊 Аналитика системы</h2>
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin-top: 20px;">
                        <h4>Активность пользователей</h4>
                        <div>Всего пользователей: ${allUsers.length}</div>
                        <div>Онлайн: ${allUsers.filter(u => u.isOnline).length}</div>
                        <div>STAFF: ${allUsers.filter(u => u.staff).length}</div>
                    </div>
                </div>
            `;
        }

        // Оптимизации
        function setupServiceWorker() {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/sw.js').catch(console.error);
            }
        }

        function startTimeTracking() {
            setInterval(() => {
                userStats.timeSpent++;
                localStorage.setItem('dluserStats', JSON.stringify(userStats));
            }, 60000);
        }

        // Вспомогательные функции
        function getRandomAvatar() {
            const avatars = ['😊', '😎', '🤩', '👻', '🐱', '🦊', '🐶', '🐼'];
            return avatars[Math.floor(Math.random() * avatars.length)];
        }

        function showNotification(message, type = 'info') {
            // Простая реализация уведомлений
            alert(message);
        }

        function logout() {
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        // Загрузка данных
        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
            }
        }

        function loadHalloweenTheme() {
            if (localStorage.getItem('dlhalloween') === 'true') {
                document.body.classList.add('halloween-theme');
                isHalloweenTheme = true;
            }
        }

        function loadTheme() {
            const theme = localStorage.getItem('dltheme') || 'purple';
            currentTheme = theme;
        }

        function initializeData() {
            const savedUsers = localStorage.getItem('dlallUsers');
            const savedChats = localStorage.getItem('dlchats');
            const savedStats = localStorage.getItem('dluserStats');
            
            allUsers = savedUsers ? JSON.parse(savedUsers) : [];
            chats = savedChats ? JSON.parse(savedChats) : [];
            userStats = savedStats ? JSON.parse(savedStats) : userStats;
        }

        function loadUserStats() {
            const saved = localStorage.getItem('dluserStats');
            if (saved) userStats = JSON.parse(saved);
        }

        // Заглушки для остальных функций
        function showNewChatModal() { alert('Функция в разработке'); }
        function showSettings() { alert('Настройки в разработке'); }
        function showFeatures() { alert('Возможности в разработке'); }
        function renderChatsList() { return '<div style="padding: 20px; color: #888; text-align: center;">Чатов пока нет</div>'; }
        function showUserManagement() { alert('Управление пользователями в разработке'); }
        function showModTools() { alert('Инструменты модерации в разработке'); }
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
        
        if not name:
            return jsonify({'success': False, 'message': 'Введите имя'})
        
        user_id = str(int(datetime.datetime.now().timestamp() * 1000))
        
        user_data = {
            'id': user_id,
            'name': name,
            'username': f"@{name}",
            'registered_at': datetime.datetime.now().isoformat(),
        }
        
        users_db[user_id] = user_data
        
        return jsonify({'success': True, 'user': user_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Ошибка сервера'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🎃 DLtrollex STAFF Edition запущен!")
    print(f"🔗 http://0.0.0.0:{port}")
    print("⭐ STAFF аккаунты: staff2025, moderator, support")
    app.run(host='0.0.0.0', port=port, debug=False)
