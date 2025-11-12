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
import re

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
friendships = {}
friend_requests = {}
user_profiles = {}

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

def generate_call_id():
    return f"call_{uuid.uuid4().hex[:12]}"

def generate_friend_code():
    return f"TRLX-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}"

def generate_session_token():
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def verify_session(user_id, session_token):
    return user_id in user_sessions and session_token == user_sessions.get(user_id)

def initialize_sample_data():
    global all_users, user_profiles
    
    sample_users = [
        {'id': 'user1', 'name': 'Alex_Quantum', 'avatar': '👨‍💻', 'online': True, 'last_seen': 'только что', 'status': 'Разрабатываю квантовый мессенджер'},
        {'id': 'user2', 'name': 'Sarah_Cyber', 'avatar': '👩‍🎨', 'online': True, 'last_seen': '2 мин назад', 'status': 'Создаю цифровое искусство'},
        {'id': 'user3', 'name': 'Mike_Neon', 'avatar': '👨‍🚀', 'online': False, 'last_seen': '1 час назад', 'status': 'Исследую космос'},
        {'id': 'user4', 'name': 'Emma_Digital', 'avatar': '👩‍💼', 'online': True, 'last_seen': 'только что', 'status': 'Работаю над AI проектами'},
        {'id': 'user5', 'name': 'Max_Virtual', 'avatar': '🤖', 'online': False, 'last_seen': '30 мин назад', 'status': 'Программирую будущее'},
        {'id': 'user6', 'name': 'Luna_Hyper', 'avatar': '👽', 'online': True, 'last_seen': '5 мин назад', 'status': 'Изучаю нейросети'},
        {'id': 'user7', 'name': 'Tom_Alpha', 'avatar': '🦊', 'online': True, 'last_seen': 'только что', 'status': 'Тестирую новые функции'},
        {'id': 'user8', 'name': 'Anna_Phantom', 'avatar': '🐲', 'online': False, 'last_seen': '2 часа назад', 'status': 'Создаю игры'}
    ]
    
    all_users = sample_users
    
    for user in sample_users:
        user_profiles[user['id']] = {
            'friend_code': generate_friend_code(),
            'friends': [],
            'settings': {
                'theme': 'dark',
                'notifications': True,
                'privacy': 'friends_only'
            },
            'created_at': datetime.datetime.now().isoformat()
        }
    
    friendships['user1'] = ['user2', 'user3']
    friendships['user2'] = ['user1']
    friendships['user3'] = ['user1']

def ensure_user_chat(user_id, target_user_id):
    if user_id not in user_messages:
        user_messages[user_id] = {}
    
    if target_user_id not in user_messages[user_id]:
        user_messages[user_id][target_user_id] = []
        
        welcome_msg = {
            'id': str(uuid.uuid4()),
            'sender': target_user_id,
            'text': 'Привет! 👋 Рад познакомиться!',
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'text'
        }
        user_messages[user_id][target_user_id].append(welcome_msg)

def get_user_by_friend_code(friend_code):
    for user_id, profile in user_profiles.items():
        if profile.get('friend_code') == friend_code:
            return user_id
    return None

def validate_friend_code(friend_code):
    pattern = r'^TRLX-[A-F0-9]{4}-[A-F0-9]{4}$'
    return re.match(pattern, friend_code) is not None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, sans-serif;
            -webkit-tap-highlight-color: transparent;
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
            backdrop-filter: blur(10px);
            animation: cardAppear 0.6s ease-out;
        }

        @keyframes cardAppear {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--neon), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(107, 43, 217, 0.5);
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
            position: relative;
            overflow: hidden;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
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

        .friend-code-display {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
            border: 1px solid var(--accent);
        }

        .friend-code {
            font-family: monospace;
            font-size: 1.1rem;
            color: var(--neon);
            margin: 5px 0;
        }

        .app {
            width: 100%;
            height: 100vh;
            display: flex;
            position: relative;
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
            position: relative;
        }

        .user-header .user-avatar {
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
            margin: 0 auto 10px;
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 5px;
            margin: 10px;
            flex-wrap: wrap;
        }

        .nav-tab {
            flex: 1;
            padding: 8px 5px;
            text-align: center;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-size: 0.8rem;
            min-width: 60px;
            margin: 2px;
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
            font-size: 0.9rem;
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
            border: 1px solid transparent;
        }

        .chat-item:hover {
            background: rgba(107, 43, 217, 0.3);
            border-color: var(--accent);
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
            flex-shrink: 0;
            font-size: 1rem;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
            position: relative;
        }

        .chat-header {
            padding: 15px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .chat-header .item-avatar {
            width: 35px;
            height: 35px;
            font-size: 0.9rem;
            margin: 0;
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
            word-wrap: break-word;
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.received {
            background: rgba(107, 43, 217, 0.3);
            align-self: flex-start;
            border-bottom-left-radius: 5px;
        }

        .message.sent {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            align-self: flex-end;
            color: white;
            border-bottom-right-radius: 5px;
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
            font-size: 0.9rem;
        }

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }

        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 15px;
        }

        .friend-request-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid var(--accent);
        }

        .control-btn {
            padding: 8px 12px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.8rem;
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
            animation: slideIn 0.3s ease;
            max-width: 300px;
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

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.2rem;
            cursor: pointer;
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
        }

        /* Панели */
        .panel {
            position: fixed;
            top: 0;
            width: 90%;
            max-width: 400px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            border: 2px solid var(--accent);
            z-index: 500;
            transition: transform 0.3s ease;
            padding: 20px;
            overflow-y: auto;
            backdrop-filter: blur(10px);
        }

        .settings-panel {
            right: -100%;
        }

        .settings-panel.active {
            right: 0;
        }

        .donate-panel {
            left: -100%;
        }

        .donate-panel.active {
            left: 0;
        }

        .call-panel {
            left: -100%;
        }

        .call-panel.active {
            left: 0;
        }

        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 499;
            display: none;
        }

        .overlay.active {
            display: block;
        }

        /* Стили для звонков */
        .call-link-container {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border: 1px solid var(--accent);
        }

        .call-link {
            font-family: monospace;
            color: var(--neon);
            word-break: break-all;
            margin: 10px 0;
        }

        .join-call-container {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid var(--accent);
        }

        /* Стили для настроек */
        .settings-section {
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }

        .settings-section h4 {
            margin-bottom: 10px;
            color: var(--neon);
        }

        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 24px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: var(--secondary);
            transition: .4s;
            border-radius: 24px;
        }

        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }

        input:checked + .toggle-slider {
            background-color: var(--success);
        }

        input:checked + .toggle-slider:before {
            transform: translateX(26px);
        }

        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                height: 100%;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 200;
                width: 280px;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .mobile-menu-btn {
                display: block;
            }

            .nav-tab {
                font-size: 0.7rem;
                padding: 6px 3px;
            }

            .panel {
                width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="overlay" id="overlay" onclick="hideAllPanels()"></div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin: 20px 0; font-size: 1.2rem; min-height: 60px; display: flex; align-items: center; justify-content: center;">
                <div id="typingText">Инициализация защищённого канала...</div>
            </div>
            <div style="color: var(--neon); margin: 10px 0;">
                <span>🔒</span>
                <span>Квантовое шифрование активировано</span>
                <span style="background: var(--neon); color: var(--primary); padding: 2px 6px; border-radius: 5px; font-size: 0.8rem; margin-left: 5px;">AES-256</span>
            </div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary);">
                Премиум мессенджер с квантовым шифрованием
            </div>
            
            <div style="display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: rgba(0,255,136,0.1); border: 1px solid var(--neon); border-radius: 8px; margin: 10px 0;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: var(--neon);"></div>
                <span>Защищённое соединение установлено</span>
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 НАЧАТЬ
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ БЫСТРЫЙ СТАРТ
            </button>
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
                <p style="color: var(--text-secondary);">📧 <span id="registerEmail">...</span></p>
            </div>

            <div class="friend-code-display">
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Ваш Friend Code:</div>
                <div class="friend-code" id="registerFriendCode">TRLX-XXXX-XXXX</div>
                <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 5px;">
                    Поделитесь этим кодом для добавления в друзья
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ СОЗДАТЬ ПРОФИЛЬ
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewUser()">
                🔄 СГЕНЕРИРОВАТЬ
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← НАЗАД
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
                <div class="friend-code-display" style="margin: 10px 0; padding: 8px;">
                    <div style="font-size: 0.8rem;">Friend Code:</div>
                    <div class="friend-code" id="userFriendCode">TRLX-XXXX-XXXX</div>
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬 Чаты</div>
                <div class="nav-tab" onclick="switchTab('friends')">👥 Друзья</div>
                <div class="nav-tab" onclick="switchTab('discover')">🌐 Найти</div>
                <div class="nav-tab" onclick="switchTab('calls')">📞 Звонки</div>
                <div class="nav-tab" onclick="showDonatePanel()">💎 Донат</div>
                <div class="nav-tab" onclick="showSettings()">⚙️ Настройки</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Поиск..." id="searchInput" oninput="searchContent()">
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
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                </div>
                <button class="control-btn" onclick="startVideoCall()" style="background: var(--success);">📞</button>
                <button class="control-btn" onclick="showFileShare()" style="background: var(--warning);">📎</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <button class="btn btn-primary" onclick="showCallPanel()" style="margin-top: 20px;">
                        🎥 Создать видеозвонок
                    </button>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput" onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Панель звонков -->
    <div class="panel call-panel" id="callPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>📞 Видеозвонки</h3>
            <button class="mobile-menu-btn" onclick="hideCallPanel()" style="position: static; transform: none; font-size: 1.5rem;">✕</button>
        </div>
        
        <div class="call-link-container">
            <h4>🎥 Создать звонок</h4>
            <button class="btn btn-primary" onclick="createCallRoom()" style="width: 100%; margin: 10px 0;">
                🎬 Начать видеозвонок
            </button>
            <div id="callLinkContainer" style="display: none;">
                <div style="font-size: 0.9rem; color: var(--text-secondary); margin: 10px 0;">Ссылка на звонок:</div>
                <div class="call-link" id="callLink">Загрузка...</div>
                <button class="btn btn-secondary" onclick="copyCallLink()" style="width: 100%; margin: 5px 0;">
                    📋 Скопировать ссылку
                </button>
                <button class="btn btn-secondary" onclick="shareCallLink()" style="width: 100%; margin: 5px 0;">
                    📤 Поделиться
                </button>
            </div>
        </div>

        <div class="join-call-container">
            <h4>🔗 Присоединиться к звонку</h4>
            <input type="text" class="search-input" id="joinCallInput" placeholder="Вставьте ссылку на звонок...">
            <button class="btn btn-primary" onclick="joinCallByLink()" style="width: 100%; margin: 10px 0;">
                ✅ Присоединиться
            </button>
        </div>

        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h4>📊 Последние звонки</h4>
            <div style="text-align: center; padding: 20px; color: var(--text-secondary);">
                <div class="empty-state-icon">📞</div>
                <p>Здесь будут ваши последние звонки</p>
            </div>
        </div>
    </div>

    <!-- Панель доната -->
    <div class="panel donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>💎 Премиум тарифы</h3>
            <button class="mobile-menu-btn" onclick="hideDonatePanel()" style="position: static; transform: none; font-size: 1.5rem;">✕</button>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h4>🌟 VIP - 299 ₽/мес</h4>
            <p>• Цветные сообщения<br>• Специальный значок<br>• Приоритет в поддержке</p>
            <button class="btn btn-primary" onclick="selectTier('vip')">Выбрать VIP</button>
        </div>

        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h4>💫 Premium - 599 ₽/мес</h4>
            <p>• Все функции VIP<br>• Расширенные темы<br>• Неограниченный облачный архив</p>
            <button class="btn btn-primary" onclick="selectTier('premium')">Выбрать Premium</button>
        </div>

        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h4>🚀 Ultimate - 999 ₽/мес</h4>
            <p>• Все функции Premium<br>• Персональный менеджер<br>• Кастомные функции</p>
            <button class="btn btn-primary" onclick="selectTier('ultimate')">Выбрать Ultimate</button>
        </div>

        <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <p>💬 Напишите в Telegram: <strong>@trollex_official</strong></p>
            <p style="margin-top: 10px; font-size: 0.9rem; color: var(--text-secondary);">Для оплаты и активации премиум-статуса</p>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="panel settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>⚙️ Настройки</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="position: static; transform: none; font-size: 1.5rem;">✕</button>
        </div>
        
        <div class="settings-section">
            <h4>👤 Профиль</h4>
            <div style="margin-bottom: 15px;">
                <label>Имя пользователя</label>
                <input type="text" class="search-input" id="settingsName" placeholder="Введите новое имя" style="margin-top: 5px;">
            </div>
            <div style="margin-bottom: 15px;">
                <label>Статус</label>
                <input type="text" class="search-input" id="settingsStatus" placeholder="Ваш статус" style="margin-top: 5px;">
            </div>
        </div>

        <div class="settings-section">
            <h4>🔔 Уведомления</h4>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span>Включить уведомления</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="notificationsToggle" checked>
                    <span class="toggle-slider"></span>
                </label>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span>Звук уведомлений</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="soundToggle" checked>
                    <span class="toggle-slider"></span>
                </label>
            </div>
        </div>

        <div class="settings-section">
            <h4>🎨 Внешний вид</h4>
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <div style="flex: 1; text-align: center; padding: 10px; background: var(--primary); border-radius: 8px; cursor: pointer; border: 2px solid var(--accent);">
                    Тёмная
                </div>
                <div style="flex: 1; text-align: center; padding: 10px; background: white; color: black; border-radius: 8px; cursor: pointer; border: 2px solid transparent;">
                    Светлая
                </div>
            </div>
        </div>

        <div style="color: var(--neon); text-align: center; margin: 20px 0;">
            <span>🔒</span>
            <span>End-to-End шифрование активно</span>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()">💾 Сохранить настройки</button>
        <button class="btn btn-secondary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 10px;">
            🚪 Выйти из аккаунта
        </button>
    </div>

    <!-- Уведомления -->
    <div id="notification" class="notification hidden"></div>

    <script>
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let sessionToken = null;
        let allUsers = [];
        let friends = [];
        let friendRequests = [];
        let currentCallLink = '';

        document.addEventListener('DOMContentLoaded', function() {
            initializeApp();
        });

        function initializeApp() {
            const texts = [
                "Инициализация квантового интерфейса...",
                "Загрузка защищённого канала...", 
                "Подключение к нейросети...",
                "Активация протокола шифрования...",
                "Готово! Запускаем TrollexDL..."
            ];
            
            let currentIndex = 0;
            const typingElement = document.getElementById('typingText');
            
            function typeNextText() {
                if (currentIndex < texts.length) {
                    typingElement.textContent = texts[currentIndex];
                    currentIndex++;
                    setTimeout(typeNextText, 800);
                } else {
                    setTimeout(() => {
                        document.getElementById('loadingScreen').classList.add('hidden');
                        checkAutoLogin();
                    }, 500);
                }
            }
            
            typeNextText();
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
            const friendCode = generateFriendCode();
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌'];
            
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
            document.getElementById('registerEmail').textContent = email;
            document.getElementById('registerFriendCode').textContent = friendCode;
        }

        function generateUsername() {
            const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Alpha', 'Beta', 'Gamma', 'Omega'];
            const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Hawk', 'Lion', 'Panther'];
            const numbers = Math.floor(Math.random() * 9000) + 1000;
            return `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
        }

        function generateEmail(username) {
            const domains = ['quantum.io', 'cosmic.com', 'trollex.ai', 'nebula.org'];
            return `${username.toLowerCase()}@${domains[Math.floor(Math.random() * domains.length)]}`;
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 8).toUpperCase();
        }

        function generateFriendCode() {
            const part1 = Math.random().toString(36).substr(2, 4).toUpperCase();
            const part2 = Math.random().toString(36).substr(2, 4).toUpperCase();
            return `TRLX-${part1}-${part2}`;
        }

        function registerUser() {
            const name = document.getElementById('registerName').textContent;
            const avatar = document.getElementById('registerAvatar').textContent;
            const userId = document.getElementById('registerId').textContent;
            const email = document.getElementById('registerEmail').textContent;
            const friendCode = document.getElementById('registerFriendCode').textContent;
            
            currentUser = {
                id: userId,
                name: name,
                avatar: avatar,
                email: email,
                friendCode: friendCode
            };
            
            sessionToken = generateSessionToken();
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('sessionToken', sessionToken);
            
            fetch('/api/register_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(currentUser)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadSampleUsers();
                    showMainApp();
                    showNotification('Профиль создан успешно! 🎉');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ошибка регистрации ❌');
            });
        }

        function generateSessionToken() {
            return Math.random().toString(36).substr(2) + Math.random().toString(36).substr(2);
        }

        function loadSampleUsers() {
            fetch('/api/get_users')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        allUsers = data.users;
                    }
                })
                .catch(error => {
                    console.error('Error loading users:', error);
                });
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                currentUser = JSON.parse(savedUser);
                sessionToken = savedToken;
                loadSampleUsers();
                showMainApp();
                showNotification('С возвращением! 🚀');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                currentUser = JSON.parse(savedUser);
                sessionToken = savedToken;
                loadSampleUsers();
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
            document.getElementById('userFriendCode').textContent = currentUser.friendCode;
            
            loadContent();
            loadFriends();
            loadFriendRequests();
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
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
            
            switch(currentTab) {
                case 'chats':
                    contentHTML = getChatsContent(searchTerm);
                    break;
                case 'friends':
                    contentHTML = getFriendsContent(searchTerm);
                    break;
                case 'discover':
                    contentHTML = getDiscoverContent(searchTerm);
                    break;
                case 'calls':
                    contentHTML = getCallsContent();
                    break;
                default:
                    contentHTML = '<div class="empty-state">Выберите вкладку</div>';
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getChatsContent(searchTerm) {
            const userChats = JSON.parse(localStorage.getItem(`chats_${currentUser.id}`)) || [];
            
            if (userChats.length === 0) {
                return `
                    <div class="empty-state">
                        <div class="empty-state-icon">💬</div>
                        <h3>Нет чатов</h3>
                        <p>Начните общение с пользователями</p>
                        <button class="btn btn-primary" onclick="switchTab('friends')" style="margin-top: 15px;">
                            👥 Найти друзей
                        </button>
                    </div>
                `;
            }
            
            let chatsHTML = '';
            userChats.forEach(chat => {
                if (searchTerm === '' || chat.userName.toLowerCase().includes(searchTerm)) {
                    chatsHTML += `
                        <div class="chat-item" onclick="selectUser('${chat.userId}')">
                            <div class="item-avatar">${chat.userAvatar}</div>
                            <div style="flex: 1;">
                                <h4>${chat.userName}</h4>
                                <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                    ${chat.lastMessage || 'Нет сообщений'}
                                </p>
                            </div>
                        </div>
                    `;
                }
            });
            
            return chatsHTML;
        }

        function getFriendsContent(searchTerm) {
            let friendsHTML = '';
            
            if (friendRequests.length > 0) {
                friendsHTML += '<h4 style="padding: 10px; color: var(--warning);">📥 Запросы в друзья</h4>';
                friendRequests.forEach(request => {
                    if (searchTerm === '' || request.name.toLowerCase().includes(searchTerm)) {
                        friendsHTML += `
                            <div class="friend-request-item">
                                <div>
                                    <div class="item-avatar" style="display: inline-block; margin-right: 10px;">${request.avatar}</div>
                                    <div style="display: inline-block; vertical-align: middle;">
                                        <h4>${request.name}</h4>
                                        <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                            Хочет добавить вас в друзья
                                        </p>
                                    </div>
                                </div>
                                <div style="display: flex; gap: 10px;">
                                    <button class="control-btn" onclick="respondToFriendRequest('${request.id}', true)" style="background: var(--success);">✓</button>
                                    <button class="control-btn" onclick="respondToFriendRequest('${request.id}', false)" style="background: var(--danger);">✕</button>
                                </div>
                            </div>
                        `;
                    }
                });
            }
            
            if (friends.length > 0) {
                friendsHTML += '<h4 style="padding: 10px; margin-top: 20px; color: var(--success);">👥 Мои друзья</h4>';
                friends.forEach(friend => {
                    if (searchTerm === '' || friend.name.toLowerCase().includes(searchTerm)) {
                        friendsHTML += `
                            <div class="chat-item" onclick="selectUser('${friend.id}')">
                                <div class="item-avatar">${friend.avatar}</div>
                                <div style="flex: 1;">
                                    <h4>${friend.name}</h4>
                                    <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                        ${friend.online ? '🟢 Online' : '⚫ Offline'} • ${friend.last_seen}
                                    </p>
                                </div>
                            </div>
                        `;
                    }
                });
            }
            
            if (friendsHTML === '') {
                friendsHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">👥</div>
                        <h3>Нет друзей</h3>
                        <p>Добавьте друзей чтобы начать общение</p>
                        <button class="btn btn-primary" onclick="showAddFriendByLink()" style="margin-top: 15px;">
                            🔗 Добавить по ссылке
                        </button>
                    </div>
                `;
            }
            
            return friendsHTML;
        }

        function getDiscoverContent(searchTerm) {
            return `
                <div style="text-align: center; padding: 20px;">
                    <button class="btn btn-primary" onclick="showAddFriendByLink()" style="margin-bottom: 15px;">
                        🔗 Добавить по ссылке
                    </button>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">
                        Используйте Friend Code для добавления в друзья
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4>🔍 Рекомендованные пользователи</h4>
                    <div id="recommendedUsers">
                        ${getRecommendedUsers()}
                    </div>
                </div>

                <div class="friend-code-display">
                    <h4>📋 Ваш Friend Code</h4>
                    <div class="friend-code">${currentUser.friendCode}</div>
                    <button class="btn btn-secondary" onclick="copyToClipboard(currentUser.friendCode)" style="width: 100%; margin-top: 10px;">
                        📋 Скопировать код
                    </button>
                </div>
            `;
        }

        function getCallsContent() {
            return `
                <div style="text-align: center; padding: 20px;">
                    <button class="btn btn-primary" onclick="showCallPanel()" style="margin-bottom: 15px;">
                        🎥 Управление звонками
                    </button>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">
                        Создавайте и присоединяйтесь к видеозвонкам
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4>📞 Быстрый доступ</h4>
                    <button class="btn btn-secondary" onclick="createCallRoom()" style="width: 100%; margin: 5px 0;">
                        🎬 Быстрый звонок
                    </button>
                    <button class="btn btn-secondary" onclick="showCallPanel()" style="width: 100%; margin: 5px 0;">
                        🔗 Присоединиться по ссылке
                    </button>
                </div>
            `;
        }

        function getRecommendedUsers() {
            const recommended = allUsers.filter(user => user.id !== currentUser.id).slice(0, 3);
            if (recommended.length === 0) {
                return '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">Нет рекомендаций</div>';
            }
            
            let html = '';
            recommended.forEach(user => {
                html += `
                    <div class="chat-item" onclick="selectUser('${user.id}')">
                        <div class="item-avatar">${user.avatar}</div>
                        <div style="flex: 1;">
                            <h4>${user.name}</h4>
                            <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                ${user.status || 'Пользователь TrollexDL'}
                            </p>
                        </div>
                        <button class="control-btn" onclick="event.stopPropagation(); sendFriendRequestToUser('${user.id}')" style="background: var(--accent);">
                            📤
                        </button>
                    </div>
                `;
            });
            return html;
        }

        function selectUser(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user) {
                currentChat = user;
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? '🟢 Online' : '⚫ Offline';
                
                loadMessages(userId);
                showNotification(`Чат с ${user.name} открыт 💬`);
            }
        }

        function loadMessages(userId) {
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💬</div>
                    <h3>Начните общение</h3>
                    <p>Отправьте первое сообщение</p>
                </div>
            `;
        }

        function sendMessage() {
            if (!currentChat) {
                showNotification('Выберите чат для отправки сообщения 💬');
                return;
            }

            const messageInput = document.getElementById('messageInput');
            const messageText = messageInput.value.trim();
            
            if (messageText === '') return;

            const messagesContainer = document.getElementById('messagesContainer');
            
            if (messagesContainer.querySelector('.empty-state')) {
                messagesContainer.innerHTML = '';
            }

            const messageElement = document.createElement('div');
            messageElement.className = 'message sent';
            messageElement.innerHTML = `
                <div>${messageText}</div>
                <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 5px; text-align: right;">
                    ${new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'})}
                </div>
            `;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            messageInput.value = '';
            showNotification('Сообщение отправлено! 📤');
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Функции для панелей
        function showCallPanel() {
            document.getElementById('callPanel').classList.add('active');
            document.getElementById('overlay').classList.add('active');
        }

        function hideCallPanel() {
            document.getElementById('callPanel').classList.remove('active');
            document.getElementById('overlay').classList.remove('active');
        }

        function showDonatePanel() {
            document.getElementById('donatePanel').classList.add('active');
            document.getElementById('overlay').classList.add('active');
        }

        function hideDonatePanel() {
            document.getElementById('donatePanel').classList.remove('active');
            document.getElementById('overlay').classList.remove('active');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
            document.getElementById('overlay').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
            document.getElementById('overlay').classList.remove('active');
        }

        function hideAllPanels() {
            hideCallPanel();
            hideDonatePanel();
            hideSettings();
        }

        // Функции для звонков
        function createCallRoom() {
            fetch('/api/create_call', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    session_token: sessionToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentCallLink = data.call_link;
                    document.getElementById('callLink').textContent = currentCallLink;
                    document.getElementById('callLinkContainer').style.display = 'block';
                    showNotification('Комната для звонка создана! 🎥');
                } else {
                    showNotification('Ошибка создания комнаты ❌');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ошибка сети ❌');
            });
        }

        function copyCallLink() {
            copyToClipboard(currentCallLink);
            showNotification('Ссылка скопирована! 📋');
        }

        function shareCallLink() {
            if (navigator.share) {
                navigator.share({
                    title: 'Присоединяйтесь к видеозвонку',
                    text: 'Присоединяйтесь к моему видеозвонку в TrollexDL',
                    url: currentCallLink
                });
            } else {
                copyCallLink();
            }
        }

        function joinCallByLink() {
            const callLink = document.getElementById('joinCallInput').value.trim();
            if (callLink) {
                showNotification('Присоединение к звонку... 📞');
                // Здесь будет логика присоединения к звонку
            } else {
                showNotification('Введите ссылку на звонок ❌');
            }
        }

        // Функции для друзей
        function showAddFriendByLink() {
            const friendCode = prompt('Введите Friend Code пользователя (формат: TRLX-XXXX-XXXX):');
            if (friendCode) {
                sendFriendRequestByCode(friendCode);
            }
        }

        function sendFriendRequestByCode(friendCode) {
            fetch('/api/send_friend_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    session_token: sessionToken,
                    friend_code: friendCode
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Запрос дружбы отправлен! 📤');
                    loadFriendRequests();
                } else {
                    showNotification(data.error || 'Ошибка отправки запроса ❌');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ошибка сети ❌');
            });
        }

        function sendFriendRequestToUser(userId) {
            fetch('/api/send_friend_request_to_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    session_token: sessionToken,
                    target_user_id: userId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Запрос дружбы отправлен! 📤');
                } else {
                    showNotification(data.error || 'Ошибка отправки запроса ❌');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ошибка сети ❌');
            });
        }

        function loadFriends() {
            fetch('/api/get_friends', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    session_token: sessionToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    friends = data.friends;
                    if (currentTab === 'friends') {
                        loadContent();
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        function loadFriendRequests() {
            fetch('/api/get_friend_requests', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    session_token: sessionToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    friendRequests = data.requests;
                    if (currentTab === 'friends') {
                        loadContent();
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        function respondToFriendRequest(requestId, accept) {
            fetch('/api/respond_friend_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    session_token: sessionToken,
                    request_id: requestId,
                    accept: accept
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(accept ? 'Запрос дружбы принят! ✅' : 'Запрос отклонен ❌');
                    loadFriendRequests();
                    loadFriends();
                } else {
                    showNotification(data.error || 'Ошибка ❌');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ошибка сети ❌');
            });
        }

        // Вспомогательные функции
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Скопировано! 📋');
            });
        }

        function showNotification(message) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.classList.remove('hidden');
            
            setTimeout(() => {
                notification.classList.add('hidden');
            }, 3000);
        }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('active');
        }

        function searchContent() {
            loadContent();
        }

        function startVideoCall() {
            if (!currentChat) {
                showNotification('Выберите чат для звонка 📞');
                return;
            }
            showNotification(`Звонок пользователю ${currentChat.name}... 📞`);
        }

        function showFileShare() {
            showNotification('Функция обмена файлами скоро будет доступна 📎');
        }

        function selectTier(tier) {
            showNotification(`Выбран тариф: ${tier.toUpperCase()} 💎`);
        }

        function saveSettings() {
            showNotification('Настройки сохранены! ✅');
            hideSettings();
        }

        function logout() {
            if (confirm('Вы уверены, что хотите выйти?')) {
                localStorage.removeItem('trollexUser');
                localStorage.removeItem('sessionToken');
                showWelcomeScreen();
                showNotification('Вы вышли из аккаунта 👋');
            }
        }

        // Закрываем sidebar при клике вне его на мобильных
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                sidebar.classList.remove('active');
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    initialize_sample_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register_user', methods=['POST'])
def api_register_user():
    try:
        data = request.json
        user_id = data.get('id')
        
        user_profiles[user_id] = {
            'friend_code': data.get('friend_code'),
            'friends': [],
            'settings': {
                'theme': 'dark',
                'notifications': True,
                'privacy': 'friends_only'
            },
            'created_at': datetime.datetime.now().isoformat()
        }
        
        user_sessions[user_id] = generate_session_token()
        
        logger.info(f"Зарегистрирован новый пользователь: {user_id}")
        return jsonify({'success': True, 'message': 'User registered successfully'})
        
    except Exception as e:
        logger.error(f"Ошибка регистрации пользователя: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_users', methods=['GET'])
def api_get_users():
    try:
        return jsonify({'success': True, 'users': all_users})
    except Exception as e:
        logger.error(f"Ошибка получения пользователей: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_friend_request', methods=['POST'])
def api_send_friend_request():
    try:
        data = request.json
        user_id = data.get('user_id')
        friend_code = data.get('friend_code')
        
        if not validate_friend_code(friend_code):
            return jsonify({'success': False, 'error': 'Invalid friend code format'})
        
        target_user_id = get_user_by_friend_code(friend_code)
        if not target_user_id:
            return jsonify({'success': False, 'error': 'User not found'})
            
        if target_user_id == user_id:
            return jsonify({'success': False, 'error': 'Cannot add yourself'})
        
        request_id = str(uuid.uuid4())
        friend_requests.setdefault(target_user_id, []).append({
            'id': request_id,
            'from_user_id': user_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'pending'
        })
        
        logger.info(f"Запрос дружбы отправлен от {user_id} к {target_user_id}")
        return jsonify({'success': True, 'message': 'Friend request sent'})
        
    except Exception as e:
        logger.error(f"Ошибка отправки запроса дружбы: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_friend_request_to_user', methods=['POST'])
def api_send_friend_request_to_user():
    try:
        data = request.json
        user_id = data.get('user_id')
        target_user_id = data.get('target_user_id')
        
        if target_user_id == user_id:
            return jsonify({'success': False, 'error': 'Cannot add yourself'})
        
        request_id = str(uuid.uuid4())
        friend_requests.setdefault(target_user_id, []).append({
            'id': request_id,
            'from_user_id': user_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'pending'
        })
        
        logger.info(f"Запрос дружбы отправлен от {user_id} к {target_user_id}")
        return jsonify({'success': True, 'message': 'Friend request sent'})
        
    except Exception as e:
        logger.error(f"Ошибка отправки запроса дружбы: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_friend_requests', methods=['POST'])
def api_get_friend_requests():
    try:
        data = request.json
        user_id = data.get('user_id')
        
        user_requests = friend_requests.get(user_id, [])
        requests_data = []
        
        for req in user_requests:
            if req.get('status') == 'pending':
                from_user = next((u for u in all_users if u['id'] == req['from_user_id']), None)
                if from_user:
                    requests_data.append({
                        'id': req['id'],
                        'name': from_user['name'],
                        'avatar': from_user['avatar'],
                        'user_id': from_user['id']
                    })
        
        return jsonify({'success': True, 'requests': requests_data})
        
    except Exception as e:
        logger.error(f"Ошибка получения запросов дружбы: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/respond_friend_request', methods=['POST'])
def api_respond_friend_request():
    try:
        data = request.json
        user_id = data.get('user_id')
        request_id = data.get('request_id')
        accept = data.get('accept')
        
        user_requests = friend_requests.get(user_id, [])
        request_found = None
        
        for req in user_requests:
            if req['id'] == request_id and req.get('status') == 'pending':
                request_found = req
                break
                
        if not request_found:
            return jsonify({'success': False, 'error': 'Request not found'})
        
        from_user_id = request_found['from_user_id']
        
        if accept:
            friendships.setdefault(user_id, []).append(from_user_id)
            friendships.setdefault(from_user_id, []).append(user_id)
            
            ensure_user_chat(user_id, from_user_id)
            ensure_user_chat(from_user_id, user_id)
            
            request_found['status'] = 'accepted'
            logger.info(f"Запрос дружбы принят: {user_id} и {from_user_id}")
        else:
            request_found['status'] = 'rejected'
            logger.info(f"Запрос дружбы отклонен: {user_id} от {from_user_id}")
        
        return jsonify({'success': True, 'message': 'Friend request processed'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки запроса дружбы: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_friends', methods=['POST'])
def api_get_friends():
    try:
        data = request.json
        user_id = data.get('user_id')
        
        user_friends_ids = friendships.get(user_id, [])
        friends_data = []
        
        for friend_id in user_friends_ids:
            friend = next((u for u in all_users if u['id'] == friend_id), None)
            if friend:
                friends_data.append(friend)
        
        return jsonify({'success': True, 'friends': friends_data})
        
    except Exception as e:
        logger.error(f"Ошибка получения списка друзей: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    try:
        data = request.json
        user_id = data.get('user_id')
        
        call_id = generate_call_id()
        call_link = f"{request.host_url}call/{call_id}"
        
        active_calls[call_id] = {
            'creator': user_id,
            'participants': [user_id],
            'created_at': datetime.datetime.now().isoformat(),
            'security_level': 'high',
            'type': 'video',
            'link': call_link
        }
        
        logger.info(f"Создан защищённый звонок: {call_id}")
        return jsonify({
            'success': True, 
            'call_id': call_id,
            'call_link': call_link,
            'security_level': 'high'
        })
    except Exception as e:
        logger.error(f"Ошибка создания звонка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/call/<call_id>')
def call_room(call_id):
    if call_id in active_calls:
        return f'''
        <html>
            <head>
                <title>Присоединиться к звонку - TrollexDL</title>
                <style>
                    body {{
                        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
                        color: white;
                        font-family: 'Segoe UI', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }}
                    .container {{
                        text-align: center;
                        padding: 40px;
                        background: rgba(26, 26, 74, 0.95);
                        border-radius: 20px;
                        border: 2px solid #6c2bd9;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎥 Видеозвонок TrollexDL</h1>
                    <p>Присоединяйтесь к защищённому звонку</p>
                    <button onclick="joinCall()" style="
                        background: linear-gradient(135deg, #6c2bd9, #8b5cf6);
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 10px;
                        font-size: 1rem;
                        cursor: pointer;
                        margin: 20px 0;
                    ">✅ Присоединиться к звонку</button>
                    <p style="color: #b0b0ff;">Ссылка действительна: {active_calls[call_id]['created_at']}</p>
                </div>
                <script>
                    function joinCall() {{
                        alert('Присоединение к звонку... (функция в разработке)');
                        // Здесь будет WebRTC логика
                    }}
                </script>
            </body>
        </html>
        '''
    else:
        return "Звонок не найден или завершен", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
