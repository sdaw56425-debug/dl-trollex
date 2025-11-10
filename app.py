# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramodern2024'

class AdvancedChatManager:
    def __init__(self):
        self.users = []
        self.chats = []
        self.messages = []
        self.voice_notes = []
    
    def add_user(self, user_data):
        user_data['premium'] = random.choice([True, False, False])
        user_data['join_date'] = datetime.datetime.now().isoformat()
        self.users.append(user_data)
        return user_data
    
    def create_chat(self, chat_data):
        chat_data['created_at'] = datetime.datetime.now().isoformat()
        chat_data['theme'] = random.choice(['purple', 'blue', 'pink', 'matrix'])
        self.chats.append(chat_data)
        return chat_data

chat_manager = AdvancedChatManager()

def generate_username():
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный', 'Голографический']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр', 'Орёл']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(1000, 9999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(16))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DL-TrolledX ✨ Ультра-Футуристический Мессенджер</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #111111;
            --bg-card: #1a1a1a;
            --bg-input: #222222;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --accent-purple: #8b5cf6;
            --accent-pink: #ec4899;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-cyan: #06b6d4;
            --gradient-primary: linear-gradient(135deg, #8b5cf6, #ec4899, #3b82f6);
            --gradient-secondary: linear-gradient(135deg, #1a1a1a, #2d1b69);
            --shadow-glow: 0 0 50px rgba(139, 92, 246, 0.3);
            --border-glow: 1px solid rgba(139, 92, 246, 0.3);
        }

        body {
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes slideInUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
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
            overflow-y: auto;
        }

        .auth-container {
            background: var(--bg-card);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 480px;
            position: relative;
            overflow: hidden;
            border: var(--border-glow);
            box-shadow: var(--shadow-glow);
            backdrop-filter: blur(20px);
            margin: 20px;
            animation: slideInUp 0.5s ease-out;
        }

        .auth-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: var(--gradient-primary);
            animation: gradientShift 8s ease infinite;
            opacity: 0.1;
            z-index: -1;
        }

        .logo {
            font-size: 3rem;
            font-weight: 800;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
            text-align: center;
            margin-bottom: 1rem;
        }

        .subtitle {
            color: var(--text-secondary);
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1.1rem;
            line-height: 1.6;
        }

        .btn {
            width: 100%;
            padding: 16px 24px;
            border: none;
            border-radius: 16px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
        }

        .btn-secondary {
            background: var(--bg-input);
            color: var(--text-primary);
            border: var(--border-glow);
        }

        .btn-secondary:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateY(-2px);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .feature-card {
            background: var(--bg-input);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: var(--border-glow);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            background: rgba(139, 92, 246, 0.1);
            box-shadow: var(--shadow-glow);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .credential-box {
            background: var(--bg-input);
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1.5rem 0;
            border: var(--border-glow);
            animation: pulse 2s infinite;
        }

        .credential-field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 0.5rem 0;
            padding: 0.75rem;
            background: var(--bg-secondary);
            border-radius: 12px;
        }

        .credential-value {
            font-family: 'Courier New', monospace;
            color: var(--accent-purple);
            font-weight: 600;
        }

        .copy-btn {
            background: var(--accent-purple);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }

        .copy-btn:hover {
            background: var(--accent-pink);
            transform: scale(1.05);
        }

        .floating-emoji {
            position: fixed;
            font-size: 2rem;
            z-index: 999;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
            pointer-events: none;
        }

        .hidden {
            display: none !important;
        }

        .stats-panel {
            background: var(--bg-card);
            padding: 1rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: var(--border-glow);
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: var(--bg-input);
            border-radius: 8px;
        }

        .progress-bar {
            width: 100%;
            height: 4px;
            background: var(--bg-input);
            border-radius: 2px;
            overflow: hidden;
            margin: 1rem 0;
        }

        .progress-fill {
            height: 100%;
            background: var(--gradient-primary);
            border-radius: 2px;
            transition: width 0.3s ease;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--gradient-primary);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 16px;
            z-index: 2000;
            animation: slideInUp 0.3s ease;
            box-shadow: var(--shadow-glow);
        }

        /* Чат интерфейс */
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-primary);
        }

        .chat-container {
            display: flex;
            height: 100vh;
            max-width: 100%;
            margin: 0;
            background: var(--bg-secondary);
            overflow: hidden;
        }

        .sidebar {
            width: 380px;
            background: var(--bg-card);
            border-right: var(--border-glow);
            display: flex;
            flex-direction: column;
        }

        .user-header {
            padding: 2rem;
            background: var(--gradient-secondary);
            border-bottom: var(--border-glow);
        }

        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .search-box {
            padding: 1.5rem;
            border-bottom: var(--border-glow);
        }

        .search-input {
            width: 100%;
            padding: 12px 16px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 0.9rem;
        }

        .chats-list {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 1rem;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
        }

        .chat-item:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateX(5px);
        }

        .chat-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            margin-right: 1rem;
        }

        .chat-info {
            flex: 1;
        }

        .chat-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .chat-preview {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
        }

        .chat-header {
            padding: 1.5rem 2rem;
            background: var(--bg-card);
            border-bottom: var(--border-glow);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .messages-container {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .message {
            max-width: 70%;
            padding: 1rem 1.5rem;
            border-radius: 20px;
            position: relative;
            animation: slideInUp 0.3s ease;
        }

        .message.received {
            background: var(--bg-input);
            align-self: flex-start;
            border-bottom-left-radius: 8px;
        }

        .message.sent {
            background: var(--gradient-primary);
            align-self: flex-end;
            border-bottom-right-radius: 8px;
        }

        .message-input-container {
            padding: 1.5rem 2rem;
            background: var(--bg-card);
            border-top: var(--border-glow);
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .message-input {
            flex: 1;
            padding: 12px 20px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 25px;
            color: var(--text-primary);
            font-size: 1rem;
        }

        .send-btn {
            padding: 12px 24px;
            background: var(--gradient-primary);
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        }

        @media (max-width: 768px) {
            .auth-container {
                padding: 2rem;
                margin: 1rem;
            }
            
            .logo {
                font-size: 2.5rem;
            }
            
            .chat-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: 50vh;
            }
        }
    </style>
</head>
<body>
    <!-- Плавающие элементы -->
    <div class="floating-emoji" style="top: 10%; left: 5%;">💫</div>
    <div class="floating-emoji" style="top: 15%; right: 8%;">✨</div>
    <div class="floating-emoji" style="top: 85%; left: 10%;">🚀</div>
    <div class="floating-emoji" style="top: 80%; right: 5%;">🌟</div>

    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen">
        <div class="auth-container">
            <div class="logo">DL-TrolledX</div>
            <div class="subtitle">Ультра-современный мессенджер с AI и космическим дизайном</div>
            
            <div class="stats-panel">
                <h4 style="margin-bottom: 1rem; text-align: center;">📊 Статистика платформы</h4>
                <div class="stat-item">
                    <span>Пользователей онлайн:</span>
                    <span style="color: var(--accent-purple); font-weight: 600;">1,247</span>
                </div>
                <div class="stat-item">
                    <span>Сообщений сегодня:</span>
                    <span style="color: var(--accent-pink); font-weight: 600;">8,492</span>
                </div>
                <div class="stat-item">
                    <span>Активных чатов:</span>
                    <span style="color: var(--accent-cyan); font-weight: 600;">356</span>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="startQuickRegistration()">
                🚀 Начать путешествие
            </button>
            
            <div class="feature-grid">
                <div class="feature-card" onclick="startQuickRegistration()">
                    <div class="feature-icon">🤖</div>
                    <div>AI Ассистент</div>
                </div>
                <div class="feature-card" onclick="showThemeSelector()">
                    <div class="feature-icon">🎨</div>
                    <div>Темы</div>
                </div>
                <div class="feature-card" onclick="showStats()">
                    <div class="feature-icon">📊</div>
                    <div>Статистика</div>
                </div>
                <div class="feature-card" onclick="showFeatures()">
                    <div class="feature-icon">⚡</div>
                    <div>Функции</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">Создание аккаунта</div>
            <div class="subtitle">Ваш цифровой пропуск в будущее общения</div>
            
            <div class="credential-box">
                <div class="credential-field">
                    <span>👤 Имя:</span>
                    <span class="credential-value" id="generatedName">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 Пароль:</span>
                    <span class="credential-value" id="generatedPassword">...</span>
                    <button class="copy-btn" onclick="copyToClipboard('generatedPassword')">📋</button>
                </div>
                <div class="credential-field">
                    <span>🆔 ID:</span>
                    <span class="credential-value" id="generatedUsername">...</span>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="registerProgress" style="width: 0%"></div>
            </div>
            
            <button class="btn btn-primary" onclick="quickRegister()">
                💫 Войти в DL-TrolledX
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewCredentials()">
                🔄 Обновить данные
            </button>
            
            <button class="btn btn-secondary" onclick="showScreen('welcomeScreen')">
                ← Назад
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="chat-container">
            <!-- Боковая панель -->
            <div class="sidebar">
                <div class="user-header">
                    <div class="user-avatar" id="userAvatar">😊</div>
                    <h3 id="userName">Пользователь</h3>
                    <p id="userStatus" style="color: var(--accent-purple);">● онлайн</p>
                </div>
                
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="🔍 Поиск чатов..." oninput="searchChats(this.value)">
                </div>
                
                <div class="chats-list" id="chatsList">
                    <!-- Список чатов будет здесь -->
                </div>
            </div>
            
            <!-- Область чата -->
            <div class="chat-area">
                <div class="chat-header">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div class="chat-avatar" id="currentChatAvatar">👤</div>
                        <div>
                            <h3 id="currentChatName">Выберите чат</h3>
                            <p id="currentChatStatus" style="color: var(--text-secondary);">для начала общения</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 1rem;">
                        <button class="btn-secondary" onclick="showSettings()">⚙️</button>
                        <button class="btn-secondary" onclick="logout()">🚪</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">💬</div>
                        <h3>Добро пожаловать в DL-TrolledX!</h3>
                        <p>Выберите чат или создайте новый для начала общения</p>
                    </div>
                </div>
                
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="Напишите сообщение..." id="messageInput" onkeypress="if(event.key=='Enter') sendMessage()">
                    <button class="send-btn" onclick="sendMessage()">Отправить</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let userStats = {
            messagesSent: 0,
            chatsCreated: 0,
            logins: 0,
            timeSpent: 0
        };

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DL-TrolledX запущен!");
            checkAutoLogin();
            initializeSampleData();
        });

        function initializeSampleData() {
            allUsers = [
                {
                    id: 'user1',
                    name: 'Алексей',
                    username: '@neuro_alex',
                    avatar: '🤖',
                    isOnline: true,
                    bio: 'AI разработчик'
                },
                {
                    id: 'user2', 
                    name: 'София',
                    username: '@digital_queen',
                    avatar: '👑',
                    isOnline: true,
                    bio: 'Дизайнер интерфейсов'
                },
                {
                    id: 'user3',
                    name: 'Максим',
                    username: '@code_master',
                    avatar: '💻',
                    isOnline: false,
                    bio: 'Full-stack разработчик'
                }
            ];

            const savedChats = localStorage.getItem('nebula_chats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
            
            const savedStats = localStorage.getItem('nebula_stats');
            if (savedStats) {
                userStats = JSON.parse(savedStats);
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('nebula_currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                userStats.logins++;
                saveUserStats();
                showMainApp();
                showNotification(`С возвращением, ${currentUser.name}! 🌟`, 'success');
            }
        }

        function saveUserStats() {
            localStorage.setItem('nebula_stats', JSON.stringify(userStats));
        }

        function showScreen(screenId) {
            console.log('Переход на экран:', screenId);
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            document.getElementById(screenId).classList.remove('hidden');
        }

        function startQuickRegistration() {
            console.log('Запуск регистрации');
            showScreen('registerScreen');
            generateNewCredentials();
        }

        function showManualLogin() {
            showNotification('Ручной вход будет доступен в следующем обновлении! 🔄', 'info');
        }

        function showFeatures() {
            showNotification(`
                🚀 Возможности DL-TrolledX:
                • AI-ассистент в чатах
                • Сквозное шифрование
                • Голосовые сообщения
                • Видеозвонки
                • Кастомизация тем
            `, 'info');
        }

        function showThemeSelector() {
            showNotification('Выбор темы будет в следующем обновлении! 🎨', 'info');
        }

        function showStats() {
            showNotification('Подробная статистика будет доступна в профиле! 📊', 'info');
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            const username = '@' + name.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
            document.getElementById('generatedUsername').textContent = username;
            
            animateProgress('registerProgress', 100, 1000);
        }

        function generateUsername() {
            const adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой'];
            const nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк'];
            return `${randomChoice(adjectives)}${randomChoice(nouns)}${Math.floor(Math.random() * 1000)}`;
        }

        function generatePassword() {
            const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
            let password = '';
            for (let i = 0; i < 12; i++) {
                password += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            return password;
        }

        function randomChoice(array) {
            return array[Math.floor(Math.random() * array.length)];
        }

        function animateProgress(elementId, to, duration) {
            const element = document.getElementById(elementId);
            let start = 0;
            const increment = to / (duration / 10);
            
            const timer = setInterval(() => {
                start += increment;
                element.style.width = Math.min(start, to) + '%';
                if (start >= to) clearInterval(timer);
            }, 10);
        }

        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Скопировано в буфер обмена! 📋', 'success');
            });
        }

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            const username = document.getElementById('generatedUsername').textContent;
            
            if (!name || name === '...') {
                showNotification('Сначала сгенерируйте данные!', 'error');
                return;
            }
            
            const avatars = ['😎', '🤖', '👽', '🐲', '🦄'];
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: username,
                avatar: randomChoice(avatars),
                isOnline: true,
                bio: 'Исследователь цифровых миров 🌌',
                password: password
            };
            
            localStorage.setItem('nebula_currentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            saveUserStats();
            
            showMainApp();
            showNotification(`Добро пожаловать в DL-TrolledX, ${name}! 🚀`, 'success');
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById('mainApp').classList.remove('hidden');
            
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            
            renderChatsList();
            startTimeTracking();
        }

        function renderChatsList() {
            const chatsList = document.getElementById('chatsList');
            
            if (chats.length === 0) {
                chatsList.innerHTML = `
                    <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                        <p>Чатов пока нет</p>
                        <button class="btn-secondary" onclick="createSampleChats()" style="margin-top: 1rem;">
                            Создать тестовые чаты
                        </button>
                    </div>
                `;
                return;
            }
            
            chatsList.innerHTML = chats.map(chat => {
                const otherUser = allUsers.find(u => u.id === chat.participants.find(p => p !== currentUser.id));
                if (!otherUser) return '';
                
                return `
                    <div class="chat-item" onclick="openChat('${chat.id}')">
                        <div class="chat-avatar">${otherUser.avatar}</div>
                        <div class="chat-info">
                            <div class="chat-name">${otherUser.name}</div>
                            <div class="chat-preview">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function createSampleChats() {
            allUsers.forEach(user => {
                if (user.id !== currentUser.id) {
                    const newChat = {
                        id: 'chat_' + Date.now() + Math.random(),
                        participants: [currentUser.id, user.id],
                        lastMessage: {
                            text: 'Привет! 👋',
                            senderId: user.id,
                            timestamp: new Date().toISOString()
                        },
                        messages: [
                            {
                                id: '1',
                                text: `Привет! Я ${user.name}. Рад познакомиться!`,
                                senderId: user.id,
                                timestamp: new Date().toISOString()
                            }
                        ]
                    };
                    chats.push(newChat);
                }
            });
            
            localStorage.setItem('nebula_chats', JSON.stringify(chats));
            renderChatsList();
            showNotification('Тестовые чаты созданы! 🎉', 'success');
        }

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== currentUser.id));
            if (!otherUser) return;
            
            document.getElementById('currentChatName').textContent = otherUser.name;
            document.getElementById('currentChatAvatar').textContent = otherUser.avatar;
            document.getElementById('currentChatStatus').textContent = otherUser.isOnline ? '● онлайн' : '● был(а) недавно';
            
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = currentChat.messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                return `
                    <div class="message ${isOwn ? 'sent' : 'received'}">
                        ${msg.text}
                    </div>
                `;
            }).join('');
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                const newMessage = {
                    id: Date.now().toString(),
                    text: message,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                
                localStorage.setItem('nebula_chats', JSON.stringify(chats));
                
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.textContent = message;
                messagesContainer.appendChild(messageElement);
                
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                userStats.messagesSent++;
                saveUserStats();
                
                setTimeout(() => {
                    if (Math.random() > 0.3) {
                        sendAutoReply();
                    }
                }, 1000 + Math.random() * 2000);
            }
        }

        function sendAutoReply() {
            if (!currentChat) return;
            
            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== currentUser.id));
            if (!otherUser) return;
            
            const replies = [
                'Интересно! Расскажи подробнее 🤔',
                'Отличная мысль! 💫',
                'Согласен с тобой! 👍',
                'А что если попробовать по-другому? 🔄'
            ];
            
            const replyMessage = {
                id: Date.now().toString() + '_reply',
                text: randomChoice(replies),
                senderId: otherUser.id,
                timestamp: new Date().toISOString()
            };
            
            currentChat.messages.push(replyMessage);
            currentChat.lastMessage = replyMessage;
            
            localStorage.setItem('nebula_chats', JSON.stringify(chats));
            
            const messagesContainer = document.getElementById('messagesContainer');
            const messageElement = document.createElement('div');
            messageElement.className = 'message received';
            messageElement.textContent = replyMessage.text;
            messagesContainer.appendChild(messageElement);
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function searchChats(query) {
            console.log('Поиск:', query);
        }

        function showSettings() {
            showNotification('Настройки будут доступны в следующем обновлении! ⚙️', 'info');
        }

        function logout() {
            if (confirm('Выйти из аккаунта?')) {
                currentUser = null;
                localStorage.removeItem('nebula_currentUser');
                showScreen('welcomeScreen');
                showNotification('До скорой встречи! 👋', 'info');
            }
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 4000);
        }

        function startTimeTracking() {
            setInterval(() => {
                if (currentUser) {
                    userStats.timeSpent++;
                    if (userStats.timeSpent % 10 === 0) {
                        saveUserStats();
                    }
                }
            }, 60000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'status': 'online',
        'users_online': random.randint(50, 100),
        'version': '1.0',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'DL-TrolledX'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 DL-TrolledX запущен!")
    print("💫 Ультра-современный дизайн")
    print("🎨 Фиолетовая неоновая тема") 
    print("⚡ AI функции и анимации")
    print(f"🔗 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
