# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import time
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramodern2024'

class AdvancedChatManager:
    def __init__(self):
        self.users = []
        self.chats = []
        self.messages = []
        self.calls = []
    
    def add_user(self, user_data):
        user_data['premium'] = random.choice([True, False, False])
        user_data['join_date'] = datetime.datetime.now().isoformat()
        user_data['level'] = random.randint(1, 100)
        user_data['xp'] = random.randint(100, 5000)
        self.users.append(user_data)
        return user_data
    
    def create_chat(self, chat_data):
        chat_data['created_at'] = datetime.datetime.now().isoformat()
        chat_data['theme'] = random.choice(['purple', 'blue', 'pink', 'matrix', 'cyber', 'galaxy'])
        chat_data['unread'] = random.randint(0, 5)
        self.chats.append(chat_data)
        return chat_data
    
    def start_call(self, call_data):
        call_data['id'] = str(uuid.uuid4())
        call_data['started_at'] = datetime.datetime.now().isoformat()
        call_data['status'] = 'active'
        self.calls.append(call_data)
        return call_data

chat_manager = AdvancedChatManager()

def generate_username():
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный', 'Голографический', 
                 'Квантовый', 'Кибернетический', 'Астральный', 'Нейронный', 'Плазменный', 'Сверхсветовой']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр', 'Орёл', 'Робот', 'Андроид', 'Киберг', 'Дроид', 'Сфинкс', 'Грифон']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(1000, 9999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(16))

def get_user_rank(level):
    if level < 10: 
        return "Новичок 🌱"
    elif level < 25: 
        return "Исследователь 🚀"
    elif level < 50: 
        return "Эксперт 💫"
    elif level < 75: 
        return "Мастер 🏆"
    else: 
        return "Легенда 👑"

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
            -webkit-tap-highlight-color: transparent;
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
            --accent-orange: #f59e0b;
            --accent-gold: #fbbf24;
            --gradient-primary: linear-gradient(135deg, #8b5cf6, #ec4899, #3b82f6);
            --gradient-secondary: linear-gradient(135deg, #1a1a1a, #2d1b69);
            --gradient-gold: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706);
            --gradient-premium: linear-gradient(135deg, #8b5cf6, #3b82f6, #06b6d4);
            --shadow-glow: 0 0 50px rgba(139, 92, 246, 0.3);
            --shadow-intense: 0 0 80px rgba(139, 92, 246, 0.5);
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
                radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                linear-gradient(45deg, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
            touch-action: manipulation;
        }

        /* Оптимизированные анимации для мобильных */
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        @keyframes pulse3D {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @keyframes slideInUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
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
            -webkit-overflow-scrolling: touch;
        }

        .auth-container {
            background: var(--bg-card);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            max-width: 500px;
            position: relative;
            overflow: hidden;
            border: var(--border-glow);
            box-shadow: var(--shadow-intense);
            backdrop-filter: blur(20px);
            animation: slideInUp 0.6s ease-out;
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 900;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn {
            width: 100%;
            padding: 16px 20px;
            border: none;
            border-radius: 15px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            min-height: 54px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        }

        .btn-secondary {
            background: var(--bg-input);
            color: var(--text-primary);
            border: var(--border-glow);
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
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: var(--border-glow);
        }

        .hidden {
            display: none !important;
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
            position: relative;
        }

        .sidebar {
            width: 100%;
            max-width: 400px;
            background: var(--bg-card);
            border-right: var(--border-glow);
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 2;
        }

        .user-header {
            padding: 1.5rem;
            background: var(--gradient-secondary);
            border-bottom: var(--border-glow);
        }

        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 15px;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .nav-tabs {
            display: flex;
            background: var(--bg-input);
            border-radius: 12px;
            padding: 4px;
            margin: 1rem 0;
        }

        .nav-tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .nav-tab.active {
            background: var(--gradient-primary);
            color: white;
        }

        .search-box {
            padding: 1rem;
            border-bottom: var(--border-glow);
        }

        .search-input {
            width: 100%;
            padding: 14px 16px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 1rem;
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            -webkit-overflow-scrolling: touch;
        }

        .chat-item, .call-item {
            display: flex;
            align-items: center;
            padding: 1rem;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
            background: rgba(255,255,255,0.02);
            border: 1px solid transparent;
        }

        .chat-item:hover, .call-item:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateX(5px);
        }

        .call-actions {
            display: flex;
            gap: 0.5rem;
            margin-left: auto;
        }

        .call-btn {
            padding: 8px 12px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .call-video {
            background: var(--accent-blue);
            color: white;
        }

        .call-voice {
            background: var(--accent-green);
            color: white;
        }

        /* Звонок интерфейс */
        .call-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-primary);
            z-index: 3000;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 2rem;
        }

        .call-header {
            text-align: center;
            margin-top: 2rem;
        }

        .call-avatar {
            width: 120px;
            height: 120px;
            border-radius: 30px;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            margin: 0 auto 1rem;
        }

        .call-controls {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .control-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .call-end {
            background: #ef4444;
            color: white;
        }

        .call-accept {
            background: var(--accent-green);
            color: white;
        }

        .call-mute {
            background: var(--bg-input);
            color: var(--text-primary);
        }

        /* Мобильная оптимизация */
        @media (max-width: 768px) {
            .auth-container {
                padding: 20px;
                margin: 10px;
                border-radius: 15px;
            }
            
            .logo {
                font-size: 2rem;
            }
            
            .btn {
                padding: 14px 18px;
                font-size: 0.9rem;
                min-height: 50px;
            }
            
            .feature-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.8rem;
            }
            
            .feature-card {
                padding: 1rem;
            }
            
            .sidebar {
                position: absolute;
                height: 100%;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 1000;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .mobile-menu-btn {
                display: block !important;
            }
            
            .call-controls {
                gap: 0.8rem;
            }
            
            .control-btn {
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }
        }

        @media (max-width: 480px) {
            .auth-container {
                padding: 15px;
            }
            
            .logo {
                font-size: 1.8rem;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
            }
            
            .call-avatar {
                width: 100px;
                height: 100px;
                font-size: 2.5rem;
            }
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text-primary);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 8px;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--gradient-primary);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 15px;
            z-index: 2000;
            animation: slideInUp 0.5s ease;
            box-shadow: var(--shadow-intense);
            max-width: 300px;
            font-weight: 600;
        }

        .logout-btn {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
            border: 1px solid #ef4444;
            margin-top: 1rem;
        }

        .logout-btn:hover {
            background: #ef4444;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen loading-screen">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <div style="font-size: 1.2rem; color: var(--text-secondary);">Запускаем DL-TrolledX...</div>
        </div>
    </div>

    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">DL-TrolledX</div>
            <div style="color: var(--text-secondary); text-align: center; margin-bottom: 2rem;">
                УЛЬТРАСОВРЕМЕННЫЙ МЕССЕНДЖЕР С VOIP ЗВОНКАМИ
            </div>
            
            <button class="btn btn-primary" onclick="startQuickRegistration()">
                🚀 НАЧАТЬ ИСПОЛЬЗОВАТЬ
            </button>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📞</div>
                    <div>VOIP Звонки</div>
                </div>
                <div class="feature-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
                    <div>Без блокировок</div>
                </div>
                <div class="feature-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
                    <div>Быстрая связь</div>
                </div>
                <div class="feature-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌐</div>
                    <div>Обход РКН</div>
                </div>
            </div>

            <div style="text-align: center; color: var(--accent-purple); margin-top: 1rem;">
                Работает в обход блокировок 🔓
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">РЕГИСТРАЦИЯ</div>
            
            <div style="background: var(--bg-input); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span>👤 Имя пользователя:</span>
                    <span style="color: var(--accent-purple); font-weight: 700;" id="generatedName">...</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span>🔐 Пароль:</span>
                    <span style="color: var(--accent-purple); font-weight: 700;" id="generatedPassword">...</span>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="quickRegister()">
                💫 СОЗДАТЬ АККАУНТ
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewCredentials()">
                🔄 СГЕНЕРИРОВАТЬ НОВЫЕ
            </button>
            
            <button class="btn btn-secondary" onclick="showScreen('welcomeScreen')">
                ← НАЗАД
            </button>

            <div style="text-align: center; color: var(--text-secondary); margin-top: 1rem;">
                Данные сохраняются локально 🔒
            </div>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="chat-container">
            <!-- Боковая панель -->
            <div class="sidebar" id="sidebar">
                <div class="user-header">
                    <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                    <div class="user-avatar" id="userAvatar">😊</div>
                    <h3 id="userName">Пользователь</h3>
                    <p style="color: var(--accent-cyan);">Уровень: <span id="userLevel">1</span></p>
                    
                    <div class="nav-tabs">
                        <div class="nav-tab active" onclick="switchTab('chats')">💬 Чаты</div>
                        <div class="nav-tab" onclick="switchTab('calls')">📞 Звонки</div>
                        <div class="nav-tab" onclick="switchTab('contacts')">👥 Контакты</div>
                    </div>
                </div>
                
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="🔍 Поиск..." id="searchInput">
                </div>
                
                <div class="content-list" id="contentList">
                    <!-- Контент будет здесь -->
                </div>

                <div style="padding: 1rem;">
                    <button class="btn logout-btn" onclick="showLogoutConfirm()">
                        🚪 Выйти из аккаунта
                    </button>
                </div>
            </div>
            
            <!-- Область чата -->
            <div class="chat-area">
                <div style="display: flex; flex-direction: column; height: 100%;">
                    <div style="padding: 1rem; background: var(--bg-card); border-bottom: var(--border-glow);">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                            <div>
                                <h3 id="currentChatName">Выберите чат</h3>
                                <p style="color: var(--text-secondary);" id="currentChatStatus">для начала общения</p>
                            </div>
                        </div>
                    </div>
                    
                    <div style="flex: 1; padding: 1rem; overflow-y: auto;" id="messagesContainer">
                        <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                            <div style="font-size: 4rem; margin-bottom: 1rem;">📞</div>
                            <h3 style="margin-bottom: 1rem;">Добро пожаловать в DL-TrolledX!</h3>
                            <p>Выберите чат или начните звонок</p>
                        </div>
                    </div>
                    
                    <div style="padding: 1rem; background: var(--bg-card); border-top: var(--border-glow);">
                        <div style="display: flex; gap: 0.5rem;">
                            <input type="text" style="flex: 1; padding: 12px; background: var(--bg-input); border: var(--border-glow); border-radius: 10px; color: var(--text-primary);" 
                                   placeholder="Введите сообщение..." id="messageInput">
                            <button style="padding: 12px 20px; background: var(--gradient-primary); border: none; border-radius: 10px; color: white; cursor: pointer;">
                                Отправить
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Экран звонка -->
    <div id="callScreen" class="call-screen">
        <div class="call-header">
            <div class="call-avatar" id="callAvatar">👤</div>
            <h2 id="callUserName">Имя пользователя</h2>
            <p id="callStatus" style="color: var(--text-secondary);">Звонок...</p>
            <p id="callTimer" style="font-size: 1.5rem; font-weight: bold; margin-top: 0.5rem;">00:00</p>
        </div>
        
        <div class="call-controls">
            <button class="control-btn call-mute" onclick="toggleMute()">🎤</button>
            <button class="control-btn call-end" onclick="endCall()">📞</button>
            <button class="control-btn call-mute" onclick="toggleVideo()">📹</button>
        </div>
    </div>

    <!-- Подтверждение выхода -->
    <div id="logoutConfirm" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 4000; align-items: center; justify-content: center;">
        <div style="background: var(--bg-card); padding: 2rem; border-radius: 15px; max-width: 400px; margin: 1rem;">
            <h3 style="margin-bottom: 1rem;">Подтверждение выхода</h3>
            <p style="margin-bottom: 1.5rem; color: var(--text-secondary);">Вы уверены, что хотите выйти? Ваши данные будут сохранены.</p>
            <div style="display: flex; gap: 1rem;">
                <button class="btn btn-secondary" onclick="hideLogoutConfirm()" style="flex: 1;">Отмена</button>
                <button class="btn logout-btn" onclick="logout()" style="flex: 1;">Выйти</button>
            </div>
        </div>
    </div>

    <script>
        let currentUser = null;
        let currentTab = 'chats';
        let callTimer = null;
        let callStartTime = null;
        let isMuted = false;

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                hideLoadingScreen();
                initializeApp();
            }, 1500);
        });

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function initializeApp() {
            const savedUser = localStorage.getItem('dl_trolledx_currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
                showNotification('С возвращением, ' + currentUser.name + '! 🚀', 'success');
            } else {
                showScreen('welcomeScreen');
            }
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

        function startQuickRegistration() {
            showScreen('registerScreen');
            generateNewCredentials();
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
        }

        function generateUsername() {
            const adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный'];
            const nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр'];
            return adjectives[Math.floor(Math.random() * adjectives.length)] + 
                   nouns[Math.floor(Math.random() * nouns.length)] + 
                   Math.floor(Math.random() * 1000);
        }

        function generatePassword() {
            const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
            let password = '';
            for (let i = 0; i < 12; i++) {
                password += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            return password;
        }

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            
            const avatars = ['😎', '🤖', '👽', '🐲', '🦄', '⚡', '🌟', '💫'];
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                avatar: avatars[Math.floor(Math.random() * avatars.length)],
                level: Math.floor(Math.random() * 50) + 1,
                premium: Math.random() > 0.7
            };
            
            localStorage.setItem('dl_trolledx_currentUser', JSON.stringify(currentUser));
            
            showMainApp();
            showNotification('Аккаунт создан! Добро пожаловать в DL-TrolledX! 🎉', 'success');
        }

        function showMainApp() {
            showScreen('mainApp');
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userLevel').textContent = currentUser.level;
            
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

            if (currentTab === 'chats') {
                contentList.innerHTML = getChatsList(searchTerm);
            } else if (currentTab === 'calls') {
                contentList.innerHTML = getCallsList(searchTerm);
            } else if (currentTab === 'contacts') {
                contentList.innerHTML = getContactsList(searchTerm);
            }
        }

        function getChatsList(searchTerm) {
            const sampleChats = [
                {id: 1, name: 'Техподдержка', avatar: '🔧', lastMessage: 'Чем можем помочь?', unread: 2},
                {id: 2, name: 'Общий чат', avatar: '👥', lastMessage: 'Добро пожаловать!', unread: 0},
                {id: 3, name: 'Новости', avatar: '📰', lastMessage: 'Новые обновления', unread: 5}
            ];

            return sampleChats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            ).map(chat => `
                <div class="chat-item" onclick="openChat(${chat.id})">
                    <div style="width: 50px; height: 50px; border-radius: 12px; background: var(--gradient-primary); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-right: 1rem;">
                        ${chat.avatar}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${chat.lastMessage}</div>
                    </div>
                    ${chat.unread > 0 ? `<div style="background: var(--accent-pink); color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700;">${chat.unread}</div>` : ''}
                </div>
            `).join('');
        }

        function getCallsList(searchTerm) {
            const sampleUsers = [
                {id: 1, name: 'Алексей', avatar: '👨‍💻', online: true},
                {id: 2, name: 'Мария', avatar: '👩‍🎨', online: true},
                {id: 3, name: 'Дмитрий', avatar: '👨‍🔬', online: false},
                {id: 4, name: 'Анна', avatar: '👩‍💼', online: true},
                {id: 5, name: 'Сергей', avatar: '👨‍🚀', online: false}
            ];

            return sampleUsers.filter(user => 
                user.name.toLowerCase().includes(searchTerm)
            ).map(user => `
                <div class="call-item">
                    <div style="width: 50px; height: 50px; border-radius: 12px; background: var(--gradient-primary); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-right: 1rem;">
                        ${user.avatar}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700;">${user.name}</div>
                        <div style="color: ${user.online ? 'var(--accent-green)' : 'var(--text-secondary)'}; font-size: 0.9rem;">
                            ${user.online ? '● онлайн' : '● офлайн'}
                        </div>
                    </div>
                    <div class="call-actions">
                        <button class="call-btn call-voice" onclick="startVoiceCall(${user.id})">📞</button>
                        <button class="call-btn call-video" onclick="startVideoCall(${user.id})">📹</button>
                    </div>
                </div>
            `).join('');
        }

        function getContactsList(searchTerm) {
            const contacts = [
                {name: 'Техподдержка', avatar: '🔧', role: 'Помощь и поддержка'},
                {name: 'Администратор', avatar: '👑', role: 'Управление системой'},
                {name: 'Модератор', avatar: '🛡️', role: 'Контроль качества'}
            ];

            return contacts.filter(contact => 
                contact.name.toLowerCase().includes(searchTerm)
            ).map(contact => `
                <div class="chat-item">
                    <div style="width: 50px; height: 50px; border-radius: 12px; background: var(--gradient-primary); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-right: 1rem;">
                        ${contact.avatar}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700;">${contact.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${contact.role}</div>
                    </div>
                </div>
            `).join('');
        }

        function openChat(chatId) {
            // Здесь будет логика открытия чата
            showNotification('Чат открыт', 'success');
        }

        function startVoiceCall(userId) {
            const user = getCallsList('').find(u => u.id === userId);
            if (user) {
                showCallScreen(user, 'voice');
            }
        }

        function startVideoCall(userId) {
            const user = getCallsList('').find(u => u.id === userId);
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
            clearInterval(callTimer);
            document.getElementById('callScreen').style.display = 'none';
            showNotification('Звонок завершен', 'info');
        }

        function toggleMute() {
            isMuted = !isMuted;
            showNotification(isMuted ? 'Микрофон выключен' : 'Микрофон включен', 'info');
        }

        function toggleVideo() {
            showNotification('Функция видео временно недоступна', 'info');
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showLogoutConfirm() {
            document.getElementById('logoutConfirm').style.display = 'flex';
        }

        function hideLogoutConfirm() {
            document.getElementById('logoutConfirm').style.display = 'none';
        }

        function logout() {
            localStorage.removeItem('dl_trolledx_currentUser');
            showScreen('welcomeScreen');
            showNotification('Вы вышли из аккаунта. Данные сохранены.', 'info');
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.style.background = type === 'error' ? '#ef4444' : 
                                           type === 'success' ? 'var(--accent-green)' : 
                                           'var(--gradient-primary)';
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Поиск
        document.getElementById('searchInput').addEventListener('input', loadContent);

        // Закрытие сайдбара при клике вне его на мобильных
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'status': 'online',
        'users_online': random.randint(1000, 5000),
        'calls_active': random.randint(50, 200),
        'version': '2.0_voip'
    })

@app.route('/api/start_call', methods=['POST'])
def start_call():
    data = request.json
    call_data = chat_manager.start_call(data)
    return jsonify(call_data)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'DL-TrolledX VoIP'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
