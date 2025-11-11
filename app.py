# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trollexdl-premium-2024'

def get_days_until_new_year():
    now = datetime.datetime.now()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    return (new_year - now).days

def generate_username():
    adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha']
    nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther']
    numbers = random.randint(1000, 9999)
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"

def generate_email(username):
    domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net']
    return f"{username.lower()}@{random.choice(domains)}"

def generate_user_id():
    return f"user_{uuid.uuid4().hex[:8]}"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }

        :root {
            --primary: #0a0a2a;
            --secondary: #1a1a4a;
            --accent: #6c2bd9;
            --accent-glow: #8b5cf6;
            --neon: #00ff88;
            --text: #ffffff;
            --text-secondary: #b0b0ff;
            --danger: #ff4444;
            --success: #00ff88;
            --warning: #ffaa00;
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
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
            padding: 20px;
            z-index: 1000;
            background: var(--primary);
        }

        .hidden {
            display: none !important;
        }

        .cosmic-card {
            background: rgba(26, 26, 74, 0.95);
            border: 2px solid var(--accent);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--neon), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            margin: 8px 0;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(107, 43, 217, 0.4);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--text);
            border: 2px solid var(--accent);
        }

        .user-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid var(--accent);
        }

        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 15px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin: 0 auto 10px;
        }

        .app {
            width: 100%;
            height: 100vh;
            display: flex;
        }

        .sidebar {
            width: 300px;
            background: rgba(26, 26, 74, 0.95);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
        }

        .user-header {
            padding: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 5px;
            margin: 10px;
        }

        .nav-tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .nav-tab.active {
            background: var(--accent);
        }

        .search-box {
            padding: 10px;
        }

        .search-input {
            width: 100%;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 10px;
            color: var(--text);
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 12px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .chat-item:hover {
            background: rgba(107, 43, 217, 0.3);
        }

        .item-avatar {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
        }

        .chat-header {
            padding: 15px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .messages-container {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .message {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 15px;
            position: relative;
        }

        .message.received {
            background: rgba(107, 43, 217, 0.3);
            align-self: flex-start;
        }

        .message.sent {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            align-self: flex-end;
            color: white;
        }

        .message-input-container {
            padding: 15px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--accent);
            display: flex;
            gap: 10px;
        }

        .message-input {
            flex: 1;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 20px;
            color: var(--text);
        }

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
        }

        .settings-panel {
            position: fixed;
            top: 0;
            right: -400px;
            width: 400px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            border-left: 2px solid var(--accent);
            z-index: 500;
            transition: right 0.3s ease;
            padding: 20px;
            overflow-y: auto;
        }

        .settings-panel.active {
            right: 0;
        }

        .donate-panel {
            position: fixed;
            top: 0;
            left: -400px;
            width: 400px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            border-right: 2px solid var(--accent);
            z-index: 500;
            transition: left 0.3s ease;
            padding: 20px;
            overflow-y: auto;
        }

        .donate-panel.active {
            left: 0;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 12px 20px;
            border-radius: 10px;
            z-index: 4000;
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.2rem;
            cursor: pointer;
        }

        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                height: 100%;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 200;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .mobile-menu-btn {
                display: block;
            }
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin: 20px 0; font-size: 1.2rem;">Initializing Quantum Protocol...</div>
            <div style="font-size: 2rem;">🚀</div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary);">
                Ultimate messaging with quantum encryption
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 START JOURNEY
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ QUICK START
            </button>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">Registration</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">🚀</div>
                <h3 id="registerName">Quantum_User</h3>
                <p style="color: var(--text-secondary);">ID: <span id="registerId">...</span></p>
                <p style="color: var(--text-secondary);">📧 <span id="registerEmail">...</span></p>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ CREATE PROFILE
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewUser()">
                🔄 GENERATE NEW
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← BACK
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="user-avatar" id="userAvatar">🚀</div>
                <h3 id="userName">User</h3>
                <p>ID: <span id="userId">...</span></p>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('users')">👥</div>
                <div class="nav-tab" onclick="switchTab('groups')">👨‍👩‍👧‍👦</div>
                <div class="nav-tab" onclick="showDonatePanel()">💎</div>
                <div class="nav-tab" onclick="showSettings()">⚙️</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Search..." id="searchInput" oninput="searchContent()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Динамически заполняется -->
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Select chat to start messaging</p>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 40px 20px; color: var(--text-secondary);">
                    <div style="font-size: 3rem; margin-bottom: 15px;">🌌</div>
                    <h3>Welcome to TrollexDL!</h3>
                    <p>Start messaging with quantum encryption</p>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Type your message..." id="messageInput">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Панель доната -->
    <div class="donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>💎 Premium Tiers</h3>
            <button class="mobile-menu-btn" onclick="hideDonatePanel()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h4>🌟 VIP - 299 ₽</h4>
            <p>Цветные сообщения, специальный значок</p>
            <button class="btn btn-primary" onclick="selectTier('vip')">Выбрать VIP</button>
        </div>

        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h4>💫 Premium - 599 ₽</h4>
            <p>Все функции VIP + расширенные темы</p>
            <button class="btn btn-primary" onclick="selectTier('premium')">Выбрать Premium</button>
        </div>

        <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <p>Напишите в Telegram: <strong>@trollex_official</strong></p>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>⚙️ Settings</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div style="margin-bottom: 15px;">
            <label>👤 Display Name</label>
            <input type="text" class="search-input" id="settingsName" placeholder="Enter new name" style="margin-top: 5px;">
        </div>

        <button class="btn btn-primary" onclick="saveSettings()">💾 Save Settings</button>
        <button class="btn btn-secondary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 10px;">
            🚪 Logout
        </button>
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
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 2000);
        });

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
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
            const name = generateUsername();
            const email = generateEmail(name);
            const userId = generateUserId();
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌'];
            
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
            document.getElementById('registerEmail').textContent = email;
        }

        function generateUsername() {
            const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital'];
            const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger'];
            const numbers = Math.floor(Math.random() * 9000) + 1000;
            return `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
        }

        function generateEmail(username) {
            const domains = ['quantum.io', 'cosmic.com', 'trollex.ai'];
            return `${username.toLowerCase()}@${domains[Math.floor(Math.random() * domains.length)]}`;
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 8).toUpperCase();
        }

        function registerUser() {
            const name = document.getElementById('registerName').textContent;
            const avatar = document.getElementById('registerAvatar').textContent;
            const userId = document.getElementById('registerId').textContent;
            const email = document.getElementById('registerEmail').textContent;
            
            currentUser = {
                id: userId,
                name: name,
                avatar: avatar,
                email: email,
                settings: {}
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            
            // Создаем тестовых пользователей
            initializeSampleUsers();
            
            showMainApp();
            showNotification('Profile created successfully! 🎉');
        }

        function initializeSampleUsers() {
            allUsers = [
                {id: 'user1', name: 'Alex_Quantum', avatar: '👨‍💻', online: true},
                {id: 'user2', name: 'Sarah_Cyber', avatar: '👩‍🎨', online: true},
                {id: 'user3', name: 'Mike_Neon', avatar: '👨‍🚀', online: false},
                {id: 'user4', name: 'Emma_Digital', avatar: '👩‍💼', online: true}
            ];
            
            // Добавляем текущего пользователя
            allUsers.push({
                id: currentUser.id,
                name: currentUser.name,
                avatar: currentUser.avatar,
                online: true
            });
            
            localStorage.setItem('allUsers', JSON.stringify(allUsers));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                showMainApp();
                showNotification('Welcome back! 🚀');
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
            
            // Заполняем данные пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            
            loadContent();
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            // Обновляем активную вкладку
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
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
                {id: 'support', name: 'Trollex Support', avatar: '🛰️', lastMessage: 'How can we help?'},
                {id: 'community', name: 'Community Chat', avatar: '👥', lastMessage: 'Welcome everyone!'}
            ];
            
            const filteredChats = chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">No chats found</div>';
            }
            
            return filteredChats.map(chat => `
                <div class="chat-item" onclick="openChat('${chat.id}')">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${chat.lastMessage}</div>
                    </div>
                </div>
            `).join('');
        }

        function getUsersContent(searchTerm) {
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && 
                user.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredUsers.length === 0) {
                return '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">No users found</div>';
            }
            
            return filteredUsers.map(user => `
                <div class="chat-item" onclick="startChatWithUser('${user.id}')">
                    <div class="item-avatar">${user.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${user.name}</div>
                        <div style="color: ${user.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.9rem;">
                            ${user.online ? 'Online' : 'Offline'}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function getGroupsContent(searchTerm) {
            const groups = [
                {id: 'group1', name: 'Quantum Coders', avatar: '👨‍💻', members: '12 members'},
                {id: 'group2', name: 'Cosmic Design', avatar: '🎨', members: '8 members'}
            ];
            
            const filteredGroups = groups.filter(group => 
                group.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredGroups.length === 0) {
                return '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">No groups found</div>';
            }
            
            return filteredGroups.map(group => `
                <div class="chat-item" onclick="openGroup('${group.id}')">
                    <div class="item-avatar">${group.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${group.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${group.members}</div>
                    </div>
                </div>
            `).join('');
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Trollex Support', avatar: '🛰️', status: 'Online'},
                'community': {name: 'Community Chat', avatar: '👥', status: '12 online'}
            };
            
            const chat = chats[chatId];
            if (chat) {
                currentChat = chat;
                currentChat.id = chatId;
                
                document.getElementById('currentChatName').textContent = chat.name;
                document.getElementById('currentChatAvatar').textContent = chat.avatar;
                document.getElementById('currentChatStatus').textContent = chat.status;
                
                showChatMessages(chatId);
            }
        }

        function startChatWithUser(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user) {
                currentChat = {
                    id: `user_${userId}`,
                    name: user.name,
                    avatar: user.avatar,
                    status: user.online ? 'Online' : 'Offline'
                };
                
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? 'Online' : 'Offline';
                
                showChatMessages(currentChat.id);
                showNotification(`Started chat with ${user.name} 💬`);
            }
        }

        function openGroup(groupId) {
            const groups = {
                'group1': {name: 'Quantum Coders', avatar: '👨‍💻', status: '12 members'},
                'group2': {name: 'Cosmic Design', avatar: '🎨', status: '8 members'}
            };
            
            const group = groups[groupId];
            if (group) {
                currentChat = group;
                currentChat.id = groupId;
                
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
                    {text: 'Welcome to TrollexDL Support! 🚀', sender: 'received', time: '12:00'},
                    {text: 'How can we assist you today?', sender: 'received', time: '12:01'}
                ],
                'community': [
                    {text: 'Welcome to Community Chat! 👋', sender: 'received', time: '10:00'},
                    {text: 'Hello everyone! 🎉', sender: 'received', time: '10:05'},
                    {text: 'This app is amazing! ⚡', sender: 'received', time: '10:10'}
                ]
            };
            
            const chatMessages = messages[chatId] || defaultMessages[chatId] || [];
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = `
                    <div style="text-align: center; padding: 40px 20px; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 15px;">💬</div>
                        <h3>${currentChat.name}</h3>
                        <p>Start conversation</p>
                    </div>
                `;
            } else {
                messagesContainer.innerHTML = chatMessages.map(msg => `
                    <div class="message ${msg.sender}">
                        ${msg.text}
                        <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">${msg.time}</div>
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
                
                // Добавляем сообщение в интерфейс
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.innerHTML = `
                    ${message}
                    <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">${time}</div>
                `;
                
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Очищаем input
                input.value = '';
                
                // Сохраняем сообщение
                if (!messages[currentChat.id]) {
                    messages[currentChat.id] = [];
                }
                messages[currentChat.id].push({
                    text: message,
                    sender: 'sent',
                    time: time
                });
                
                // Имитация ответа
                setTimeout(() => {
                    if (currentChat) {
                        simulateReply();
                    }
                }, 1000);
                
                showNotification('Message sent! ✨');
            }
        }

        function simulateReply() {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            
            const replies = {
                'support': [
                    'Thanks for your message! How can we help? 🚀',
                    'We appreciate your feedback!'
                ],
                'user': [
                    'Hey! Thanks for reaching out! 👋',
                    'That sounds interesting!'
                ],
                'community': [
                    'Great message! 👍',
                    'Thanks for sharing! 💫'
                ]
            };
            
            const chatReplies = replies[currentChat.type] || ['Thank you for your message!'];
            const replyText = chatReplies[Math.floor(Math.random() * chatReplies.length)];
            
            const replyElement = document.createElement('div');
            replyElement.className = 'message received';
            replyElement.innerHTML = `
                ${replyText}
                <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">${time}</div>
            `;
            
            messagesContainer.appendChild(replyElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            if (!messages[currentChat.id]) {
                messages[currentChat.id] = [];
            }
            messages[currentChat.id].push({
                text: replyText,
                sender: 'received',
                time: time
            });
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showDonatePanel() {
            document.getElementById('donatePanel').classList.add('active');
        }

        function hideDonatePanel() {
            document.getElementById('donatePanel').classList.remove('active');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
        }

        function selectTier(tier) {
            showNotification(`Selected ${tier.toUpperCase()} tier! Contact @trollex_official 💎`);
            hideDonatePanel();
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            if (newName) {
                currentUser.name = newName;
                document.getElementById('userName').textContent = newName;
                localStorage.setItem('trollexUser', JSON.stringify(currentUser));
                showNotification('Name updated! ✅');
            }
            hideSettings();
        }

        function logout() {
            localStorage.removeItem('trollexUser');
            showWelcomeScreen();
            showNotification('See you soon! 👋');
        }

        function showNotification(message) {
            // Создаем уведомление
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            document.body.appendChild(notification);
            
            // Удаляем через 3 секунды
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Обработка Enter для отправки сообщений
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Закрытие панелей при клике вне их
        document.addEventListener('click', function(event) {
            const donatePanel = document.getElementById('donatePanel');
            const settingsPanel = document.getElementById('settingsPanel');
            
            if (donatePanel.classList.contains('active') && 
                !donatePanel.contains(event.target) && 
                !event.target.closest('.nav-tab')) {
                hideDonatePanel();
            }
            
            if (settingsPanel.classList.contains('active') && 
                !settingsPanel.contains(event.target) && 
                !event.target.closest('.nav-tab')) {
                hideSettings();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    data = request.json
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running', 
        'service': 'TrollexDL',
        'days_until_new_year': get_days_until_new_year()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
