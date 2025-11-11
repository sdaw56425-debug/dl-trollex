# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trollexdl-ultimate-2024'

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
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        .cosmic-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(107, 43, 217, 0.4) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(0, 255, 136, 0.2) 0%, transparent 50%);
            animation: cosmicShift 15s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes cosmicShift {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.02); }
        }

        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes glow {
            0%, 100% { 
                box-shadow: 0 0 20px var(--accent-glow),
                           0 0 40px rgba(139, 92, 246, 0.3);
            }
            50% { 
                box-shadow: 0 0 30px var(--accent-glow),
                           0 0 60px rgba(139, 92, 246, 0.5),
                           0 0 80px rgba(0, 255, 136, 0.2);
            }
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
            padding: 15px;
            z-index: 1000;
            overflow-y: auto;
        }

        .hidden {
            display: none !important;
        }

        .cosmic-card {
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(20px);
            border: 2px solid var(--accent);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            max-width: 450px;
            animation: slideUp 0.6s ease-out, glow 4s infinite;
            position: relative;
            overflow: hidden;
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--neon), var(--accent-glow), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn {
            width: 100%;
            padding: 16px 20px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(107, 43, 217, 0.4);
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
            text-align: center;
        }

        .user-avatar {
            width: 70px;
            height: 70px;
            border-radius: 15px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            margin: 0 auto 12px;
        }

        .app {
            width: 100%;
            height: 100vh;
            background: var(--primary);
            display: flex;
        }

        .sidebar {
            width: 100%;
            max-width: 350px;
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(10px);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
        }

        .user-header {
            padding: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
        }

        .new-year-countdown {
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            margin: 10px 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid var(--neon);
            animation: glow 3s infinite;
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 4px;
            margin: 12px;
            flex-wrap: wrap;
        }

        .nav-tab {
            flex: 1;
            padding: 10px 8px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 0.9rem;
            min-width: 60px;
        }

        .nav-tab.active {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .search-box {
            padding: 12px;
        }

        .search-input {
            width: 100%;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 12px;
            color: var(--text);
            font-size: 0.95rem;
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }

        .chat-item:hover, .chat-item.active {
            background: rgba(107, 43, 217, 0.2);
            border-color: var(--accent);
            transform: translateX(3px);
        }

        .item-avatar {
            width: 45px;
            height: 45px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 1.2rem;
        }

        .online-dot {
            width: 10px;
            height: 10px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
            margin-left: auto;
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
            gap: 12px;
        }

        .messages-container {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .message {
            max-width: 85%;
            padding: 12px 15px;
            border-radius: 15px;
            position: relative;
            animation: slideUp 0.3s ease-out;
        }

        .message.received {
            background: rgba(107, 43, 217, 0.3);
            align-self: flex-start;
            border-bottom-left-radius: 5px;
            border: 1px solid var(--accent);
        }

        .message.sent {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            align-self: flex-end;
            border-bottom-right-radius: 5px;
            color: white;
        }

        .message-actions {
            position: absolute;
            top: -25px;
            right: 0;
            background: rgba(26, 26, 74, 0.9);
            border: 1px solid var(--accent);
            border-radius: 8px;
            display: none;
            gap: 5px;
            padding: 5px;
        }

        .message:hover .message-actions {
            display: flex;
        }

        .message-action {
            background: none;
            border: none;
            color: var(--text);
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .message-action:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 4px;
            text-align: right;
        }

        .message-input-container {
            padding: 15px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--accent);
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .message-input {
            flex: 1;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 20px;
            color: var(--text);
            font-size: 0.95rem;
            outline: none;
        }

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-weight: bold;
        }

        .settings-panel {
            position: fixed;
            top: 0;
            right: -100%;
            width: 100%;
            max-width: 400px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            backdrop-filter: blur(20px);
            border-left: 2px solid var(--accent);
            z-index: 500;
            transition: right 0.3s ease;
            padding: 25px;
            overflow-y: auto;
        }

        .settings-panel.active {
            right: 0;
        }

        .setting-item {
            margin-bottom: 18px;
        }

        .setting-label {
            display: block;
            margin-bottom: 6px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.95rem;
        }

        .setting-input {
            width: 100%;
            padding: 10px 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 8px;
            color: var(--text);
            font-size: 0.95rem;
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
            background-color: rgba(255, 255, 255, 0.2);
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
            background-color: var(--accent);
        }

        input:checked + .toggle-slider:before {
            transform: translateX(26px);
        }

        .notification {
            position: fixed;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 12px 20px;
            border-radius: 12px;
            z-index: 4000;
            animation: slideUp 0.3s ease, glow 2s infinite;
            border: 1px solid var(--accent);
            max-width: 300px;
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.3rem;
            cursor: pointer;
            padding: 8px;
        }

        .group-creation {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            margin: 10px 0;
            border: 1px solid var(--accent);
        }

        .friends-list {
            max-height: 200px;
            overflow-y: auto;
            margin: 10px 0;
        }

        .friend-item {
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 5px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
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
            
            .settings-panel {
                width: 100%;
                max-width: none;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .cosmic-card {
                padding: 20px;
                margin: 10px;
            }
            
            .nav-tabs {
                flex-wrap: nowrap;
                overflow-x: auto;
            }
            
            .nav-tab {
                min-width: 70px;
                font-size: 0.85rem;
            }
            
            .message {
                max-width: 90%;
            }
        }

        @media (max-width: 480px) {
            .cosmic-card {
                padding: 15px;
            }
            
            .btn {
                padding: 14px 16px;
                font-size: 0.9rem;
            }
            
            .user-avatar {
                width: 60px;
                height: 60px;
                font-size: 1.5rem;
            }
            
            .message-input {
                padding: 10px 12px;
                font-size: 0.9rem;
            }
            
            .send-btn {
                padding: 10px 16px;
            }
        }
    </style>
</head>
<body>
    <div class="cosmic-bg"></div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card" style="text-align: center;">
            <div class="logo">TrollexDL</div>
            <div style="margin-top: 20px; font-size: 1.8rem;">🚀</div>
            <div style="color: var(--text-secondary); margin-top: 15px;">Loading quantum protocol...</div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="text-align: center; color: var(--text-secondary); margin-bottom: 25px; line-height: 1.5;">
                Ultimate messaging with quantum encryption<br>
                and cosmic design
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 START JOURNEY
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ QUICK START
            </button>

            <div class="new-year-countdown">
                🎄 <span id="newYearCountdown">...</span> until New Year!
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">Registration</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">🚀</div>
                <h3 id="registerName">Quantum_User</h3>
                <p style="color: var(--text-secondary);">ID: <span id="registerId">...</span></p>
                <p style="color: var(--text-secondary); margin-top: 5px;">📧 <span id="registerEmail">...</span></p>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ CREATE PROFILE
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewUser()">
                🔄 GENERATE NEW
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← BACK
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
                <p style="opacity: 0.8;">ID: <span id="userId">...</span></p>
            </div>

            <div class="new-year-countdown">
                🎄 <span id="sidebarCountdown">...</span> until New Year!
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('friends')">👥</div>
                <div class="nav-tab" onclick="switchTab('groups')">👨‍👩‍👧‍👦</div>
                <div class="nav-tab" onclick="showSettings()">⚙️</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Search..." id="searchInput" oninput="searchItems()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Динамически заполняется -->
            </div>

            <div style="padding: 15px;">
                <button class="btn btn-secondary" onclick="showLogoutConfirm()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger);">
                    🚪 Logout
                </button>
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Select chat to start messaging</p>
                </div>
                <button class="mobile-menu-btn" onclick="showSettings()">⚙️</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 40px 15px; color: var(--text-secondary);">
                    <div style="font-size: 3.5rem; margin-bottom: 15px;">🌌</div>
                    <h3 style="margin-bottom: 12px;">Welcome to TrollexDL!</h3>
                    <p>Start messaging with quantum encryption</p>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Type your message..." id="messageInput">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 25px;">
            <h3 style="margin: 0;">⚙️ Settings</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div class="setting-item">
            <label class="setting-label">👤 Display Name</label>
            <input type="text" class="setting-input" id="settingsName" placeholder="Enter new name">
        </div>

        <div class="setting-item">
            <label class="setting-label">📧 Email</label>
            <input type="email" class="setting-input" id="settingsEmail" placeholder="Enter email">
        </div>

        <div class="setting-item">
            <label class="setting-label">🔔 Notifications</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsNotifications" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">🌙 Dark Mode</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsDarkMode" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">💾 Auto-save Messages</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsAutoSave" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div style="margin-bottom: 25px;">
            <h4 style="margin-bottom: 12px; color: var(--text-secondary);">Profile Info</h4>
            <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                <div>🆔 ID: <span id="settingsUserId">-</span></div>
                <div>📅 Registered: <span id="settingsUserRegDate">-</span></div>
                <div>💾 Storage: <span id="settingsStorage">0</span> messages</div>
            </div>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()" style="margin-bottom: 12px;">💾 Save Settings</button>
        <button class="btn btn-secondary" onclick="exportData()">📤 Export Data</button>
    </div>

    <!-- Подтверждение выхода -->
    <div id="logoutConfirm" class="screen hidden" style="background: rgba(10, 10, 42, 0.95); z-index: 4000;">
        <div class="cosmic-card">
            <h3 style="margin-bottom: 20px; text-align: center;">🚪 Confirm Logout</h3>
            <p style="text-align: center; margin-bottom: 25px; color: var(--text-secondary);">
                Your data will be saved securely.<br>
                You can return anytime!
            </p>
            <button class="btn btn-primary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger);">
                ✅ Logout
            </button>
            <button class="btn btn-secondary" onclick="hideLogoutConfirm()">
                ❌ Cancel
            </button>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let messages = {};
        let friends = [];
        let groups = [];
        let editingMessageId = null;

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            updateNewYearCountdown();
            setInterval(updateNewYearCountdown, 60000); // Обновлять каждую минуту
            
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 1500);
        });

        function updateNewYearCountdown() {
            const now = new Date();
            const newYear = new Date(now.getFullYear() + 1, 0, 1);
            const diff = newYear - now;
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            
            document.getElementById('newYearCountdown').textContent = `${days} days`;
            document.getElementById('sidebarCountdown').textContent = `${days} days`;
        }

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
            const name = generateUsername();
            const email = generateEmail(name);
            const userId = generateUserId();
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌', '🌟', '⭐', '☄️', '🌠', '🪐'];
            
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
            document.getElementById('registerEmail').textContent = email;
        }

        function generateUsername() {
            const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha'];
            const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther'];
            const numbers = Math.floor(Math.random() * 9000) + 1000;
            return `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
        }

        function generateEmail(username) {
            const domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net'];
            return `${username.toLowerCase()}@${domains[Math.floor(Math.random() * domains.length)]}`;
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 9).toUpperCase();
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
                settings: {
                    notifications: true,
                    darkMode: true,
                    autoSave: true,
                    theme: 'cosmic'
                },
                created_at: new Date().toISOString()
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('userMessages', JSON.stringify(messages));
            
            // Создаем тестовых друзей и группы
            initializeSampleData();
            
            showMainApp();
            showNotification('Quantum profile created! 🎉', 'success');
        }

        function initializeSampleData() {
            // Тестовые друзья
            friends = [
                {id: 'friend1', name: 'Tech_Support', avatar: '🛰️', online: true},
                {id: 'friend2', name: 'System_Bot', avatar: '🤖', online: true},
                {id: 'friend3', name: 'Community_Manager', avatar: '👨‍💼', online: false}
            ];
            
            // Тестовые группы
            groups = [
                {id: 'group1', name: 'Quantum_Coders', avatar: '👨‍💻', members: 3, online: 2},
                {id: 'group2', name: 'Cosmic_Gamers', avatar: '🎮', members: 5, online: 3},
                {id: 'group3', name: 'AI_Researchers', avatar: '🧠', members: 8, online: 4}
            ];
            
            localStorage.setItem('userFriends', JSON.stringify(friends));
            localStorage.setItem('userGroups', JSON.stringify(groups));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedMessages = localStorage.getItem('userMessages');
                const savedFriends = localStorage.getItem('userFriends');
                const savedGroups = localStorage.getItem('userGroups');
                
                if (savedMessages) messages = JSON.parse(savedMessages);
                if (savedFriends) friends = JSON.parse(savedFriends);
                if (savedGroups) groups = JSON.parse(savedGroups);
                
                showMainApp();
                showNotification('Welcome back to TrollexDL! 🚀', 'success');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedMessages = localStorage.getItem('userMessages');
                const savedFriends = localStorage.getItem('userFriends');
                const savedGroups = localStorage.getItem('userGroups');
                
                if (savedMessages) messages = JSON.parse(savedMessages);
                if (savedFriends) friends = JSON.parse(savedFriends);
                if (savedGroups) groups = JSON.parse(savedGroups);
                
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
            
            // Заполняем настройки
            loadSettings();
            
            loadContent();
        }

        function loadSettings() {
            document.getElementById('settingsName').value = currentUser.name;
            document.getElementById('settingsEmail').value = currentUser.email;
            document.getElementById('settingsNotifications').checked = currentUser.settings.notifications;
            document.getElementById('settingsDarkMode').checked = currentUser.settings.darkMode;
            document.getElementById('settingsAutoSave').checked = currentUser.settings.autoSave;
            document.getElementById('settingsUserId').textContent = currentUser.id;
            document.getElementById('settingsUserRegDate').textContent = new Date(currentUser.created_at).toLocaleDateString();
            updateStorageInfo();
        }

        function updateStorageInfo() {
            const totalMessages = Object.values(messages).reduce((acc, msgs) => acc + msgs.length, 0);
            document.getElementById('settingsStorage').textContent = totalMessages;
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
            
            if (currentTab === 'chats') {
                contentHTML = getChatsContent(searchTerm);
            } else if (currentTab === 'friends') {
                contentHTML = getFriendsContent(searchTerm);
            } else if (currentTab === 'groups') {
                contentHTML = getGroupsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 'support', name: 'Trollex Support', avatar: '🛰️', lastMessage: 'How can we help?', online: true},
                {id: 'updates', name: 'System Updates', avatar: '🔧', lastMessage: 'Latest features available', online: true},
                {id: 'community', name: 'Community Chat', avatar: '👥', lastMessage: 'Welcome to TrollexDL!', online: true}
            ];
            
            const filteredChats = chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">💬 No chats found</div>';
            }
            
            return filteredChats.map(chat => `
                <div class="chat-item ${currentChat?.id === chat.id ? 'active' : ''}" onclick="openChat('${chat.id}')">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.85rem;">${chat.lastMessage}</div>
                    </div>
                    ${chat.online ? '<div class="online-dot"></div>' : ''}
                </div>
            `).join('');
        }

        function getFriendsContent(searchTerm) {
            const filteredFriends = friends.filter(friend => 
                friend.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredFriends.length === 0) {
                return '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">👥 No friends found</div>';
            }
            
            return filteredFriends.map(friend => `
                <div class="chat-item">
                    <div class="item-avatar">${friend.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${friend.name}</div>
                        <div style="color: ${friend.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.85rem;">
                            ${friend.online ? '● Online' : '○ Offline'}
                        </div>
                    </div>
                    <div style="display: flex; gap: 5px;">
                        <button onclick="startChatWithFriend('${friend.id}')" style="background: var(--accent); color: white; border: none; border-radius: 6px; padding: 6px 10px; cursor: pointer; font-size: 0.8rem;">💬</button>
                        <button onclick="removeFriend('${friend.id}')" style="background: var(--danger); color: white; border: none; border-radius: 6px; padding: 6px 10px; cursor: pointer; font-size: 0.8rem;">❌</button>
                    </div>
                </div>
            `).join('') + `
                <div class="chat-item" onclick="showAddFriendDialog()" style="justify-content: center; background: rgba(0, 255, 136, 0.1); border-color: var(--success);">
                    <div style="font-weight: bold; color: var(--success);">+ Add Friend</div>
                </div>
            `;
        }

        function getGroupsContent(searchTerm) {
            const filteredGroups = groups.filter(group => 
                group.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredGroups.length === 0) {
                return '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">👨‍👩‍👧‍👦 No groups found</div>';
            }
            
            return filteredGroups.map(group => `
                <div class="chat-item" onclick="openGroup('${group.id}')">
                    <div class="item-avatar">${group.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${group.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.85rem;">
                            ${group.members} members • ${group.online} online
                        </div>
                    </div>
                </div>
            `).join('') + `
                <div class="chat-item" onclick="showCreateGroupDialog()" style="justify-content: center; background: rgba(107, 43, 217, 0.2); border-color: var(--accent);">
                    <div style="font-weight: bold; color: var(--accent);">+ Create Group</div>
                </div>
            `;
        }

        function searchItems() {
            loadContent();
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Trollex Support', avatar: '🛰️', status: 'online'},
                'updates': {name: 'System Updates', avatar: '🔧', status: 'online'},
                'community': {name: 'Community Chat', avatar: '👥', status: 'online'}
            };
            
            const chat = chats[chatId];
            if (chat) {
                currentChat = {...chat, id: chatId};
                
                document.getElementById('currentChatName').textContent = chat.name;
                document.getElementById('currentChatAvatar').textContent = chat.avatar;
                document.getElementById('currentChatStatus').textContent = chat.status;
                
                loadContent();
                showChatMessages(chatId);
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const chatMessages = messages[chatId] || getDefaultMessages(chatId);
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = getWelcomeMessage(chatId);
            } else {
                messagesContainer.innerHTML = chatMessages.map(msg => `
                    <div class="message ${msg.sender}" data-message-id="${msg.id}">
                        ${msg.text}
                        <div class="message-actions">
                            <button class="message-action" onclick="editMessage('${msg.id}')">✏️</button>
                            <button class="message-action" onclick="deleteMessage('${msg.id}')">🗑️</button>
                            ${msg.views ? `<button class="message-action">👁️ ${msg.views}</button>` : ''}
                        </div>
                        <div class="message-time">${msg.time}</div>
                    </div>
                `).join('');
            }
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function getDefaultMessages(chatId) {
            const defaults = {
                'support': [
                    {id: '1', text: 'Welcome to TrollexDL Support! 🚀', sender: 'received', time: '12:00', views: 1},
                    {id: '2', text: 'How can we assist you today?', sender: 'received', time: '12:01', views: 1}
                ]
            };
            return defaults[chatId] || [];
        }

        function getWelcomeMessage(chatId) {
            return `
                <div style="text-align: center; padding: 40px 15px; color: var(--text-secondary);">
                    <div style="font-size: 3rem; margin-bottom: 15px;">💬</div>
                    <h3 style="margin-bottom: 12px;">${currentChat.name}</h3>
                    <p>Start conversation with quantum encryption</p>
                </div>
            `;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                if (editingMessageId) {
                    editExistingMessage(editingMessageId, message);
                } else {
                    createNewMessage(message);
                }
                
                input.value = '';
                editingMessageId = null;
            }
        }

        function createNewMessage(message) {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const messageId = 'msg_' + Date.now();
            
            const messageElement = document.createElement('div');
            messageElement.className = 'message sent';
            messageElement.setAttribute('data-message-id', messageId);
            messageElement.innerHTML = `
                ${message}
                <div class="message-actions">
                    <button class="message-action" onclick="editMessage('${messageId}')">✏️</button>
                    <button class="message-action" onclick="deleteMessage('${messageId}')">🗑️</button>
                    <button class="message-action">👁️ 1</button>
                </div>
                <div class="message-time">${time}</div>
            `;
            
            if (!messages[currentChat.id] || messages[currentChat.id].length === 0) {
                messagesContainer.innerHTML = '';
            }
            
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Сохраняем сообщение
            if (!messages[currentChat.id]) {
                messages[currentChat.id] = [];
            }
            messages[currentChat.id].push({
                id: messageId,
                text: message,
                sender: 'sent',
                time: time,
                views: 1,
                timestamp: new Date().toISOString()
            });
            
            saveData();
            showNotification('Message sent! ✨', 'success');
            
            // Имитация ответа
            setTimeout(() => {
                if (currentChat) {
                    simulateReply();
                }
            }, 1000 + Math.random() * 2000);
        }

        function editMessage(messageId) {
            const message = messages[currentChat.id]?.find(m => m.id === messageId);
            if (message && message.sender === 'sent') {
                document.getElementById('messageInput').value = message.text;
                document.getElementById('messageInput').focus();
                editingMessageId = messageId;
                showNotification('Editing message... ✏️', 'info');
            }
        }

        function editExistingMessage(messageId, newText) {
            const messageIndex = messages[currentChat.id]?.findIndex(m => m.id === messageId);
            if (messageIndex > -1) {
                messages[currentChat.id][messageIndex].text = newText;
                messages[currentChat.id][messageIndex].edited = true;
                
                // Обновляем отображение
                const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
                if (messageElement) {
                    messageElement.querySelector('div:first-child').textContent = newText + ' (edited)';
                }
                
                saveData();
                showNotification('Message updated! ✅', 'success');
            }
        }

        function deleteMessage(messageId) {
            if (confirm('Delete this message?')) {
                messages[currentChat.id] = messages[currentChat.id]?.filter(m => m.id !== messageId) || [];
                const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
                if (messageElement) {
                    messageElement.remove();
                }
                saveData();
                showNotification('Message deleted 🗑️', 'info');
            }
        }

        function simulateReply() {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const replyId = 'msg_' + Date.now();
            
            const replies = {
                'support': [
                    'Thanks for your message! How can we help? 🚀',
                    'We appreciate your feedback!',
                    'Our team will review your message shortly. 👨‍🚀'
                ]
            };
            
            const chatReplies = replies[currentChat.id] || ['Thank you for your message!'];
            const replyText = chatReplies[Math.floor(Math.random() * chatReplies.length)];
            
            const replyElement = document.createElement('div');
            replyElement.className = 'message received';
            replyElement.setAttribute('data-message-id', replyId);
            replyElement.innerHTML = `
                ${replyText}
                <div class="message-actions">
                    <button class="message-action">👁️ 1</button>
                </div>
                <div class="message-time">${time}</div>
            `;
            
            messagesContainer.appendChild(replyElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Сохраняем ответ
            if (!messages[currentChat.id]) {
                messages[currentChat.id] = [];
            }
            messages[currentChat.id].push({
                id: replyId,
                text: replyText,
                sender: 'received',
                time: time,
                views: 1,
                timestamp: new Date().toISOString()
            });
            
            saveData();
        }

        function startChatWithFriend(friendId) {
            const friend = friends.find(f => f.id === friendId);
            if (friend) {
                const chatId = `friend_${friendId}`;
                currentChat = {
                    id: chatId,
                    name: friend.name,
                    avatar: friend.avatar,
                    status: 'online',
                    type: 'friend'
                };
                
                document.getElementById('currentChatName').textContent = friend.name;
                document.getElementById('currentChatAvatar').textContent = friend.avatar;
                document.getElementById('currentChatStatus').textContent = 'online';
                
                showChatMessages(chatId);
                showNotification(`Started chat with ${friend.name} 💬`, 'success');
            }
        }

        function removeFriend(friendId) {
            if (confirm('Remove this friend?')) {
                friends = friends.filter(f => f.id !== friendId);
                localStorage.setItem('userFriends', JSON.stringify(friends));
                loadContent();
                showNotification('Friend removed 👋', 'info');
            }
        }

        function showAddFriendDialog() {
            const friendName = prompt('Enter friend username:');
            if (friendName && friendName.trim()) {
                const newFriend = {
                    id: 'friend_' + Date.now(),
                    name: friendName.trim(),
                    avatar: '👤',
                    online: true
                };
                friends.push(newFriend);
                localStorage.setItem('userFriends', JSON.stringify(friends));
                loadContent();
                showNotification('Friend added! 👥', 'success');
            }
        }

        function openGroup(groupId) {
            const group = groups.find(g => g.id === groupId);
            if (group) {
                currentChat = {
                    id: groupId,
                    name: group.name,
                    avatar: group.avatar,
                    status: `${group.online}/${group.members} online`,
                    type: 'group'
                };
                
                document.getElementById('currentChatName').textContent = group.name;
                document.getElementById('currentChatAvatar').textContent = group.avatar;
                document.getElementById('currentChatStatus').textContent = `${group.online}/${group.members} online`;
                
                showChatMessages(groupId);
            }
        }

        function showCreateGroupDialog() {
            const groupName = prompt('Enter group name:');
            if (groupName && groupName.trim()) {
                const newGroup = {
                    id: 'group_' + Date.now(),
                    name: groupName.trim(),
                    avatar: '👨‍👩‍👧‍👦',
                    members: 1,
                    online: 1
                };
                groups.push(newGroup);
                localStorage.setItem('userGroups', JSON.stringify(groups));
                loadContent();
                showNotification('Group created! 🎉', 'success');
            }
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            const newEmail = document.getElementById('settingsEmail').value.trim();
            
            if (newName && newName !== currentUser.name) {
                currentUser.name = newName;
                document.getElementById('userName').textContent = newName;
                showNotification('Name updated! ✅', 'success');
            }
            
            if (newEmail && newEmail !== currentUser.email) {
                currentUser.email = newEmail;
                showNotification('Email updated! 📧', 'success');
            }
            
            currentUser.settings.notifications = document.getElementById('settingsNotifications').checked;
            currentUser.settings.darkMode = document.getElementById('settingsDarkMode').checked;
            currentUser.settings.autoSave = document.getElementById('settingsAutoSave').checked;
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            hideSettings();
            showNotification('Settings saved! ⚙️', 'success');
        }

        function exportData() {
            const data = {
                user: currentUser,
                messages: messages,
                friends: friends,
                groups: groups,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `trollexdl_backup_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            showNotification('Data exported! 📤', 'success');
        }

        function saveData() {
            if (currentUser.settings.autoSave) {
                localStorage.setItem('userMessages', JSON.stringify(messages));
                updateStorageInfo();
            }
        }

        function showLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.remove('hidden');
        }

        function hideLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.add('hidden');
        }

        function logout() {
            localStorage.removeItem('trollexUser');
            showWelcomeScreen();
            showNotification('See you soon in TrollexDL! 👋', 'info');
        }

        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            
            if (type === 'error') {
                notification.style.background = 'linear-gradient(135deg, var(--danger), #cc0000)';
            } else if (type === 'warning') {
                notification.style.background = 'linear-gradient(135deg, var(--warning), #ff8800)';
            }
            
            document.body.appendChild(notification);
            
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

        // Закрытие сайдбара и настроек при клике вне их
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                sidebar.classList.remove('active');
            }
            
            const settingsPanel = document.getElementById('settingsPanel');
            if (settingsPanel.classList.contains('active') && 
                !settingsPanel.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                settingsPanel.classList.remove('active');
            }
        });

        // Адаптация для мобильных устройств
        function handleResize() {
            if (window.innerWidth > 768) {
                document.getElementById('sidebar').classList.remove('active');
            }
        }

        window.addEventListener('resize', handleResize);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    days_until_new_year = get_days_until_new_year()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    data = request.json
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running', 
        'service': 'TrollexDL',
        'days_until_new_year': get_days_until_new_year()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
