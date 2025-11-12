# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trollexdl-premium-2024')

# Хранилище активных звонков
active_calls = {}

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

def generate_call_id():
    return f"call_{uuid.uuid4().hex[:12]}"

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

        /* Стили для видеозвонков */
        .call-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--primary);
            z-index: 2000;
            display: none;
            flex-direction: column;
        }

        .call-container.active {
            display: flex;
        }

        .video-grid {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 10px;
            padding: 20px;
        }

        .video-container {
            position: relative;
            background: var(--secondary);
            border-radius: 15px;
            overflow: hidden;
            border: 2px solid var(--accent);
        }

        .video-container.remote {
            border-color: var(--neon);
        }

        .video-container.local {
            border-color: var(--accent);
        }

        .video-element {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .video-label {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            padding: 5px 10px;
            border-radius: 10px;
            font-size: 0.9rem;
        }

        .call-controls {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            display: flex;
            justify-content: center;
            gap: 15px;
            border-top: 2px solid var(--accent);
        }

        .control-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .control-btn.call-end {
            background: var(--danger);
            color: white;
        }

        .control-btn.mic-toggle {
            background: var(--success);
            color: white;
        }

        .control-btn.mic-toggle.muted {
            background: var(--danger);
        }

        .control-btn.cam-toggle {
            background: var(--accent);
            color: white;
        }

        .control-btn.cam-toggle.off {
            background: var(--warning);
        }

        .call-link-container {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 15px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .call-link {
            color: var(--neon);
            font-family: monospace;
            font-size: 0.9rem;
        }

        .copy-link-btn {
            background: var(--accent);
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .call-invite {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(26, 26, 74, 0.95);
            border: 2px solid var(--accent);
            border-radius: 20px;
            padding: 30px;
            z-index: 3000;
            text-align: center;
            display: none;
        }

        .call-invite.active {
            display: block;
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

            .video-grid {
                grid-template-columns: 1fr;
                padding: 10px;
            }

            .control-btn {
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }

            .call-link-container {
                top: 10px;
                left: 10px;
                padding: 8px 12px;
            }
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin: 20px 0; font-size: 1.2rem;">Установка квантовой связи...</div>
            <div style="font-size: 2rem;">🌌</div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary);">
                Мессенджер с квантовым шифрованием и видеозвонками
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
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('users')">👥</div>
                <div class="nav-tab" onclick="switchTab('calls')">📞</div>
                <div class="nav-tab" onclick="showDonatePanel()">💎</div>
                <div class="nav-tab" onclick="showSettings()">⚙️</div>
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
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 40px 20px; color: var(--text-secondary);">
                    <div style="font-size: 3rem; margin-bottom: 15px;">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <button class="btn btn-primary" onclick="createCallRoom()" style="margin-top: 20px;">
                        🎥 Создать видеозвонок
                    </button>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Контейнер видеозвонка -->
    <div id="callContainer" class="call-container">
        <div class="call-link-container">
            <span class="call-link" id="callLink">Загрузка...</span>
            <button class="copy-link-btn" onclick="copyCallLink()">📋</button>
        </div>
        
        <div class="video-grid" id="videoGrid">
            <div class="video-container local">
                <video id="localVideo" autoplay muted class="video-element"></video>
                <div class="video-label">Вы (🔴 Live)</div>
            </div>
            <div class="video-container remote">
                <video id="remoteVideo" autoplay class="video-element"></video>
                <div class="video-label">Участник</div>
            </div>
        </div>
        
        <div class="call-controls">
            <button class="control-btn mic-toggle" id="micToggle" onclick="toggleMicrophone()">🎤</button>
            <button class="control-btn cam-toggle" id="camToggle" onclick="toggleCamera()">📹</button>
            <button class="control-btn call-end" onclick="endCall()">📞</button>
        </div>
    </div>

    <!-- Приглашение на звонок -->
    <div id="callInvite" class="call-invite">
        <div class="logo">📞 Входящий вызов</div>
        <div class="user-card">
            <div class="user-avatar" id="callerAvatar">👤</div>
            <h3 id="callerName">Unknown</h3>
            <p style="color: var(--text-secondary);">приглашает вас на видеозвонок</p>
        </div>
        <button class="btn btn-primary" onclick="acceptCall()">✅ Принять</button>
        <button class="btn btn-secondary" onclick="declineCall()">❌ Отклонить</button>
    </div>

    <!-- Панель доната -->
    <div class="donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>💎 Премиум тарифы</h3>
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
            <h3>⚙️ Настройки</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div style="margin-bottom: 15px;">
            <label>👤 Имя пользователя</label>
            <input type="text" class="search-input" id="settingsName" placeholder="Введите новое имя" style="margin-top: 5px;">
        </div>

        <div style="margin-bottom: 15px;">
            <label>🎥 Камера по умолчанию</label>
            <select class="search-input" id="cameraSelect" style="margin-top: 5px;">
                <option value="">Автовыбор</option>
            </select>
        </div>

        <div style="margin-bottom: 15px;">
            <label>🎤 Микрофон по умолчанию</label>
            <select class="search-input" id="microphoneSelect" style="margin-top: 5px;">
                <option value="">Автовыбор</option>
            </select>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()">💾 Сохранить</button>
        <button class="btn btn-secondary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 10px;">
            🚪 Выйти
        </button>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let messages = {};
        let allUsers = [];
        
        // Переменные для видеозвонков
        let localStream = null;
        let remoteStream = null;
        let peerConnection = null;
        let currentCallId = null;
        let isInCall = false;
        let isMicMuted = false;
        let isCamOff = false;
        
        // STUN/TURN серверы для обхода блокировок
        const iceServers = [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' },
            { urls: 'stun:stun2.l.google.com:19302' },
            { urls: 'stun:stun3.l.google.com:19302' },
            { urls: 'stun:stun4.l.google.com:19302' },
            // Резервные TURN серверы
            {
                urls: 'turn:turn.anyfirewall.com:443?transport=tcp',
                username: 'webrtc',
                credential: 'webrtc'
            },
            {
                urls: 'turn:numb.viagenie.ca',
                username: 'webrtc@live.com',
                credential: 'muazkh'
            }
        ];

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 2000);
            
            // Проверяем URL на наличие приглашения на звонок
            checkCallInvite();
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
            showNotification('Профиль создан успешно! 🎉');
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
                showNotification('С возвращением! 🚀');
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
            loadMediaDevices();
        }

        // Функции для видеозвонков
        async function createCallRoom() {
            try {
                showNotification('Создание комнаты для звонка... 🎥');
                
                // Генерируем ID звонка
                currentCallId = 'call_' + Math.random().toString(36).substr(2, 12);
                
                // Получаем медиапоток
                await getLocalStream();
                
                // Создаем ссылку для приглашения
                const callLink = `${window.location.origin}?call=${currentCallId}&inviter=${currentUser.id}`;
                document.getElementById('callLink').textContent = callLink;
                
                // Показываем интерфейс звонка
                document.getElementById('callContainer').classList.add('active');
                
                showNotification('Комната создана! Отправьте ссылку участникам 🔗');
                
            } catch (error) {
                console.error('Ошибка создания комнаты:', error);
                showNotification('Ошибка доступа к камере/микрофону ❌');
            }
        }

        async function getLocalStream() {
            try {
                const constraints = {
                    video: {
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        frameRate: { ideal: 30 }
                    },
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true
                    }
                };
                
                localStream = await navigator.mediaDevices.getUserMedia(constraints);
                document.getElementById('localVideo').srcObject = localStream;
                
                return localStream;
            } catch (error) {
                console.error('Ошибка доступа к медиаустройствам:', error);
                throw error;
            }
        }

        function toggleMicrophone() {
            if (localStream) {
                const audioTracks = localStream.getAudioTracks();
                if (audioTracks.length > 0) {
                    isMicMuted = !isMicMuted;
                    audioTracks[0].enabled = !isMicMuted;
                    
                    const micBtn = document.getElementById('micToggle');
                    micBtn.textContent = isMicMuted ? '🎤❌' : '🎤';
                    micBtn.classList.toggle('muted', isMicMuted);
                    
                    showNotification(isMicMuted ? 'Микрофон выключен 🔇' : 'Микрофон включен 🔊');
                }
            }
        }

        function toggleCamera() {
            if (localStream) {
                const videoTracks = localStream.getVideoTracks();
                if (videoTracks.length > 0) {
                    isCamOff = !isCamOff;
                    videoTracks[0].enabled = !isCamOff;
                    
                    const camBtn = document.getElementById('camToggle');
                    camBtn.textContent = isCamOff ? '📹❌' : '📹';
                    camBtn.classList.toggle('off', isCamOff);
                    
                    showNotification(isCamOff ? 'Камера выключена 📷' : 'Камера включена 📹');
                }
            }
        }

        function copyCallLink() {
            const callLink = document.getElementById('callLink').textContent;
            navigator.clipboard.writeText(callLink).then(() => {
                showNotification('Ссылка скопирована в буфер! 📋');
            });
        }

        function endCall() {
            // Останавливаем все медиапотоки
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
                localStream = null;
            }
            
            if (remoteStream) {
                remoteStream.getTracks().forEach(track => track.stop());
                remoteStream = null;
            }
            
            // Закрываем соединение
            if (peerConnection) {
                peerConnection.close();
                peerConnection = null;
            }
            
            // Скрываем интерфейс звонка
            document.getElementById('callContainer').classList.remove('active');
            document.getElementById('callInvite').classList.remove('active');
            
            isInCall = false;
            currentCallId = null;
            
            showNotification('Звонок завершен 📞');
        }

        function checkCallInvite() {
            const urlParams = new URLSearchParams(window.location.search);
            const callId = urlParams.get('call');
            const inviterId = urlParams.get('inviter');
            
            if (callId && inviterId) {
                // Находим информацию о звонящем
                const inviter = allUsers.find(user => user.id === inviterId) || 
                               { name: 'Unknown User', avatar: '👤' };
                
                document.getElementById('callerName').textContent = inviter.name;
                document.getElementById('callerAvatar').textContent = inviter.avatar;
                
                currentCallId = callId;
                document.getElementById('callInvite').classList.add('active');
            }
        }

        async function acceptCall() {
            try {
                document.getElementById('callInvite').classList.remove('active');
                
                // Получаем медиапоток
                await getLocalStream();
                
                // Показываем интерфейс звонка
                document.getElementById('callContainer').classList.add('active');
                document.getElementById('callLink').textContent = 'Присоединились к звонку';
                
                showNotification('Вы присоединились к звонку! 🎥');
                
                // Здесь должна быть логика подключения через WebRTC
                // Для демо просто показываем интерфейс
                
            } catch (error) {
                console.error('Ошибка подключения к звонку:', error);
                showNotification('Ошибка подключения к звонку ❌');
            }
        }

        function declineCall() {
            document.getElementById('callInvite').classList.remove('active');
            currentCallId = null;
            showNotification('Вы отклонили вызов 📞');
        }

        async function loadMediaDevices() {
            try {
                const devices = await navigator.mediaDevices.enumerateDevices();
                const cameraSelect = document.getElementById('cameraSelect');
                const microphoneSelect = document.getElementById('microphoneSelect');
                
                cameraSelect.innerHTML = '<option value="">Автовыбор</option>';
                microphoneSelect.innerHTML = '<option value="">Автовыбор</option>';
                
                devices.forEach(device => {
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.textContent = device.label || `${device.kind} ${device.deviceId.slice(0, 5)}`;
                    
                    if (device.kind === 'videoinput') {
                        cameraSelect.appendChild(option);
                    } else if (device.kind === 'audioinput') {
                        microphoneSelect.appendChild(option);
                    }
                });
            } catch (error) {
                console.error('Ошибка загрузки медиаустройств:', error);
            }
        }

        function startVideoCall() {
            if (currentChat) {
                createCallRoom();
            } else {
                showNotification('Выберите чат для начала звонка 💬');
            }
        }

        // Остальные функции (switchTab, loadContent, и т.д.) остаются без изменений
        function switchTab(tabName) {
            currentTab = tabName;
            
            // Обновляем активную вкладку
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Находим активную вкладку по индексу
            const tabs = document.querySelectorAll('.nav-tab');
            const tabIndex = ['chats', 'users', 'calls', 'donate', 'settings'].indexOf(tabName);
            if (tabIndex !== -1 && tabs[tabIndex]) {
                tabs[tabIndex].classList.add('active');
            }
            
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
            } else if (currentTab === 'calls') {
                contentHTML = getCallsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getCallsContent(searchTerm) {
            return `
                <div style="text-align: center; padding: 20px;">
                    <button class="btn btn-primary" onclick="createCallRoom()" style="margin-bottom: 15px;">
                        🎥 Создать видеозвонок
                    </button>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">
                        Создайте комнату и отправьте ссылку друзьям
                    </div>
                </div>
                <div class="user-card">
                    <h4>📞 Быстрый доступ</h4>
                    <button class="btn btn-secondary" onclick="testVideoCall()" style="margin-top: 10px;">
                        Тестовый звонок
                    </button>
                </div>
            `;
        }

        function testVideoCall() {
            createCallRoom();
        }

        // Остальные функции остаются без изменений...
        function searchContent() {
            loadContent();
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 'support', name: 'Поддержка TrollexDL', avatar: '🛰️', lastMessage: 'Чем можем помочь?'},
                {id: 'community', name: 'Общий чат', avatar: '👥', lastMessage: 'Добро пожаловать!'}
            ];
            
            const filteredChats = chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">Чаты не найдены</div>';
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
                return '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">Пользователи не найдены</div>';
            }
            
            return filteredUsers.map(user => `
                <div class="chat-item" onclick="startChatWithUser('${user.id}')">
                    <div class="item-avatar">${user.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${user.name}</div>
                        <div style="color: ${user.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.9rem;">
                            ${user.online ? 'В сети' : 'Не в сети'}
                        </div>
                    </div>
                    <button class="control-btn" onclick="event.stopPropagation(); inviteToCall('${user.id}')" style="background: var(--success); font-size: 0.8rem; width: 30px; height: 30px;">📞</button>
                </div>
            `).join('');
        }

        function inviteToCall(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user) {
                createCallRoom();
                showNotification(`Приглашение отправлено ${user.name} 📞`);
            }
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Поддержка TrollexDL', avatar: '🛰️', status: 'Онлайн', type: 'support'},
                'community': {name: 'Общий чат', avatar: '👥', status: '12 онлайн', type: 'community'}
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
                    status: user.online ? 'В сети' : 'Не в сети',
                    type: 'user'
                };
                
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? 'В сети' : 'Не в сети';
                
                showChatMessages(currentChat.id);
                showNotification(`Начат чат с ${user.name} 💬`);
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const defaultMessages = {
                'support': [
                    {text: 'Добро пожаловать в поддержку TrollexDL! 🚀', sender: 'received', time: '12:00'},
                    {text: 'Чем можем вам помочь?', sender: 'received', time: '12:01'}
                ],
                'community': [
                    {text: 'Добро пожаловать в общий чат! 👋', sender: 'received', time: '10:00'},
                    {text: 'Привет всем! 🎉', sender: 'received', time: '10:05'},
                    {text: 'Этот мессенджер потрясающий! ⚡', sender: 'received', time: '10:10'}
                ]
            };
            
            const chatMessages = messages[chatId] || defaultMessages[chatId] || [];
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = `
                    <div style="text-align: center; padding: 40px 20px; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 15px;">💬</div>
                        <h3>${currentChat.name}</h3>
                        <p>Начните общение</p>
                        <button class="btn btn-primary" onclick="createCallRoom()" style="margin-top: 20px;">
                            🎥 Начать видеозвонок
                        </button>
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
                
                showNotification('Сообщение отправлено! ✨');
            }
        }

        function simulateReply() {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            
            const replies = {
                'support': [
                    'Спасибо за ваше сообщение! Чем можем помочь? 🚀',
                    'Мы ценим ваш отзыв!'
                ],
                'user': [
                    'Привет! Спасибо что написали! 👋',
                    'Звучит интересно!'
                ],
                'community': [
                    'Отличное сообщение! 👍',
                    'Спасибо что поделились! 💫'
                ]
            };
            
            const chatReplies = replies[currentChat.type] || ['Спасибо за ваше сообщение!'];
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
            showNotification(`Выбран тариф ${tier.toUpperCase()}! Свяжитесь с @trollex_official 💎`);
            hideDonatePanel();
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            if (newName) {
                currentUser.name = newName;
                document.getElementById('userName').textContent = newName;
                localStorage.setItem('trollexUser', JSON.stringify(currentUser));
                showNotification('Имя обновлено! ✅');
            }
            hideSettings();
        }

        function logout() {
            // Завершаем звонок если активен
            if (isInCall) {
                endCall();
            }
            
            localStorage.removeItem('trollexUser');
            showWelcomeScreen();
            showNotification('До скорой встречи! 👋');
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

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    data = request.json
    call_id = generate_call_id()
    active_calls[call_id] = {
        'creator': data.get('user_id'),
        'participants': [],
        'created_at': datetime.datetime.now().isoformat()
    }
    return jsonify({'success': True, 'call_id': call_id, 'call_link': f'{request.host_url}?call={call_id}'})

@app.route('/api/join_call', methods=['POST'])
def api_join_call():
    data = request.json
    call_id = data.get('call_id')
    
    if call_id in active_calls:
        active_calls[call_id]['participants'].append(data.get('user_id'))
        return jsonify({'success': True, 'call_data': active_calls[call_id]})
    else:
        return jsonify({'success': False, 'error': 'Call not found'}), 404

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    data = request.json
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running', 
        'service': 'TrollexDL',
        'active_calls': len(active_calls),
        'days_until_new_year': get_days_until_new_year()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
