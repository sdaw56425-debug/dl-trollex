from flask import Flask, render_template_string, request, jsonify, send_file
import datetime
import random
import os
import uuid
import json
import time
import io
from PIL import Image, ImageDraw, ImageFont
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trollexdl-premium-2024')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Создаем папку для загрузок
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class TrollexMessenger:
    def __init__(self):
        self.users = {}
        self.messages = {}
        self.groups = {}
        self.stories = {}
        self.server_start_time = time.time()
    
    def get_days_until_new_year(self):
        now = datetime.datetime.now()
        new_year = datetime.datetime(now.year + 1, 1, 1)
        return (new_year - now).days
    
    def generate_username(self):
        adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha', 'Cosmic', 'Galactic', 'Nova', 'Phantom', 'Shadow']
        nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther', 'Unicorn', 'Pegasus', 'Griffin', 'Fox', 'Bear']
        numbers = random.randint(1000, 9999)
        return f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"
    
    def generate_email(self, username):
        domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net', 'galaxy.tech', 'future.dev']
        return f"{username.lower()}@{random.choice(domains)}"
    
    def generate_user_id(self):
        return f"user_{uuid.uuid4().hex[:8]}"
    
    def get_server_stats(self):
        return {
            'uptime': int(time.time() - self.server_start_time),
            'users_online': random.randint(50, 500),
            'messages_today': random.randint(1000, 10000),
            'server_load': random.randint(10, 90)
        }
    
    def create_sample_users(self):
        sample_users = [
            {'id': 'user1', 'name': 'Алекс_Квантум', 'avatar': '👨‍💻', 'online': True, 'premium': 'vip'},
            {'id': 'user2', 'name': 'Сара_Кибер', 'avatar': '👩‍🎨', 'online': True, 'premium': 'premium'},
            {'id': 'user3', 'name': 'Майк_Неон', 'avatar': '👨‍🚀', 'online': False, 'premium': 'none'},
            {'id': 'user4', 'name': 'Эмма_Дигитал', 'avatar': '👩‍💼', 'online': True, 'premium': 'ultra'},
            {'id': 'user5', 'name': 'Том_Хайпер', 'avatar': '🧑‍🔬', 'online': False, 'premium': 'none'},
        ]
        
        for user in sample_users:
            self.users[user['id']] = user
    
    def generate_story_image(self, text, emoji):
        """Генерация изображения для сторис"""
        img = Image.new('RGB', (400, 600), color=(10, 10, 42))
        d = ImageDraw.Draw(img)
        
        # Простая реализация без шрифтов
        d.text((50, 200), text, fill=(107, 43, 217))
        d.text((180, 300), emoji, fill=(255, 255, 255))
        
        # Добавляем градиентный бордер
        for i in range(5):
            d.rectangle([i, i, 400-i, 600-i], outline=(139, 92, 246), width=1)
        
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return base64.b64encode(img_io.getvalue()).decode()

messenger = TrollexMessenger()
messenger.create_sample_users()

# HTML шаблон полностью в Python строке
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    
    <!-- PWA META TAGS -->
    <meta name="theme-color" content="#6c2bd9">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="TrollexDL">
    <link rel="manifest" href="/manifest.json">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        
        :root {
            --primary: #0a0a2a; --secondary: #1a1a4a; --accent: #6c2bd9; --accent-glow: #8b5cf6;
            --neon: #00ff88; --text: #ffffff; --text-secondary: #b0b0ff; --danger: #ff4444;
            --success: #00ff88; --warning: #ffaa00; --vip: #ffd700; --premium: #c0c0c0;
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            color: var(--text); min-height: 100vh; overflow-x: hidden;
        }

        .cosmic-bg {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 20% 80%, rgba(107, 43, 217, 0.4) 0%, transparent 50%),
                       radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.3) 0%, transparent 50%);
            animation: cosmicShift 20s ease-in-out infinite; z-index: -1;
        }

        @keyframes cosmicShift { 0%, 100% { opacity: 0.6; transform: scale(1); } 50% { opacity: 0.8; transform: scale(1.02); } }
        @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @keyframes glow { 0%, 100% { box-shadow: 0 0 20px var(--accent-glow); } 50% { box-shadow: 0 0 30px var(--accent-glow); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.8; } }

        .screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 20px; z-index: 1000; }
        .hidden { display: none !important; }

        .cosmic-card {
            background: rgba(26, 26, 74, 0.95); backdrop-filter: blur(20px); border: 2px solid var(--accent);
            border-radius: 25px; padding: 30px; width: 100%; max-width: 450px;
            animation: slideUp 0.6s ease-out, glow 4s infinite;
        }

        .logo {
            font-size: 2.8rem; font-weight: 900; text-align: center; margin-bottom: 20px;
            background: linear-gradient(45deg, var(--neon), var(--accent-glow), var(--accent));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: pulse 3s infinite;
        }

        .btn {
            width: 100%; padding: 16px 20px; border: none; border-radius: 15px; font-size: 1rem;
            font-weight: 700; cursor: pointer; transition: all 0.3s ease; margin-bottom: 12px;
            text-transform: uppercase; letter-spacing: 0.5px;
        }

        .btn-primary { background: linear-gradient(135deg, var(--accent), var(--accent-glow)); color: white; }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(107, 43, 217, 0.4); }
        .btn-secondary { background: rgba(255, 255, 255, 0.1); color: var(--text); border: 2px solid var(--accent); }

        .user-card {
            background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 20px; margin: 15px 0;
            border: 1px solid var(--accent); text-align: center; animation: slideUp 0.6s ease-out;
        }

        .user-avatar {
            width: 80px; height: 80px; border-radius: 20px; background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 12px;
            animation: pulse 3s ease-in-out infinite;
        }

        .app { width: 100%; height: 100vh; background: var(--primary); display: flex; }
        
        .sidebar {
            width: 100%; max-width: 380px; background: rgba(26, 26, 74, 0.95); backdrop-filter: blur(15px);
            border-right: 2px solid var(--accent); display: flex; flex-direction: column;
        }

        .user-header {
            padding: 25px; background: linear-gradient(135deg, var(--accent), var(--accent-glow)); text-align: center;
        }

        .chat-area { flex: 1; display: flex; flex-direction: column; background: var(--primary); }
        
        .chat-header {
            padding: 20px; background: rgba(26, 26, 74, 0.9); border-bottom: 2px solid var(--accent);
            display: flex; align-items: center; gap: 15px;
        }

        .messages-container { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        
        .message {
            max-width: 80%; padding: 15px 18px; border-radius: 20px; position: relative;
            animation: slideUp 0.4s ease-out;
        }

        .message.received { background: rgba(107, 43, 217, 0.25); align-self: flex-start; border: 1px solid var(--accent); }
        .message.sent { background: linear-gradient(135deg, var(--accent), var(--accent-glow)); align-self: flex-end; color: white; }

        .message-input-container {
            padding: 20px; background: rgba(26, 26, 74, 0.9); border-top: 2px solid var(--accent);
            display: flex; gap: 12px; align-items: center;
        }

        .message-input {
            flex: 1; padding: 15px 20px; background: rgba(255, 255, 255, 0.1); border: 2px solid var(--accent);
            border-radius: 25px; color: var(--text); font-size: 1rem; outline: none;
        }

        .send-btn { padding: 15px 25px; background: linear-gradient(135deg, var(--accent), var(--accent-glow)); color: white; border: none; border-radius: 20px; cursor: pointer; }

        .online-users { background: rgba(255, 255, 255, 0.05); padding: 15px; margin: 15px; border-radius: 15px; }
        
        .online-user {
            display: flex; align-items: center; padding: 10px; margin: 5px 0; border-radius: 10px;
            transition: all 0.3s ease; cursor: pointer;
        }

        .online-user:hover { background: rgba(107, 43, 217, 0.2); transform: translateX(5px); }

        .nav-tabs { display: flex; background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 6px; margin: 15px; gap: 4px; }
        
        .nav-tab {
            flex: 1; padding: 12px 8px; text-align: center; border-radius: 12px; cursor: pointer;
            transition: all 0.3s ease; font-weight: 600; min-width: 60px;
        }

        .nav-tab.active { background: linear-gradient(135deg, var(--accent), var(--accent-glow)); color: white; transform: scale(1.05); }

        @media (max-width: 768px) {
            .sidebar { position: fixed; height: 100%; transform: translateX(-100%); transition: transform 0.4s ease; z-index: 300; max-width: 85%; }
            .sidebar.active { transform: translateX(0); }
            .cosmic-card { padding: 20px; margin: 15px; }
            .message { max-width: 90%; }
        }
    </style>
</head>
<body>
    <div class="cosmic-bg"></div>
    
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="text-align: center; margin: 30px 0;">
                <div style="width: 60px; height: 60px; border: 4px solid rgba(139, 92, 246, 0.3); border-top: 4px solid #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
            </div>
            <div style="text-align: center; color: var(--text-secondary);" id="loadingText">Загрузка космического интерфейса...</div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="text-align: center; color: var(--text-secondary); margin-bottom: 30px; line-height: 1.6;">
                Ультимативный мессенджер с квантовым шифрованием
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 НАЧАТЬ ПУТЕШЕСТВИЕ
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ МГНОВЕННЫЙ ВХОД
            </button>

            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 15px; margin-top: 20px; text-align: center;">
                🎄 До Нового Года: <span id="newYearCountdown">...</span> дней!
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">Регистрация</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">🚀</div>
                <h3 id="registerName">Quantum_User</h3>
                <p style="color: var(--text-secondary);">ID: <span id="registerId">...</span></p>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ СОЗДАТЬ ПРОФИЛЬ
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewUser()">
                🔄 СГЕНЕРИРОВАТЬ НОВЫЙ
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← НАЗАД
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <!-- Сайдбар -->
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()" style="background: none; border: none; color: white; font-size: 1.4rem; position: absolute; top: 20px; left: 20px;">☰</button>
                <div class="user-avatar" id="userAvatar">🚀</div>
                <h3 id="userName">User</h3>
                <p>ID: <span id="userId">...</span></p>
            </div>

            <div class="online-users">
                <div style="font-weight: bold; margin-bottom: 10px;">🟢 Сейчас онлайн</div>
                <div id="onlineUsersList">
                    <!-- Динамически заполняется -->
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats', this)">💬 Чаты</div>
                <div class="nav-tab" onclick="switchTab('users', this)">👥 Люди</div>
                <div class="nav-tab" onclick="switchTab('groups', this)">👨‍👩‍👧‍👦 Группы</div>
            </div>

            <div style="padding: 15px;">
                <input type="text" style="width: 100%; padding: 12px 15px; background: rgba(255,255,255,0.1); border: 2px solid var(--accent); border-radius: 12px; color: white;" placeholder="🔍 Поиск..." id="searchInput" oninput="searchContent()">
            </div>

            <div style="flex: 1; overflow-y: auto; padding: 10px;" id="contentList">
                <!-- Контент загружается динамически -->
            </div>
        </div>

        <!-- Область чата -->
        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()" style="background: none; border: none; color: white; font-size: 1.4rem;">☰</button>
                <div style="width: 50px; height: 50px; border-radius: 12px; background: linear-gradient(135deg, var(--accent), var(--accent-glow)); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🌌</div>
                    <h3 style="margin-bottom: 15px;">Добро пожаловать в TrollexDL!</h3>
                    <p>Начните ваше космическое общение</p>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите ваше сообщение..." id="messageInput">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let messages = {};
        let allUsers = [];

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            updateNewYearCountdown();
            setInterval(updateNewYearCountdown, 60000);
            
            // Симуляция загрузки
            setTimeout(() => {
                document.getElementById('loadingScreen').classList.add('hidden');
                checkAutoLogin();
            }, 2000);
        });

        function updateNewYearCountdown() {
            const now = new Date();
            const newYear = new Date(now.getFullYear() + 1, 1, 1);
            const diff = newYear - now;
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            document.getElementById('newYearCountdown').textContent = days;
        }

        function showWelcomeScreen() {
            hideAllScreens();
            document.getElementById('welcomeScreen').classList.remove('hidden');
        }

        function showRegisterScreen() {
            hideAllScreens();
            document.getElementById('registerScreen').classList.remove('hidden');
            generateNewUser();
        }

        function hideAllScreens() {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
        }

        function generateNewUser() {
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌', '🌟', '⭐', '☄️'];
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            
            // Генерация имени
            const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Cosmic'];
            const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon'];
            const numbers = Math.floor(Math.random() * 9000) + 1000;
            const name = `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
            
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = 'user_' + Math.random().toString(36).substr(2, 8);
        }

        function registerUser() {
            const name = document.getElementById('registerName').textContent;
            const avatar = document.getElementById('registerAvatar').textContent;
            const userId = document.getElementById('registerId').textContent;
            
            currentUser = {
                id: userId,
                name: name,
                avatar: avatar,
                premium: 'none'
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            initializeSampleUsers();
            showMainApp();
            showNotification('Профиль создан! 🎉');
        }

        function initializeSampleUsers() {
            allUsers = [
                {id: 'user1', name: 'Алекс_Квантум', avatar: '👨‍💻', online: true, premium: 'vip'},
                {id: 'user2', name: 'Сара_Кибер', avatar: '👩‍🎨', online: true, premium: 'premium'},
                {id: 'user3', name: 'Майк_Неон', avatar: '👨‍🚀', online: false, premium: 'none'},
                {id: 'user4', name: 'Эмма_Дигитал', avatar: '👩‍💼', online: true, premium: 'ultra'},
            ];
            
            // Добавляем текущего пользователя
            allUsers.push(currentUser);
            localStorage.setItem('allUsers', JSON.stringify(allUsers));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                showMainApp();
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                showMainApp();
            } else {
                showWelcomeScreen();
            }
        }

        function showMainApp() {
            hideAllScreens();
            document.getElementById('mainApp').classList.remove('hidden');
            
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            
            loadContent();
            updateOnlineUsers();
        }

        function updateOnlineUsers() {
            const onlineUsers = allUsers.filter(user => user.online && user.id !== currentUser.id);
            const onlineUsersList = document.getElementById('onlineUsersList');
            
            if (onlineUsers.length === 0) {
                onlineUsersList.innerHTML = '<div style="color: var(--text-secondary); text-align: center;">Нет пользователей онлайн</div>';
                return;
            }
            
            onlineUsersList.innerHTML = onlineUsers.map(user => `
                <div class="online-user" onclick="startChatWithUser('${user.id}')">
                    <div style="width: 8px; height: 8px; background: var(--success); border-radius: 50%; margin-right: 8px;"></div>
                    <div>${user.name}</div>
                </div>
            `).join('');
        }

        function switchTab(tabName, element) {
            currentTab = tabName;
            
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            element.classList.add('active');
            
            loadContent();
        }

        function loadContent() {
            const contentList = document.getElementById('contentList');
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            let contentHTML = '';
            
            if (currentTab === 'chats') {
                contentHTML = getChatsContent(searchTerm);
            } else if (currentTab === 'users') {
                contentHTML = getUsersContent(searchTerm);
            } else if (currentTab === 'groups') {
                contentHTML = getGroupsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function searchContent() {
            loadContent();
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 'support', name: 'Поддержка TrollexDL', avatar: '🛰️', lastMessage: 'Чем можем помочь?', online: true},
                {id: 'updates', name: 'Обновления системы', avatar: '🔧', lastMessage: 'Доступны новые функции', online: true},
            ];
            
            const filteredChats = chats.filter(chat => chat.name.toLowerCase().includes(searchTerm));
            
            return filteredChats.map(chat => `
                <div class="online-user" onclick="openChat('${chat.id}')">
                    <div style="width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--accent-glow)); display: flex; align-items: center; justify-content: center; margin-right: 10px;">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${chat.lastMessage}</div>
                    </div>
                </div>
            `).join('');
        }

        function getUsersContent(searchTerm) {
            const filteredUsers = allUsers.filter(user => user.id !== currentUser.id && user.name.toLowerCase().includes(searchTerm));
            
            return filteredUsers.map(user => `
                <div class="online-user" onclick="startChatWithUser('${user.id}')">
                    <div style="width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--accent-glow)); display: flex; align-items: center; justify-content: center; margin-right: 10px;">${user.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${user.name}</div>
                        <div style="color: ${user.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.9rem;">
                            ${user.online ? '● В сети' : '○ Не в сети'}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function getGroupsContent(searchTerm) {
            const groups = [
                {id: 'group1', name: 'Квантовые_Разработчики', avatar: '👨‍💻', members: 15},
                {id: 'group2', name: 'Космические_Дизайнеры', avatar: '🎨', members: 12},
            ];
            
            const filteredGroups = groups.filter(group => group.name.toLowerCase().includes(searchTerm));
            
            return filteredGroups.map(group => `
                <div class="online-user" onclick="openGroup('${group.id}')">
                    <div style="width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--accent-glow)); display: flex; align-items: center; justify-content: center; margin-right: 10px;">${group.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${group.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${group.members} участников</div>
                    </div>
                </div>
            `).join('');
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Поддержка TrollexDL', avatar: '🛰️', status: 'Онлайн', type: 'support'},
                'updates': {name: 'Обновления системы', avatar: '🔧', status: 'Всегда активен', type: 'updates'},
            };
            
            const chat = chats[chatId];
            if (chat) {
                currentChat = {...chat, id: chatId};
                
                document.getElementById('currentChatName').textContent = chat.name;
                document.getElementById('currentChatAvatar').textContent = chat.avatar;
                document.getElementById('currentChatStatus').textContent = chat.status;
                
                showChatMessages(chatId);
            }
        }

        function startChatWithUser(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user) {
                const chatId = `user_${userId}`;
                currentChat = {
                    id: chatId,
                    name: user.name,
                    avatar: user.avatar,
                    status: user.online ? 'В сети' : 'Не в сети',
                    type: 'user'
                };
                
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? 'В сети' : 'Не в сети';
                
                showChatMessages(chatId);
                showNotification(`Чат с ${user.name} начат 💬`);
            }
        }

        function openGroup(groupId) {
            const groups = {
                'group1': {name: 'Квантовые_Разработчики', avatar: '👨‍💻', status: '15 участников', type: 'group'},
                'group2': {name: 'Космические_Дизайнеры', avatar: '🎨', status: '12 участников', type: 'group'},
            };
            
            const group = groups[groupId];
            if (group) {
                currentChat = {...group, id: groupId};
                
                document.getElementById('currentChatName').textContent = group.name;
                document.getElementById('currentChatAvatar').textContent = group.avatar;
                document.getElementById('currentChatStatus').textContent = group.status;
                
                showChatMessages(groupId);
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const defaultMessages = {
                'support': [
                    {id: '1', text: 'Добро пожаловать в поддержку TrollexDL! 🚀', sender: 'received', time: '12:00'},
                    {id: '2', text: 'Чем можем помочь в вашем космическом путешествии?', sender: 'received', time: '12:01'}
                ]
            };
            
            const chatMessages = messages[chatId] || defaultMessages[chatId] || [];
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = `
                    <div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">
                        <div style="font-size: 4rem; margin-bottom: 20px;">💬</div>
                        <h3 style="margin-bottom: 15px;">${currentChat.name}</h3>
                        <p>Начните вашу беседу</p>
                    </div>
                `;
            } else {
                messagesContainer.innerHTML = chatMessages.map(msg => `
                    <div class="message ${msg.sender}">
                        ${msg.text}
                        <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 6px; text-align: ${msg.sender === 'sent' ? 'right' : 'left'};">${msg.time}</div>
                    </div>
                `).join('');
            }
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                const messageId = 'msg_' + Date.now();
                
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.innerHTML = `
                    ${message}
                    <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 6px; text-align: right;">${time}</div>
                `;
                
                if (!messages[currentChat.id]) {
                    messagesContainer.innerHTML = '';
                }
                
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                if (!messages[currentChat.id]) {
                    messages[currentChat.id] = [];
                }
                messages[currentChat.id].push({
                    id: messageId,
                    text: message,
                    sender: 'sent',
                    time: time
                });
                
                localStorage.setItem('userMessages', JSON.stringify(messages));
                input.value = '';
                
                // Симуляция ответа
                if (currentChat.type === 'user' || currentChat.id === 'support') {
                    setTimeout(() => {
                        simulateReply();
                    }, 1000);
                }
            }
        }

        function simulateReply() {
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const replyId = 'msg_' + Date.now();
            
            const replies = {
                'support': [
                    'Спасибо за ваше сообщение! Чем можем помочь? 🚀',
                    'Мы ценим ваш отзыв!',
                    'Наша команда рассмотрит ваше сообщение.'
                ],
                'user': [
                    'Привет! Спасибо что написали! 👋',
                    'Звучит интересно! Расскажите подробнее...',
                ]
            };
            
            const chatReplies = replies[currentChat.type] || ['Спасибо за ваше сообщение!'];
            const replyText = chatReplies[Math.floor(Math.random() * chatReplies.length)];
            
            const messagesContainer = document.getElementById('messagesContainer');
            const replyElement = document.createElement('div');
            replyElement.className = 'message received';
            replyElement.innerHTML = `
                ${replyText}
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 6px;">${time}</div>
            `;
            
            messagesContainer.appendChild(replyElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            messages[currentChat.id].push({
                id: replyId,
                text: replyText,
                sender: 'received',
                time: time
            });
            
            localStorage.setItem('userMessages', JSON.stringify(messages));
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showNotification(message) {
            // Простая реализация уведомления
            alert(message);
        }

        // Обработчик Enter для отправки сообщений
        document.getElementById('messageInput')?.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Адаптация для мобильных
        function handleResize() {
            if (window.innerWidth > 768) {
                const sidebar = document.getElementById('sidebar');
                if (sidebar) {
                    sidebar.classList.remove('active');
                }
            }
        }

        window.addEventListener('resize', handleResize);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/manifest.json')
def manifest():
    manifest_data = {
        "name": "TrollexDL Messenger",
        "short_name": "TrollexDL", 
        "description": "Космический мессенджер с AI и Stories",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0a2a",
        "theme_color": "#6c2bd9",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            }
        ]
    }
    return jsonify(manifest_data)

@app.route('/static/icon-192x192.png')
def icon_192():
    # Создаем простую иконку программно
    img = Image.new('RGB', (192, 192), color=(107, 43, 217))
    draw = ImageDraw.Draw(img)
    # Добавляем простой логотип
    draw.ellipse([50, 50, 142, 142], fill=(139, 92, 246))
    draw.text((96, 96), 'TD', fill=(255, 255, 255), anchor='mm')
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    try:
        data = request.json
        return jsonify({
            'success': True, 
            'message': 'Сообщение отправлено',
            'message_id': f"msg_{int(time.time())}",
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/server_stats')
def api_server_stats():
    return jsonify(messenger.get_server_stats())

@app.route('/api/users/online')
def api_online_users():
    online_users = [user for user in messenger.users.values() if user.get('online', False)]
    return jsonify({'online_users': online_users})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running', 
        'service': 'TrollexDL Ultimate',
        'days_until_new_year': messenger.get_days_until_new_year(),
        'version': '5.0.0',
        'uptime': int(time.time() - messenger.server_start_time)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL Ultimate запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    print(f"📱 Доступно как PWA приложение")
    app.run(host='0.0.0.0', port=port, debug=False)
