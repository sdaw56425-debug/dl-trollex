# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ХЕЛЛОУИН 2025 + РЕАЛЬНЫЕ ПОЛЬЗОВАТЕЛИ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

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
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
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
            border: 2px solid var(--accent-color);
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
            background: var(--accent-color);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
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
        }
        
        .message.own {
            background: var(--accent-color);
            align-self: flex-end;
        }
        
        .chat-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
        }
        
        .chat-item:hover {
            background: var(--secondary-color);
        }
        
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
        
        .call-controls {
            display: flex;
            gap: 20px;
            margin-top: 30px;
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
        
        .avatar-upload {
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
        }
        
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
        }
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
                <input type="file" id="avatarInput" accept="image/*" style="display: none;" onchange="previewAvatar(event)">
            </div>
            
            <input type="text" class="input-field" placeholder="👤 Ваше имя" id="regName">
            
            <button class="btn" onclick="quickRegister()">
                <span>🚀 Начать использовать</span>
            </button>
            
            <button class="btn" onclick="showScreen('screen1')" style="background: #666;">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- ОСНОВНОЙ ИНТЕРФЕЙС -->
    <div id="mainApp" class="app hidden">
        <!-- Будет заполнен JavaScript -->
    </div>

    <!-- ЗВОНОК -->
    <div id="callContainer" class="call-container hidden">
        <div class="call-avatar" id="callAvatar">👤</div>
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 24px; font-weight: bold;" id="callUserName">Пользователь</div>
            <div style="color: #888;" id="callStatus">Входящий вызов...</div>
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
                    id: 'user1', 
                    name: 'Алексей Кодеров', 
                    username: '@alex_coder', 
                    avatar: '👨‍💻',
                    bio: 'Fullstack разработчик', 
                    city: 'Москва', 
                    age: 28, 
                    isOnline: true,
                    interests: ['Программирование', 'Музыка']
                },
                {
                    id: 'user2', 
                    name: 'Мария Дизайнерова', 
                    username: '@maria_design', 
                    avatar: '👩‍🎨',
                    bio: 'UI/UX дизайнер', 
                    city: 'СПб', 
                    age: 25, 
                    isOnline: true,
                    interests: ['Дизайн', 'Фотография']
                },
                {
                    id: 'user3', 
                    name: 'Дмитрий Геймеров', 
                    username: '@dima_gamer', 
                    avatar: '🎮',
                    bio: 'Профессиональный геймер', 
                    city: 'Новосибирск', 
                    age: 22, 
                    isOnline: false,
                    interests: ['Игры', 'Стриминг']
                },
                {
                    id: 'user4', 
                    name: 'Анна Ученова', 
                    username: '@anna_science', 
                    avatar: '🔬',
                    bio: 'Ученый-биолог', 
                    city: 'Казань', 
                    age: 30, 
                    isOnline: true,
                    interests: ['Наука', 'Природа']
                }
            ];
        }

        document.addEventListener('DOMContentLoaded', function() {
            console.log("DLtrollex загружается...");
            initializeRealUsers();
            checkAutoLogin();
            loadTheme();
        });

        function startQuickRegistration() {
            showScreen('quickRegisterScreen');
        }

        function showScreen(screenId) {
            console.log("Показываем экран:", screenId);
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById(screenId).classList.remove('hidden');
        }

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

        function quickRegister() {
            const name = document.getElementById('regName').value.trim();
            if (!name) {
                alert('Введите имя');
                return;
            }

            const avatarElement = document.getElementById('avatarPreview');
            const avatar = avatarElement.querySelector('img') ? 
                avatarElement.innerHTML : '😊';

            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: '@' + name.toLowerCase().replace(/[^a-z0-9]/g, ''),
                avatar: avatar,
                bio: 'Новый пользователь DLtrollex 🚀',
                city: 'Москва',
                age: 25,
                isOnline: true,
                interests: ['Общение', 'Знакомства']
            };

            allUsers.push(currentUser);
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            
            showMainApp();
            showNotification('Добро пожаловать в DLtrollex! 🎉');
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    const savedUsers = localStorage.getItem('dlallUsers');
                    if (savedUsers) allUsers = JSON.parse(savedUsers);
                    showMainApp();
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
            console.log("Рендерим основной интерфейс");
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div style="display: flex; align-items: center; gap: 15px;">
                                <div style="font-size: 32px;">${currentUser.avatar}</div>
                                <div>
                                    <div style="font-weight: bold; font-size: 18px;">${currentUser.name}</div>
                                    <div style="color: #888; font-size: 14px;">Онлайн 🟢</div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color); display: flex; gap: 10px;">
                            <button class="btn" onclick="showChats()" style="flex: 1;">💬 Чаты</button>
                            <button class="btn" onclick="showFriends()" style="flex: 1;">👥 Друзья</button>
                            <button class="btn" onclick="showSettings()" style="flex: 1;">⚙️</button>
                        </div>
                        
                        <div id="contentArea" style="flex: 1; overflow-y: auto; padding: 10px;">
                            ${renderChatsList()}
                        </div>
                    </div>
                    
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column; padding: 20px;">
                            <div style="font-size: 80px; margin-bottom: 20px;">💬</div>
                            <h2 style="margin-bottom: 10px; text-align: center;">Добро пожаловать!</h2>
                            <p style="color: #888; text-align: center; margin-bottom: 30px;">
                                Выберите чат для начала общения
                            </p>
                            <button class="btn" onclick="showNewChatModal()" style="max-width: 200px;">
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
                        <div style="font-size: 48px; margin-bottom: 15px;">💬</div>
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
                    <div class="chat-item" onclick="openChat('${chat.id}')">
                        <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                            <div style="font-size: 28px;">${otherUser.avatar}</div>
                            <div style="flex: 1;">
                                <div style="font-weight: bold;">${otherUser.name}</div>
                                <div style="color: #888; font-size: 14px;">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                            </div>
                            <button class="btn" onclick="event.stopPropagation(); startCall('${otherUser.id}')" style="padding: 8px 12px; font-size: 14px;">
                                📞
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function showNewChatModal() {
            const availableUsers = allUsers.filter(u => u.id !== currentUser.id);
            
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <h3 style="margin-bottom: 15px;">💬 Выберите пользователя</h3>
                    <div style="max-height: 60vh; overflow-y: auto;">
                        ${availableUsers.map(user => `
                            <div class="chat-item" onclick="startNewChat('${user.id}')">
                                <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                                    <div style="font-size: 28px;">${user.avatar}</div>
                                    <div style="flex: 1;">
                                        <div style="font-weight: bold;">${user.name}</div>
                                        <div style="color: #888; font-size: 14px;">${user.bio}</div>
                                    </div>
                                    <button class="btn" onclick="event.stopPropagation(); addFriend('${user.id}')" style="padding: 8px 12px; font-size: 14px; background: #10b981;">
                                        ➕
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
            showNotification(`Чат с ${user.name} начат! 💬`);
        }

        function openChat(chatId) {
            currentChat = chats.find(c => c.id === chatId);
            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(id => id !== currentUser.id));
            
            document.getElementById('chatContent').innerHTML = `
                <div style="display: flex; flex-direction: column; height: 100%; width: 100%;">
                    <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="font-size: 32px;">${otherUser.avatar}</div>
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
        }

        function renderChatMessages() {
            if (!currentChat.messages) return '';
            
            return currentChat.messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                return `
                    <div class="message ${isOwn ? 'own' : ''}">
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
                openChat(currentChat.id);
            }
        }

        function showFriends() {
            document.getElementById('contentArea').innerHTML = `
                <div style="padding: 10px;">
                    <h3 style="margin-bottom: 15px;">👥 Мои друзья</h3>
                    <div id="friendsList">
                        ${renderFriendsList()}
                    </div>
                </div>
            `;
        }

        function renderFriendsList() {
            if (friends.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">👥</div>
                        <div>Друзей пока нет</div>
                        <div style="font-size: 12px; margin-top: 5px;">Добавьте друзей из списка чатов</div>
                    </div>
                `;
            }
            
            return friends.map(friendId => {
                const friend = allUsers.find(u => u.id === friendId);
                return `
                    <div class="chat-item">
                        <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                            <div style="font-size: 28px;">${friend.avatar}</div>
                            <div style="flex: 1;">
                                <div style="font-weight: bold;">${friend.name}</div>
                                <div style="color: #888; font-size: 14px;">${friend.bio}</div>
                            </div>
                            <div style="display: flex; gap: 5px;">
                                <button class="btn" onclick="startCall('${friend.id}')" style="padding: 8px 12px; font-size: 14px;">
                                    📞
                                </button>
                                <button class="btn" onclick="removeFriend('${friend.id}')" style="padding: 8px 12px; font-size: 14px; background: #ef4444;">
                                    🗑️
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function addFriend(userId) {
            if (!friends.includes(userId)) {
                friends.push(userId);
                showNotification('Пользователь добавлен в друзья! 👥');
            }
        }

        function removeFriend(userId) {
            friends = friends.filter(id => id !== userId);
            showFriends();
            showNotification('Пользователь удален из друзей');
        }

        function startCall(userId) {
            const user = allUsers.find(u => u.id === userId);
            currentCall = { userId: userId, type: 'outgoing' };
            
            document.getElementById('callContainer').classList.remove('hidden');
            document.getElementById('callAvatar').innerHTML = user.avatar;
            document.getElementById('callUserName').textContent = user.name;
            document.getElementById('callStatus').textContent = 'Звонок...';
            document.querySelector('.call-controls').innerHTML = `
                <div class="call-btn call-end" onclick="endCall()">📵</div>
            `;
        }

        function simulateIncomingCall() {
            const randomUser = allUsers.filter(u => u.id !== currentUser.id && u.isOnline)[0];
            if (!randomUser) return;
            
            currentCall = { userId: randomUser.id, type: 'incoming' };
            
            document.getElementById('callContainer').classList.remove('hidden');
            document.getElementById('callAvatar').innerHTML = randomUser.avatar;
            document.getElementById('callUserName').textContent = randomUser.name;
            document.getElementById('callStatus').textContent = 'Входящий вызов...';
            document.querySelector('.call-controls').innerHTML = `
                <div class="call-btn call-accept" onclick="acceptCall()">📞</div>
                <div class="call-btn call-decline" onclick="declineCall()">📵</div>
            `;
        }

        function acceptCall() {
            document.getElementById('callStatus').textContent = 'Разговор...';
            document.querySelector('.call-controls').innerHTML = `
                <div class="call-btn call-end" onclick="endCall()">📵</div>
            `;
        }

        function declineCall() {
            endCall();
        }

        function endCall() {
            document.getElementById('callContainer').classList.add('hidden');
            currentCall = null;
        }

        // СЛУЧАЙНЫЕ ВХОДЯЩИЕ ЗВОНКИ
        setInterval(() => {
            if (!currentCall && Math.random() < 0.02) {
                simulateIncomingCall();
            }
        }, 30000);

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
                            <input type="file" id="settingsAvatarInput" accept="image/*" style="display: none;" onchange="updateAvatar(event)">
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
            showNotification('Тема изменена! 🎨');
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
                    showNotification('Аватар обновлен! 📸');
                    renderMainInterface();
                }
                reader.readAsDataURL(file);
            }
        }

        function logout() {
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function showNotification(message) {
            // Создаем простое уведомление
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--accent-color);
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                z-index: 3000;
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Добавляем анимацию для уведомлений
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🎃 DLtrollex Mobile запущен!")
    print(f"🔗 http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
