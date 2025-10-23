# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ХЕЛЛОУИН 2025 + РЕАЛЬНЫЕ ПОЛЬЗОВАТЕЛИ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

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
            --success-color: #10b981;
            --error-color: #ef4444;
            --story-color: #ec4899;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
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
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes bounce {
            0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
            40%, 43% { transform: translate3d(0,-8px,0); }
            70% { transform: translate3d(0,-4px,0); }
            90% { transform: translate3d(0,-2px,0); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
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
        
        .bounce {
            animation: bounce 1s ease;
        }
        
        .shake {
            animation: shake 0.5s ease-in-out;
        }
        
        .rainbow-text {
            background: linear-gradient(45deg, #ff6b6b, #ffa726, #4ecdc4, #45b7d1, #96ceb4, #ff9ff3);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbow 3s ease infinite;
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
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .credential-box {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid var(--accent-color);
            animation: pulse 2s infinite;
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
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
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
            animation: slideIn 0.3s ease-out;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .message:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .message.own {
            background: var(--accent-color);
            align-self: flex-end;
        }
        
        .message::before {
            content: '';
            position: absolute;
            bottom: -5px;
            width: 10px;
            height: 10px;
            background: inherit;
            transform: rotate(45deg);
        }
        
        .message.own::before {
            right: 10px;
        }
        
        .message:not(.own)::before {
            left: 10px;
        }
        
        .chat-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .chat-item:hover {
            background: var(--secondary-color);
            transform: translateX(5px);
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
            transition: all 0.3s ease;
        }
        
        .chat-item:hover .chat-avatar {
            transform: scale(1.1) rotate(5deg);
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
            animation: pulse 2s infinite;
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
        
        .floating-emoji {
            position: fixed;
            font-size: 20px;
            z-index: 99;
            opacity: 0.3;
            animation: float 8s ease-in-out infinite;
            pointer-events: none;
        }
        
        @media (max-width: 768px) {
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
            
            .auth-box {
                padding: 30px 20px;
            }
            
            .message {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <!-- Плавающие эмодзи -->
    <div class="floating-emoji" style="top: 10%; left: 5%; animation-delay: 0s;">✨</div>
    <div class="floating-emoji" style="top: 20%; right: 10%; animation-delay: 1s;">🎮</div>
    <div class="floating-emoji" style="top: 60%; left: 15%; animation-delay: 2s;">💜</div>
    <div class="floating-emoji" style="top: 80%; right: 20%; animation-delay: 3s;">🚀</div>

    <!-- ПЕРВАЯ СТРАНИЦА -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo rainbow-text">🎃 DLtrollex</div>
            <div class="subtitle">Ультра-кастомизируемый чат 2025</div>
            
            <button class="btn pulse" onclick="startQuickRegistration()">
                <span>💬 Начать общение</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                ✨ Анимации • 🎨 Красота • 💬 Реальные люди • 🚀 Быстро
            </div>
        </div>
    </div>

    <!-- РЕГИСТРАЦИЯ -->
    <div id="quickRegisterScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Для вас создан аккаунт!</div>
            
            <div class="credential-box slide-in">
                <div class="credential-field">
                    <span>👤 Имя:</span>
                    <span class="credential-value" id="generatedName">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 Пароль:</span>
                    <span class="credential-value" id="generatedPassword">...</span>
                </div>
            </div>
            
            <button class="btn btn-success pulse" onclick="quickRegister()">
                <span>🚀 Продолжить в чат!</span>
            </button>
            
            <button class="btn" onclick="generateNewCredentials()">
                <span>🔄 Сгенерировать заново</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen1')" style="background: #666;">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- ОСНОВНОЙ ИНТЕРФЕЙС -->
    <div id="mainApp" class="app hidden">
        <!-- Заполнится JavaScript -->
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let currentTheme = 'purple';

        // ИНИЦИАЛИЗАЦИЯ РЕАЛЬНЫХ ПОЛЬЗОВАТЕЛЕЙ
        function initializeRealUsers() {
            allUsers = [
                {
                    id: 'user1',
                    name: 'Алексей Кодеров',
                    username: '@alex_coder',
                    avatar: '👨‍💻',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'Fullstack разработчик | Люблю Python и JS',
                    city: 'Москва',
                    age: 28,
                    interests: ['Программирование', 'Музыка']
                },
                {
                    id: 'user2',
                    name: 'Мария Дизайнерова',
                    username: '@maria_design',
                    avatar: '👩‍🎨',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'UI/UX дизайнер | Люблю искусство',
                    city: 'СПб',
                    age: 25,
                    interests: ['Дизайн', 'Фотография']
                },
                {
                    id: 'user3',
                    name: 'Дмитрий Геймеров',
                    username: '@dima_gamer',
                    avatar: '🎮',
                    isOnline: false,
                    lastSeen: new Date(Date.now() - 3600000).toISOString(),
                    bio: 'Профессиональный геймер',
                    city: 'Новосибирск',
                    age: 22,
                    interests: ['Игры', 'Стриминг']
                }
            ];
        }

        document.addEventListener('DOMContentLoaded', function() {
            console.log("DLtrollex загружается...");
            initializeRealUsers();
            checkAutoLogin();
            createFloatingEmojis();
        });

        function createFloatingEmojis() {
            const emojis = ['🌟', '⚡', '💫', '🔥', '🌈', '🎭', '🎨'];
            const container = document.body;
            
            emojis.forEach((emoji, index) => {
                const element = document.createElement('div');
                element.className = 'floating-emoji';
                element.textContent = emoji;
                element.style.left = Math.random() * 90 + '%';
                element.style.top = Math.random() * 90 + '%';
                element.style.animationDelay = (Math.random() * 5) + 's';
                element.style.animationDuration = (8 + Math.random() * 7) + 's';
                container.appendChild(element);
            });
        }

        function startQuickRegistration() {
            showScreen('quickRegisterScreen');
            generateNewCredentials();
        }

        function showScreen(screenId) {
            console.log("Показываем экран:", screenId);
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById(screenId).classList.remove('hidden');
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
        }

        function generateUsername() {
            const adjectives = ['Весёлый', 'Серьёзный', 'Смелый', 'Умный', 'Быстрый', 'Креативный'];
            const nouns = ['Единорог', 'Дракон', 'Волк', 'Феникс', 'Тигр', 'Орёл'];
            return `${randomChoice(adjectives)}${randomChoice(nouns)}${Math.floor(Math.random() * 1000)}`;
        }

        function generatePassword() {
            return Math.random().toString(36).slice(-12);
        }

        function randomChoice(array) {
            return array[Math.floor(Math.random() * array.length)];
        }

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            const username = '@' + name.toLowerCase().replace(/[^a-z0-9]/g, '');
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: username,
                avatar: '😊',
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Новый пользователь DLtrollex 🚀',
                city: 'Москва',
                age: Math.floor(Math.random() * 20) + 18,
                interests: ['Общение', 'Знакомства']
            };

            allUsers.push(currentUser);
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            
            showMainApp();
            showNotification('Добро пожаловать в DLtrollex! 🎉', 'success');
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    const savedUsers = localStorage.getItem('dlallUsers');
                    if (savedUsers) allUsers = JSON.parse(savedUsers);
                    showMainApp();
                    showNotification('С возвращением! 👋', 'success');
                } catch (e) {
                    console.error("Ошибка автологина:", e);
                    localStorage.removeItem('dlcurrentUser');
                }
            }
        }

        function showMainApp() {
            showScreen('mainApp');
            renderMainInterface();
        }

        function renderMainInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div style="display: flex; align-items: center; gap: 15px;">
                                <div style="font-size: 32px; position: relative;">
                                    ${currentUser.avatar}
                                    <div class="online-indicator"></div>
                                </div>
                                <div>
                                    <div style="font-weight: bold; font-size: 18px;">${currentUser.name}</div>
                                    <div style="color: #888; font-size: 14px;">Онлайн 🟢</div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color); display: flex; gap: 10px;">
                            <button class="btn" onclick="showChats()" style="flex: 1;">💬 Чаты</button>
                            <button class="btn" onclick="showUsers()" style="flex: 1;">👥 Люди</button>
                            <button class="btn" onclick="showSettings()" style="flex: 1;">⚙️</button>
                        </div>
                        
                        <div id="contentArea" style="flex: 1; overflow-y: auto; padding: 10px;">
                            ${renderChatsList()}
                        </div>
                    </div>
                    
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column; padding: 20px;">
                            <div style="font-size: 80px; margin-bottom: 20px; animation: bounce 2s infinite;">💬</div>
                            <h2 style="margin-bottom: 10px; text-align: center;">Добро пожаловать!</h2>
                            <p style="color: #888; text-align: center; margin-bottom: 30px;">
                                Выберите чат для начала общения
                            </p>
                            <button class="btn pulse" onclick="showNewChatModal()" style="max-width: 200px;">
                                💬 Начать новый чат
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        function showChats() {
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <button class="btn" onclick="showNewChatModal()" style="width: 100%; margin-bottom: 15px;">
                        ➕ Новый чат
                    </button>
                    <div id="chatsList">
                        ${renderChatsList()}
                    </div>
                </div>
            `;
        }

        function renderChatsList() {
            if (chats.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px; animation: pulse 2s infinite;">💬</div>
                        <div>Чатов пока нет</div>
                        <div style="font-size: 12px; margin-top: 5px;">Начните новый чат</div>
                    </div>
                `;
            }
            
            return chats.map(chat => {
                const otherUserId = chat.participants.find(id => id !== currentUser.id);
                const otherUser = allUsers.find(u => u.id === otherUserId);
                if (!otherUser) return '';
                
                return `
                    <div class="chat-item slide-in" onclick="openChat('${chat.id}')">
                        <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                            <div style="position: relative;">
                                <div class="chat-avatar">${otherUser.avatar}</div>
                                ${otherUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: bold;">${otherUser.name}</div>
                                <div style="color: #888; font-size: 14px;">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function showUsers() {
            const availableUsers = allUsers.filter(u => u.id !== currentUser.id);
            
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <h3 style="margin-bottom: 15px;">👥 Все пользователи</h3>
                    <div style="max-height: 60vh; overflow-y: auto;">
                        ${availableUsers.map(user => `
                            <div class="chat-item slide-in" onclick="startNewChat('${user.id}')">
                                <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                                    <div style="position: relative;">
                                        <div class="chat-avatar">${user.avatar}</div>
                                        ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                                    </div>
                                    <div style="flex: 1;">
                                        <div style="font-weight: bold;">
                                            ${user.name}
                                            ${user.isOnline ? ' 🟢' : ' ⚫'}
                                        </div>
                                        <div style="color: #888; font-size: 14px;">${user.bio}</div>
                                    </div>
                                    <button class="btn" onclick="event.stopPropagation(); startNewChat('${user.id}')" style="padding: 8px 12px; font-size: 14px;">
                                        💬
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        function showNewChatModal() {
            showUsers();
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            const existingChat = chats.find(c => c.participants.includes(userId));
            
            if (existingChat) {
                openChat(existingChat.id);
                return;
            }

            const newChat = {
                id: 'chat_' + Date.now(),
                participants: [currentUser.id, userId],
                lastMessage: { 
                    text: 'Чат начат 🚀', 
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                },
                messages: [
                    { 
                        id: '1', 
                        text: `Привет! Я ${currentUser.name}. Рад познакомиться! 👋`, 
                        senderId: currentUser.id, 
                        timestamp: new Date().toISOString() 
                    }
                ]
            };

            chats.push(newChat);
            openChat(newChat.id);
            showNotification(`Чат с ${user.name} начат! 💬`, 'success');
        }

        function openChat(chatId) {
            currentChat = chats.find(c => c.id === chatId);
            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(id => id !== currentUser.id));
            
            document.getElementById('chatContent').innerHTML = `
                <div style="display: flex; flex-direction: column; height: 100%; width: 100%;">
                    <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="position: relative;">
                                <div style="font-size: 32px;">${otherUser.avatar}</div>
                                ${otherUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                            </div>
                            <div>
                                <div style="font-weight: bold; font-size: 18px;">${otherUser.name}</div>
                                <div style="color: #888; font-size: 14px;">${otherUser.bio}</div>
                            </div>
                        </div>
                        <button class="btn" onclick="renderMainInterface()" style="padding: 10px 15px;">
                            ← Назад
                        </button>
                    </div>
                    
                    <div class="messages-container" id="messagesContainer">
                        ${renderChatMessages()}
                    </div>
                    
                    <div style="padding: 15px; border-top: 1px solid var(--border-color); display: flex; gap: 10px;">
                        <input type="text" 
                               style="flex: 1; padding: 12px 15px; background: var(--secondary-color); border: 1px solid var(--border-color); border-radius: 25px; color: white; font-size: 16px;" 
                               placeholder="Введите сообщение..." 
                               id="messageInput"
                               onkeypress="if(event.key === 'Enter') sendMessage()">
                        <button class="btn" onclick="sendMessage()" style="padding: 12px 20px; min-width: 60px;">
                            📤
                        </button>
                    </div>
                </div>
            `;
            
            // Анимация появления чата
            document.getElementById('messagesContainer').classList.add('slide-in');
        }

        function renderChatMessages() {
            if (!currentChat.messages) return '';
            
            return currentChat.messages.map((msg, index) => {
                const isOwn = msg.senderId === currentUser.id;
                return `
                    <div class="message ${isOwn ? 'own' : ''} slide-in" style="animation-delay: ${index * 0.1}s">
                        <div>${msg.text}</div>
                        <div style="font-size: 11px; color: ${isOwn ? 'rgba(255,255,255,0.7)' : '#888'}; margin-top: 5px; text-align: ${isOwn ? 'right' : 'left'};">
                            ${new Date(msg.timestamp).toLocaleTimeString()}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (text && currentChat) {
                const newMessage = {
                    id: 'msg_' + Date.now(),
                    text: text,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                input.value = '';
                
                // Анимация отправки сообщения
                const messagesContainer = document.getElementById('messagesContainer');
                const newMessageElement = document.createElement('div');
                newMessageElement.className = 'message own slide-in';
                newMessageElement.innerHTML = `
                    <div>${text}</div>
                    <div style="font-size: 11px; color: rgba(255,255,255,0.7); margin-top: 5px; text-align: right;">
                        ${new Date().toLocaleTimeString()}
                    </div>
                `;
                messagesContainer.appendChild(newMessageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                showNotification('Сообщение отправлено! ✨', 'success');
            }
        }

        function showSettings() {
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 15px;">
                    <h3 style="margin-bottom: 20px;">⚙️ Настройки</h3>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                        <h4 style="margin-bottom: 15px;">👤 Профиль</h4>
                        <div style="text-align: center; margin-bottom: 15px;">
                            <div style="font-size: 48px; margin-bottom: 10px;">${currentUser.avatar}</div>
                            <div style="font-weight: bold;">${currentUser.name}</div>
                            <div style="color: #888; font-size: 14px;">${currentUser.username}</div>
                        </div>
                    </div>
                    
                    <button class="btn" onclick="logout()" style="background: #ef4444; width: 100%;">
                        🚪 Выйти
                    </button>
                </div>
            `;
        }

        function logout() {
            localStorage.removeItem('dlcurrentUser');
            showNotification('До свидания! 👋', 'success');
            setTimeout(() => location.reload(), 1000);
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

        // Добавляем обработчики для анимаций при наведении
        document.addEventListener('mouseover', function(e) {
            if (e.target.classList.contains('btn')) {
                e.target.classList.add('bounce');
            }
        });

        document.addEventListener('mouseout', function(e) {
            if (e.target.classList.contains('btn')) {
                e.target.classList.remove('bounce');
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🎃 DLtrollex с анимациями запущен!")
    print(f"🔗 http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
