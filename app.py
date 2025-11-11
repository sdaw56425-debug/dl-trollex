# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trollexdl-secret-2024'

# Глобальные хранилища
users_db = {}
messages_db = {}
active_calls = {}

def generate_username():
    adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha']
    nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther']
    numbers = random.randint(1000, 9999)
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"

def generate_email(username):
    domains = ['cosmic.com', 'quantum.io', 'nebula.org', 'galaxy.net', 'universe.ai']
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

        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
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

        .cosmic-card {
            background: rgba(26, 26, 74, 0.9);
            backdrop-filter: blur(20px);
            border: 2px solid var(--accent);
            border-radius: 25px;
            padding: 40px;
            width: 100%;
            max-width: 450px;
            animation: slideUp 0.8s ease-out, glow 4s infinite;
            position: relative;
            overflow: hidden;
        }

        .cosmic-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(107, 43, 217, 0.1), transparent);
            animation: shine 6s infinite;
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
            background: linear-gradient(45deg, var(--neon), var(--accent-glow), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
        }

        .typewriter {
            overflow: hidden;
            border-right: 2px solid var(--neon);
            white-space: nowrap;
            animation: typewriter 3s steps(40, end), blink-caret 0.75s step-end infinite;
        }

        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: var(--neon); }
        }

        .btn {
            width: 100%;
            padding: 18px 25px;
            border: none;
            border-radius: 15px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 15px;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(107, 43, 217, 0.4);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--text);
            border: 2px solid var(--accent);
        }

        .user-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px;
            margin: 20px 0;
            border: 1px solid var(--accent);
            text-align: center;
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 15px;
        }

        .app {
            width: 100%;
            height: 100vh;
            background: var(--primary);
            display: flex;
        }

        .sidebar {
            width: 350px;
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(10px);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
        }

        .user-header {
            padding: 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
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
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .search-box {
            padding: 15px;
        }

        .search-input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 15px;
            color: var(--text);
            font-size: 1rem;
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 18px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }

        .chat-item:hover {
            background: rgba(107, 43, 217, 0.2);
            border-color: var(--accent);
            transform: translateX(5px);
        }

        .chat-item.active {
            background: rgba(107, 43, 217, 0.3);
            border-color: var(--accent);
        }

        .item-avatar {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 1.3rem;
        }

        .online-dot {
            width: 12px;
            height: 12px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--success);
            margin-left: auto;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
        }

        .chat-header {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--accent);
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
        }

        .message {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
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

        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 5px;
            text-align: right;
        }

        .message-input-container {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--accent);
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .message-input {
            flex: 1;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 25px;
            color: var(--text);
            font-size: 1rem;
            outline: none;
        }

        .send-btn {
            padding: 15px 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
        }

        .settings-panel {
            position: fixed;
            top: 0;
            right: -400px;
            width: 350px;
            height: 100%;
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(20px);
            border-left: 2px solid var(--accent);
            z-index: 500;
            transition: right 0.3s ease;
            padding: 30px;
            overflow-y: auto;
        }

        .settings-panel.active {
            right: 0;
        }

        .setting-item {
            margin-bottom: 20px;
        }

        .setting-label {
            display: block;
            margin-bottom: 8px;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .setting-input {
            width: 100%;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 10px;
            color: var(--text);
            font-size: 1rem;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 15px 25px;
            border-radius: 15px;
            z-index: 4000;
            animation: slideUp 0.3s ease, glow 2s infinite;
            border: 1px solid var(--accent);
        }

        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background: var(--neon);
            animation: confettiFall 5s linear forwards;
            z-index: 10000;
        }

        @keyframes confettiFall {
            0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 10px 15px;
            background: rgba(107, 43, 217, 0.2);
            border-radius: 15px;
            margin: 10px 20px;
            align-self: flex-start;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }

        .typing-dots {
            display: flex;
            margin-left: 10px;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--neon);
            border-radius: 50%;
            margin: 0 2px;
            animation: typingBounce 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
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
            
            .cosmic-card {
                padding: 25px;
                margin: 10px;
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
            <div class="typewriter">Initializing quantum protocol...</div>
            <div style="margin-top: 30px; font-size: 2rem;">🚀</div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="text-align: center; color: var(--text-secondary); margin-bottom: 30px; line-height: 1.6;">
                Ultimate messaging experience<br>
                with quantum encryption & neon design
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 START JOURNEY
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ QUICK START
            </button>

            <div style="text-align: center; margin-top: 25px; color: var(--text-secondary); font-size: 0.9rem;">
                • Quantum Encryption<br>
                • HD Voice/Video Calls<br>
                • Cosmic Design<br>
                • Cross-Platform
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

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('calls')">📞</div>
                <div class="nav-tab" onclick="showSettings()">⚙️</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Search universe..." id="searchInput" oninput="searchItems()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Динамически заполняется -->
            </div>

            <div style="padding: 20px;">
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
                <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🌌</div>
                    <h3 style="margin-bottom: 15px;">Welcome to TrollexDL!</h3>
                    <p>Start messaging with quantum encryption</p>
                    <div style="margin-top: 30px; font-size: 0.9rem; opacity: 0.7;">
                        🔒 Quantum Encryption<br>
                        📞 HD Calls<br>
                        🚀 Ultra Fast
                    </div>
                </div>
            </div>

            <div class="typing-indicator hidden" id="typingIndicator">
                <span id="typingUser">User</span> is typing
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Type your quantum message..." id="messageInput" oninput="handleTyping()">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="settings-panel" id="settingsPanel">
        <h3 style="margin-bottom: 25px; text-align: center;">⚙️ Settings</h3>
        
        <div class="setting-item">
            <label class="setting-label">👤 Display Name</label>
            <input type="text" class="setting-input" id="settingsName" placeholder="Enter new name">
        </div>

        <div class="setting-item">
            <label class="setting-label">📧 Email</label>
            <input type="email" class="setting-input" id="settingsEmail" placeholder="Enter email">
        </div>

        <div class="setting-item">
            <label class="setting-label">🎨 Theme</label>
            <select class="setting-input" id="settingsTheme">
                <option>🌌 Cosmic</option>
                <option>🚀 Neon</option>
                <option>⚡ Quantum</option>
                <option>🔮 Mystic</option>
            </select>
        </div>

        <div class="setting-item">
            <label class="setting-label">🔔 Notifications</label>
            <div style="display: flex; gap: 10px;">
                <button class="btn btn-secondary" style="flex: 1;" onclick="toggleSetting('notifications', true)">🔔 On</button>
                <button class="btn btn-secondary" style="flex: 1;" onclick="toggleSetting('notifications', false)">🔕 Off</button>
            </div>
        </div>

        <div style="margin-bottom: 30px;">
            <h4 style="margin-bottom: 15px; color: var(--text-secondary);">Profile Info</h4>
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
                <div>🆔 ID: <span id="settingsUserId">-</span></div>
                <div>📅 Registered: <span id="settingsUserRegDate">-</span></div>
                <div>💾 Storage: <span id="settingsStorage">0</span> messages</div>
            </div>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()" style="margin-bottom: 15px;">💾 Save Settings</button>
        <button class="btn btn-secondary" onclick="showLogoutConfirm()">🚪 Logout</button>
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
        let typingTimer = null;

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 2000);
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
                theme: 'cosmic',
                notifications: true,
                created_at: new Date().toISOString()
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('userMessages', JSON.stringify(messages));
            
            showMainApp();
            createConfetti();
            showNotification('Quantum profile created! 🎉', 'success');
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
                showNotification('Welcome back to TrollexDL! 🚀', 'success');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            const savedMessages = localStorage.getItem('userMessages');
            
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                if (savedMessages) {
                    messages = JSON.parse(savedMessages);
                }
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
            
            // Настройки
            document.getElementById('settingsName').value = currentUser.name;
            document.getElementById('settingsEmail').value = currentUser.email;
            document.getElementById('settingsUserId').textContent = currentUser.id;
            document.getElementById('settingsUserRegDate').textContent = new Date(currentUser.created_at).toLocaleDateString();
            document.getElementById('settingsStorage').textContent = Object.values(messages).reduce((acc, msgs) => acc + msgs.length, 0);
            
            loadContent();
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
            } else if (currentTab === 'calls') {
                contentHTML = getCallsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 'support', name: 'Trollex Support', avatar: '🛰️', lastMessage: 'How can we help?', online: true, type: 'support'},
                {id: 'updates', name: 'System Updates', avatar: '🔧', lastMessage: 'Latest features available', online: true, type: 'updates'},
                {id: 'community', name: 'Community Chat', avatar: '👥', lastMessage: 'Welcome to TrollexDL!', online: true, type: 'community'}
            ];
            
            const filteredChats = chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--text-secondary);">🌌 No chats found</div>';
            }
            
            return filteredChats.map(chat => `
                <div class="chat-item ${currentChat?.id === chat.id ? 'active' : ''}" onclick="openChat('${chat.id}')">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 1.1rem;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${chat.lastMessage}</div>
                    </div>
                    ${chat.online ? '<div class="online-dot"></div>' : ''}
                </div>
            `).join('');
        }

        function getCallsContent(searchTerm) {
            const callHistory = [
                {id: '1', name: 'Trollex Support', avatar: '🛰️', type: 'voice', duration: '2:30', date: 'Today', status: 'completed'},
                {id: '2', name: 'System Bot', avatar: '🤖', type: 'video', duration: '5:15', date: 'Yesterday', status: 'completed'},
                {id: '3', name: 'Community', avatar: '👥', type: 'voice', duration: '1:45', date: '2 days ago', status: 'missed'}
            ];
            
            const filteredCalls = callHistory.filter(call => 
                call.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredCalls.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--text-secondary);">📞 No call history</div>';
            }
            
            return filteredCalls.map(call => `
                <div class="chat-item">
                    <div class="item-avatar">${call.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 1.1rem;">${call.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">
                            ${call.type === 'video' ? '📹' : '📞'} • ${call.duration} • ${call.date}
                        </div>
                    </div>
                    <div style="color: ${call.status === 'completed' ? 'var(--success)' : 'var(--danger)'};">
                        ${call.status === 'completed' ? '✅' : '❌'}
                    </div>
                </div>
            `).join('');
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
                
                // Обновляем активный чат в списке
                loadContent();
                showChatMessages(chatId);
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            
            // Загружаем сохраненные сообщения для этого чата
            const chatMessages = messages[chatId] || getDefaultMessages(chatId);
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = getWelcomeMessage(chatId);
            } else {
                messagesContainer.innerHTML = chatMessages.map(msg => `
                    <div class="message ${msg.sender}" data-message-id="${msg.id}">
                        ${msg.text}
                        <div class="message-time">${msg.time}</div>
                    </div>
                `).join('');
            }
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function getDefaultMessages(chatId) {
            const defaults = {
                'support': [
                    {id: '1', text: 'Welcome to TrollexDL Support! 🚀', sender: 'received', time: '12:00'},
                    {id: '2', text: 'How can we assist you today?', sender: 'received', time: '12:01'}
                ],
                'updates': [
                    {id: '1', text: 'System Updates Channel 📡', sender: 'received', time: '11:30'},
                    {id: '2', text: 'Latest version: TrollexDL v2.0', sender: 'received', time: '11:31'}
                ],
                'community': [
                    {id: '1', text: 'Welcome to Community Chat! 👥', sender: 'received', time: '10:15'},
                    {id: '2', text: 'Share your experiences with TrollexDL', sender: 'received', time: '10:16'}
                ]
            };
            return defaults[chatId] || [];
        }

        function getWelcomeMessage(chatId) {
            const welcomeTexts = {
                'support': 'Get help and support for TrollexDL',
                'updates': 'Stay updated with latest features',
                'community': 'Connect with other TrollexDL users'
            };
            
            return `
                <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                    <div style="font-size: 4rem; margin-bottom: 20px;">💬</div>
                    <h3 style="margin-bottom: 15px;">${currentChat.name}</h3>
                    <p>${welcomeTexts[chatId]}</p>
                    <div style="margin-top: 30px; font-size: 0.9rem; opacity: 0.7;">
                        Start typing to begin conversation
                    </div>
                </div>
            `;
        }

        function handleTyping() {
            if (currentChat) {
                showTypingIndicator();
                
                // Сбрасываем таймер при каждом вводе
                clearTimeout(typingTimer);
                typingTimer = setTimeout(() => {
                    hideTypingIndicator();
                }, 1000);
            }
        }

        function showTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            indicator.classList.remove('hidden');
        }

        function hideTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            indicator.classList.add('hidden');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                const messagesContainer = document.getElementById('messagesContainer');
                const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                const messageId = 'msg_' + Date.now();
                
                // Создаем элемент сообщения
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.setAttribute('data-message-id', messageId);
                messageElement.innerHTML = `
                    ${message}
                    <div class="message-time">${time}</div>
                `;
                
                // Если это первое сообщение, очищаем welcome message
                if (!messages[currentChat.id] || messages[currentChat.id].length === 0) {
                    messagesContainer.innerHTML = '';
                }
                
                messagesContainer.appendChild(messageElement);
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                hideTypingIndicator();
                
                // Сохраняем сообщение
                if (!messages[currentChat.id]) {
                    messages[currentChat.id] = [];
                }
                messages[currentChat.id].push({
                    id: messageId,
                    text: message,
                    sender: 'sent',
                    time: time,
                    timestamp: new Date().toISOString()
                });
                
                // Сохраняем в localStorage
                localStorage.setItem('userMessages', JSON.stringify(messages));
                
                showNotification('Message sent! ✨', 'success');
                
                // Имитация ответа через 1-3 секунды
                setTimeout(() => {
                    if (currentChat) { // Проверяем что чат все еще открыт
                        simulateReply();
                    }
                }, 1000 + Math.random() * 2000);
            }
        }

        function simulateReply() {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const replyId = 'msg_' + Date.now();
            
            const replies = {
                'support': [
                    'Thanks for your message! How can we assist you further? 🚀',
                    'We appreciate your feedback! Is there anything specific you need help with?',
                    'Our team will review your message shortly. Thank you! 👨‍🚀'
                ],
                'updates': [
                    'New features are coming soon! Stay tuned! ⚡',
                    'Your system is up to date with the latest version! ✅',
                    'We are working on exciting new updates! 🌟'
                ],
                'community': [
                    'Great to see you in the community! 👋',
                    'Thanks for sharing! Other users will appreciate this! 💫',
                    'Welcome to our growing community! 🎉'
                ]
            };
            
            const chatReplies = replies[currentChat.id] || ['Thank you for your message!'];
            const replyText = chatReplies[Math.floor(Math.random() * chatReplies.length)];
            
            const replyElement = document.createElement('div');
            replyElement.className = 'message received';
            replyElement.setAttribute('data-message-id', replyId);
            replyElement.innerHTML = `
                ${replyText}
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
                timestamp: new Date().toISOString()
            });
            
            localStorage.setItem('userMessages', JSON.stringify(messages));
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

        function toggleSetting(setting, value) {
            currentUser[setting] = value;
            showNotification(`${setting.charAt(0).toUpperCase() + setting.slice(1)} ${value ? 'enabled' : 'disabled'}!`, 'info');
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            const newEmail = document.getElementById('settingsEmail').value.trim();
            
            if (newName && newName !== currentUser.name) {
                currentUser.name = newName;
                document.getElementById('userName').textContent = newName;
                showNotification('Name updated successfully! ✅', 'success');
            }
            
            if (newEmail && newEmail !== currentUser.email) {
                currentUser.email = newEmail;
                showNotification('Email updated successfully! 📧', 'success');
            }
            
            currentUser.theme = document.getElementById('settingsTheme').value;
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            hideSettings();
            
            createConfetti();
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
            }
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        function createConfetti() {
            for (let i = 0; i < 50; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.background = `hsl(${Math.random() * 360}, 100%, 50%)`;
                    confetti.style.width = Math.random() * 10 + 5 + 'px';
                    confetti.style.height = confetti.style.width;
                    
                    document.body.appendChild(confetti);
                    
                    setTimeout(() => {
                        confetti.remove();
                    }, 5000);
                }, i * 100);
            }
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

        // Загрузка сообщений при изменении чата
        function updateMessagesStorage() {
            document.getElementById('settingsStorage').textContent = Object.values(messages).reduce((acc, msgs) => acc + msgs.length, 0);
        }
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
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/health')
def health_check():
    return jsonify({'status': 'running', 'service': 'TrollexDL'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
