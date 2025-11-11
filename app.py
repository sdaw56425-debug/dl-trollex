# app.py
from flask import Flask, render_template_string, request, jsonify, session
import datetime
import random
import os
import json
import uuid
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cosmic-secret-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)

# Базы данных в памяти
users_db = {}
chats_db = {}
messages_db = {}
calls_db = {}

class CosmicChat:
    def __init__(self):
        self.online_users = set()
    
    def add_user(self, user_data):
        user_id = str(uuid.uuid4())
        user_data.update({
            'id': user_id,
            'online': True,
            'created_at': datetime.datetime.now().isoformat(),
            'last_seen': datetime.datetime.now().isoformat(),
            'level': random.randint(1, 100),
            'stars': random.randint(100, 5000),
            'avatar': random.choice(['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌', '🌟', '⭐', '☄️', '🌠', '🪐']),
            'theme': 'cosmic'
        })
        users_db[user_id] = user_data
        self.online_users.add(user_id)
        return user_data
    
    def create_chat(self, user1_id, user2_id):
        chat_id = str(uuid.uuid4())
        chat_data = {
            'id': chat_id,
            'participants': [user1_id, user2_id],
            'created_at': datetime.datetime.now().isoformat(),
            'last_activity': datetime.datetime.now().isoformat(),
            'unread_count': {user1_id: 0, user2_id: 0}
        }
        chats_db[chat_id] = chat_data
        return chat_data
    
    def send_message(self, chat_id, user_id, text):
        message_id = str(uuid.uuid4())
        message_data = {
            'id': message_id,
            'chat_id': chat_id,
            'user_id': user_id,
            'text': text,
            'timestamp': datetime.datetime.now().isoformat(),
            'read': False
        }
        messages_db[message_id] = message_data
        
        # Обновляем последнюю активность чата
        if chat_id in chats_db:
            chats_db[chat_id]['last_activity'] = datetime.datetime.now().isoformat()
            # Увеличиваем счетчик непрочитанных для другого пользователя
            for participant in chats_db[chat_id]['participants']:
                if participant != user_id:
                    chats_db[chat_id]['unread_count'][participant] += 1
        
        return message_data

cosmic_chat = CosmicChat()

# Создаем тестовых пользователей при запуске
def initialize_sample_users():
    sample_users = [
        {'name': 'Космонавт_Алекс', 'username': 'cosmo_alex'},
        {'name': 'Звездная_София', 'username': 'star_sofia'},
        {'name': 'Галактический_Макс', 'username': 'galaxy_max'},
        {'name': 'Лунная_Анна', 'username': 'moon_anna'},
        {'name': 'Орбитальный_Даня', 'username': 'orbit_danya'},
        {'name': 'Туманная_Катя', 'username': 'nebula_katya'},
        {'name': 'Комета_Сергей', 'username': 'comet_sergey'},
        {'name': 'Спутник_Оля', 'username': 'satellite_olya'}
    ]
    
    for user_data in sample_users:
        cosmic_chat.add_user(user_data)

initialize_sample_users()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CosmicChat 🚀 Межгалактическое общение</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        :root {
            --cosmic-primary: #0a0a2a;
            --cosmic-secondary: #1a1a4a;
            --cosmic-accent: #4a1a8c;
            --cosmic-glow: #6c2bd9;
            --cosmic-nebula: #8b5cf6;
            --cosmic-star: #fbbf24;
            --cosmic-text: #ffffff;
            --cosmic-text-secondary: #b0b0ff;
        }

        body {
            background: linear-gradient(135deg, var(--cosmic-primary) 0%, var(--cosmic-secondary) 50%, var(--cosmic-accent) 100%);
            color: var(--cosmic-text);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(107, 43, 217, 0.4) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(251, 191, 36, 0.2) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
            animation: cosmicShift 20s ease-in-out infinite;
        }

        @keyframes cosmicShift {
            0%, 100% { opacity: 0.8; }
            50% { opacity: 1; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-10px) rotate(120deg); }
            66% { transform: translateY(-5px) rotate(240deg); }
        }

        @keyframes glowPulse {
            0%, 100% { 
                box-shadow: 0 0 20px var(--cosmic-glow),
                           0 0 40px var(--cosmic-nebula);
            }
            50% { 
                box-shadow: 0 0 30px var(--cosmic-glow),
                           0 0 60px var(--cosmic-nebula),
                           0 0 80px var(--cosmic-star);
            }
        }

        @keyframes starTwinkle {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        .star {
            position: fixed;
            background: white;
            border-radius: 50%;
            animation: starTwinkle 3s infinite;
            z-index: -1;
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
        }

        .hidden {
            display: none !important;
        }

        .cosmic-container {
            background: rgba(26, 26, 74, 0.8);
            backdrop-filter: blur(20px);
            border: 2px solid var(--cosmic-glow);
            border-radius: 25px;
            padding: 40px;
            width: 100%;
            max-width: 450px;
            position: relative;
            overflow: hidden;
            animation: glowPulse 4s infinite;
        }

        .cosmic-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(107, 43, 217, 0.1), transparent);
            animation: shine 6s infinite;
            z-index: -1;
        }

        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }

        .logo {
            font-size: 3rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--cosmic-star), var(--cosmic-nebula), var(--cosmic-glow));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
            animation: float 6s ease-in-out infinite;
        }

        .subtitle {
            text-align: center;
            color: var(--cosmic-text-secondary);
            margin-bottom: 30px;
            font-size: 1.1rem;
            line-height: 1.6;
        }

        .btn {
            width: 100%;
            padding: 18px 25px;
            border: none;
            border-radius: 15px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            margin-bottom: 15px;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 1px;
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

        .btn-primary {
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            color: white;
            box-shadow: 0 10px 30px rgba(107, 43, 217, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(107, 43, 217, 0.6);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--cosmic-text);
            border: 2px solid var(--cosmic-glow);
        }

        .btn-secondary:hover {
            background: rgba(107, 43, 217, 0.2);
            transform: translateY(-2px);
        }

        .user-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px;
            margin: 20px 0;
            border: 1px solid var(--cosmic-glow);
            text-align: center;
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 15px;
            animation: float 4s ease-in-out infinite;
        }

        .app {
            width: 100%;
            height: 100vh;
            background: var(--cosmic-primary);
            display: flex;
        }

        .sidebar {
            width: 350px;
            background: rgba(26, 26, 74, 0.9);
            backdrop-filter: blur(10px);
            border-right: 2px solid var(--cosmic-glow);
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 100;
        }

        .user-header {
            padding: 25px;
            background: linear-gradient(135deg, var(--cosmic-accent), var(--cosmic-glow));
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .user-header::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="white" opacity="0.3"/></svg>');
            animation: starsMove 20s linear infinite;
        }

        @keyframes starsMove {
            from { transform: translateY(0); }
            to { transform: translateY(-100px); }
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 5px;
            margin: 15px;
        }

        .nav-tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }

        .nav-tab.active {
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            color: white;
        }

        .search-box {
            padding: 15px;
        }

        .search-input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--cosmic-glow);
            border-radius: 15px;
            color: var(--cosmic-text);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            box-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
        }

        .search-input::placeholder {
            color: var(--cosmic-text-secondary);
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .chat-item, .user-item {
            display: flex;
            align-items: center;
            padding: 18px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            position: relative;
        }

        .chat-item:hover, .user-item:hover {
            background: rgba(107, 43, 217, 0.2);
            border-color: var(--cosmic-glow);
            transform: translateX(5px);
        }

        .item-avatar {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 1.3rem;
            animation: float 3s ease-in-out infinite;
        }

        .online-dot {
            position: absolute;
            top: 15px;
            right: 15px;
            width: 12px;
            height: 12px;
            background: #00ff00;
            border-radius: 50%;
            box-shadow: 0 0 10px #00ff00;
        }

        .unread-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: var(--cosmic-star);
            color: var(--cosmic-primary);
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--cosmic-primary);
            position: relative;
        }

        .chat-header {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--cosmic-glow);
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="1" fill="white" opacity="0.1"/><circle cx="80" cy="40" r="1" fill="white" opacity="0.1"/><circle cx="40" cy="80" r="1" fill="white" opacity="0.1"/></svg>');
        }

        .message {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
            position: relative;
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.received {
            background: rgba(107, 43, 217, 0.3);
            align-self: flex-start;
            border-bottom-left-radius: 5px;
            border: 1px solid var(--cosmic-glow);
        }

        .message.sent {
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            align-self: flex-end;
            border-bottom-right-radius: 5px;
            color: white;
        }

        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 5px;
            text-align: right;
        }

        .message-input-container {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--cosmic-glow);
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .message-input {
            flex: 1;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--cosmic-glow);
            border-radius: 25px;
            color: var(--cosmic-text);
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .message-input:focus {
            box-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
        }

        .send-btn {
            padding: 15px 25px;
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(107, 43, 217, 0.6);
        }

        .call-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--cosmic-primary), var(--cosmic-accent));
            z-index: 3000;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 40px 20px;
        }

        .call-avatar {
            width: 150px;
            height: 150px;
            border-radius: 30px;
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            margin-bottom: 20px;
            animation: glowPulse 3s infinite;
        }

        .call-controls {
            display: flex;
            gap: 25px;
            margin-bottom: 40px;
        }

        .control-btn {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: none;
            font-size: 1.8rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .control-btn:hover {
            transform: scale(1.1);
        }

        .call-end {
            background: #ff4444;
            color: white;
        }

        .call-accept {
            background: #00ff00;
            color: white;
        }

        .call-mute {
            background: var(--cosmic-secondary);
            color: white;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula));
            color: white;
            padding: 15px 25px;
            border-radius: 15px;
            z-index: 4000;
            animation: slideInRight 0.3s ease, glowPulse 2s infinite;
            box-shadow: 0 10px 30px rgba(107, 43, 217, 0.4);
            border: 1px solid var(--cosmic-glow);
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .settings-panel {
            position: fixed;
            top: 0;
            right: -400px;
            width: 350px;
            height: 100%;
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(20px);
            border-left: 2px solid var(--cosmic-glow);
            z-index: 500;
            transition: right 0.3s ease;
            padding: 30px;
            overflow-y: auto;
        }

        .settings-panel.active {
            right: 0;
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--cosmic-text);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 10px;
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
            
            .cosmic-container {
                padding: 25px;
                margin: 10px;
            }
            
            .call-controls {
                gap: 15px;
            }
            
            .control-btn {
                width: 60px;
                height: 60px;
                font-size: 1.5rem;
            }
        }

        /* Создаем звезды на фоне */
        .stars-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .star {
            position: absolute;
            background: white;
            border-radius: 50%;
            animation: starTwinkle 3s infinite;
        }
    </style>
</head>
<body>
    <!-- Фоновые звезды -->
    <div class="stars-container" id="starsContainer"></div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-container" style="text-align: center;">
            <div class="logo">🌌 CosmicChat</div>
            <div class="subtitle">Запуск межгалактической связи...</div>
            <div style="font-size: 2rem; margin: 20px 0;">🚀</div>
            <div style="color: var(--cosmic-text-secondary);">Инициализация протоколов связи</div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-container">
            <div class="logo">CosmicChat</div>
            <div class="subtitle">
                Межгалактический мессенджер с защищенными звонками<br>
                и космическим дизайном
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🌟 НАЧАТЬ ПУТЕШЕСТВИЕ
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                🚀 БЫСТРЫЙ СТАРТ
            </button>

            <div style="text-align: center; margin-top: 25px; color: var(--cosmic-text-secondary);">
                ⚡ Мгновенные сообщения<br>
                📞 HD звонки<br>
                🌐 Работает везде
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-container">
            <div class="logo">Регистрация</div>
            <div class="subtitle">Создайте свой космический профиль</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">👨‍🚀</div>
                <h3 id="registerName">Космонавт</h3>
                <p style="color: var(--cosmic-text-secondary);">ID: <span id="registerId">...</span></p>
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
                <div class="user-avatar" id="userAvatar">👨‍🚀</div>
                <h3 id="userName">Космонавт</h3>
                <p style="opacity: 0.8;">ID: <span id="userId">...</span></p>
                <div style="margin-top: 10px;">
                    <span style="color: var(--cosmic-star);">⭐</span>
                    <span id="userStars">1000</span> звезд
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('calls')">📞</div>
                <div class="nav-tab" onclick="switchTab('contacts')">👥</div>
                <div class="nav-tab" onclick="showSettings()">⚙️</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Поиск во Вселенной..." id="searchInput" oninput="searchItems()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Динамически заполняется -->
            </div>

            <div style="padding: 20px;">
                <button class="btn btn-secondary" onclick="showLogoutConfirm()" style="background: rgba(255,68,68,0.2); color: #ff4444; border-color: #ff4444;">
                    🚪 Выйти
                </button>
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">CosmicChat</h3>
                    <p style="color: var(--cosmic-text-secondary);" id="currentChatStatus">Выберите чат для общения</p>
                </div>
                <button class="mobile-menu-btn" onclick="showSettings()">⚙️</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 50px 20px; color: var(--cosmic-text-secondary);">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🌌</div>
                    <h3 style="margin-bottom: 15px;">Добро пожаловать в CosmicChat!</h3>
                    <p>Начните общение с другими космическими путешественниками</p>
                    <div style="margin-top: 30px; font-size: 0.9rem; opacity: 0.7;">
                        🔒 Защищенные сообщения<br>
                        📞 Качественные звонки<br>
                        🌐 Доступно везде
                    </div>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите ваше межгалактическое сообщение..." id="messageInput">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="settings-panel" id="settingsPanel">
        <h3 style="margin-bottom: 25px; text-align: center;">⚙️ Настройки</h3>
        
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; color: var(--cosmic-text-secondary);">Тема:</label>
            <select style="width: 100%; padding: 12px; background: rgba(255,255,255,0.1); border: 1px solid var(--cosmic-glow); border-radius: 10px; color: var(--cosmic-text);">
                <option>🌌 Космическая</option>
                <option>🚀 Галактическая</option>
                <option>⭐ Звездная</option>
            </select>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; color: var(--cosmic-text-secondary);">Уведомления:</label>
            <div style="display: flex; gap: 10px;">
                <button class="btn btn-secondary" style="flex: 1;">🔔 Вкл</button>
                <button class="btn btn-secondary" style="flex: 1;">🔕 Выкл</button>
            </div>
        </div>

        <div style="margin-bottom: 30px;">
            <h4 style="margin-bottom: 15px; color: var(--cosmic-text-secondary);">Ваш профиль</h4>
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
                <div>👤 Имя: <span id="settingsUserName">-</span></div>
                <div>🆔 ID: <span id="settingsUserId">-</span></div>
                <div>⭐ Звезд: <span id="settingsUserStars">0</span></div>
                <div>📅 Регистрация: <span id="settingsUserRegDate">-</span></div>
            </div>
        </div>

        <button class="btn btn-primary" onclick="hideSettings()" style="margin-bottom: 15px;">✅ Сохранить</button>
        <button class="btn btn-secondary" onclick="showLogoutConfirm()">🚪 Выйти</button>
    </div>

    <!-- Экран звонка -->
    <div id="callScreen" class="call-screen hidden">
        <div style="text-align: center;">
            <div class="call-avatar" id="callAvatar">👨‍🚀</div>
            <h2 id="callUserName">Космонавт</h2>
            <p id="callStatus" style="color: var(--cosmic-text-secondary); font-size: 1.2rem;">Установка связи...</p>
            <p id="callTimer" style="font-size: 2.5rem; font-weight: bold; margin: 20px 0;">00:00</p>
        </div>
        
        <div class="call-controls">
            <button class="control-btn call-mute" onclick="toggleMute()">🎤</button>
            <button class="control-btn call-end" onclick="endCall()">📞</button>
            <button class="control-btn call-mute" onclick="toggleVideo()">📹</button>
        </div>
    </div>

    <!-- Подтверждение выхода -->
    <div id="logoutConfirm" class="screen hidden" style="background: rgba(10, 10, 42, 0.95); z-index: 4000;">
        <div class="cosmic-container">
            <h3 style="margin-bottom: 20px; text-align: center;">🚪 Подтверждение выхода</h3>
            <p style="text-align: center; margin-bottom: 25px; color: var(--cosmic-text-secondary);">
                Ваш профиль будет сохранен.<br>
                Вернуться можно в любой момент!
            </p>
            <button class="btn btn-primary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: #ff4444; border-color: #ff4444;">
                ✅ Выйти
            </button>
            <button class="btn btn-secondary" onclick="hideLogoutConfirm()">
                ❌ Отмена
            </button>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let callTimer = null;
        let callStartTime = null;
        let messages = {};
        let users = {};

        // Создаем звездное небо
        function createStars() {
            const container = document.getElementById('starsContainer');
            for (let i = 0; i < 150; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.width = Math.random() * 3 + 'px';
                star.style.height = star.style.width;
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 5 + 's';
                star.style.opacity = Math.random() * 0.7 + 0.3;
                container.appendChild(star);
            }
        }

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            createStars();
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 2500);
        });

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function showWelcomeScreen() {
            showScreen('welcomeScreen');
        }

        function showRegisterScreen() {
            showScreen('registerScreen');
            generateNewUser();
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            const targetScreen = document.getElementById(screenId);
            if (targetScreen) {
                targetScreen.classList.remove('hidden');
            }
        }

        function generateNewUser() {
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌', '🌟', '⭐', '☄️', '🌠', '🪐'];
            const names = ['Космонавт', 'Астронавт', 'Галактик', 'Звездный', 'Орбитальный', 'Лунный', 'Марсианский', 'Спутник'];
            const suffixes = ['Искатель', 'Путешественник', 'Первопроходец', 'Исследователь', 'Наблюдатель'];
            
            const avatar = avatars[Math.floor(Math.random() * avatars.length)];
            const name = names[Math.floor(Math.random() * names.length)] + '_' + suffixes[Math.floor(Math.random() * suffixes.length)];
            const userId = 'user_' + Date.now();
            
            document.getElementById('registerAvatar').textContent = avatar;
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
        }

        function registerUser() {
            const name = document.getElementById('registerName').textContent;
            const avatar = document.getElementById('registerAvatar').textContent;
            const userId = document.getElementById('registerId').textContent;
            
            currentUser = {
                id: userId,
                name: name,
                avatar: avatar,
                stars: Math.floor(Math.random() * 5000) + 1000,
                level: Math.floor(Math.random() * 100) + 1,
                online: true,
                created_at: new Date().toISOString()
            };
            
            // Сохраняем в localStorage
            localStorage.setItem('cosmicUser', JSON.stringify(currentUser));
            
            showMainApp();
            showNotification('Космический профиль создан! 🎉', 'success');
        }

        function quickStart() {
            const savedUser = localStorage.getItem('cosmicUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
                showNotification('С возвращением в космос! 🚀', 'success');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('cosmicUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
            } else {
                showWelcomeScreen();
            }
        }

        function showMainApp() {
            showScreen('mainApp');
            
            // Заполняем данные пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            document.getElementById('userStars').textContent = currentUser.stars;
            
            // Настройки
            document.getElementById('settingsUserName').textContent = currentUser.name;
            document.getElementById('settingsUserId').textContent = currentUser.id;
            document.getElementById('settingsUserStars').textContent = currentUser.stars;
            document.getElementById('settingsUserRegDate').textContent = new Date(currentUser.created_at).toLocaleDateString('ru-RU');
            
            loadContent();
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            // Обновляем активные табы
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
            } else if (currentTab === 'calls') {
                contentHTML = getCallsContent(searchTerm);
            } else if (currentTab === 'contacts') {
                contentHTML = getContactsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getChatsContent(searchTerm) {
            const sampleChats = [
                {id: 'chat1', name: 'Космическая_Поддержка', avatar: '🛰️', lastMessage: 'Чем можем помочь?', unread: 2, online: true, type: 'support'},
                {id: 'chat2', name: 'Технический_Отдел', avatar: '🔧', lastMessage: 'Обновление системы', unread: 0, online: true, type: 'tech'},
                {id: 'chat3', name: 'Новости_Галактики', avatar: '📡', lastMessage: 'Новые космические открытия', unread: 5, online: true, type: 'news'}
            ];
            
            const filteredChats = sampleChats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--cosmic-text-secondary);">🌌 Чаты не найдены</div>';
            }
            
            return filteredChats.map(chat => `
                <div class="chat-item" onclick="openChat('${chat.id}')">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 1.1rem;">${chat.name}</div>
                        <div style="color: var(--cosmic-text-secondary); font-size: 0.9rem;">${chat.lastMessage}</div>
                    </div>
                    ${chat.online ? '<div class="online-dot"></div>' : ''}
                    ${chat.unread > 0 ? `<div class="unread-badge">${chat.unread}</div>` : ''}
                </div>
            `).join('');
        }

        function getCallsContent(searchTerm) {
            const sampleUsers = [
                {id: 'user1', name: 'Алексей_Звездный', avatar: '👨‍🚀', online: true, lastCall: '2 мин назад', status: 'available'},
                {id: 'user2', name: 'София_Галактика', avatar: '👩‍🚀', online: true, lastCall: '5 мин назад', status: 'available'},
                {id: 'user3', name: 'Максим_Орбита', avatar: '🧑‍🚀', online: false, lastCall: '1 час назад', status: 'busy'},
                {id: 'user4', name: 'Анна_Лунная', avatar: '👩‍🔬', online: true, lastCall: '10 мин назад', status: 'available'},
                {id: 'user5', name: 'Дмитрий_Марсианский', avatar: '👨‍🔬', online: false, lastCall: '2 часа назад', status: 'offline'}
            ];
            
            const filteredUsers = sampleUsers.filter(user => 
                user.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredUsers.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--cosmic-text-secondary);">🌌 Пользователи не найдены</div>';
            }
            
            return filteredUsers.map(user => `
                <div class="user-item">
                    <div class="item-avatar">${user.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 1.1rem;">${user.name}</div>
                        <div style="color: ${user.online ? '#00ff00' : 'var(--cosmic-text-secondary)'}; font-size: 0.9rem;">
                            ${user.online ? '● онлайн' : '○ офлайн'} • ${user.lastCall}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button onclick="startVoiceCall('${user.id}')" style="background: var(--cosmic-glow); color: white; border: none; border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 0.9rem;">📞</button>
                        <button onclick="startVideoCall('${user.id}')" style="background: var(--cosmic-nebula); color: white; border: none; border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 0.9rem;">📹</button>
                    </div>
                </div>
            `).join('');
        }

        function getContactsContent(searchTerm) {
            const contacts = [
                {name: 'Центр_Управления', avatar: '🛰️', role: 'Главный координатор'},
                {name: 'Тех_Поддержка', avatar: '🔧', role: 'Техническая помощь'},
                {name: 'Безопасность', avatar: '🛡️', role: 'Защита системы'},
                {name: 'Разработчики', avatar: '👨‍💻', role: 'Создатели платформы'}
            ];
            
            const filteredContacts = contacts.filter(contact => 
                contact.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredContacts.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--cosmic-text-secondary);">🌌 Контакты не найдены</div>';
            }
            
            return filteredContacts.map(contact => `
                <div class="chat-item">
                    <div class="item-avatar">${contact.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 1.1rem;">${contact.name}</div>
                        <div style="color: var(--cosmic-text-secondary); font-size: 0.9rem;">${contact.role}</div>
                    </div>
                </div>
            `).join('');
        }

        function searchItems() {
            loadContent();
        }

        function openChat(chatId) {
            const chats = {
                'chat1': {name: 'Космическая_Поддержка', avatar: '🛰️', status: 'онлайн'},
                'chat2': {name: 'Технический_Отдел', avatar: '🔧', status: 'онлайн'},
                'chat3': {name: 'Новости_Галактики', avatar: '📡', status: 'рассылка'}
            };
            
            const chat = chats[chatId];
            if (chat) {
                currentChat = chat;
                
                document.getElementById('currentChatName').textContent = chat.name;
                document.getElementById('currentChatAvatar').textContent = chat.avatar;
                document.getElementById('currentChatStatus').textContent = chat.status;
                
                showChatMessages(chatId);
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const chatMessages = {
                'chat1': [
                    {text: 'Добро пожаловать в космическую поддержку! 👨‍🚀', sender: 'received', time: '12:00', id: '1'},
                    {text: 'Чем можем помочь в вашем межгалактическом путешествии?', sender: 'received', time: '12:01', id: '2'},
                    {text: 'Привет! Как работает система звонков?', sender: 'sent', time: '12:02', id: '3'},
                    {text: 'Система звонков использует квантовое шифрование для максимальной безопасности! 🔒', sender: 'received', time: '12:03', id: '4'}
                ],
                'chat2': [
                    {text: 'Технический отдел на связи! 🔧', sender: 'received', time: '11:30', id: '1'},
                    {text: 'Готовы помочь с любыми техническими вопросами', sender: 'received', time: '11:31', id: '2'}
                ],
                'chat3': [
                    {text: 'Добро пожаловать в новости галактики! 🌌', sender: 'received', time: '10:15', id: '1'},
                    {text: 'Сегодня открыта новая планета в системе Альфа Центавра!', sender: 'received', time: '10:16', id: '2'}
                ]
            };
            
            const messages = chatMessages[chatId] || [];
            messagesContainer.innerHTML = messages.map(msg => `
                <div class="message ${msg.sender}" data-message-id="${msg.id}">
                    ${msg.text}
                    <div class="message-time">${msg.time}</div>
                </div>
            `).join('');
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                const messagesContainer = document.getElementById('messagesContainer');
                const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                const messageId = 'msg_' + Date.now();
                
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.setAttribute('data-message-id', messageId);
                messageElement.innerHTML = `
                    ${message}
                    <div class="message-time">${time}</div>
                `;
                
                messagesContainer.appendChild(messageElement);
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Сохраняем сообщение
                if (!messages[currentChat.name]) {
                    messages[currentChat.name] = [];
                }
                messages[currentChat.name].push({
                    id: messageId,
                    text: message,
                    sender: 'sent',
                    time: time,
                    timestamp: new Date().toISOString()
                });
                
                // Сохраняем в localStorage
                localStorage.setItem('cosmicMessages', JSON.stringify(messages));
                
                showNotification('Сообщение отправлено в космос! ✨', 'success');
                
                // Имитация ответа
                setTimeout(() => {
                    const replyTime = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                    const replyId = 'msg_' + Date.now();
                    
                    const replies = [
                        'Отличное сообщение! 🚀',
                        'Понял вас! Продолжаем...',
                        'Интересно! Расскажите подробнее 🌟',
                        'Спасибо за ваше сообщение! 👨‍🚀'
                    ];
                    
                    const replyElement = document.createElement('div');
                    replyElement.className = 'message received';
                    replyElement.setAttribute('data-message-id', replyId);
                    replyElement.innerHTML = `
                        ${replies[Math.floor(Math.random() * replies.length)]}
                        <div class="message-time">${replyTime}</div>
                    `;
                    
                    messagesContainer.appendChild(replyElement);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    // Сохраняем ответ
                    if (!messages[currentChat.name]) {
                        messages[currentChat.name] = [];
                    }
                    messages[currentChat.name].push({
                        id: replyId,
                        text: replyElement.textContent,
                        sender: 'received',
                        time: replyTime,
                        timestamp: new Date().toISOString()
                    });
                    
                    localStorage.setItem('cosmicMessages', JSON.stringify(messages));
                }, 1000 + Math.random() * 2000);
            }
        }

        function startVoiceCall(userId) {
            const users = {
                'user1': {name: 'Алексей_Звездный', avatar: '👨‍🚀'},
                'user2': {name: 'София_Галактика', avatar: '👩‍🚀'},
                'user3': {name: 'Максим_Орбита', avatar: '🧑‍🚀'},
                'user4': {name: 'Анна_Лунная', avatar: '👩‍🔬'},
                'user5': {name: 'Дмитрий_Марсианский', avatar: '👨‍🔬'}
            };
            
            const user = users[userId];
            if (user) {
                showCallScreen(user, 'voice');
            }
        }

        function startVideoCall(userId) {
            const users = {
                'user1': {name: 'Алексей_Звездный', avatar: '👨‍🚀'},
                'user2': {name: 'София_Галактика', avatar: '👩‍🚀'},
                'user3': {name: 'Максим_Орбита', avatar: '🧑‍🚀'},
                'user4': {name: 'Анна_Лунная', avatar: '👩‍🔬'},
                'user5': {name: 'Дмитрий_Марсианский', avatar: '👨‍🔬'}
            };
            
            const user = users[userId];
            if (user) {
                showCallScreen(user, 'video');
            }
        }

        function showCallScreen(user, type) {
            document.getElementById('callScreen').style.display = 'flex';
            document.getElementById('callAvatar').textContent = user.avatar;
            document.getElementById('callUserName').textContent = user.name;
            document.getElementById('callStatus').textContent = type === 'voice' ? 'Голосовой звонок...' : 'Видеозвонок...';
            
            startCallTimer();
            showNotification(`Установка связи с ${user.name}...`, 'info');
        }

        function startCallTimer() {
            callStartTime = new Date();
            callTimer = setInterval(() => {
                const now = new Date();
                const diff = Math.floor((now - callStartTime) / 1000);
                const minutes = Math.floor(diff / 60);
                const seconds = diff % 60;
                document.getElementById('callTimer').textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }, 1000);
        }

        function endCall() {
            if (callTimer) {
                clearInterval(callTimer);
            }
            document.getElementById('callScreen').style.display = 'none';
            showNotification('Космическая связь завершена 📞', 'info');
        }

        function toggleMute() {
            showNotification('Микрофон переключен 🎤', 'info');
        }

        function toggleVideo() {
            showNotification('Камера переключена 📹', 'info');
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
            showNotification('Настройки сохранены! ✅', 'success');
        }

        function showLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.remove('hidden');
        }

        function hideLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.add('hidden');
        }

        function logout() {
            localStorage.removeItem('cosmicUser');
            showWelcomeScreen();
            showNotification('До новых космических встреч! 👋', 'info');
        }

        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            
            if (type === 'error') {
                notification.style.background = 'linear-gradient(135deg, #ff4444, #cc0000)';
            } else if (type === 'info') {
                notification.style.background = 'linear-gradient(135deg, var(--cosmic-glow), var(--cosmic-nebula))';
            }
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 4000);
        }

        // Загрузка сохраненных сообщений
        function loadSavedMessages() {
            const savedMessages = localStorage.getItem('cosmicMessages');
            if (savedMessages) {
                messages = JSON.parse(savedMessages);
            }
        }

        // Обработка Enter для отправки сообщений
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Закрытие сайдбара при клике вне его на мобильных
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                sidebar.classList.remove('active');
            }
            
            // Закрытие настроек при клике вне
            const settingsPanel = document.getElementById('settingsPanel');
            if (settingsPanel.classList.contains('active') && 
                !settingsPanel.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                settingsPanel.classList.remove('active');
            }
        });

        // Загружаем сохраненные сообщения при старте
        loadSavedMessages();
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
    message_id = str(uuid.uuid4())
    
    message_data = {
        'id': message_id,
        'chat_id': data.get('chat_id'),
        'user_id': data.get('user_id'),
        'text': data.get('text'),
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    messages_db[message_id] = message_data
    return jsonify({'success': True, 'message': message_data})

@app.route('/api/get_messages/<chat_id>')
def api_get_messages(chat_id):
    chat_messages = [msg for msg in messages_db.values() if msg.get('chat_id') == chat_id]
    return jsonify({'messages': chat_messages})

@app.route('/api/get_users')
def api_get_users():
    return jsonify({'users': list(users_db.values())})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'cosmic_online',
        'users_online': len([u for u in users_db.values() if u.get('online')]),
        'total_messages': len(messages_db),
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 CosmicChat запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
