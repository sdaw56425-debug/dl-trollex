# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ЧАТЫ И ПОИСК)
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
        'text': 'Это фиолетовый мессенджер с максимальной кастомизацией! 💜',
        'sender_name': 'Администратор', 
        'timestamp': datetime.datetime.now().isoformat(),
    }
]

# Админ
ADMIN_PASSWORD = "dltrollex123"

# Создаем фавикон роут чтобы убрать 404 ошибку
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'DLtrollex is running'})

def generate_user_id():
    return str(int(datetime.datetime.now().timestamp() * 1000)) + str(random.randint(1000, 9999))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💜</text></svg>">
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
            height: 100vh;
            overflow: hidden;
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
        
        /* Стили для чатов */
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
        
        .search-icon {
            position: absolute;
            right: 35px;
            top: 50%;
            transform: translateY(-50%);
            color: #888;
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
    </style>
</head>
<body>
    <!-- Главный экран выбора -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Фиолетовый чат с максимальной кастомизацией</div>
            
            <button class="btn pulse" onclick="showRegisterScreen()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-admin pulse" onclick="showAdminScreen()">
                <span>👑 Войти как администратор</span>
            </button>
        </div>
    </div>

    <!-- Экран регистрации -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Создание аккаунта</div>
            
            <input type="text" id="regName" class="input-field" placeholder="💁 Ваше имя" required>
            <input type="text" id="regUsername" class="input-field" placeholder="👤 @username (не обязательно)">
            <div class="optional">✨ Юзернейм не обязателен. Если не указать, будет сгенерирован автоматически</div>
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" onclick="showMainScreen()">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
            <div id="registerSuccess" class="success hidden"></div>
        </div>
    </div>

    <!-- Экран входа админа -->
    <div id="adminScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
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

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            checkAutoLogin();
            initializeChats();
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

        function initializeChats() {
            // Создаем тестовые чаты и пользователей
            allUsers = [
                {
                    id: 'user1',
                    name: 'Алексей',
                    username: '@alexey',
                    avatar: '😎',
                    isOnline: true,
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user2', 
                    name: 'Мария',
                    username: '@maria',
                    avatar: '👩',
                    isOnline: true,
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user3',
                    name: 'Дмитрий',
                    username: '@dmitry',
                    avatar: '🧑',
                    isOnline: false,
                    lastSeen: new Date(Date.now() - 300000).toISOString()
                },
                {
                    id: 'user4',
                    name: 'Елена',
                    username: '@elena',
                    avatar: '👸',
                    isOnline: true,
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user5',
                    name: 'Сергей',
                    username: '@sergey',
                    avatar: '🤵',
                    isOnline: false,
                    lastSeen: new Date(Date.now() - 600000).toISOString()
                }
            ];

            chats = [
                {
                    id: 'chat1',
                    type: 'private',
                    participants: [currentUser ? currentUser.id : 'user1', 'user2'],
                    lastMessage: {
                        text: 'Привет! Как дела? 😊',
                        senderId: 'user2',
                        timestamp: new Date().toISOString()
                    },
                    unreadCount: 2
                },
                {
                    id: 'chat2',
                    type: 'private', 
                    participants: [currentUser ? currentUser.id : 'user1', 'user3'],
                    lastMessage: {
                        text: 'Жду твоего ответа! 👍',
                        senderId: currentUser ? currentUser.id : 'user1',
                        timestamp: new Date(Date.now() - 120000).toISOString()
                    },
                    unreadCount: 0
                },
                {
                    id: 'chat3',
                    type: 'group',
                    name: 'Общий чат DLtrollex',
                    participants: ['user1', 'user2', 'user3', 'user4', 'user5'],
                    lastMessage: {
                        text: 'Добро пожаловать в общий чат! 🎉',
                        senderId: 'user4',
                        timestamp: new Date(Date.now() - 300000).toISOString()
                    },
                    unreadCount: 5
                }
            ];
        }

        function showMainScreen() {
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showRegisterScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            renderChatsInterface();
            showNotification('Добро пожаловать в DLtrollex! 💜', 'success');
        }

        function renderChatsInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <!-- Боковая панель с чатами -->
                    <div class="sidebar">
                        <!-- Заголовок -->
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">💜 DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Чаты</div>
                        </div>
                        
                        <!-- Поиск -->
                        <div class="search-box">
                            <div style="position: relative;">
                                <input type="text" class="search-input" placeholder="🔍 Поиск собеседников..." oninput="searchUsers(this.value)">
                                <div class="search-icon">🔍</div>
                            </div>
                        </div>
                        
                        <!-- Список чатов -->
                        <div class="chats-list" id="chatsList">
                            ${renderChatsList()}
                        </div>
                        
                        <!-- Кнопка нового чата -->
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            <button class="btn" onclick="showNewChatModal()" style="margin-bottom: 10px;">➕ Новый чат</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            <button class="btn" onclick="logout()">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Область чата -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <div class="logo glowing-logo" style="font-size: 80px;">💜</div>
                            <h2>Добро пожаловать в чаты!</h2>
                            <p style="color: #888; margin: 10px 0 20px 0;">Выберите чат для начала общения</p>
                            <button class="btn" onclick="showNewChatModal()">💬 Начать новый чат</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderChatsList() {
            return chats.map(chat => {
                const otherParticipants = chat.participants.filter(p => p !== currentUser.id);
                const chatUser = allUsers.find(u => u.id === otherParticipants[0]) || allUsers[0];
                const isActive = currentChat && currentChat.id === chat.id;
                
                return `
                    <div class="chat-item ${isActive ? 'active' : ''}" onclick="openChat('${chat.id}')">
                        <div style="position: relative;">
                            <div class="chat-avatar">${chat.type === 'group' ? '👥' : chatUser.avatar}</div>
                            ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div class="chat-info">
                            <div class="chat-name">
                                ${chat.type === 'group' ? chat.name : chatUser.name}
                                ${chatUser.isOnline ? '<span class="user-status">● онлайн</span>' : ''}
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
            const chatUser = allUsers.find(u => u.id === otherParticipants[0]) || allUsers[0];
            
            document.getElementById('chatContent').innerHTML = `
                <!-- Заголовок чата -->
                <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <div style="position: relative; margin-right: 15px;">
                            <div class="chat-avatar">${currentChat.type === 'group' ? '👥' : chatUser.avatar}</div>
                            ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div>
                            <div style="font-weight: bold; font-size: 16px;">
                                ${currentChat.type === 'group' ? currentChat.name : chatUser.name}
                            </div>
                            <div style="color: #888; font-size: 12px;">
                                ${chatUser.isOnline ? 'online' : `был(а) ${formatLastSeen(chatUser.lastSeen)}`}
                            </div>
                        </div>
                    </div>
                    <button class="btn" onclick="showChatInfo()" style="padding: 8px 15px; font-size: 12px;">ℹ️ Инфо</button>
                </div>
                
                <!-- Сообщения -->
                <div class="messages-container" id="messagesContainer">
                    ${renderChatMessages()}
                </div>
                
                <!-- Ввод сообщения -->
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="💬 Введите сообщение..." id="messageInput">
                    <button class="send-btn" onclick="sendMessage()">📤</button>
                </div>
            `;

            // Прокрутка вниз
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Фокус на поле ввода
            document.getElementById('messageInput').focus();
            
            // Обновляем активный чат в списке
            renderChatsList();
        }

        function renderChatMessages() {
            // Тестовые сообщения для чата
            const messages = [
                {
                    id: '1',
                    text: 'Привет! Как дела? 😊',
                    senderId: currentChat.participants.find(p => p !== currentUser.id),
                    timestamp: new Date(Date.now() - 300000).toISOString()
                },
                {
                    id: '2',
                    text: 'Привет! Все отлично, спасибо! 👍',
                    senderId: currentUser.id,
                    timestamp: new Date(Date.now() - 240000).toISOString()
                },
                {
                    id: '3',
                    text: 'Как тебе новый DLtrollex? 💜',
                    senderId: currentChat.participants.find(p => p !== currentUser.id),
                    timestamp: new Date(Date.now() - 180000).toISOString()
                },
                {
                    id: '4', 
                    text: 'Очень круто! Особенно поиск собеседников и чаты! 🚀',
                    senderId: currentUser.id,
                    timestamp: new Date(Date.now() - 120000).toISOString()
                },
                {
                    id: '5',
                    text: 'Согласен! А анимации просто огонь! 🔥',
                    senderId: currentChat.participants.find(p => p !== currentUser.id),
                    timestamp: new Date(Date.now() - 60000).toISOString()
                }
            ];

            return messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                const sender = allUsers.find(u => u.id === msg.senderId) || {name: 'Неизвестный', avatar: '👤'};
                
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
                const messagesContainer = document.getElementById('messagesContainer');
                const newMessage = {
                    id: Date.now().toString(),
                    text: message,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                const messageElement = document.createElement('div');
                messageElement.className = 'message own';
                messageElement.innerHTML = `
                    <div style="margin-bottom: 5px;">${message}</div>
                    <div style="font-size: 11px; color: rgba(255,255,255,0.7); text-align: right;">
                        ${formatTime(newMessage.timestamp)}
                    </div>
                `;
                
                messagesContainer.appendChild(messageElement);
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Обновляем последнее сообщение в чате
                currentChat.lastMessage = newMessage;
                renderChatsList();
                
                // Имитация ответа
                setTimeout(() => {
                    const responses = [
                        'Круто! 😎',
                        'Интересно! 🤔',
                        'Согласен! 👍',
                        'Продолжай! 💪',
                        'Отличное сообщение! 🔥'
                    ];
                    const response = responses[Math.floor(Math.random() * responses.length)];
                    
                    const responseMessage = {
                        id: Date.now().toString(),
                        text: response,
                        senderId: currentChat.participants.find(p => p !== currentUser.id),
                        timestamp: new Date().toISOString()
                    };
                    
                    const responseElement = document.createElement('div');
                    responseElement.className = 'message';
                    const responder = allUsers.find(u => u.id === responseMessage.senderId) || {name: 'Собеседник', avatar: '👤'};
                    
                    responseElement.innerHTML = `
                        <div style="margin-bottom: 5px;">
                            <strong>${responder.name}:</strong> ${response}
                        </div>
                        <div style="font-size: 11px; color: #888;">
                            ${formatTime(responseMessage.timestamp)}
                        </div>
                    `;
                    
                    messagesContainer.appendChild(responseElement);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    // Обновляем последнее сообщение
                    currentChat.lastMessage = responseMessage;
                    renderChatsList();
                    
                }, 1000 + Math.random() * 2000);
            }
        }

        function searchUsers(query) {
            if (!query.trim()) {
                document.getElementById('chatsList').innerHTML = renderChatsList();
                return;
            }
            
            const filteredUsers = allUsers.filter(user => 
                user.name.toLowerCase().includes(query.toLowerCase()) ||
                user.username.toLowerCase().includes(query.toLowerCase())
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
                            <div class="chat-name">
                                ${user.name}
                                ${user.isOnline ? '<span class="user-status">● онлайн</span>' : ''}
                            </div>
                            <div class="chat-last-message">${user.username}</div>
                        </div>
                        <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Чат</button>
                    </div>
                `).join('');
            } else {
                searchHTML = `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">🔍</div>
                        <div>Ничего не найдено</div>
                        <div style="font-size: 12px; margin-top: 5px;">Попробуйте другой запрос</div>
                    </div>
                `;
            }
            
            document.getElementById('chatsList').innerHTML = searchHTML;
        }

        function showNewChatModal() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 30px; max-width: 500px; margin: 0 auto;">
                    <h2 style="margin-bottom: 20px;">💬 Новый чат</h2>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">👥 Все пользователи</h3>
                        <div style="max-height: 400px; overflow-y: auto;">
                            ${allUsers.map(user => `
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
                                        <div class="chat-last-message">${user.username}</div>
                                    </div>
                                    <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Начать чат</button>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <button class="btn" onclick="renderChatsInterface()" style="margin-top: 20px;">← Назад к чатам</button>
                </div>
            `;
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

            // Создаем новый чат
            const newChat = {
                id: 'chat' + Date.now(),
                type: 'private',
                participants: [currentUser.id, userId],
                lastMessage: {
                    text: 'Чат начат 🚀',
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                },
                unreadCount: 0
            };

            chats.unshift(newChat);
            currentChat = newChat;
            
            // Открываем новый чат
            openChat(newChat.id);
            showNotification(`Чат с ${user.name} начат!`, 'success');
        }

        function showChatInfo() {
            if (!currentChat) return;
            
            const otherParticipants = currentChat.participants.filter(p => p !== currentUser.id);
            const chatUser = allUsers.find(u => u.id === otherParticipants[0]) || allUsers[0];
            
            alert(`Информация о чате:\n\nУчастник: ${chatUser.name}\nЮзернейм: ${chatUser.username}\nСтатус: ${chatUser.isOnline ? 'online' : 'offline'}\n\nID чата: ${currentChat.id}`);
        }

        function showSettings() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 30px; max-width: 500px; margin: 0 auto;">
                    <h2 style="margin-bottom: 20px;">⚙️ Настройки</h2>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="margin-bottom: 15px;">👤 Профиль</h3>
                        <input type="text" class="input-field" value="${currentUser.name}" placeholder="Ваше имя">
                        <input type="text" class="input-field" value="${currentUser.username}" placeholder="Юзернейм">
                        <button class="btn" style="margin-top: 10px;">💾 Сохранить</button>
                    </div>
                    
                    <button class="btn" onclick="renderChatsInterface()">← Назад к чатам</button>
                </div>
            `;
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

        function registerUser() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            const user_id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
            const finalUsername = username || `user${Math.floor(Math.random() * 10000)}`;
            
            currentUser = {
                id: user_id,
                name: name,
                username: finalUsername,
                avatar: '👤',
                avatar_bg: '#6b21a8',
                registered_at: new Date().toISOString(),
            };
            
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            showMainApp();
        }

        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    is_admin: true
                };
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
                showNotification('Вход как администратор выполнен', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        function logout() {
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

        // Обработка Enter
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                if (!document.getElementById('registerScreen').classList.contains('hidden')) {
                    registerUser();
                }
                if (!document.getElementById('adminScreen').classList.contains('hidden')) {
                    adminLogin();
                }
                if (document.getElementById('messageInput')) {
                    sendMessage();
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
        
        user_id = generate_user_id()
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
    print("🚀 Запуск DLtrollex с чатами и поиском...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("💬 Добавлены чаты и поиск собеседников!")
    print("🔍 Лупа для поиска работает!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
