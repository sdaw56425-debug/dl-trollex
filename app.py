# DLtrollex - МЕССЕНДЖЕР С АВТО-ГЕНЕРАЦИЕЙ И ХЕЛЛОУИНОМ
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
        'text': 'Мессенджер с авто-генерацией профиля! 💜',
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
            padding: 12px 15px;
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
        
        .feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        
        .feature-card {
            background: var(--card-color);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
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
        
        .badge {
            background: var(--accent-color);
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 10px;
            margin-left: 5px;
        }
        
        .typing-indicator {
            color: #888;
            font-style: italic;
            padding: 10px;
            font-size: 12px;
        }
        
        .profile-preview {
            background: var(--secondary-color);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
        }
        
        .generated-name {
            font-size: 24px;
            font-weight: bold;
            color: var(--accent-color);
            margin: 10px 0;
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
            <div class="subtitle">Хеллоуин 2025 Edition! Авто-генерация профиля</div>
            
            <button class="btn pulse" onclick="generateAndContinue()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-admin pulse" onclick="showAdminScreen()">
                <span>👑 Войти как администратор</span>
            </button>
            
            <button class="btn btn-halloween pulse" onclick="toggleHalloweenTheme()">
                <span>🎃 Активировать хеллоуин!</span>
            </button>
        </div>
    </div>

    <!-- Экран сгенерированного профиля -->
    <div id="profileScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Ваш профиль сгенерирован!</div>
            
            <div class="profile-preview">
                <div class="chat-avatar" style="width: 80px; height: 80px; font-size: 32px; margin: 0 auto 15px;" id="generatedAvatar">👤</div>
                <div class="generated-name" id="generatedName">Имя</div>
                <div style="color: #888;" id="generatedUsername">@username</div>
                <div style="color: #666; font-size: 12px; margin-top: 10px;">Вы можете изменить эти данные в настройках</div>
            </div>
            
            <button class="btn pulse" onclick="continueWithProfile()">
                <span>✅ Продолжить</span>
            </button>
            
            <button class="btn" onclick="generateNewProfile()">
                <span>🔄 Сгенерировать заново</span>
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
        let currentTheme = 'purple';
        let isHalloweenTheme = false;
        let onlineUsers = new Set();
        let generatedProfile = null;

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
            // Загружаем пользователей из localStorage или создаем пустой массив
            const savedUsers = localStorage.getItem('dlallUsers');
            if (savedUsers) {
                allUsers = JSON.parse(savedUsers);
            } else {
                allUsers = [];
            }

            // Загружаем чаты
            const savedChats = localStorage.getItem('dlchats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
            
            // Обновляем онлайн статус текущего пользователя
            if (currentUser) {
                onlineUsers.add(currentUser.id);
            }
        }

        function generateAndContinue() {
            // Генерируем случайный профиль
            generatedProfile = generateRandomProfile();
            
            // Показываем экран сгенерированного профиля
            document.getElementById('generatedAvatar').textContent = generatedProfile.avatar;
            document.getElementById('generatedName').textContent = generatedProfile.name;
            document.getElementById('generatedUsername').textContent = generatedProfile.username;
            
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('profileScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function generateRandomProfile() {
            const names = [
                'Лунный Воин', 'Фиолетовая Искра', 'Темный Рыцарь', 'Светлый Ангел', 
                'Огненный Дракон', 'Ледяной Ветер', 'Таинственный Странник', 'Бессмертный Дух',
                'Хеллоуинский Призрак', 'Тыквенный Король', 'Ночной Охотник', 'Магический Воин',
                'Пурпурная Тень', 'Звездный Скиталец', 'Древний Мудрец', 'Серебряный Волк'
            ];
            
            const halloweenNames = [
                'Тыквенный Призрак', 'Хеллоуинский Ведьмак', 'Ночной Оборотень', 'Кровавая Луна',
                'Темный Алхимик', 'Зомби Охотник', 'Вампирский Лорд', 'Призрачный Рыцарь',
                'Паутинный Маг', 'Летучий Демон', 'Скелетный Воин', 'Проклятый Дух'
            ];
            
            const avatars = ['😊', '😎', '🤩', '🐱', '🦊', '🐶', '🐼', '🐯', '🦁', '🐮', '👻', '🎃', '🦇', '🕷️'];
            const halloweenAvatars = ['👻', '🎃', '🦇', '🕷️', '💀', '☠️', '🧛', '🧙'];
            
            const nameList = isHalloweenTheme ? halloweenNames : names;
            const avatarList = isHalloweenTheme ? halloweenAvatars : avatars;
            
            const randomName = nameList[Math.floor(Math.random() * nameList.length)];
            const randomAvatar = avatarList[Math.floor(Math.random() * avatarList.length)];
            const randomUsername = `user${Math.floor(Math.random() * 10000)}`;
            
            return {
                name: randomName,
                username: randomUsername,
                avatar: randomAvatar,
                bio: isHalloweenTheme ? 'Страшный и ужасный пользователь 🎃' : 'Новый пользователь DLtrollex 🚀'
            };
        }

        function generateNewProfile() {
            generatedProfile = generateRandomProfile();
            document.getElementById('generatedAvatar').textContent = generatedProfile.avatar;
            document.getElementById('generatedName').textContent = generatedProfile.name;
            document.getElementById('generatedUsername').textContent = generatedProfile.username;
        }

        function continueWithProfile() {
            if (!generatedProfile) {
                generatedProfile = generateRandomProfile();
            }
            
            // Создаем пользователя
            const user_id = 'user_' + Date.now();
            
            currentUser = {
                id: user_id,
                name: generatedProfile.name,
                username: generatedProfile.username,
                bio: generatedProfile.bio,
                avatar: generatedProfile.avatar,
                isOnline: true,
                lastSeen: new Date().toISOString(),
                registered: new Date().toISOString()
            };
            
            // Добавляем в общий список пользователей
            allUsers.push(currentUser);
            onlineUsers.add(user_id);
            
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            showMainApp();
        }

        function showMainScreen() {
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('profileScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('profileScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('profileScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            renderChatsInterface();
            showNotification(`Добро пожаловать в DLtrollex, ${currentUser.name}! 🎉`, 'success');
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
                            <div style="color: #10b981; font-size: 10px; margin-top: 5px;">● онлайн</div>
                            ${isHalloweenTheme ? '<div style="color: #ff7b25; font-size: 10px; margin-top: 2px;">🎃 Хеллоуин 2025!</div>' : ''}
                        </div>
                        
                        <!-- Поиск -->
                        <div class="search-box">
                            <input type="text" class="search-input" placeholder="🔍 Поиск пользователей..." oninput="searchUsers(this.value)">
                        </div>
                        
                        <!-- Список чатов -->
                        <div class="chats-list" id="chatsList">
                            ${renderChatsList()}
                        </div>
                        
                        <!-- Нижняя панель -->
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            <div class="feature-grid">
                                <div class="feature-card" onclick="showNewChatModal()">
                                    <div style="font-size: 24px; margin-bottom: 10px;">💬</div>
                                    <div>Новый чат</div>
                                </div>
                                <div class="feature-card" onclick="showAllUsers()">
                                    <div style="font-size: 24px; margin-bottom: 10px;">👥</div>
                                    <div>Все пользователи</div>
                                </div>
                                <div class="feature-card" onclick="showSettings()">
                                    <div style="font-size: 24px; margin-bottom: 10px;">⚙️</div>
                                    <div>Настройки</div>
                                </div>
                                <div class="feature-card" onclick="showStats()">
                                    <div style="font-size: 24px; margin-bottom: 10px;">📊</div>
                                    <div>Статистика</div>
                                </div>
                            </div>
                            
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-top: 10px; margin-bottom: 10px;">
                                ${isHalloweenTheme ? '👻 Выкл.Хеллоуин' : '🎃 Вкл.Хеллоуин'}
                            </button>
                            
                            ${currentUser && currentUser.is_admin ? 
                                '<button class="btn btn-admin" onclick="showAdminPanel()" style="margin-bottom: 10px;">👑 Админ-панель</button>' : ''}
                            <button class="btn" onclick="logout()" style="background: #dc2626;">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Область чата -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div class="logo glowing-logo ${isHalloweenTheme ? 'spooky' : ''}" style="font-size: 80px;">${isHalloweenTheme ? '🎃' : '💜'}</div>
                            <h2>Добро пожаловать в DLtrollex${isHalloweenTheme ? ' 🎃' : ''}!</h2>
                            <p style="color: #888; margin: 10px 0 20px 0; text-align: center;">
                                ${isHalloweenTheme ? 'Страшный мессенджер для ужасно веселого общения! 👻' : 'Мессенджер для реального общения с друзьями'}
                            </p>
                            <div class="feature-grid" style="max-width: 400px;">
                                <div class="feature-card" onclick="showNewChatModal()">
                                    <div style="font-size: 32px; margin-bottom: 15px;">💬</div>
                                    <div style="font-weight: bold;">Начать чат</div>
                                    <div style="color: #888; font-size: 12px; margin-top: 5px;">Создать новый чат</div>
                                </div>
                                <div class="feature-card" onclick="showAllUsers()">
                                    <div style="font-size: 32px; margin-bottom: 15px;">👥</div>
                                    <div style="font-weight: bold;">Найти друзей</div>
                                    <div style="color: #888; font-size: 12px; margin-top: 5px;">${allUsers.length - 1} пользователей</div>
                                </div>
                            </div>
                            ${isHalloweenTheme ? `
                                <div style="color: #ff7b25; margin-top: 20px; text-align: center;">
                                    <div style="font-size: 14px;">🎃 Счастливого Хеллоуина 2025! 👻</div>
                                    <div style="font-size: 12px; color: #888; margin-top: 5px;">Найдите страшных собеседников!</div>
                                </div>
                            ` : ''}
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
                const isOnline = onlineUsers.has(chatUser.id);
                
                return `
                    <div class="chat-item ${isActive ? 'active' : ''}" onclick="openChat('${chat.id}')">
                        <div style="position: relative;">
                            <div class="chat-avatar">${chatUser.avatar}</div>
                            ${isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div class="chat-info">
                            <div class="chat-name">
                                ${chatUser.name}
                                ${isOnline ? '<span class="user-status">● онлайн</span>' : ''}
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
            
            const isOnline = onlineUsers.has(chatUser.id);
            
            document.getElementById('chatContent').innerHTML = `
                <!-- Заголовок чата -->
                <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <div style="position: relative; margin-right: 15px;">
                            <div class="chat-avatar">${chatUser.avatar}</div>
                            ${isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div>
                            <div style="font-weight: bold; font-size: 16px;">${chatUser.name}</div>
                            <div style="color: #888; font-size: 12px;">
                                ${isOnline ? '● онлайн' : `был(а) ${formatLastSeen(chatUser.lastSeen)}`}
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
                
                <!-- Индикатор набора -->
                <div class="typing-indicator" id="typingIndicator" style="display: none;">
                    ${chatUser.name} печатает...
                </div>
                
                <!-- Ввод сообщения -->
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="💬 Введите сообщение..." id="messageInput" 
                           onkeypress="if(event.key=='Enter') sendMessage()" 
                           oninput="handleTyping()">
                    <button class="send-btn" onclick="sendMessage()">📤</button>
                    <button class="send-btn" onclick="showReactions()" style="background: #10b981;">😊</button>
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
                            ${msg.reaction ? `<span style="margin-left: 5px;">${msg.reaction}</span>` : ''}
                        </div>
                        <div style="font-size: 11px; color: ${isOwn ? 'rgba(255,255,255,0.7)' : '#888'}; text-align: ${isOwn ? 'right' : 'left'};">
                            ${formatTime(msg.timestamp)}
                            ${msg.edited ? '<span style="margin-left: 5px;">(изменено)</span>' : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function handleTyping() {
            const typingIndicator = document.getElementById('typingIndicator');
            if (typingIndicator) {
                typingIndicator.style.display = 'block';
                clearTimeout(window.typingTimeout);
                window.typingTimeout = setTimeout(() => {
                    typingIndicator.style.display = 'none';
                }, 1000);
            }
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
                    timestamp: new Date().toISOString(),
                    edited: false
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                
                // Сбрасываем индикатор набора
                const typingIndicator = document.getElementById('typingIndicator');
                if (typingIndicator) {
                    typingIndicator.style.display = 'none';
                }
                
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

        function showReactions() {
            const reactions = isHalloweenTheme ? 
                ['👻', '🎃', '🦇', '💀', '☠️', '🍬', '🕷️', '😱'] : 
                ['😊', '😂', '❤️', '🔥', '🎉', '👏', '👍', '🤔'];
                
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
                <div style="background: var(--card-color); padding: 20px; border-radius: 15px; text-align: center;">
                    <h3 style="margin-bottom: 15px;">${isHalloweenTheme ? '🎃 Выберите страшную реакцию!' : 'Выберите реакцию'}</h3>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                        ${reactions.map(reaction => `
                            <button onclick="sendReaction('${reaction}'); this.parentElement.parentElement.parentElement.remove();" 
                                    style="font-size: 24px; background: none; border: none; cursor: pointer; padding: 10px; border-radius: 10px; transition: background 0.2s;">
                                ${reaction}
                            </button>
                        `).join('')}
                    </div>
                    <button class="btn" onclick="this.parentElement.parentElement.remove()" style="margin-top: 15px;">Отмена</button>
                </div>
            `;
            
            document.body.appendChild(modal);
        }

        function sendReaction(reaction) {
            if (!currentChat || !currentChat.messages || currentChat.messages.length === 0) return;
            
            const lastMessage = currentChat.messages[currentChat.messages.length - 1];
            lastMessage.reaction = reaction;
            
            localStorage.setItem('dlchats', JSON.stringify(chats));
            openChat(currentChat.id);
            showNotification('Реакция отправлена!', 'success');
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
                searchHTML = filteredUsers.map(user => {
                    const isOnline = onlineUsers.has(user.id);
                    return `
                        <div class="chat-item" onclick="startNewChat('${user.id}')">
                            <div style="position: relative;">
                                <div class="chat-avatar">${user.avatar}</div>
                                ${isOnline ? '<div class="online-indicator"></div>' : ''}
                            </div>
                            <div class="chat-info">
                                <div class="chat-name">
                                    ${user.name}
                                    ${isOnline ? '<span class="user-status">● онлайн</span>' : ''}
                                </div>
                                <div class="chat-last-message">${user.bio || 'Нет описания'}</div>
                            </div>
                            <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Чат</button>
                        </div>
                    `;
                }).join('');
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
                    
                    ${availableUsers.length > 0 ? `
                        <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                            <h3 style="margin-bottom: 15px;">👥 Все пользователи (${availableUsers.length})</h3>
                            <div style="max-height: 60vh; overflow-y: auto;">
                                ${availableUsers.map(user => {
                                    const isOnline = onlineUsers.has(user.id);
                                    return `
                                        <div class="chat-item" onclick="startNewChat('${user.id}')">
                                            <div style="position: relative;">
                                                <div class="chat-avatar">${user.avatar}</div>
                                                ${isOnline ? '<div class="online-indicator"></div>' : ''}
                                            </div>
                                            <div class="chat-info">
                                                <div class="chat-name">
                                                    ${user.name}
                                                    ${isOnline ? '<span class="user-status">● онлайн</span>' : ''}
                                                </div>
                                                <div class="chat-last-message">${user.bio || 'Нет описания'}</div>
                                            </div>
                                            <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Начать чат</button>
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                    ` : `
                        <div style="text-align: center; padding: 40px 20px; color: #888;">
                            <div style="font-size: 48px; margin-bottom: 15px;">👥</div>
                            <div>Других пользователей пока нет</div>
                            <div style="font-size: 12px; margin-top: 5px;">Пригласите друзей присоединиться!</div>
                        </div>
                    `}
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
                        ${allUsers.map(user => {
                            const isOnline = onlineUsers.has(user.id);
                            const isCurrentUser = user.id === currentUser.id;
                            return `
                                <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                                    <div style="display: flex; align-items: center; margin-bottom: ${user.bio ? '15px' : '0'};">
                                        <div style="position: relative; margin-right: 15px;">
                                            <div class="chat-avatar">${user.avatar}</div>
                                            ${isOnline ? '<div class="online-indicator"></div>' : ''}
                                        </div>
                                        <div style="flex: 1;">
                                            <div style="font-weight: bold; font-size: 18px;">
                                                ${user.name}
                                                ${isCurrentUser ? '<span class="badge">Вы</span>' : ''}
                                            </div>
                                            <div style="color: #888;">${user.username}</div>
                                            <div style="color: #666; font-size: 12px; margin-top: 5px;">
                                                Зарегистрирован: ${formatDate(user.registered)}
                                            </div>
                                        </div>
                                        ${!isCurrentUser ? 
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
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

            // Проверяем, есть ли уже чат с этим пользователем
            const existingChat = chats.find(chat => 
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
                        timestamp: new Date().toISOString(),
                        edited: false
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

            const isOnline = onlineUsers.has(userId);
            const isCurrentUser = user.id === currentUser.id;

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
                        <h2>${user.name} ${isCurrentUser ? '<span class="badge">Вы</span>' : ''}</h2>
                        <div style="color: #888; margin-bottom: 5px;">${user.username}</div>
                        <div style="color: ${isOnline ? '#10b981' : '#888'}; font-size: 14px;">
                            ${isOnline ? '● онлайн' : `был(а) ${formatLastSeen(user.lastSeen)}`}
                        </div>
                    </div>
                    
                    ${user.bio ? `
                        <div style="margin-bottom: 20px;">
                            <strong>ℹ️ О себе:</strong>
                            <div style="color: #888; margin-top: 5px;">${user.bio}</div>
                        </div>
                    ` : ''}
                    
                    <div style="color: #666; font-size: 12px; margin-bottom: 20px;">
                        Зарегистрирован: ${formatDate(user.registered)}
                    </div>
                    
                    ${!isCurrentUser ? `
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
                        <button class="btn" onclick="clearAllData()" style="background: #dc2626;">🗑️ Полный сброс</button>
                    </div>
                </div>
            `;
        }

        function showStats() {
            const totalUsers = allUsers.length;
            const onlineCount = onlineUsers.size;
            const totalChats = chats.length;
            const totalMessages = chats.reduce((acc, chat) => acc + (chat.messages ? chat.messages.length : 0), 0);
            
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px; height: 100%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2>📊 Статистика</h2>
                        <button class="btn" onclick="renderChatsInterface()">← Назад</button>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px;">
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${totalUsers}</div>
                            <div style="color: #888;">Всего пользователей</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: #10b981;">${onlineCount}</div>
                            <div style="color: #888;">Сейчас онлайн</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${totalChats}</div>
                            <div style="color: #888;">Активных чатов</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: #f97316;">${totalMessages}</div>
                            <div style="color: #888;">Всего сообщений</div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 25px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">📈 Ваша активность</h3>
                        <div style="color: #888; margin-bottom: 10px;">Ваша регистрация: ${formatDate(currentUser.registered)}</div>
                        <div style="color: #888; margin-bottom: 10px;">Ваших чатов: ${chats.filter(chat => chat.participants.includes(currentUser.id)).length}</div>
                        <div style="color: #888;">Ваших сообщений: ${chats.reduce((acc, chat) => 
                            acc + (chat.messages ? chat.messages.filter(msg => msg.senderId === currentUser.id).length : 0), 0)}</div>
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
                            <div style="font-size: 24px; color: var(--accent-color);">${onlineUsers.size}</div>
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
            const bio = document.getElementById('settingsBio').value.trim();
            
            if (!name) {
                showNotification('Введите имя!', 'error');
                return;
            }
            
            currentUser.name = name;
            currentUser.username = username;
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

        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    bio: 'Администратор системы DLtrollex',
                    avatar: '👑',
                    isOnline: true,
                    is_admin: true,
                    lastSeen: new Date().toISOString(),
                    registered: new Date().toISOString()
                };
                onlineUsers.add('admin');
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
                showNotification('Вход как администратор выполнен', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        function createTestUsers() {
            const testUsers = [
                {
                    id: 'test_' + Date.now(),
                    name: 'Тестовый Пользователь',
                    username: '@testuser',
                    bio: 'Тестовый пользователь для проверки системы',
                    avatar: '🧪',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    registered: new Date().toISOString()
                }
            ];
            
            allUsers.push(...testUsers);
            testUsers.forEach(user => onlineUsers.add(user.id));
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
                onlineUsers.clear();
                showNotification('Все данные очищены!', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        }

        function exportData() {
            const data = {
                users: allUsers,
                chats: chats,
                exportDate: new Date().toISOString(),
                version: '1.0'
            };
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `dltrollex_backup_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            showNotification('Данные экспортированы!', 'success');
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
                onlineUsers.delete(currentUser.id);
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
    print("🎃 Запуск DLtrollex с авто-генерацией и хеллоуином...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("🚀 Авто-генерация профиля!")
    print("🎃 Хеллоуин 2025 тема!")
    print("👥 Только реальные пользователи!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
