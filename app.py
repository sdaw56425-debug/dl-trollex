# app.py
from flask import Flask, render_template_string, request, jsonify, session
import datetime
import random
import os
import uuid
import logging
import hashlib
import time
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trollexdl-premium-2024')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

# Хранилища данных в памяти (в продакшене используйте БД)
users_db = {}
messages_db = {}
calls_db = {}
active_sessions = {}

class User:
    def __init__(self, user_id, username, avatar, email=None):
        self.id = user_id
        self.username = username
        self.avatar = avatar
        self.email = email
        self.online = True
        self.last_seen = datetime.datetime.now()
        self.status = "В сети"
        self.created_at = datetime.datetime.now()

class Message:
    def __init__(self, message_id, sender_id, receiver_id, content, message_type="text"):
        self.id = message_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.type = message_type
        self.timestamp = datetime.datetime.now()
        self.read = False

class Call:
    def __init__(self, call_id, creator_id, call_type="audio"):
        self.id = call_id
        self.creator_id = creator_id
        self.type = call_type
        self.participants = [creator_id]
        self.started_at = datetime.datetime.now()
        self.ended_at = None
        self.active = True

def generate_user_id():
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_message_id():
    return f"msg_{uuid.uuid4().hex[:12]}"

def generate_call_id():
    return f"call_{uuid.uuid4().hex[:12]}"

def generate_session_token():
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def init_sample_data():
    """Инициализация тестовых данных"""
    if not users_db:
        sample_users = [
            {"id": "user_1", "username": "Алексей Волнов", "avatar": "🌊", "status": "Слушаю музыку..."},
            {"id": "user_2", "username": "Мария Эфирная", "avatar": "🎵", "status": "В сети"},
            {"id": "user_3", "username": "Максим Космический", "avatar": "🚀", "status": "Не беспокоить"},
            {"id": "user_4", "username": "Анна Звуковая", "avatar": "🎧", "status": "Разрабатываю TrollexDL"},
        ]
        
        for user_data in sample_users:
            user = User(
                user_id=user_data["id"],
                username=user_data["username"],
                avatar=user_data["avatar"]
            )
            user.status = user_data["status"]
            users_db[user.id] = user

def get_user_by_id(user_id):
    return users_db.get(user_id)

def get_user_messages(user_id):
    """Получить все чаты пользователя"""
    user_messages = {}
    for msg_id, message in messages_db.items():
        if message.sender_id == user_id or message.receiver_id == user_id:
            contact_id = message.receiver_id if message.sender_id == user_id else message.sender_id
            if contact_id not in user_messages:
                user_messages[contact_id] = []
            user_messages[contact_id].append(message)
    
    # Сортируем сообщения по времени
    for contact_id in user_messages:
        user_messages[contact_id].sort(key=lambda x: x.timestamp)
    
    return user_messages

def create_message(sender_id, receiver_id, content, message_type="text"):
    message_id = generate_message_id()
    message = Message(message_id, sender_id, receiver_id, content, message_type)
    messages_db[message_id] = message
    return message

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrollexDL 🚀 Премиум Мессенджер</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
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
            --cyber: #00ffff;
            --card-bg: rgba(255, 255, 255, 0.05);
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .app-container {
            display: flex;
            height: 100vh;
        }

        /* Боковая панель */
        .sidebar {
            width: 350px;
            background: rgba(26, 26, 74, 0.95);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
        }

        .user-header {
            padding: 30px 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 15px;
            border: 3px solid rgba(255,255,255,0.3);
        }

        .user-info h2 {
            font-size: 1.3rem;
            margin-bottom: 5px;
        }

        .user-info p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .nav-tabs {
            display: flex;
            padding: 20px;
            gap: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .nav-tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            background: var(--card-bg);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            font-size: 0.9rem;
        }

        .nav-tab.active {
            background: var(--accent);
            border-color: var(--accent-glow);
            box-shadow: 0 4px 15px rgba(107, 43, 217, 0.3);
        }

        .nav-tab:hover {
            border-color: var(--accent);
        }

        .search-box {
            padding: 20px;
        }

        .search-input {
            width: 100%;
            padding: 12px 20px;
            background: var(--card-bg);
            border: 1px solid var(--accent);
            border-radius: 10px;
            color: var(--text);
            font-size: 0.9rem;
        }

        .contacts-list {
            flex: 1;
            overflow-y: auto;
            padding: 0 20px 20px;
        }

        .contact-card {
            display: flex;
            align-items: center;
            padding: 15px;
            background: var(--card-bg);
            border-radius: 12px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }

        .contact-card:hover {
            border-color: var(--accent);
            transform: translateX(5px);
        }

        .contact-card.active {
            border-color: var(--neon);
            background: rgba(0, 255, 136, 0.1);
        }

        .contact-avatar {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            margin-right: 15px;
        }

        .contact-info {
            flex: 1;
        }

        .contact-name {
            font-weight: 600;
            margin-bottom: 4px;
        }

        .contact-status {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .online-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            display: inline-block;
            margin-right: 5px;
        }

        /* Область чата */
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
        }

        .chat-header {
            padding: 20px 30px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            justify-content: space-between;
            backdrop-filter: blur(10px);
        }

        .chat-partner {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .chat-actions {
            display: flex;
            gap: 10px;
        }

        .action-btn {
            width: 45px;
            height: 45px;
            border-radius: 10px;
            background: var(--card-bg);
            border: 1px solid var(--accent);
            color: var(--text);
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }

        .action-btn:hover {
            background: var(--accent);
            transform: scale(1.1);
        }

        .messages-container {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 70%;
            padding: 0;
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.received {
            align-self: flex-start;
        }

        .message.sent {
            align-self: flex-end;
        }

        .message-bubble {
            padding: 15px 20px;
            border-radius: 18px;
            position: relative;
        }

        .message.received .message-bubble {
            background: var(--card-bg);
            border: 1px solid rgba(255,255,255,0.1);
            border-bottom-left-radius: 5px;
        }

        .message.sent .message-bubble {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            border-bottom-right-radius: 5px;
            color: white;
        }

        .message-text {
            font-size: 0.95rem;
            line-height: 1.4;
        }

        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 5px;
            text-align: right;
        }

        .message-input-container {
            padding: 20px 30px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--accent);
            backdrop-filter: blur(10px);
        }

        .input-wrapper {
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }

        .message-input {
            flex: 1;
            padding: 15px 20px;
            background: var(--card-bg);
            border: 1px solid var(--accent);
            border-radius: 15px;
            color: var(--text);
            font-size: 0.95rem;
            resize: none;
            min-height: 50px;
            max-height: 120px;
        }

        .send-button {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            border: none;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }

        .send-button:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 20px rgba(107, 43, 217, 0.4);
        }

        .input-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .input-action {
            padding: 8px 15px;
            background: var(--card-bg);
            border: 1px solid var(--accent);
            border-radius: 8px;
            color: var(--text);
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .input-action:hover {
            background: var(--accent);
        }

        /* Экран загрузки */
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }

        .loading-content {
            text-align: center;
        }

        .loading-logo {
            font-size: 4rem;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .hidden {
            display: none !important;
        }

        /* Уведомления */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 1000;
            animation: slideInRight 0.3s ease;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }

        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        /* Адаптивность */
        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                width: 100%;
                height: 100%;
                z-index: 100;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }

            .sidebar.active {
                transform: translateX(0);
            }

            .mobile-menu-btn {
                display: block;
                background: none;
                border: none;
                color: var(--text);
                font-size: 1.2rem;
                cursor: pointer;
            }

            .message {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div class="loading-screen" id="loadingScreen">
        <div class="loading-content">
            <div class="loading-logo">🚀</div>
            <h2>TrollexDL</h2>
            <p>Запуск премиум мессенджера...</p>
        </div>
    </div>

    <!-- Главное приложение -->
    <div class="app-container" id="app" style="display: none;">
        <!-- Боковая панель -->
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <div class="user-avatar" id="userAvatar">🚀</div>
                <div class="user-info">
                    <h2 id="userName">Пользователь</h2>
                    <p id="userStatus">Загрузка...</p>
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬 Чаты</div>
                <div class="nav-tab" onclick="switchTab('contacts')">👥 Контакты</div>
                <div class="nav-tab" onclick="switchTab('calls')">📞 Звонки</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" id="searchInput" placeholder="Поиск..." oninput="searchContacts()">
            </div>

            <div class="contacts-list" id="contactsList">
                <!-- Контакты загружаются динамически -->
            </div>
        </div>

        <!-- Область чата -->
        <div class="chat-area">
            <div class="chat-header">
                <div class="chat-partner">
                    <button class="mobile-menu-btn" onclick="toggleSidebar()" style="display: none;">☰</button>
                    <div class="user-avatar" id="chatAvatar">💬</div>
                    <div>
                        <h2 id="chatUserName">TrollexDL</h2>
                        <p id="chatUserStatus">Выберите чат для общения</p>
                    </div>
                </div>
                <div class="chat-actions">
                    <button class="action-btn" onclick="startVoiceCall()" title="Голосовой вызов">🎤</button>
                    <button class="action-btn" onclick="startVideoCall()" title="Видеозвонок">📹</button>
                    <button class="action-btn" onclick="showSettings()" title="Настройки">⚙️</button>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🚀</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Выберите чат или начните новый разговор</p>
                </div>
            </div>

            <div class="message-input-container">
                <div class="input-wrapper">
                    <textarea class="message-input" id="messageInput" placeholder="Введите сообщение..." rows="1"></textarea>
                    <button class="send-button" onclick="sendMessage()">➤</button>
                </div>
                <div class="input-actions">
                    <div class="input-action" onclick="attachFile()">
                        📎 Прикрепить файл
                    </div>
                    <div class="input-action" onclick="sendVoiceMessage()">
                        🎤 Голосовое сообщение
                    </div>
                    <div class="input-action" onclick="showEmojiPicker()">
                        😊 Эмодзи
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentChat = null;
        let allContacts = [];
        let messages = {};
        let currentTab = 'chats';

        // Инициализация приложения
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initializeApp, 2000);
        });

        function initializeApp() {
            document.getElementById('loadingScreen').style.display = 'none';
            document.getElementById('app').style.display = 'flex';
            
            loadCurrentUser();
            loadContacts();
            setupEventListeners();
            
            showNotification('TrollexDL успешно запущен! 🚀');
        }

        function loadCurrentUser() {
            // Пробуем загрузить пользователя из localStorage
            const savedUser = localStorage.getItem('trollexdl_current_user');
            
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
            } else {
                // Создаем нового пользователя
                currentUser = {
                    id: generateUserId(),
                    username: generateUsername(),
                    avatar: '🚀',
                    status: 'В сети',
                    online: true
                };
                localStorage.setItem('trollexdl_current_user', JSON.stringify(currentUser));
            }
            
            updateUserInterface();
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 9);
        }

        function generateUsername() {
            const names = ['Космический Путешественник', 'Цифровой Номад', 'Виртуальный Исследователь', 'Техно Мечтатель'];
            return names[Math.floor(Math.random() * names.length)];
        }

        function updateUserInterface() {
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userName').textContent = currentUser.username;
            document.getElementById('userStatus').textContent = currentUser.status;
        }

        function loadContacts() {
            // Загружаем тестовые контакты
            allContacts = [
                {id: 'user_1', username: 'Алексей Волнов', avatar: '🌊', status: 'Слушаю музыку...', online: true, lastSeen: 'только что'},
                {id: 'user_2', username: 'Мария Эфирная', avatar: '🎵', status: 'В сети', online: true, lastSeen: '2 мин назад'},
                {id: 'user_3', username: 'Максим Космический', avatar: '🚀', status: 'Не беспокоить', online: false, lastSeen: '1 час назад'},
                {id: 'user_4', username: 'Анна Звуковая', avatar: '🎧', status: 'Разрабатываю TrollexDL', online: true, lastSeen: 'только что'}
            ];
            
            renderContacts();
        }

        function renderContacts() {
            const container = document.getElementById('contactsList');
            let html = '';
            
            allContacts.forEach(contact => {
                html += `
                    <div class="contact-card ${currentChat?.id === contact.id ? 'active' : ''}" 
                         onclick="selectContact('${contact.id}')">
                        <div class="contact-avatar">${contact.avatar}</div>
                        <div class="contact-info">
                            <div class="contact-name">${contact.username}</div>
                            <div class="contact-status">
                                <span class="online-dot" style="background: ${contact.online ? '#00ff88' : '#b0b0ff'}"></span>
                                ${contact.status}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }

        function selectContact(contactId) {
            const contact = allContacts.find(c => c.id === contactId);
            if (contact) {
                currentChat = contact;
                renderContacts();
                
                // Обновляем заголовок чата
                document.getElementById('chatAvatar').textContent = contact.avatar;
                document.getElementById('chatUserName').textContent = contact.username;
                document.getElementById('chatUserStatus').textContent = contact.online ? '🟢 Online' : '⚫ Offline';
                
                // Загружаем сообщения
                loadMessages(contactId);
                
                showNotification(`Чат с ${contact.username} открыт 💬`);
            }
        }

        function loadMessages(contactId) {
            const container = document.getElementById('messagesContainer');
            
            // Загружаем сообщения из localStorage
            const savedMessages = localStorage.getItem(`trollexdl_messages_${contactId}`);
            if (savedMessages) {
                messages[contactId] = JSON.parse(savedMessages);
            } else {
                // Создаем тестовые сообщения
                messages[contactId] = [
                    {id: 1, text: 'Привет! Добро пожаловать в TrollexDL! 🚀', sender: contactId, time: '10:30', type: 'received'},
                    {id: 2, text: 'Спасибо! Крутой мессенджер! Как тут всё работает?', sender: currentUser.id, time: '10:31', type: 'sent'},
                    {id: 3, text: 'Очень просто! Пиши сообщения, звони, общайся безопасно! 🔒', sender: contactId, time: '10:32', type: 'received'},
                    {id: 4, text: 'Отлично! А есть видеозвонки?', sender: currentUser.id, time: '10:33', type: 'sent'},
                    {id: 5, text: 'Конечно! Нажимай на кнопку камеры вверху 📹', sender: contactId, time: '10:34', type: 'received'}
                ];
                saveMessages(contactId);
            }
            
            renderMessages(contactId);
        }

        function renderMessages(contactId) {
            const container = document.getElementById('messagesContainer');
            const messageList = messages[contactId] || [];
            
            if (messageList.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 20px;">💬</div>
                        <h3>Начните разговор</h3>
                        <p>Отправьте первое сообщение</p>
                    </div>
                `;
                return;
            }
            
            let html = '';
            messageList.forEach(message => {
                html += `
                    <div class="message ${message.type}">
                        <div class="message-bubble">
                            <div class="message-text">${message.text}</div>
                            <div class="message-time">${message.time}</div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            container.scrollTop = container.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (!text || !currentChat) {
                showNotification('Выберите чат и введите сообщение');
                return;
            }
            
            // Создаем новое сообщение
            const newMessage = {
                id: Date.now(),
                text: text,
                sender: currentUser.id,
                time: new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'}),
                type: 'sent'
            };
            
            // Добавляем в историю
            if (!messages[currentChat.id]) {
                messages[currentChat.id] = [];
            }
            messages[currentChat.id].push(newMessage);
            
            // Сохраняем
            saveMessages(currentChat.id);
            
            // Очищаем input
            input.value = '';
            input.style.height = 'auto';
            
            // Обновляем интерфейс
            renderMessages(currentChat.id);
            
            // Показываем уведомление
            showNotification('Сообщение отправлено! ✨');
            
            // Симулируем ответ через 1-3 секунды
            setTimeout(simulateReply, 1000 + Math.random() * 2000);
        }

        function simulateReply() {
            if (!currentChat) return;
            
            const replies = [
                'Интересно! Расскажи подробнее 🚀',
                'Понял тебя! Что думаешь о TrollexDL?',
                'Крутая идея! Давай обсудим детали',
                'Согласен с тобой! Продолжаем в том же духе 🌟',
                'Отличное предложение! Как насчет звонка? 📞'
            ];
            
            const replyMessage = {
                id: Date.now() + 1,
                text: replies[Math.floor(Math.random() * replies.length)],
                sender: currentChat.id,
                time: new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'}),
                type: 'received'
            };
            
            messages[currentChat.id].push(replyMessage);
            saveMessages(currentChat.id);
            renderMessages(currentChat.id);
            
            showNotification(`Новое сообщение от ${currentChat.username}`);
        }

        function saveMessages(contactId) {
            localStorage.setItem(`trollexdl_messages_${contactId}`, JSON.stringify(messages[contactId]));
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            // Обновляем активные вкладки
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Здесь можно добавить логику для разных вкладок
            showNotification(`Переключено на: ${getTabName(tabName)}`);
        }

        function getTabName(tabName) {
            const names = {
                'chats': 'Чаты',
                'contacts': 'Контакты', 
                'calls': 'Звонки'
            };
            return names[tabName] || tabName;
        }

        function searchContacts() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const filteredContacts = allContacts.filter(contact => 
                contact.username.toLowerCase().includes(searchTerm) ||
                contact.status.toLowerCase().includes(searchTerm)
            );
            
            const container = document.getElementById('contactsList');
            let html = '';
            
            filteredContacts.forEach(contact => {
                html += `
                    <div class="contact-card ${currentChat?.id === contact.id ? 'active' : ''}" 
                         onclick="selectContact('${contact.id}')">
                        <div class="contact-avatar">${contact.avatar}</div>
                        <div class="contact-info">
                            <div class="contact-name">${contact.username}</div>
                            <div class="contact-status">
                                <span class="online-dot" style="background: ${contact.online ? '#00ff88' : '#b0b0ff'}"></span>
                                ${contact.status}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html || '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">Контакты не найдены</div>';
        }

        function showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        function startVoiceCall() {
            if (!currentChat) {
                showNotification('Выберите контакт для звонка');
                return;
            }
            showNotification(`Звонок ${currentChat.username}... 📞`);
        }

        function startVideoCall() {
            if (!currentChat) {
                showNotification('Выберите контакт для видеозвонка');
                return;
            }
            showNotification(`Видеозвонок ${currentChat.username}... 📹`);
        }

        function showSettings() {
            showNotification('Настройки TrollexDL ⚙️');
            // Здесь можно открыть модальное окно с настройками
        }

        function attachFile() {
            showNotification('Выберите файл для отправки 📎');
        }

        function sendVoiceMessage() {
            showNotification('Запись голосового сообщения... 🎤');
        }

        function showEmojiPicker() {
            showNotification('Выбор эмодзи 😊');
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function setupEventListeners() {
            // Обработка Enter для отправки сообщения
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // Авто-размер textarea
            document.getElementById('messageInput').addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });

            // Адаптивность
            if (window.innerWidth <= 768) {
                document.querySelector('.mobile-menu-btn').style.display = 'block';
            }
        }

        // Публичные методы для API
        window.sendMessage = sendMessage;
        window.selectContact = selectContact;
        window.startVoiceCall = startVoiceCall;
        window.startVideoCall = startVideoCall;
        window.showSettings = showSettings;
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    init_sample_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    try:
        data = request.json
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        message_text = data.get('message')
        
        if not all([sender_id, receiver_id, message_text]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Проверяем существование пользователей
        sender = get_user_by_id(sender_id)
        receiver = get_user_by_id(receiver_id)
        
        if not sender or not receiver:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Создаем сообщение
        message = create_message(sender_id, receiver_id, message_text)
        
        return jsonify({
            'success': True, 
            'message': {
                'id': message.id,
                'text': message.content,
                'sender': message.sender_id,
                'time': message.timestamp.strftime('%H:%M'),
                'type': 'sent'
            }
        })
        
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_messages/<user_id>/<contact_id>')
def api_get_messages(user_id, contact_id):
    try:
        user_messages = get_user_messages(user_id)
        contact_messages = user_messages.get(contact_id, [])
        
        messages_data = []
        for msg in contact_messages:
            messages_data.append({
                'id': msg.id,
                'text': msg.content,
                'sender': msg.sender_id,
                'time': msg.timestamp.strftime('%H:%M'),
                'type': 'sent' if msg.sender_id == user_id else 'received'
            })
        
        return jsonify({'success': True, 'messages': messages_data})
        
    except Exception as e:
        logger.error(f"Ошибка получения сообщений: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    try:
        data = request.json
        creator_id = data.get('creator_id')
        call_type = data.get('type', 'audio')
        
        if not creator_id:
            return jsonify({'success': False, 'error': 'Creator ID required'}), 400
        
        creator = get_user_by_id(creator_id)
        if not creator:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        call_id = generate_call_id()
        call = Call(call_id, creator_id, call_type)
        calls_db[call_id] = call
        
        logger.info(f"Создан звонок: {call_id}")
        return jsonify({
            'success': True, 
            'call_id': call_id,
            'call_link': f'/call/{call_id}'
        })
        
    except Exception as e:
        logger.error(f"Ошибка создания звонка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_contacts')
def api_get_contacts():
    try:
        contacts_data = []
        for user_id, user in users_db.items():
            contacts_data.append({
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar,
                'status': user.status,
                'online': user.online,
                'last_seen': user.last_seen.strftime('%H:%M')
            })
        
        return jsonify({'success': True, 'contacts': contacts_data})
        
    except Exception as e:
        logger.error(f"Ошибка получения контактов: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
