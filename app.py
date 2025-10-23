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
friends_db = {}
calls_db = {}

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
        }
        
        /* ТЕМЫ */
        body.theme-ocean {
            --bg-color: #001f3f;
            --card-color: #003366;
            --accent-color: #0074D9;
            --text-color: #ffffff;
            --secondary-color: #004080;
        }
        
        body.theme-night {
            --bg-color: #0a0a0a;
            --card-color: #1a1a1a;
            --accent-color: #6b46c1;
            --text-color: #e2e8f0;
            --secondary-color: #2d3748;
        }
        
        body.theme-sunset {
            --bg-color: #2d1b69;
            --card-color: #4a2c8a;
            --accent-color: #e53e3e;
            --text-color: #fed7d7;
            --secondary-color: #5e2ca5;
        }
        
        body.theme-forest {
            --bg-color: #1a3c2d;
            --card-color: #2d5a45;
            --accent-color: #38a169;
            --text-color: #c6f6d5;
            --secondary-color: #366c4f;
        }
        
        body.theme-midnight {
            --bg-color: #1a202c;
            --card-color: #2d3748;
            --accent-color: #805ad5;
            --text-color: #e2e8f0;
            --secondary-color: #4a5568;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            overflow-x: hidden;
            transition: all 0.3s ease;
        }
        
        /* МОБИЛЬНАЯ ОПТИМИЗАЦИЯ */
        @media (max-width: 768px) {
            .chat-container {
                flex-direction: column;
                height: 100vh;
            }
            
            .sidebar {
                width: 100%;
                height: 50vh;
                border-right: none;
                border-bottom: 1px solid var(--border-color);
            }
            
            .chat-area {
                height: 50vh;
            }
            
            .auth-box {
                margin: 10px;
                padding: 30px 20px;
            }
            
            .logo {
                font-size: 32px;
            }
            
            .btn {
                min-height: 44px;
                padding: 12px;
                font-size: 14px;
            }
            
            .stories-container {
                padding: 15px;
                gap: 10px;
            }
            
            .story-avatar {
                width: 50px;
                height: 50px;
                font-size: 20px;
            }
            
            .message {
                max-width: 85%;
                font-size: 14px;
            }
            
            .call-container {
                padding: 20px;
            }
            
            .call-controls {
                bottom: 20px;
            }
        }
        
        /* СЕНСОРНЫЕ ЭЛЕМЕНТЫ */
        .btn {
            touch-action: manipulation;
            user-select: none;
            -webkit-user-select: none;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px 16px;
            border: none;
            border-radius: 12px;
            background: var(--accent-color);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
            margin: 5px 0;
        }
        
        .btn:active {
            transform: scale(0.95);
        }
        
        .chat-item {
            padding: 12px 15px;
            min-height: 60px;
        }
        
        /* ОСНОВНЫЕ СТИЛИ */
        .screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-color);
            z-index: 1000;
            padding: 20px;
        }
        
        .auth-box {
            background: var(--card-color);
            padding: 40px 30px;
            border-radius: 20px;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        
        .logo {
            font-size: 42px;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 15px;
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
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .message {
            background: var(--secondary-color);
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
            position: relative;
        }
        
        .message.own {
            background: var(--accent-color);
            align-self: flex-end;
        }
        
        .message-actions {
            position: absolute;
            top: -25px;
            right: 0;
            background: var(--card-color);
            border-radius: 10px;
            padding: 5px;
            display: none;
        }
        
        .message:hover .message-actions {
            display: flex;
        }
        
        .delete-btn {
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 12px;
            cursor: pointer;
        }
        
        /* ЗВОНКИ */
        .call-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-color);
            z-index: 2000;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .call-avatar {
            font-size: 80px;
            margin-bottom: 20px;
        }
        
        .call-info {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .call-controls {
            display: flex;
            gap: 20px;
        }
        
        .call-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
        }
        
        .call-accept {
            background: #10b981;
        }
        
        .call-decline {
            background: #ef4444;
        }
        
        .call-end {
            background: #ef4444;
        }
        
        /* ДРУЗЬЯ */
        .friend-item {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .friend-actions {
            margin-left: auto;
            display: flex;
            gap: 10px;
        }
        
        .remove-friend {
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 12px;
            cursor: pointer;
        }
        
        .add-friend {
            background: #10b981;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 12px;
            cursor: pointer;
        }
        
        /* АВАТАРКИ */
        .avatar-upload {
            position: relative;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            cursor: pointer;
            margin: 0 auto 20px;
            overflow: hidden;
        }
        
        .avatar-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
        }
        
        .avatar-upload input {
            position: absolute;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }
        
        /* ТЕМЫ */
        .theme-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 15px 0;
        }
        
        .theme-option {
            width: 60px;
            height: 60px;
            border-radius: 10px;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .theme-option.active {
            border-color: white;
        }
        
        .theme-purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
        .theme-ocean { background: linear-gradient(135deg, #0074D9, #0056b3); }
        .theme-night { background: linear-gradient(135deg, #6b46c1, #553c9a); }
        .theme-sunset { background: linear-gradient(135deg, #e53e3e, #c53030); }
        .theme-forest { background: linear-gradient(135deg, #38a169, #2f855a); }
        .theme-midnight { background: linear-gradient(135deg, #805ad5, #6b46c1); }
    </style>
</head>
<body class="theme-purple">
    <!-- ПЕРВАЯ СТРАНИЦА -->
    <div id="screen1" class="screen">
        <div class="auth-box">
            <div class="logo">🎃 DLtrollex</div>
            <div class="subtitle">Мобильный мессенджер нового поколения</div>
            
            <button class="btn" onclick="startQuickRegistration()">
                <span>💬 Начать общение</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                📱 Оптимизировано для телефонов • 🎨 Темы • 📞 Звонки • 👥 Друзья
            </div>
        </div>
    </div>

    <!-- РЕГИСТРАЦИЯ -->
    <div id="quickRegisterScreen" class="screen hidden">
        <div class="auth-box">
            <div class="logo">🎃 DLtrollex</div>
            <div class="subtitle">Создайте свой аккаунт</div>
            
            <div class="avatar-upload" onclick="document.getElementById('avatarInput').click()">
                <div id="avatarPreview">😊</div>
                <input type="file" id="avatarInput" accept="image/*" onchange="previewAvatar(event)">
            </div>
            
            <input type="text" class="input-field" placeholder="👤 Ваше имя" id="regName">
            
            <button class="btn" onclick="quickRegister()">
                <span>🚀 Начать использовать</span>
            </button>
        </div>
    </div>

    <!-- ОСНОВНОЙ ИНТЕРФЕЙС -->
    <div id="mainApp" class="app">
        <!-- Генерируется JavaScript -->
    </div>

    <!-- ЗВОНОК -->
    <div id="callContainer" class="call-container">
        <div class="call-avatar" id="callAvatar">👤</div>
        <div class="call-info">
            <div id="callUserName">Пользователь</div>
            <div id="callStatus">Входящий вызов...</div>
        </div>
        <div class="call-controls">
            <div class="call-btn call-accept" onclick="acceptCall()">📞</div>
            <div class="call-btn call-decline" onclick="declineCall()">📵</div>
        </div>
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let friends = [];
        let currentCall = null;
        let currentTheme = 'purple';

        // ИНИЦИАЛИЗАЦИЯ РЕАЛЬНЫХ ПОЛЬЗОВАТЕЛЕЙ
        function initializeRealUsers() {
            allUsers = [
                {
                    id: 'user1', name: 'Алексей Кодеров', username: '@alex_coder', avatar: '👨‍💻',
                    bio: 'Fullstack разработчик', city: 'Москва', age: 28, isOnline: true,
                    interests: ['Программирование', 'Музыка']
                },
                {
                    id: 'user2', name: 'Мария Дизайнерова', username: '@maria_design', avatar: '👩‍🎨',
                    bio: 'UI/UX дизайнер', city: 'СПб', age: 25, isOnline: true,
                    interests: ['Дизайн', 'Фотография']
                },
                {
                    id: 'user3', name: 'Дмитрий Геймеров', username: '@dima_gamer', avatar: '🎮',
                    bio: 'Профессиональный геймер', city: 'Новосибирск', age: 22, isOnline: false,
                    interests: ['Игры', 'Стриминг']
                }
            ];
        }

        document.addEventListener('DOMContentLoaded', function() {
            initializeRealUsers();
            checkAutoLogin();
            loadTheme();
        });

        // АВАТАРКИ ИЗ ГАЛЕРЕИ
        function previewAvatar(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('avatarPreview').innerHTML = 
                        `<img src="${e.target.result}" class="avatar-image">`;
                }
                reader.readAsDataURL(file);
            }
        }

        function startQuickRegistration() {
            showScreen('quickRegisterScreen');
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
            document.getElementById(screenId).classList.remove('hidden');
        }

        function quickRegister() {
            const name = document.getElementById('regName').value.trim();
            if (!name) {
                alert('Введите имя');
                return;
            }

            const avatarElement = document.getElementById('avatarPreview');
            const avatar = avatarElement.querySelector('img') ? 
                avatarElement.innerHTML : avatarElement.textContent;

            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: '@' + name.toLowerCase(),
                avatar: avatar,
                bio: 'Новый пользователь',
                city: 'Москва',
                age: 25,
                isOnline: true
            };

            allUsers.push(currentUser);
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            showMainApp();
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedUsers = localStorage.getItem('dlallUsers');
                if (savedUsers) allUsers = JSON.parse(savedUsers);
                showMainApp();
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
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color);">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="font-size: 24px;">${currentUser.avatar}</div>
                                <div>
                                    <div style="font-weight: bold;">${currentUser.name}</div>
                                    <div style="color: #888; font-size: 12px;">Онлайн</div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="padding: 10px; border-bottom: 1px solid var(--border-color); display: flex; gap: 5px;">
                            <button class="btn" onclick="showChats()" style="flex: 1;">💬 Чаты</button>
                            <button class="btn" onclick="showFriends()" style="flex: 1;">👥 Друзья</button>
                            <button class="btn" onclick="showSettings()" style="flex: 1;">⚙️</button>
                        </div>
                        
                        <div id="contentArea" style="flex: 1; overflow-y: auto;">
                            ${renderChatsList()}
                        </div>
                    </div>
                    
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div style="font-size: 64px; margin-bottom: 20px;">💬</div>
                            <div style="color: #888; text-align: center;">Выберите чат для общения</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // ЧАТЫ
        function showChats() {
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <button class="btn" onclick="showNewChatModal()" style="width: 100%; margin-bottom: 10px;">
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
                return '<div style="text-align: center; padding: 40px; color: #888;">Чатов пока нет</div>';
            }
            
            return chats.map(chat => {
                const otherUser = allUsers.find(u => u.id === chat.participants.find(id => id !== currentUser.id));
                return `
                    <div class="chat-item" onclick="openChat('${chat.id}')">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div style="font-size: 24px;">${otherUser.avatar}</div>
                            <div>
                                <div style="font-weight: bold;">${otherUser.name}</div>
                                <div style="color: #888; font-size: 12px;">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function showNewChatModal() {
            const availableUsers = allUsers.filter(u => u.id !== currentUser.id);
            
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <h3 style="margin-bottom: 15px;">💬 Новый чат</h3>
                    <div style="max-height: 60vh; overflow-y: auto;">
                        ${availableUsers.map(user => `
                            <div class="chat-item" onclick="startNewChat('${user.id}')">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="font-size: 24px;">${user.avatar}</div>
                                    <div>
                                        <div style="font-weight: bold;">${user.name}</div>
                                        <div style="color: #888; font-size: 12px;">${user.bio}</div>
                                    </div>
                                    <button class="add-friend" onclick="event.stopPropagation(); addFriend('${user.id}')">
                                        ➕ Друг
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
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
                lastMessage: { text: 'Чат начат', senderId: currentUser.id },
                messages: [
                    { id: '1', text: `Привет! Я ${currentUser.name}`, senderId: currentUser.id, timestamp: new Date().toISOString() }
                ]
            };

            chats.push(newChat);
            openChat(newChat.id);
        }

        function openChat(chatId) {
            currentChat = chats.find(c => c.id === chatId);
            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(id => id !== currentUser.id));
            
            document.getElementById('chatContent').innerHTML = `
                <div style="display: flex; flex-direction: column; height: 100%;">
                    <div style="padding: 15px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div style="font-size: 24px;">${otherUser.avatar}</div>
                            <div>
                                <div style="font-weight: bold;">${otherUser.name}</div>
                                <div style="color: #888; font-size: 12px;">${otherUser.bio}</div>
                            </div>
                        </div>
                        <button class="btn" onclick="startCall('${otherUser.id}')">📞</button>
                    </div>
                    
                    <div class="messages-container" id="messagesContainer">
                        ${renderChatMessages()}
                    </div>
                    
                    <div style="padding: 15px; border-top: 1px solid var(--border-color); display: flex; gap: 10px;">
                        <input type="text" 
                               style="flex: 1; padding: 12px; background: var(--secondary-color); border: none; border-radius: 20px; color: white;" 
                               placeholder="Сообщение..." 
                               id="messageInput"
                               onkeypress="if(event.key=='Enter') sendMessage()">
                        <button class="btn" onclick="sendMessage()" style="padding: 12px 20px;">📤</button>
                    </div>
                </div>
            `;
        }

        function renderChatMessages() {
            return currentChat.messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                return `
                    <div class="message ${isOwn ? 'own' : ''}">
                        ${msg.text}
                        <div class="message-actions">
                            <button class="delete-btn" onclick="deleteMessage('${msg.id}')">🗑️</button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (text) {
                const newMessage = {
                    id: 'msg_' + Date.now(),
                    text: text,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                input.value = '';
                openChat(currentChat.id);
            }
        }

        function deleteMessage(messageId) {
            currentChat.messages = currentChat.messages.filter(m => m.id !== messageId);
            openChat(currentChat.id);
        }

        // ДРУЗЬЯ
        function showFriends() {
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <h3 style="margin-bottom: 15px;">👥 Друзья</h3>
                    <div id="friendsList">
                        ${renderFriendsList()}
                    </div>
                </div>
            `;
        }

        function renderFriendsList() {
            if (friends.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: #888;">Друзей пока нет</div>';
            }
            
            return friends.map(friendId => {
                const friend = allUsers.find(u => u.id === friendId);
                return `
                    <div class="friend-item">
                        <div style="display: flex; align-items: center; gap: 10px; flex: 1;">
                            <div style="font-size: 24px;">${friend.avatar}</div>
                            <div>
                                <div style="font-weight: bold;">${friend.name}</div>
                                <div style="color: #888; font-size: 12px;">${friend.bio}</div>
                            </div>
                        </div>
                        <div class="friend-actions">
                            <button class="btn" onclick="startCall('${friend.id}')">📞</button>
                            <button class="remove-friend" onclick="removeFriend('${friend.id}')">🗑️</button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function addFriend(userId) {
            if (!friends.includes(userId)) {
                friends.push(userId);
                showNotification('Пользователь добавлен в друзья!');
                showNewChatModal();
            }
        }

        function removeFriend(userId) {
            friends = friends.filter(id => id !== userId);
            showFriends();
        }

        // ЗВОНКИ
        function startCall(userId) {
            const user = allUsers.find(u => u.id === userId);
            currentCall = { userId, type: 'outgoing' };
            
            document.getElementById('callContainer').style.display = 'flex';
            document.getElementById('callAvatar').innerHTML = user.avatar;
            document.getElementById('callUserName').textContent = user.name;
            document.getElementById('callStatus').textContent = 'Звонок...';
            document.getElementById('callControls').innerHTML = `
                <div class="call-btn call-end" onclick="endCall()">📵</div>
            `;
        }

        function simulateIncomingCall() {
            const randomUser = allUsers.filter(u => u.id !== currentUser.id)[0];
            currentCall = { userId: randomUser.id, type: 'incoming' };
            
            document.getElementById('callContainer').style.display = 'flex';
            document.getElementById('callAvatar').innerHTML = randomUser.avatar;
            document.getElementById('callUserName').textContent = randomUser.name;
            document.getElementById('callStatus').textContent = 'Входящий вызов...';
        }

        function acceptCall() {
            document.getElementById('callStatus').textContent = 'Разговор...';
            document.getElementById('callControls').innerHTML = `
                <div class="call-btn call-end" onclick="endCall()">📵</div>
            `;
        }

        function declineCall() {
            endCall();
        }

        function endCall() {
            document.getElementById('callContainer').style.display = 'none';
            currentCall = null;
        }

        // СЛУЧАЙНЫЕ ВХОДЯЩИЕ ЗВОНКИ
        setInterval(() => {
            if (!currentCall && Math.random() < 0.01) { // 1% шанс каждые X ms
                simulateIncomingCall();
            }
        }, 30000);

        // НАСТРОЙКИ И ТЕМЫ
        function showSettings() {
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 15px;">
                    <h3 style="margin-bottom: 20px;">⚙️ Настройки</h3>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                        <h4 style="margin-bottom: 15px;">🎨 Темы оформления</h4>
                        <div class="theme-grid">
                            <div class="theme-option theme-purple ${currentTheme === 'purple' ? 'active' : ''}" onclick="changeTheme('purple')"></div>
                            <div class="theme-option theme-ocean ${currentTheme === 'ocean' ? 'active' : ''}" onclick="changeTheme('ocean')"></div>
                            <div class="theme-option theme-night ${currentTheme === 'night' ? 'active' : ''}" onclick="changeTheme('night')"></div>
                            <div class="theme-option theme-sunset ${currentTheme === 'sunset' ? 'active' : ''}" onclick="changeTheme('sunset')"></div>
                            <div class="theme-option theme-forest ${currentTheme === 'forest' ? 'active' : ''}" onclick="changeTheme('forest')"></div>
                            <div class="theme-option theme-midnight ${currentTheme === 'midnight' ? 'active' : ''}" onclick="changeTheme('midnight')"></div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin-bottom: 15px;">
                        <h4 style="margin-bottom: 15px;">👤 Смена аватарки</h4>
                        <div class="avatar-upload" onclick="document.getElementById('settingsAvatarInput').click()">
                            <div id="settingsAvatarPreview">${currentUser.avatar}</div>
                            <input type="file" id="settingsAvatarInput" accept="image/*" onchange="updateAvatar(event)">
                        </div>
                    </div>
                    
                    <button class="btn" onclick="logout()" style="background: #ef4444; width: 100%;">
                        🚪 Выйти
                    </button>
                </div>
            `;
        }

        function changeTheme(theme) {
            currentTheme = theme;
            document.body.className = 'theme-' + theme;
            localStorage.setItem('dltheme', theme);
        }

        function loadTheme() {
            const savedTheme = localStorage.getItem('dltheme');
            if (savedTheme) {
                changeTheme(savedTheme);
            }
        }

        function updateAvatar(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    currentUser.avatar = `<img src="${e.target.result}" class="avatar-image">`;
                    localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                    document.getElementById('settingsAvatarPreview').innerHTML = currentUser.avatar;
                    showNotification('Аватар обновлен!');
                }
                reader.readAsDataURL(file);
            }
        }

        function logout() {
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function showNotification(message) {
            // Простое уведомление для мобильных
            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification(message);
            } else {
                alert(message);
            }
        }

        // ЗАПРОС РАЗРЕШЕНИЯ НА УВЕДОМЛЕНИЯ
        if ('Notification' in window) {
            Notification.requestPermission();
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("📱 DLtrollex Mobile запущен!")
    print(f"🔗 http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
