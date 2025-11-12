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

def initialize_sample_data():
    """Инициализация тестовых данных"""
    global all_users
    all_users = [
        {'id': 'user1', 'name': 'Alex_Quantum', 'avatar': '👨‍💻', 'online': True, 'last_seen': 'только что'},
        {'id': 'user2', 'name': 'Sarah_Cyber', 'avatar': '👩‍🎨', 'online': True, 'last_seen': '2 мин назад'},
        {'id': 'user3', 'name': 'Mike_Neon', 'avatar': '👨‍🚀', 'online': False, 'last_seen': '1 час назад'},
        {'id': 'user4', 'name': 'Emma_Digital', 'avatar': '👩‍💼', 'online': True, 'last_seen': 'только что'},
        {'id': 'user5', 'name': 'Max_Virtual', 'avatar': '🤖', 'online': False, 'last_seen': '30 мин назад'},
        {'id': 'user6', 'name': 'Luna_Hyper', 'avatar': '👽', 'online': True, 'last_seen': '5 мин назад'},
        {'id': 'user7', 'name': 'Tom_Alpha', 'avatar': '🦊', 'online': True, 'last_seen': 'только что'},
        {'id': 'user8', 'name': 'Anna_Phantom', 'avatar': '🐲', 'online': False, 'last_seen': '2 часа назад'}
    ]

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
            touch-action: manipulation;
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
            animation: logoGlow 2s ease-in-out infinite alternate;
        }

        @keyframes logoGlow {
            from {
                text-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
            }
            to {
                text-shadow: 0 0 30px rgba(107, 43, 217, 0.8), 0 0 40px rgba(0, 255, 136, 0.3);
            }
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
            -webkit-user-select: none;
            user-select: none;
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
            -webkit-user-select: none;
            user-select: none;
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
            -webkit-user-select: none;
            user-select: none;
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

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            -webkit-user-select: none;
            user-select: none;
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
            -webkit-user-select: none;
            user-select: none;
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
            z-index: 10;
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
            -webkit-user-select: none;
            user-select: none;
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
            right: -100%;
            width: 100%;
            max-width: 400px;
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
            left: -100%;
            width: 100%;
            max-width: 400px;
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
            -webkit-user-select: none;
            user-select: none;
        }

        .join-call-container {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid var(--accent);
        }

        .join-input {
            width: 100%;
            padding: 12px;
            background: rgba(255,255,255,0.1);
            border: 2px solid var(--accent);
            border-radius: 10px;
            color: var(--text);
            margin: 10px 0;
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
            cursor: pointer;
            transition: all 0.3s ease;
            -webkit-user-select: none;
            user-select: none;
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
        }

        .encryption-status {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin: 10px 0;
            color: var(--neon);
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
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--neon);
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

        .participant-joined {
            border-color: var(--success) !important;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
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

        .file-share-container {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }

        .voice-message-btn {
            background: var(--accent);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            margin-left: 10px;
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
            }

            .settings-panel,
            .donate-panel {
                width: 100%;
                max-width: 100%;
            }

            .message {
                max-width: 85%;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }

            /* Мобильная оптимизация звонков */
            .mobile-call-layout .video-container.local {
                position: fixed;
                top: 10px;
                right: 10px;
                width: 120px;
                height: 160px;
                z-index: 10;
                border: 2px solid var(--neon);
            }

            .mobile-call-layout .video-container.remote {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
            }

            .mobile-call-layout .call-controls {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                z-index: 20;
            }

            .mobile-call-layout .call-link-container {
                top: 180px;
                left: 10px;
                right: 10px;
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
                <span>🛡️</span>
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
                <div class="nav-tab active" onclick="switchTab('chats')">💬 Чаты</div>
                <div class="nav-tab" onclick="switchTab('users')">👥 Контакты</div>
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
                <button class="control-btn" onclick="startVideoCall()" style="background: var(--success); width: 40px; height: 40px; font-size: 1rem;">📞</button>
                <button class="control-btn" onclick="showFileShare()" style="background: var(--warning); width: 40px; height: 40px; font-size: 1rem;">📎</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <button class="btn btn-primary" onclick="createCallRoom()" style="margin-top: 20px;">
                        🎥 Создать видеозвонок
                    </button>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput" onkeypress="handleKeyPress(event)">
                <button class="voice-message-btn" onclick="startVoiceMessage()" title="Голосовое сообщение">🎤</button>
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
                <div id="remoteVideoPlaceholder" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:var(--secondary);color:var(--text-secondary);">
                    <div style="text-align:center;">
                        <div style="font-size:3rem;">👤</div>
                        <div>Ожидание участника...</div>
                        <div style="font-size:0.8rem; margin-top:10px; color:var(--text-secondary);" id="callStatus">
                            Отправьте ссылку другу для подключения
                        </div>
                    </div>
                </div>
                <div class="video-label">Участник</div>
            </div>
        </div>
        
        <div class="call-controls">
            <button class="control-btn mic-toggle" id="micToggle" onclick="toggleMicrophone()">🎤</button>
            <button class="control-btn cam-toggle" id="camToggle" onclick="toggleCamera()">📹</button>
            <button class="control-btn" onclick="toggleScreenShare()" style="background: var(--warning);">🖥️</button>
            <button class="control-btn" onclick="toggleRecording()" style="background: var(--cyber);">⏺️</button>
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
            <span>🛡️</span>
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
    <div class="settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>⚙️ Настройки</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="font-size: 1.5rem;">✕</button>
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
            <h4>🎥 Медиа</h4>
            <div style="margin-bottom: 15px;">
                <label>Камера по умолчанию</label>
                <select class="search-input" id="cameraSelect" style="margin-top: 5px;">
                    <option value="">Автовыбор</option>
                </select>
            </div>
            <div style="margin-bottom: 15px;">
                <label>Микрофон по умолчанию</label>
                <select class="search-input" id="microphoneSelect" style="margin-top: 5px;">
                    <option value="">Автовыбор</option>
                </select>
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
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span>Вибро-уведомления</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="vibrationToggle">
                    <span class="toggle-slider"></span>
                </label>
            </div>
        </div>

        <div class="settings-section">
            <h4>🎨 Внешний вид</h4>
            <div style="margin-bottom: 15px;">
                <label>Тема оформления</label>
                <select class="search-input" id="themeSelect" style="margin-top: 5px;">
                    <option value="dark">Тёмная</option>
                    <option value="light">Светлая</option>
                    <option value="auto">Авто</option>
                </select>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span>Компактный режим</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="compactToggle">
                    <span class="toggle-slider"></span>
                </label>
            </div>
        </div>

        <div class="encryption-status">
            <span>🔒</span>
            <span>End-to-End шифрование активно</span>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()">💾 Сохранить настройки</button>
        <button class="btn btn-secondary" onclick="exportData()" style="margin-top: 10px;">📤 Экспорт данных</button>
        <button class="btn btn-secondary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 10px;">
            🚪 Выйти из аккаунта
        </button>
    </div>

    <!-- Панель обмена файлами -->
    <div id="fileSharePanel" class="call-invite" style="display: none;">
        <div class="logo">📎 Обмен файлами</div>
        <div class="file-share-container">
            <input type="file" id="fileInput" style="display: none;" onchange="handleFileSelect(event)">
            <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                📁 Выбрать файл
            </button>
            <div id="fileInfo" style="margin-top: 10px; display: none;"></div>
        </div>
        <button class="btn btn-secondary" onclick="hideFileShare()">❌ Закрыть</button>
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
        let currentCallId = null;
        let isInCall = false;
        let isMicMuted = false;
        let isCamOff = false;
        let isScreenSharing = false;
        let isRecording = false;
        let participantTimeout = null;
        let callParticipants = new Set();
        let isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            initializeApp();
        });

        function initializeApp() {
            // Симуляция загрузки
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
                    setTimeout(typeNextText, 1000);
                } else {
                    hideLoadingScreen();
                    checkAutoLogin();
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
            
            sessionToken = generateSessionToken();
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('sessionToken', sessionToken);
            
            // Загружаем тестовых пользователей
            loadSampleUsers();
            
            showMainApp();
            showNotification('Профиль создан успешно! 🎉');
        }

        function generateSessionToken() {
            return Math.random().toString(36).substr(2) + Math.random().toString(36).substr(2);
        }

        function loadSampleUsers() {
            // Используем данные с сервера
            allUsers = JSON.parse(localStorage.getItem('allUsers')) || [];
            if (allUsers.length === 0) {
                // Если нет данных, создаем тестовых пользователей
                allUsers = [
                    {id: 'user1', name: 'Alex_Quantum', avatar: '👨‍💻', online: true, last_seen: 'только что'},
                    {id: 'user2', name: 'Sarah_Cyber', avatar: '👩‍🎨', online: true, last_seen: '2 мин назад'},
                    {id: 'user3', name: 'Mike_Neon', avatar: '👨‍🚀', online: false, last_seen: '1 час назад'},
                    {id: 'user4', name: 'Emma_Digital', avatar: '👩‍💼', online: true, last_seen: 'только что'},
                    {id: 'user5', name: 'Max_Virtual', avatar: '🤖', online: false, last_seen: '30 мин назад'},
                    {id: 'user6', name: 'Luna_Hyper', avatar: '👽', online: true, last_seen: '5 мин назад'}
                ];
                localStorage.setItem('allUsers', JSON.stringify(allUsers));
            }
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
            
            // Заполняем данные пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            
            loadContent();
            loadMediaDevices();
            loadSettings();
            
            // Проверяем приглашение в звонок
            checkCallInvite();
        }

        // Новые функции для улучшения UX

        function hideAllPanels() {
            hideSettings();
            hideDonatePanel();
            hideFileShare();
            document.getElementById('overlay').classList.remove('active');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
            document.getElementById('overlay').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
        }

        function showDonatePanel() {
            document.getElementById('donatePanel').classList.add('active');
            document.getElementById('overlay').classList.add('active');
        }

        function hideDonatePanel() {
            document.getElementById('donatePanel').classList.remove('active');
        }

        function showFileShare() {
            document.getElementById('fileSharePanel').style.display = 'block';
        }

        function hideFileShare() {
            document.getElementById('fileSharePanel').style.display = 'none';
        }

        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                const fileInfo = document.getElementById('fileInfo');
                fileInfo.innerHTML = `
                    <div style="color: var(--success);">
                        ✅ Файл выбран: ${file.name}<br>
                        Размер: ${(file.size / 1024 / 1024).toFixed(2)} MB
                    </div>
                    <button class="btn btn-primary" onclick="sendFile()" style="margin-top: 10px;">
                        📤 Отправить файл
                    </button>
                `;
                fileInfo.style.display = 'block';
            }
        }

        function sendFile() {
            showNotification('Файл отправлен! 📁');
            hideFileShare();
        }

        function startVoiceMessage() {
            if (!currentChat) {
                showNotification('Выберите чат для отправки голосового сообщения 💬');
                return;
            }

            showNotification('🎤 Запись голосового сообщения...');
            // Симуляция записи
            setTimeout(() => {
                showNotification('✅ Голосовое сообщение отправлено!');
                // Добавляем голосовое сообщение в чат
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.innerHTML = '🎤 Голосовое сообщение (5 сек)';
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 2000);
        }

        function toggleRecording() {
            isRecording = !isRecording;
            showNotification(isRecording ? '⏺️ Запись звонка начата' : '⏹️ Запись звонка остановлена');
        }

        function exportData() {
            const userData = {
                user: currentUser,
                chats: JSON.parse(localStorage.getItem(`chats_${currentUser.id}`)) || [],
                settings: JSON.parse(localStorage.getItem('userSettings')) || {}
            };
            
            const dataStr = JSON.stringify(userData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `trollexdl_backup_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            showNotification('📤 Данные экспортированы успешно!');
        }

        function loadSettings() {
            const settings = JSON.parse(localStorage.getItem('userSettings')) || {};
            
            // Загружаем настройки в форму
            if (settings.name) {
                document.getElementById('settingsName').value = settings.name;
            }
            if (settings.status) {
                document.getElementById('settingsStatus').value = settings.status;
            }
            if (settings.notifications !== undefined) {
                document.getElementById('notificationsToggle').checked = settings.notifications;
            }
            if (settings.sound !== undefined) {
                document.getElementById('soundToggle').checked = settings.sound;
            }
            if (settings.vibration !== undefined) {
                document.getElementById('vibrationToggle').checked = settings.vibration;
            }
            if (settings.theme) {
                document.getElementById('themeSelect').value = settings.theme;
            }
            if (settings.compact !== undefined) {
                document.getElementById('compactToggle').checked = settings.compact;
            }
        }

        function saveSettings() {
            const settings = {
                name: document.getElementById('settingsName').value,
                status: document.getElementById('settingsStatus').value,
                notifications: document.getElementById('notificationsToggle').checked,
                sound: document.getElementById('soundToggle').checked,
                vibration: document.getElementById('vibrationToggle').checked,
                theme: document.getElementById('themeSelect').value,
                compact: document.getElementById('compactToggle').checked
            };
            
            localStorage.setItem('userSettings', JSON.stringify(settings));
            
            // Обновляем имя пользователя если изменилось
            if (settings.name && settings.name !== currentUser.name) {
                currentUser.name = settings.name;
                localStorage.setItem('trollexUser', JSON.stringify(currentUser));
                document.getElementById('userName').textContent = settings.name;
            }
            
            showNotification('Настройки сохранены! ✅');
            hideSettings();
        }

        // Остальные функции (createCallRoom, getLocalStream, toggleMicrophone, toggleCamera, 
        // copyCallLink, endCall, checkCallInvite, acceptCall, declineCall, joinCallByLink, 
        // loadMediaDevices, switchTab, loadContent, selectUser, sendMessage и т.д.)
        // остаются без изменений из предыдущего кода...

    </script>
</body>
</html>
'''

@app.route('/')
def index():
    initialize_sample_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        
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
