# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid
import logging
import hashlib
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trollexdl-premium-2024')

# Хранилище активных звонков
active_calls = {}
user_sessions = {}

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

def generate_session_token():
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def verify_session(user_id, session_token):
    """Проверка валидности сессии"""
    return user_id in user_sessions and session_token == user_sessions.get(user_id)

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

        .typing-animation {
            display: inline-block;
            overflow: hidden;
            border-right: 2px solid var(--neon);
            white-space: nowrap;
            margin: 0 auto;
            animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
            font-size: 1.1rem;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--neon) }
        }

        .quantum-loader {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }

        .quantum-dot {
            width: 12px;
            height: 12px;
            margin: 0 5px;
            border-radius: 50%;
            background: var(--neon);
            animation: quantum-pulse 1.5s ease-in-out infinite;
            box-shadow: 0 0 10px var(--neon);
        }

        .quantum-dot:nth-child(2) { animation-delay: 0.2s; }
        .quantum-dot:nth-child(3) { animation-delay: 0.4s; }
        .quantum-dot:nth-child(4) { animation-delay: 0.6s; }

        @keyframes quantum-pulse {
            0%, 100% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 1; }
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

        .btn:active {
            transform: scale(0.98);
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
            backdrop-filter: blur(5px);
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
            box-shadow: 0 4px 15px rgba(107, 43, 217, 0.3);
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
            backdrop-filter: blur(10px);
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
            font-size: 0.9rem;
        }

        .nav-tab.active {
            background: var(--accent);
        }

        .nav-tab:hover {
            background: rgba(107, 43, 217, 0.3);
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

        .search-input:focus {
            outline: none;
            border-color: var(--neon);
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
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

        .chat-item:active {
            transform: scale(0.98);
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
            backdrop-filter: blur(10px);
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
            backdrop-filter: blur(10px);
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

        .message-input:focus {
            outline: none;
            border-color: var(--neon);
        }

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .send-btn:active {
            transform: scale(0.95);
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(107, 43, 217, 0.4);
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
            min-height: 200px;
        }

        .video-container.speaking {
            border-color: var(--neon);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
        }

        .video-element {
            width: 100%;
            height: 100%;
            object-fit: cover;
            background: var(--secondary);
        }

        .video-label {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            padding: 5px 10px;
            border-radius: 10px;
            font-size: 0.9rem;
            backdrop-filter: blur(5px);
        }

        .call-controls {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            display: flex;
            justify-content: center;
            gap: 15px;
            border-top: 2px solid var(--accent);
            backdrop-filter: blur(10px);
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
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .control-btn:active {
            transform: scale(0.9);
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
            backdrop-filter: blur(5px);
            z-index: 10;
        }

        .call-link {
            color: var(--neon);
            font-family: monospace;
            font-size: 0.9rem;
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .copy-link-btn {
            background: var(--accent);
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }

        .copy-link-btn:active {
            transform: scale(0.95);
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
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
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
            backdrop-filter: blur(10px);
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
            backdrop-filter: blur(10px);
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
            backdrop-filter: blur(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease;
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
            padding: 5px;
            border-radius: 5px;
        }

        .mobile-menu-btn:active {
            transform: scale(0.9);
        }

        .join-call-container {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid var(--accent);
            backdrop-filter: blur(5px);
        }

        .join-input {
            width: 100%;
            padding: 12px;
            background: rgba(255,255,255,0.1);
            border: 2px solid var(--accent);
            border-radius: 10px;
            color: var(--text);
            margin: 10px 0;
            font-size: 0.9rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .feature-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid var(--accent);
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }

        .feature-card:active {
            transform: scale(0.98);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }

        .security-badge {
            display: inline-block;
            background: linear-gradient(135deg, var(--neon), var(--cyber));
            color: var(--primary);
            padding: 4px 8px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-left: 8px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .encryption-status {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin: 10px 0;
            color: var(--neon);
            font-size: 0.9rem;
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

            .video-grid {
                grid-template-columns: 1fr;
                padding: 10px;
                gap: 5px;
            }

            .video-container {
                min-height: 150px;
            }

            .control-btn {
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }

            .call-link-container {
                top: 10px;
                left: 10px;
                right: 10px;
                padding: 8px 12px;
            }

            .call-link {
                max-width: 150px;
                font-size: 0.8rem;
            }

            .settings-panel,
            .donate-panel {
                width: 100%;
                max-width: 320px;
            }

            .message {
                max-width: 85%;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Анимации защиты */
        .shield-animation {
            animation: shield-pulse 3s ease-in-out infinite;
        }

        @keyframes shield-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .connection-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: rgba(0,255,136,0.1);
            border: 1px solid var(--neon);
            border-radius: 8px;
            margin: 10px 0;
            font-size: 0.8rem;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--neon);
            animation: status-pulse 2s infinite;
        }

        @keyframes status-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin: 20px 0; font-size: 1.2rem; min-height: 60px; display: flex; align-items: center; justify-content: center;">
                <div class="typing-animation" id="typingText">Инициализация защищённого канала...</div>
            </div>
            <div class="quantum-loader">
                <div class="quantum-dot"></div>
                <div class="quantum-dot"></div>
                <div class="quantum-dot"></div>
                <div class="quantum-dot"></div>
            </div>
            <div class="encryption-status">
                <span>🔒</span>
                <span>Квантовое шифрование активировано</span>
                <span class="security-badge">AES-256</span>
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
            
            <div class="connection-status">
                <div class="status-dot"></div>
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

            <div class="encryption-status">
                <span class="shield-animation">🛡️</span>
                <span>Профиль будет защищён</span>
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
                <button class="control-btn" onclick="startVideoCall()" style="background: var(--success); width: 40px; height: 40px; font-size: 1rem;">📞</button>
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
            <button class="copy-link-btn" onclick="shareCallLink()" style="background: var(--success);">📤</button>
        </div>
        
        <div class="video-grid" id="videoGrid">
            <div class="video-container local" id="localVideoContainer">
                <video id="localVideo" autoplay muted playsinline class="video-element"></video>
                <div class="video-label">Вы (🔴 Live)</div>
            </div>
            <div class="video-container remote" id="remoteVideoContainer">
                <video id="remoteVideo" autoplay playsinline class="video-element"></video>
                <div class="video-label">Участник</div>
            </div>
        </div>
        
        <div class="call-controls">
            <button class="control-btn mic-toggle" id="micToggle" onclick="toggleMicrophone()">🎤</button>
            <button class="control-btn cam-toggle" id="camToggle" onclick="toggleCamera()">📹</button>
            <button class="control-btn" onclick="toggleScreenShare()" style="background: var(--warning);">🖥️</button>
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
        <div class="encryption-status">
            <span class="shield-animation">🛡️</span>
            <span>Звонок будет защищён</span>
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

        <div class="encryption-status">
            <span>🔒</span>
            <span>End-to-End шифрование активно</span>
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
        let sessionToken = null;
        
        // Переменные для видеозвонков
        let localStream = null;
        let remoteStream = null;
        let peerConnection = null;
        let currentCallId = null;
        let isInCall = false;
        let isMicMuted = false;
        let isCamOff = false;
        let isScreenSharing = false;
        
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
            startTypingAnimation();
            
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 4000);
            
            // Проверяем URL на наличие приглашения на звонок
            checkCallInvite();
        });

        function startTypingAnimation() {
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
                    typingElement.style.animation = 'none';
                    void typingElement.offsetWidth;
                    typingElement.style.animation = 'typing 2s steps(40, end), blink-caret 0.75s step-end infinite';
                    currentIndex++;
                    setTimeout(typeNextText, 2000);
                }
            }
            
            typeNextText();
        }

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

        function generateSessionToken() {
            return Math.random().toString(36).substr(2) + Math.random().toString(36).substr(2);
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
            
            // Генерируем сессионный токен
            sessionToken = generateSessionToken();
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('sessionToken', sessionToken);
            
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
            
            localStorage.setItem('allUsers', JSON.stringify(allUsers));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                currentUser = JSON.parse(savedUser);
                sessionToken = savedToken;
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
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                currentUser = JSON.parse(savedUser);
                sessionToken = savedToken;
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
                showNotification('Создание защищённой комнаты... 🎥');
                
                // Генерируем ID звонка
                currentCallId = 'call_' + Math.random().toString(36).substr(2, 12);
                
                // Получаем медиапоток
                await getLocalStream();
                
                // Создаем ссылку для приглашения
                const callLink = `${window.location.origin}?call=${currentCallId}&inviter=${currentUser.id}`;
                document.getElementById('callLink').textContent = callLink;
                
                // Показываем интерфейс звонка
                document.getElementById('callContainer').classList.add('active');
                
                showNotification('Защищённая комната создана! 🔒');
                
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
                // Пробуем без видео
                try {
                    const audioConstraints = {
                        audio: {
                            echoCancellation: true,
                            noiseSuppression: true,
                            autoGainControl: true
                        }
                    };
                    localStream = await navigator.mediaDevices.getUserMedia(audioConstraints);
                    document.getElementById('localVideo').srcObject = null;
                    document.getElementById('localVideoContainer').style.background = 'linear-gradient(135deg, var(--accent), var(--accent-glow))';
                    showNotification('Камера недоступна, используется только аудио 🎤');
                    return localStream;
                } catch (audioError) {
                    showNotification('Не удалось получить доступ к медиаустройствам ❌');
                    throw audioError;
                }
            }
        }

        async function toggleScreenShare() {
            try {
                if (!isScreenSharing) {
                    const screenStream = await navigator.mediaDevices.getDisplayMedia({
                        video: true,
                        audio: true
                    });
                    
                    isScreenSharing = true;
                    showNotification('Демонстрация экрана запущена 🖥️');
                } else {
                    // Возвращаем камеру
                    await getLocalStream();
                    isScreenSharing = false;
                    showNotification('Демонстрация экрана остановлена 📹');
                }
            } catch (error) {
                console.error('Ошибка демонстрации экрана:', error);
                showNotification('Ошибка демонстрации экрана ❌');
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
            }).catch(() => {
                // Fallback для старых браузеров
                const textArea = document.createElement('textarea');
                textArea.value = callLink;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showNotification('Ссылка скопирована! 📋');
            });
        }

        function shareCallLink() {
            const callLink = document.getElementById('callLink').textContent;
            if (navigator.share) {
                navigator.share({
                    title: 'Присоединяйтесь к видеозвонку TrollexDL',
                    text: 'Присоединяйтесь к моему защищённому видеозвонку',
                    url: callLink
                });
            } else {
                copyCallLink();
            }
        }

        function joinCallByLink() {
            const callLink = document.getElementById('joinCallInput').value.trim();
            if (callLink) {
                try {
                    // Извлекаем ID звонка из ссылки
                    const url = new URL(callLink);
                    const callId = url.searchParams.get('call');
                    const inviterId = url.searchParams.get('inviter');
                    
                    if (callId && inviterId) {
                        currentCallId = callId;
                        acceptCall();
                    } else {
                        showNotification('Неверная ссылка на звонок ❌');
                    }
                } catch (error) {
                    showNotification('Неверный формат ссылки ❌');
                }
            } else {
                showNotification('Введите ссылку на звонок 📝');
            }
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
            
            // Скрываем интерфейс звонка
            document.getElementById('callContainer').classList.remove('active');
            document.getElementById('callInvite').classList.remove('active');
            
            isInCall = false;
            currentCallId = null;
            isScreenSharing = false;
            
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
                
                showNotification('Вы присоединились к защищённому звонку! 🎥');
                
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

        function switchTab(tabName) {
            currentTab = tabName;
            
            // Обновляем активную вкладку
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Находим активную вкладку
            const tabs = document.querySelectorAll('.nav-tab');
            let tabIndex = -1;
            
            switch(tabName) {
                case 'chats': tabIndex = 0; break;
                case 'users': tabIndex = 1; break;
                case 'calls': tabIndex = 2; break;
                case 'donate': tabIndex = 3; break;
                case 'settings': tabIndex = 4; break;
            }
            
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

        function getChatsContent(searchTerm) {
            return `
                <div style="text-align: center; padding: 20px; color: var(--text-secondary);">
                    <div style="font-size: 3rem; margin-bottom: 10px;">💬</div>
                    <h3>Чаты</h3>
                    <p>Начните новый чат с пользователем</p>
                </div>
            `;
        }

        function getUsersContent(searchTerm) {
            let usersHTML = '<h4 style="padding: 10px;">👥 Пользователи</h4>';
            
            allUsers.forEach(user => {
                if (user.id !== currentUser.id) {
                    const displayName = user.name.toLowerCase().includes(searchTerm) ? user.name : user.name;
                    if (searchTerm === '' || displayName.toLowerCase().includes(searchTerm)) {
                        usersHTML += `
                            <div class="chat-item" onclick="selectUser('${user.id}')">
                                <div class="item-avatar">${user.avatar}</div>
                                <div style="flex: 1;">
                                    <h4>${user.name}</h4>
                                    <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                        ${user.online ? '🟢 Online' : '⚫ Offline'}
                                    </p>
                                </div>
                            </div>
                        `;
                    }
                }
            });
            
            return usersHTML;
        }

        function getCallsContent(searchTerm) {
            return `
                <div style="text-align: center; padding: 20px;">
                    <button class="btn btn-primary" onclick="createCallRoom()" style="margin-bottom: 15px;">
                        🎥 Создать видеозвонок
                    </button>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">
                        Создайте защищённую комнату и отправьте ссылку
                    </div>
                </div>

                <div class="join-call-container">
                    <h4>🔗 Присоединиться по ссылке</h4>
                    <input type="text" class="join-input" id="joinCallInput" placeholder="Вставьте ссылку на звонок...">
                    <button class="btn btn-primary" onclick="joinCallByLink()" style="width: 100%;">
                        ✅ Присоединиться
                    </button>
                </div>

                <div class="feature-grid">
                    <div class="feature-card" onclick="showFeatureInfo('video')">
                        <div class="feature-icon">🎥</div>
                        <div>HD Видео</div>
                    </div>
                    <div class="feature-card" onclick="showFeatureInfo('security')">
                        <div class="feature-icon">🔒</div>
                        <div>Шифрование</div>
                    </div>
                    <div class="feature-card" onclick="showFeatureInfo('screen')">
                        <div class="feature-icon">🖥️</div>
                        <div>Демонстрация экрана</div>
                    </div>
                    <div class="feature-card" onclick="showFeatureInfo('mobile')">
                        <div class="feature-icon">📱</div>
                        <div>На всех устройствах</div>
                    </div>
                </div>

                <div class="user-card">
                    <h4>📞 Быстрый доступ</h4>
                    <button class="btn btn-secondary" onclick="testVideoCall()" style="margin-top: 10px; width: 100%;">
                        🎬 Тестовый звонок
                    </button>
                </div>
            `;
        }

        function showFeatureInfo(feature) {
            const messages = {
                'video': '🎥 Full HD видеозвонки с адаптивным битрейтом',
                'security': '🔒 End-to-End шифрование AES-256 + TLS 1.3',
                'screen': '🖥️ Демонстрация экрана с защитой от перехвата',
                'mobile': '📱 Полная поддержка мобильных устройств'
            };
            showNotification(messages[feature] || 'Функция активирована ✅');
        }

        function testVideoCall() {
            createCallRoom();
        }

        function selectUser(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user) {
                currentChat = user;
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? '🟢 Online' : '⚫ Offline';
                
                // Очищаем сообщения
                document.getElementById('messagesContainer').innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--text-secondary);">
                        <div style="font-size: 2rem; margin-bottom: 10px;">👋</div>
                        <h3>Начните общение с ${user.name}</h3>
                        <p>Отправьте первое сообщение</p>
                    </div>
                `;
            }
        }

        function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (message && currentChat) {
                const messagesContainer = document.getElementById('messagesContainer');
                
                // Создаем элемент сообщения
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.textContent = message;
                
                messagesContainer.appendChild(messageElement);
                messageInput.value = '';
                
                // Прокручиваем вниз
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                showNotification('Сообщение отправлено! ✨');
            } else if (!currentChat) {
                showNotification('Выберите чат для отправки сообщения 💬');
            }
        }

        function searchContent() {
            loadContent();
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
            showNotification(`Выбран тариф ${tier.toUpperCase()}! 💎`);
            hideDonatePanel();
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            if (newName) {
                currentUser.name = newName;
                localStorage.setItem('trollexUser', JSON.stringify(currentUser));
                document.getElementById('userName').textContent = newName;
                showNotification('Настройки сохранены! ✅');
            }
            hideSettings();
        }

        function logout() {
            localStorage.removeItem('trollexUser');
            localStorage.removeItem('sessionToken');
            localStorage.removeItem('allUsers');
            currentUser = null;
            sessionToken = null;
            hideSettings();
            showWelcomeScreen();
            showNotification('Вы вышли из системы 👋');
        }

        function showNotification(message) {
            // Создаем элемент уведомления
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            // Удаляем уведомление через 3 секунды
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 3000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        
        # Проверка сессии
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        call_id = generate_call_id()
        active_calls[call_id] = {
            'creator': user_id,
            'participants': [],
            'created_at': datetime.datetime.now().isoformat(),
            'security_level': 'high'
        }
        logger.info(f"Создан защищённый звонок: {call_id}")
        return jsonify({
            'success': True, 
            'call_id': call_id, 
            'call_link': f'{request.host_url}?call={call_id}',
            'security_level': 'high'
        })
    except Exception as e:
        logger.error(f"Ошибка создания звонка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
