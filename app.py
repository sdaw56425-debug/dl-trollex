# app.py
from flask import Flask, render_template_string, request, jsonify
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

# Хранилища данных
active_calls = {}
user_sessions = {}
user_messages = {}
all_users = []

def get_days_until_new_year():
    now = datetime.datetime.now()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    return (new_year - now).days

def generate_username():
    adjectives = ['Волна', 'Поток', 'Эфир', 'Квант', 'Цифра', 'Виртуальный', 'Голосовой', 'Звуковой']
    nouns = ['Искатель', 'Слушатель', 'Творец', 'Мечтатель', 'Навигатор', 'Проводник', 'Исследователь']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def generate_user_id():
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_call_id():
    return f"call_{uuid.uuid4().hex[:12]}"

def generate_session_token():
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def verify_session(user_id, session_token):
    return user_id in user_sessions and session_token == user_sessions.get(user_id)

def initialize_sample_data():
    global all_users
    all_users = [
        {'id': 'user1', 'name': 'Алексей Волнов', 'avatar': '🌊', 'online': True, 'last_seen': 'только что', 'status': 'Слушаю волны...'},
        {'id': 'user2', 'name': 'Мария Эфирная', 'avatar': '🎵', 'online': True, 'last_seen': '2 мин назад', 'status': 'Создаю музыку'},
        {'id': 'user3', 'name': 'Иван Потоков', 'avatar': '🚀', 'online': False, 'last_seen': '1 час назад', 'status': 'В офлайне'},
        {'id': 'user4', 'name': 'Анна Звуковая', 'avatar': '🎧', 'online': True, 'last_seen': 'только что', 'status': 'В эфире'},
    ]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SoundWave 🎵 Мессенджер</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎵</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        :root {
            --primary: #0f1a2f;
            --secondary: #1a2b4a;
            --accent: #4361ee;
            --accent-light: #4895ef;
            --text: #ffffff;
            --text-secondary: #8ba0c7;
            --success: #4cc9f0;
            --warning: #f72585;
            --card-bg: rgba(255, 255, 255, 0.08);
            --gradient: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
            --wave-gradient: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        }

        body {
            background: var(--primary);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .app-container {
            display: flex;
            height: 100vh;
            background: var(--primary);
        }

        /* Боковая панель */
        .sidebar {
            width: 380px;
            background: var(--secondary);
            display: flex;
            flex-direction: column;
            border-right: 1px solid rgba(255,255,255,0.1);
            position: relative;
            overflow: hidden;
        }

        .sidebar::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--wave-gradient);
            animation: waveFlow 8s linear infinite;
        }

        @keyframes waveFlow {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .user-header {
            padding: 30px 25px;
            background: var(--gradient);
            position: relative;
            z-index: 2;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 20px;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255,255,255,0.3);
        }

        .user-details h2 {
            font-size: 18px;
            margin-bottom: 5px;
        }

        .user-details .status {
            font-size: 14px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
        }

        /* Навигация */
        .nav-tabs {
            display: flex;
            padding: 20px 25px;
            gap: 10px;
            position: relative;
            z-index: 2;
        }

        .nav-tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            background: var(--card-bg);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }

        .nav-tab.active {
            background: var(--accent);
            border-color: var(--accent-light);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(67, 97, 238, 0.3);
        }

        .nav-tab:hover {
            border-color: var(--accent-light);
        }

        /* Поиск */
        .search-container {
            padding: 0 25px 20px;
            position: relative;
            z-index: 2;
        }

        .search-box {
            position: relative;
        }

        .search-input {
            width: 100%;
            padding: 15px 45px 15px 20px;
            background: var(--card-bg);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            color: var(--text);
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
        }

        .search-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
        }

        /* Список контактов */
        .contacts-list {
            flex: 1;
            overflow-y: auto;
            padding: 0 25px 25px;
            position: relative;
            z-index: 2;
        }

        .contact-card {
            display: flex;
            align-items: center;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            position: relative;
            overflow: hidden;
        }

        .contact-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--wave-gradient);
            transition: left 0.5s ease;
        }

        .contact-card:hover::before {
            left: 100%;
        }

        .contact-card:hover {
            border-color: var(--accent);
            transform: translateX(5px);
        }

        .contact-card.active {
            border-color: var(--accent);
            background: rgba(67, 97, 238, 0.15);
        }

        .contact-avatar {
            width: 50px;
            height: 50px;
            border-radius: 15px;
            background: var(--gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-right: 15px;
            flex-shrink: 0;
        }

        .contact-info {
            flex: 1;
        }

        .contact-name {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .contact-status {
            font-size: 13px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .contact-meta {
            text-align: right;
        }

        .contact-time {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 5px;
        }

        .unread-badge {
            background: var(--warning);
            color: white;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
        }

        /* Область чата */
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
            position: relative;
        }

        .chat-header {
            padding: 25px 30px;
            background: var(--secondary);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
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
            border-radius: 12px;
            background: var(--card-bg);
            border: none;
            color: var(--text);
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }

        .action-btn:hover {
            background: var(--accent);
            transform: scale(1.1);
        }

        /* Сообщения */
        .messages-container {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .message {
            max-width: 70%;
            padding: 0;
            position: relative;
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
            border-radius: 20px;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .message.received .message-bubble {
            background: var(--card-bg);
            border-bottom-left-radius: 5px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .message.sent .message-bubble {
            background: var(--gradient);
            border-bottom-right-radius: 5px;
            color: white;
        }

        .message-text {
            font-size: 15px;
            line-height: 1.4;
        }

        .message-time {
            font-size: 11px;
            opacity: 0.7;
            margin-top: 5px;
            text-align: right;
        }

        .message.received .message-time {
            text-align: left;
        }

        /* Ввод сообщения */
        .message-input-container {
            padding: 25px 30px;
            background: var(--secondary);
            border-top: 1px solid rgba(255,255,255,0.1);
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
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            color: var(--text);
            font-size: 15px;
            resize: none;
            min-height: 50px;
            max-height: 120px;
            transition: all 0.3s ease;
        }

        .message-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
        }

        .send-button {
            width: 50px;
            height: 50px;
            border-radius: 15px;
            background: var(--gradient);
            border: none;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .send-button:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(67, 97, 238, 0.4);
        }

        .input-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .input-action {
            padding: 8px 15px;
            background: var(--card-bg);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: var(--text);
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .input-action:hover {
            background: var(--accent);
            border-color: var(--accent);
        }

        /* Волновой эффект */
        .wave-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100px;
            overflow: hidden;
            pointer-events: none;
            z-index: 1;
        }

        .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 200%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none"><path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="%234361ee"/><path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" fill="%234361ee"/><path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" fill="%234361ee"/></svg>');
            animation: wave 12s linear infinite;
            opacity: 0.1;
        }

        .wave:nth-child(2) {
            animation: wave 8s linear infinite reverse;
            opacity: 0.05;
        }

        .wave:nth-child(3) {
            animation: wave 10s linear infinite;
            opacity: 0.07;
        }

        @keyframes wave {
            0% { transform: translateX(0); }
            50% { transform: translateX(-25%); }
            100% { transform: translateX(-50%); }
        }

        /* Аудио визуализатор */
        .audio-visualizer {
            display: flex;
            align-items: center;
            gap: 3px;
            height: 30px;
            margin: 10px 0;
        }

        .bar {
            width: 3px;
            background: var(--accent);
            border-radius: 2px;
            animation: audioBar 1.5s ease-in-out infinite;
        }

        .bar:nth-child(odd) {
            height: 15px;
            animation-delay: 0.1s;
        }

        .bar:nth-child(even) {
            height: 25px;
            animation-delay: 0.3s;
        }

        @keyframes audioBar {
            0%, 100% { transform: scaleY(0.5); opacity: 0.7; }
            50% { transform: scaleY(1); opacity: 1; }
        }

        /* Адаптивность */
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                position: absolute;
                z-index: 100;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }

            .sidebar.active {
                transform: translateX(0);
            }

            .mobile-menu-btn {
                display: block;
            }

            .message {
                max-width: 85%;
            }
        }

        /* Уведомления */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--gradient);
            color: white;
            padding: 15px 20px;
            border-radius: 12px;
            z-index: 1000;
            animation: slideInRight 0.3s ease;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
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

        /* Загрузчик */
        .loader {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: var(--primary);
        }

        .loader-content {
            text-align: center;
        }

        .loader-wave {
            font-size: 48px;
            margin-bottom: 20px;
            animation: waveBounce 2s ease-in-out infinite;
        }

        @keyframes waveBounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
</head>
<body>
    <div class="loader" id="loader">
        <div class="loader-content">
            <div class="loader-wave">🎵</div>
            <h2>SoundWave</h2>
            <p>Запуск аудио-мессенджера...</p>
        </div>
    </div>

    <div class="app-container" id="app" style="display: none;">
        <!-- Боковая панель -->
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <div class="user-info">
                    <div class="user-avatar" id="userAvatar">🎵</div>
                    <div class="user-details">
                        <h2 id="userName">Пользователь</h2>
                        <div class="status">
                            <div class="status-dot"></div>
                            <span id="userStatus">В сети</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬 Чаты</div>
                <div class="nav-tab" onclick="switchTab('contacts')">👥 Контакты</div>
                <div class="nav-tab" onclick="switchTab('calls')">📞 Звонки</div>
            </div>

            <div class="search-container">
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="Поиск сообщений..." id="searchInput">
                    <div class="search-icon">🔍</div>
                </div>
            </div>

            <div class="contacts-list" id="contactsList">
                <!-- Контакты загружаются динамически -->
            </div>
        </div>

        <!-- Область чата -->
        <div class="chat-area">
            <div class="chat-header">
                <div class="chat-partner">
                    <div class="user-avatar" id="chatAvatar">💬</div>
                    <div>
                        <h2 id="chatUserName">SoundWave</h2>
                        <div class="status">
                            <div class="status-dot"></div>
                            <span id="chatUserStatus">Выберите чат для общения</span>
                        </div>
                    </div>
                </div>
                <div class="chat-actions">
                    <button class="action-btn" onclick="startVoiceCall()">🎤</button>
                    <button class="action-btn" onclick="startVideoCall()">📹</button>
                    <button class="action-btn" onclick="showSettings()">⚙️</button>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                    <div style="font-size: 64px; margin-bottom: 20px;">🎵</div>
                    <h3>Добро пожаловать в SoundWave</h3>
                    <p>Выберите чат или начните новый разговор</p>
                    <div class="audio-visualizer" style="justify-content: center; margin: 30px 0;">
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                        <div class="bar"></div>
                    </div>
                </div>
            </div>

            <div class="message-input-container">
                <div class="input-wrapper">
                    <textarea class="message-input" id="messageInput" placeholder="Введите сообщение..." rows="1"></textarea>
                    <button class="send-button" onclick="sendMessage()">➤</button>
                </div>
                <div class="input-actions">
                    <div class="input-action" onclick="attachFile()">
                        📎 Прикрепить
                    </div>
                    <div class="input-action" onclick="sendVoiceMessage()">
                        🎤 Голосовое
                    </div>
                    <div class="input-action" onclick="sendEmoji()">
                        😊 Эмодзи
                    </div>
                </div>
            </div>
        </div>

        <!-- Волновой эффект -->
        <div class="wave-container">
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentChat = null;
        let allContacts = [];
        let messages = {};

        // Инициализация приложения
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initializeApp, 1500);
        });

        function initializeApp() {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('app').style.display = 'flex';
            
            // Загружаем или создаем пользователя
            loadCurrentUser();
            // Загружаем контакты
            loadContacts();
            // Загружаем настройки
            loadSettings();
            
            showNotification('SoundWave запущен! 🎵');
        }

        function loadCurrentUser() {
            const savedUser = localStorage.getItem('soundwave_user');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
            } else {
                // Создаем нового пользователя
                currentUser = {
                    id: generateUserId(),
                    name: generateUsername(),
                    avatar: '🎵',
                    status: 'В сети',
                    online: true
                };
                localStorage.setItem('soundwave_user', JSON.stringify(currentUser));
            }
            
            updateUserInterface();
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 9);
        }

        function generateUsername() {
            const names = ['Волна Искатель', 'Поток Слушатель', 'Эфир Творец', 'Звук Мечтатель'];
            return names[Math.floor(Math.random() * names.length)];
        }

        function updateUserInterface() {
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userStatus').textContent = currentUser.status;
        }

        function loadContacts() {
            // Загружаем тестовые контакты
            allContacts = [
                {id: 'user1', name: 'Алексей Волнов', avatar: '🌊', online: true, status: 'Слушаю волны...', lastSeen: 'только что', unread: 2},
                {id: 'user2', name: 'Мария Эфирная', avatar: '🎵', online: true, status: 'Создаю музыку', lastSeen: '2 мин назад', unread: 0},
                {id: 'user3', name: 'Иван Потоков', avatar: '🚀', online: false, status: 'В офлайне', lastSeen: '1 час назад', unread: 5},
                {id: 'user4', name: 'Анна Звуковая', avatar: '🎧', online: true, status: 'В эфире', lastSeen: 'только что', unread: 0}
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
                            <div class="contact-name">${contact.name}</div>
                            <div class="contact-status">
                                <div class="status-dot" style="background: ${contact.online ? '#4cc9f0' : '#8ba0c7'}"></div>
                                ${contact.status}
                            </div>
                        </div>
                        <div class="contact-meta">
                            <div class="contact-time">${contact.lastSeen}</div>
                            ${contact.unread > 0 ? `<div class="unread-badge">${contact.unread}</div>` : ''}
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
                document.getElementById('chatUserName').textContent = contact.name;
                document.getElementById('chatUserStatus').textContent = contact.online ? 'В сети' : 'Не в сети';
                
                // Загружаем сообщения
                loadMessages(contactId);
                
                showNotification(`Чат с ${contact.name} открыт`);
            }
        }

        function loadMessages(contactId) {
            const container = document.getElementById('messagesContainer');
            
            // Загружаем сообщения из localStorage или создаем тестовые
            const savedMessages = localStorage.getItem(`messages_${contactId}`);
            if (savedMessages) {
                messages[contactId] = JSON.parse(savedMessages);
            } else {
                // Создаем тестовые сообщения
                messages[contactId] = [
                    {id: 1, text: 'Привет! Как твои музыкальные проекты?', sender: contactId, time: '10:30', type: 'received'},
                    {id: 2, text: 'Привет! Всё отлично, работаю над новым треком 🎵', sender: currentUser.id, time: '10:31', type: 'sent'},
                    {id: 3, text: 'Круто! Можешь скинуть превью?', sender: contactId, time: '10:32', type: 'received'},
                    {id: 4, text: 'Конечно! Вот ссылка на демо...', sender: currentUser.id, time: '10:33', type: 'sent'}
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
                        <div style="font-size: 64px; margin-bottom: 20px;">💬</div>
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
            
            // Обновляем интерфейс
            renderMessages(currentChat.id);
            
            // Показываем уведомление
            showNotification('Сообщение отправлено ✨');
            
            // Симулируем ответ
            simulateReply();
        }

        function simulateReply() {
            if (!currentChat) return;
            
            setTimeout(() => {
                const replies = [
                    'Интересно! Расскажи подробнее 🎵',
                    'Понял тебя! Что думаешь о новом проекте?',
                    'Крутая идея! Давай обсудим детали',
                    'Согласен с тобой! Продолжаем в том же духе 🌊'
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
                
                showNotification(`Новое сообщение от ${currentChat.name}`);
            }, 2000);
        }

        function saveMessages(contactId) {
            localStorage.setItem(`messages_${contactId}`, JSON.stringify(messages[contactId]));
        }

        function switchTab(tabName) {
            // Обновляем активные вкладки
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Здесь можно добавить логику для разных вкладок
            showNotification(`Переключено на: ${tabName === 'chats' ? 'Чаты' : tabName === 'contacts' ? 'Контакты' : 'Звонки'}`);
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
            showNotification(`Звонок ${currentChat.name}... 📞`);
            
            // Анимация визуализатора
            const visualizer = document.createElement('div');
            visualizer.className = 'audio-visualizer';
            visualizer.innerHTML = `
                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                <div class="bar"></div><div class="bar"></div>
            `;
            
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.innerHTML = `
                <div>📞 Звонок ${currentChat.name}</div>
                ${visualizer.outerHTML}
                <button onclick="endCall()" style="margin-top: 10px; padding: 5px 10px; background: #f72585; border: none; border-radius: 5px; color: white; cursor: pointer;">Завершить</button>
            `;
            
            document.body.appendChild(notification);
        }

        function startVideoCall() {
            if (!currentChat) {
                showNotification('Выберите контакт для видеозвонка');
                return;
            }
            showNotification(`Видеозвонок ${currentChat.name}... 📹`);
        }

        function endCall() {
            showNotification('Звонок завершён');
            document.querySelectorAll('.notification').forEach(note => note.remove());
        }

        function attachFile() {
            showNotification('Выберите файл для отправки 📎');
        }

        function sendVoiceMessage() {
            showNotification('Запись голосового сообщения... 🎤');
        }

        function sendEmoji() {
            showNotification('Выбор эмодзи 😊');
        }

        function showSettings() {
            showNotification('Открытие настроек ⚙️');
        }

        function loadSettings() {
            // Загрузка настроек из localStorage
            const settings = localStorage.getItem('soundwave_settings');
            if (settings) {
                // Применяем настройки
            }
        }

        // Обработка нажатия Enter для отправки сообщения
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
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    initialize_sample_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    try:
        data = request.json
        user_id = data.get('user_id')
        contact_id = data.get('contact_id')
        message_text = data.get('message')
        
        # Сохраняем сообщение
        message_key = f"messages_{user_id}_{contact_id}"
        messages = json.loads(user_messages.get(message_key, '[]'))
        
        new_message = {
            'id': str(uuid.uuid4()),
            'text': message_text,
            'sender': user_id,
            'time': datetime.datetime.now().isoformat(),
            'type': 'sent'
        }
        
        messages.append(new_message)
        user_messages[message_key] = json.dumps(messages)
        
        return jsonify({'success': True, 'message': new_message})
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    try:
        data = request.json
        user_id = data.get('user_id')
        
        call_id = generate_call_id()
        active_calls[call_id] = {
            'creator': user_id,
            'participants': [user_id],
            'created_at': datetime.datetime.now().isoformat(),
            'type': 'audio'
        }
        
        logger.info(f"Создан аудио-звонок: {call_id}")
        return jsonify({
            'success': True, 
            'call_id': call_id,
            'call_link': f'/call/{call_id}'
        })
    except Exception as e:
        logger.error(f"Ошибка создания звонка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🎵 SoundWave запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
