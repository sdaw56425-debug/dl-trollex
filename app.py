# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ХЕЛЛОУИН 2025 + РЕАЛЬНЫЕ ПОЛЬЗОВАТЕЛИ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

# База данных в памяти
users_db = {}
messages_db = {}
chats_db = {}
stories_db = {}
streams_db = {}

# Реальные пользователи (без ботов)
real_users = [
    {
        'id': 'user_real_1',
        'name': 'Алексей Кодеров',
        'username': '@alex_coder',
        'email': 'alex.coder@mail.ru',
        'avatar': '👨‍💻',
        'isOnline': True,
        'lastSeen': datetime.datetime.now().isoformat(),
        'bio': 'Fullstack разработчик | Люблю Python и JS | Играю на гитаре',
        'registered': datetime.datetime.now().isoformat(),
        'city': 'Москва',
        'age': 28,
        'interests': ['Программирование', 'Музыка', 'Путешествия']
    },
    {
        'id': 'user_real_2', 
        'name': 'Мария Дизайнерова',
        'username': '@maria_design',
        'email': 'maria.design@yandex.ru',
        'avatar': '👩‍🎨',
        'isOnline': True,
        'lastSeen': datetime.datetime.now().isoformat(),
        'bio': 'UI/UX дизайнер | Люблю искусство и кофе | Фотографирую',
        'registered': datetime.datetime.now().isoformat(),
        'city': 'Санкт-Петербург',
        'age': 25,
        'interests': ['Дизайн', 'Фотография', 'Искусство']
    },
    {
        'id': 'user_real_3', 
        'name': 'Дмитрий Геймеров',
        'username': '@dima_gamer',
        'email': 'dima.gamer@gmail.com',
        'avatar': '🎮',
        'isOnline': False,
        'lastSeen': datetime.datetime.now().isoformat(),
        'bio': 'Профессиональный геймер | Стример | Кибеспортсмен',
        'registered': datetime.datetime.now().isoformat(),
        'city': 'Новосибирск',
        'age': 22,
        'interests': ['Игры', 'Стриминг', 'Технологии']
    },
    {
        'id': 'user_real_4',
        'name': 'Анна Ученова',
        'username': '@anna_science',
        'email': 'anna.science@mail.ru',
        'avatar': '🔬',
        'isOnline': True,
        'lastSeen': datetime.datetime.now().isoformat(),
        'bio': 'Ученый-биолог | Исследую ДНК | Люблю природу',
        'registered': datetime.datetime.now().isoformat(),
        'city': 'Казань',
        'age': 30,
        'interests': ['Наука', 'Природа', 'Исследования']
    },
    {
        'id': 'user_real_5',
        'name': 'Сергей Спортов',
        'username': '@serg_sport',
        'email': 'serg.sport@yandex.ru',
        'avatar': '🏃‍♂️',
        'isOnline': False,
        'lastSeen': datetime.datetime.now().isoformat(),
        'bio': 'Фитнес-тренер | ЗОЖ | Питание и тренировки',
        'registered': datetime.datetime.now().isoformat(),
        'city': 'Екатеринбург',
        'age': 26,
        'interests': ['Спорт', 'Здоровье', 'Питание']
    },
    {
        'id': 'user_real_6',
        'name': 'Ольга Творческая',
        'username': '@olga_artist',
        'email': 'olga.artist@gmail.com',
        'avatar': '🎨',
        'isOnline': True,
        'lastSeen': datetime.datetime.now().isoformat(),
        'bio': 'Художник | Иллюстратор | Преподаю искусство',
        'registered': datetime.datetime.now().isoformat(),
        'city': 'Ростов-на-Дону',
        'age': 27,
        'interests': ['Живопись', 'Рисование', 'Преподавание']
    }
]

def generate_username():
    adjectives = ['Весёлый', 'Серьёзный', 'Смелый', 'Умный', 'Быстрый', 'Креативный', 'Яркий', 'Тайный', 'Фиолетовый', 'Хеллоуинский']
    nouns = ['Единорог', 'Дракон', 'Волк', 'Феникс', 'Тигр', 'Орёл', 'Кот', 'Призрак', 'Тыква', 'Паук']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(100, 999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(12))

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'DLtrollex is running'})

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex 🎃</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎃</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }
        
        :root {
            --bg-color: #0f0f0f;
            --card-color: #1a1a1a;
            --accent-color: #8b5cf6;
            --text-color: #ffffff;
            --secondary-color: #2d2d2d;
            --border-color: #3d3d3d;
            --halloween-color: #ff7b25;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --story-color: #ec4899;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
            transition: all 0.3s ease;
            touch-action: manipulation;
        }
        
        body.halloween-theme {
            --accent-color: #ff7b25;
            --bg-color: #1a0f00;
            --card-color: #2a1a00;
            --secondary-color: #3a2a00;
        }
        
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 10px var(--accent-color), 0 0 20px var(--accent-color);
            }
            50% {
                text-shadow: 0 0 20px var(--accent-color), 0 0 30px var(--accent-color), 0 0 40px var(--accent-color);
            }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes recording {
            0%, 100% { transform: scale(1); background: #ef4444; }
            50% { transform: scale(1.2); background: #ff6b6b; }
        }
        
        @keyframes storyProgress {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        
        .glowing-logo {
            animation: glow 3s ease-in-out infinite;
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        .recording {
            animation: recording 1s ease-in-out infinite;
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
            background: linear-gradient(135deg, var(--bg-color) 0%, var(--card-color) 100%);
            z-index: 1000;
            padding: 20px;
        }
        
        .auth-box {
            background: var(--card-color);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 2px solid var(--accent-color);
            width: 100%;
            max-width: 450px;
            text-align: center;
            position: relative;
            overflow: hidden;
            z-index: 1001;
        }
        
        .auth-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, var(--accent-color), transparent);
            animation: shine 3s linear infinite;
            opacity: 0.1;
        }
        
        @keyframes shine {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .logo {
            font-size: 42px;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 15px;
        }
        
        .subtitle {
            color: #888;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            min-height: 50px;
            display: flex !important;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1002;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn-voice {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }
        
        .btn-story {
            background: linear-gradient(135deg, #ec4899, #db2777);
        }
        
        .btn-stream {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        }
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
        }
        
        /* Стили для голосовых сообщений */
        .voice-message {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 20px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .voice-message:hover {
            background: var(--accent-color);
        }
        
        .voice-play-btn {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        
        .voice-waveform {
            flex: 1;
            height: 30px;
            background: linear-gradient(90deg, var(--accent-color) 0%, transparent 100%);
            border-radius: 15px;
            position: relative;
            overflow: hidden;
        }
        
        .voice-duration {
            color: #888;
            font-size: 12px;
        }
        
        /* Стили для историй */
        .stories-container {
            display: flex;
            gap: 15px;
            padding: 20px;
            overflow-x: auto;
            background: var(--card-color);
            border-bottom: 1px solid var(--border-color);
        }
        
        .story-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            position: relative;
        }
        
        .story-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #ffa726, #4ecdc4, #45b7d1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-bottom: 5px;
            border: 3px solid var(--story-color);
            padding: 2px;
        }
        
        .story-username {
            font-size: 12px;
            color: #888;
            max-width: 70px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .story-viewer {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 2000;
            display: none;
        }
        
        .story-progress {
            display: flex;
            gap: 5px;
            padding: 20px;
        }
        
        .story-progress-bar {
            height: 3px;
            background: #555;
            flex: 1;
            border-radius: 2px;
            overflow: hidden;
        }
        
        .story-progress-fill {
            height: 100%;
            background: white;
            width: 0%;
            transition: width 0.1s linear;
        }
        
        /* Стили для стримов */
        .streams-container {
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .stream-card {
            background: var(--card-color);
            border-radius: 15px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stream-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .stream-preview {
            width: 100%;
            height: 180px;
            background: linear-gradient(45deg, #8b5cf6, #ec4899);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
        }
        
        .stream-info {
            padding: 15px;
        }
        
        .stream-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stream-stats {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #888;
            font-size: 12px;
        }
        
        .live-badge {
            background: #ef4444;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 10px;
            animation: pulse 2s infinite;
        }
        
        /* Остальные стили... */
    </style>
</head>
<body>
    <!-- ПЕРВАЯ СТРАНИЦА - НАЧАТЬ ОБЩЕНИЕ -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Хеллоуин 2025 Edition! Чат с реальными пользователями</div>
            
            <button class="btn pulse" onclick="startQuickRegistration()">
                <span>💬 Начать общение</span>
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                🔊 Голосовые сообщения • 📸 Истории • 📡 Стримы • 👥 Реальные люди
            </div>
        </div>
    </div>

    <!-- ВТОРАЯ СТРАНИЦА - АВТО-РЕГИСТРАЦИЯ -->
    <div id="quickRegisterScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Для вас создан аккаунт!</div>
            
            <div class="credential-box">
                <div class="credential-field">
                    <span>👤 Имя:</span>
                    <span class="credential-value" id="generatedName">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 Пароль:</span>
                    <span class="credential-value" id="generatedPassword">...</span>
                </div>
            </div>
            
            <button class="btn btn-success pulse" onclick="quickRegister()">
                <span>🚀 Продолжить в чат!</span>
            </button>
            
            <button class="btn" onclick="generateNewCredentials()">
                <span>🔄 Сгенерировать заново</span>
            </button>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <!-- Интерфейс будет генерироваться JavaScript -->
    </div>

    <!-- Вьювер историй -->
    <div id="storyViewer" class="story-viewer">
        <div class="story-progress" id="storyProgress"></div>
        <div id="storyContent" style="flex: 1; display: flex; align-items: center; justify-content: center;"></div>
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let stories = [];
        let streams = [];
        let isRecording = false;
        let mediaRecorder = null;
        let audioChunks = [];

        // Инициализация реальных пользователей
        function initializeRealUsers() {
            allUsers = [
                {
                    id: 'user_real_1',
                    name: 'Алексей Кодеров',
                    username: '@alex_coder',
                    email: 'alex.coder@mail.ru',
                    avatar: '👨‍💻',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'Fullstack разработчик | Люблю Python и JS | Играю на гитаре',
                    registered: new Date().toISOString(),
                    city: 'Москва',
                    age: 28,
                    interests: ['Программирование', 'Музыка', 'Путешествия']
                },
                {
                    id: 'user_real_2', 
                    name: 'Мария Дизайнерова',
                    username: '@maria_design',
                    email: 'maria.design@yandex.ru',
                    avatar: '👩‍🎨',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'UI/UX дизайнер | Люблю искусство и кофе | Фотографирую',
                    registered: new Date().toISOString(),
                    city: 'Санкт-Петербург',
                    age: 25,
                    interests: ['Дизайн', 'Фотография', 'Искусство']
                },
                {
                    id: 'user_real_3', 
                    name: 'Дмитрий Геймеров',
                    username: '@dima_gamer',
                    email: 'dima.gamer@gmail.com',
                    avatar: '🎮',
                    isOnline: false,
                    lastSeen: new Date(Date.now() - 3600000).toISOString(),
                    bio: 'Профессиональный геймер | Стример | Кибеспортсмен',
                    registered: new Date().toISOString(),
                    city: 'Новосибирск',
                    age: 22,
                    interests: ['Игры', 'Стриминг', 'Технологии']
                },
                {
                    id: 'user_real_4',
                    name: 'Анна Ученова',
                    username: '@anna_science',
                    email: 'anna.science@mail.ru',
                    avatar: '🔬',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'Ученый-биолог | Исследую ДНК | Люблю природу',
                    registered: new Date().toISOString(),
                    city: 'Казань',
                    age: 30,
                    interests: ['Наука', 'Природа', 'Исследования']
                },
                {
                    id: 'user_real_5',
                    name: 'Сергей Спортов',
                    username: '@serg_sport',
                    email: 'serg.sport@yandex.ru',
                    avatar: '🏃‍♂️',
                    isOnline: false,
                    lastSeen: new Date(Date.now() - 7200000).toISOString(),
                    bio: 'Фитнес-тренер | ЗОЖ | Питание и тренировки',
                    registered: new Date().toISOString(),
                    city: 'Екатеринбург',
                    age: 26,
                    interests: ['Спорт', 'Здоровье', 'Питание']
                },
                {
                    id: 'user_real_6',
                    name: 'Ольга Творческая',
                    username: '@olga_artist',
                    email: 'olga.artist@gmail.com',
                    avatar: '🎨',
                    isOnline: true,
                    lastSeen: new Date().toISOString(),
                    bio: 'Художник | Иллюстратор | Преподаю искусство',
                    registered: new Date().toISOString(),
                    city: 'Ростов-на-Дону',
                    age: 27,
                    interests: ['Живопись', 'Рисование', 'Преподавание']
                }
            ];
        }

        // Инициализация историй
        function initializeStories() {
            stories = [
                {
                    id: 'story1',
                    userId: 'user_real_1',
                    type: 'text',
                    content: '🎵 Сегодня записываю новый трек! #музыка',
                    createdAt: new Date().toISOString(),
                    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
                },
                {
                    id: 'story2',
                    userId: 'user_real_2',
                    type: 'text', 
                    content: '✨ Новый дизайн проекта готов! #дизайн',
                    createdAt: new Date().toISOString(),
                    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
                },
                {
                    id: 'story3',
                    userId: 'user_real_3',
                    type: 'text',
                    content: '🎮 Стрим сегодня в 20:00! Заходи! #игры',
                    createdAt: new Date().toISOString(),
                    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
                }
            ];
        }

        // Инициализация стримов
        function initializeStreams() {
            streams = [
                {
                    id: 'stream1',
                    userId: 'user_real_3',
                    title: '🎮 Играем в Cyberpunk 2077!',
                    viewers: 124,
                    isLive: true,
                    category: 'Игры',
                    thumbnail: '🎮'
                },
                {
                    id: 'stream2',
                    userId: 'user_real_1',
                    title: '💻 Пишем код вместе - React + Node.js',
                    viewers: 87,
                    isLive: true,
                    category: 'Программирование',
                    thumbnail: '💻'
                },
                {
                    id: 'stream3',
                    userId: 'user_real_2',
                    title: '🎨 Дизайн интерфейса в Figma',
                    viewers: 56,
                    isLive: false,
                    category: 'Дизайн',
                    thumbnail: '🎨'
                }
            ];
        }

        document.addEventListener('DOMContentLoaded', function() {
            initializeRealUsers();
            initializeStories();
            initializeStreams();
            checkAutoLogin();
        });

        function startQuickRegistration() {
            showScreen('quickRegisterScreen');
            generateNewCredentials();
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById(screenId).classList.remove('hidden');
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
        }

        function generateUsername() {
            const adjectives = ['Весёлый', 'Серьёзный', 'Смелый', 'Умный', 'Быстрый', 'Креативный'];
            const nouns = ['Единорог', 'Дракон', 'Волк', 'Феникс', 'Тигр', 'Орёл'];
            return `${randomChoice(adjectives)}${randomChoice(nouns)}${Math.floor(Math.random() * 1000)}`;
        }

        function generatePassword() {
            return Math.random().toString(36).slice(-12);
        }

        function randomChoice(array) {
            return array[Math.floor(Math.random() * array.length)];
        }

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            const username = '@' + name.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: username,
                email: '',
                avatar: '😊',
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Новый пользователь DLtrollex 🚀',
                registered: new Date().toISOString(),
                password: password,
                city: 'Москва',
                age: Math.floor(Math.random() * 20) + 18,
                interests: ['Общение', 'Знакомства', 'Технологии']
            };
            
            allUsers.push(currentUser);
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            showMainApp();
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
            }
        }

        function showMainApp() {
            showScreen('mainApp');
            renderMainInterface();
        }

        function renderMainInterface() {
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px;">🎃 DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                        </div>
                        
                        <div class="stories-container" id="storiesList">
                            ${renderStories()}
                        </div>
                        
                        <div class="search-box">
                            <input type="text" class="search-input" placeholder="🔍 Поиск реальных пользователей..." oninput="searchRealUsers(this.value)">
                        </div>
                        
                        <div class="chats-list" id="chatsList">
                            ${renderChatsList()}
                        </div>
                        
                        <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                            <button class="btn" onclick="showNewChatModal()">➕ Новый чат</button>
                            <button class="btn btn-voice" onclick="showVoiceRecorder()">🎤 Голосовые</button>
                            <button class="btn btn-story" onclick="showStoryCreator()">📸 Добавить историю</button>
                            <button class="btn btn-stream" onclick="showStreams()">📡 Стримы</button>
                        </div>
                    </div>
                    
                    <div class="chat-area">
                        <div id="chatContent">
                            <div style="text-align: center; padding: 50px 20px;">
                                <div style="font-size: 80px; margin-bottom: 20px;">💬</div>
                                <h2>Начните общение!</h2>
                                <p style="color: #888; margin: 10px 0 20px 0;">Выберите пользователя для чата</p>
                                <button class="btn" onclick="showNewChatModal()">💬 Начать чат</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderStories() {
            return stories.map(story => {
                const user = allUsers.find(u => u.id === story.userId);
                if (!user) return '';
                
                return `
                    <div class="story-item" onclick="viewStory('${story.id}')">
                        <div class="story-avatar">${user.avatar}</div>
                        <div class="story-username">${user.name.split(' ')[0]}</div>
                    </div>
                `;
            }).join('') + `
                <div class="story-item" onclick="showStoryCreator()">
                    <div class="story-avatar" style="background: var(--secondary-color); border: 2px dashed #888;">➕</div>
                    <div class="story-username">Ваша история</div>
                </div>
            `;
        }

        function renderChatsList() {
            if (chats.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div>Чатов пока нет</div>
                        <div style="font-size: 12px; margin-top: 5px;">Начните новый чат</div>
                    </div>
                `;
            }
            
            return chats.map(chat => {
                const otherUserId = chat.participants.find(id => id !== currentUser.id);
                const otherUser = allUsers.find(u => u.id === otherUserId);
                if (!otherUser) return '';
                
                return `
                    <div class="chat-item" onclick="openChat('${chat.id}')">
                        <div class="chat-avatar">${otherUser.avatar}</div>
                        <div class="chat-info">
                            <div class="chat-name">${otherUser.name}</div>
                            <div class="chat-last-message">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function searchRealUsers(query) {
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && (
                    user.name.toLowerCase().includes(query.toLowerCase()) ||
                    user.username.toLowerCase().includes(query.toLowerCase()) ||
                    user.bio.toLowerCase().includes(query.toLowerCase()) ||
                    user.interests.some(interest => interest.toLowerCase().includes(query.toLowerCase()))
                )
            );
            
            let html = '';
            if (filteredUsers.length > 0) {
                html = filteredUsers.map(user => `
                    <div class="chat-item" onclick="startNewChat('${user.id}')">
                        <div class="chat-avatar">${user.avatar}</div>
                        <div class="chat-info">
                            <div class="chat-name">
                                ${user.name}
                                ${user.isOnline ? '🟢' : '⚫'}
                            </div>
                            <div class="chat-last-message">
                                ${user.bio} • ${user.city}
                            </div>
                        </div>
                    </div>
                `).join('');
            } else {
                html = '<div style="text-align: center; padding: 20px; color: #888;">Пользователи не найдены</div>';
            }
            
            document.getElementById('chatsList').innerHTML = html;
        }

        // ГОЛОСОВЫЕ СООБЩЕНИЯ
        function showVoiceRecorder() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px;">
                    <h2>🎤 Голосовые сообщения</h2>
                    <div style="background: var(--card-color); padding: 30px; border-radius: 15px; text-align: center; margin-top: 20px;">
                        <div id="voiceRecorder" style="margin-bottom: 20px;">
                            <button class="btn btn-voice" onclick="startVoiceRecording()" id="recordBtn">
                                🎤 Начать запись
                            </button>
                            <div id="recordingStatus" style="margin-top: 10px; color: #888;"></div>
                        </div>
                        <div id="voiceMessagesList">
                            ${renderVoiceMessages()}
                        </div>
                    </div>
                </div>
            `;
        }

        async function startVoiceRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    saveVoiceMessage(audioBlob);
                };
                
                mediaRecorder.start();
                isRecording = true;
                document.getElementById('recordBtn').innerHTML = '⏹️ Остановить запись';
                document.getElementById('recordBtn').classList.add('recording');
                document.getElementById('recordingStatus').textContent = 'Запись...';
                
                document.getElementById('recordBtn').onclick = stopVoiceRecording;
                
            } catch (error) {
                alert('Ошибка доступа к микрофону');
            }
        }

        function stopVoiceRecording() {
            if (mediaRecorder && isRecording) {
                mediaRecorder.stop();
                isRecording = false;
                document.getElementById('recordBtn').innerHTML = '🎤 Начать запись';
                document.getElementById('recordBtn').classList.remove('recording');
                document.getElementById('recordingStatus').textContent = 'Запись сохранена!';
                
                document.getElementById('recordBtn').onclick = startVoiceRecording;
            }
        }

        function saveVoiceMessage(audioBlob) {
            const voiceMessage = {
                id: 'voice_' + Date.now(),
                userId: currentUser.id,
                audioUrl: URL.createObjectURL(audioBlob),
                duration: Math.floor(Math.random() * 30) + 5, // случайная длительность 5-35 сек
                timestamp: new Date().toISOString()
            };
            
            // Сохраняем в localStorage
            const savedMessages = JSON.parse(localStorage.getItem('voiceMessages') || '[]');
            savedMessages.push(voiceMessage);
            localStorage.setItem('voiceMessages', JSON.stringify(savedMessages));
            
            showVoiceRecorder(); // Обновляем список
        }

        function renderVoiceMessages() {
            const savedMessages = JSON.parse(localStorage.getItem('voiceMessages') || '[]');
            const userMessages = savedMessages.filter(msg => msg.userId === currentUser.id);
            
            if (userMessages.length === 0) {
                return '<div style="color: #888; text-align: center;">У вас пока нет голосовых сообщений</div>';
            }
            
            return userMessages.map(msg => `
                <div class="voice-message" onclick="playVoiceMessage('${msg.audioUrl}')">
                    <div class="voice-play-btn">▶️</div>
                    <div class="voice-waveform"></div>
                    <div class="voice-duration">${msg.duration} сек</div>
                </div>
            `).join('');
        }

        function playVoiceMessage(audioUrl) {
            const audio = new Audio(audioUrl);
            audio.play();
        }

        // ИСТОРИИ
        function showStoryCreator() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px;">
                    <h2>📸 Создать историю</h2>
                    <div style="background: var(--card-color); padding: 30px; border-radius: 15px; margin-top: 20px;">
                        <textarea id="storyText" placeholder="Что у вас нового?" style="width: 100%; height: 100px; background: var(--secondary-color); border: 1px solid var(--border-color); border-radius: 10px; padding: 15px; color: white; margin-bottom: 15px;"></textarea>
                        <button class="btn btn-story" onclick="createStory()">📸 Опубликовать историю</button>
                    </div>
                </div>
            `;
        }

        function createStory() {
            const text = document.getElementById('storyText').value.trim();
            if (!text) {
                alert('Введите текст истории');
                return;
            }
            
            const newStory = {
                id: 'story_' + Date.now(),
                userId: currentUser.id,
                type: 'text',
                content: text,
                createdAt: new Date().toISOString(),
                expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
            };
            
            stories.push(newStory);
            renderMainInterface();
            showNotification('История опубликована! 📸');
        }

        function viewStory(storyId) {
            const story = stories.find(s => s.id === storyId);
            const user = allUsers.find(u => u.id === story.userId);
            
            if (!story || !user) return;
            
            document.getElementById('storyViewer').style.display = 'flex';
            document.getElementById('storyContent').innerHTML = `
                <div style="text-align: center;">
                    <div style="font-size: 48px; margin-bottom: 20px;">${user.avatar}</div>
                    <div style="font-size: 24px; margin-bottom: 10px;">${user.name}</div>
                    <div style="font-size: 18px; color: #ccc;">${story.content}</div>
                </div>
            `;
            
            // Автоматическое закрытие через 5 секунд
            setTimeout(() => {
                document.getElementById('storyViewer').style.display = 'none';
            }, 5000);
        }

        // СТРИМЫ
        function showStreams() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px;">
                    <h2>📡 Прямые трансляции</h2>
                    <div class="streams-container">
                        ${renderStreams()}
                    </div>
                </div>
            `;
        }

        function renderStreams() {
            return streams.map(stream => {
                const user = allUsers.find(u => u.id === stream.userId);
                if (!user) return '';
                
                return `
                    <div class="stream-card" onclick="watchStream('${stream.id}')">
                        <div class="stream-preview">${stream.thumbnail}</div>
                        <div class="stream-info">
                            <div class="stream-title">${stream.title}</div>
                            <div class="stream-stats">
                                <span>${user.name}</span>
                                <span>•</span>
                                <span>👁️ ${stream.viewers}</span>
                                ${stream.isLive ? '<span class="live-badge">LIVE</span>' : ''}
                            </div>
                            <div style="color: #888; font-size: 12px; margin-top: 5px;">${stream.category}</div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function watchStream(streamId) {
            const stream = streams.find(s => s.id === streamId);
            const user = allUsers.find(u => u.id === stream.userId);
            
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px;">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 20px;">
                        <h2>📡 ${stream.title}</h2>
                        <button class="btn" onclick="showStreams()">← Назад</button>
                    </div>
                    <div style="background: var(--card-color); border-radius: 15px; overflow: hidden;">
                        <div style="background: linear-gradient(45deg, #8b5cf6, #ec4899); height: 300px; display: flex; align-items: center; justify-content: center; font-size: 64px;">
                            ${stream.thumbnail}
                        </div>
                        <div style="padding: 20px;">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                                <div style="font-size: 24px;">${user.avatar}</div>
                                <div>
                                    <div style="font-weight: bold;">${user.name}</div>
                                    <div style="color: #888; font-size: 12px;">${stream.category}</div>
                                </div>
                            </div>
                            <div style="color: #888; margin-bottom: 15px;">👁️ ${stream.viewers} зрителей</div>
                            <button class="btn btn-stream">🎥 Смотреть трансляцию</button>
                        </div>
                    </div>
                </div>
            `;
        }

        // ОСНОВНЫЕ ФУНКЦИИ ЧАТА
        function showNewChatModal() {
            const availableUsers = allUsers.filter(user => user.id !== currentUser.id);
            
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 20px;">
                    <h2>💬 Новый чат</h2>
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin-top: 20px;">
                        <div style="max-height: 60vh; overflow-y: auto;">
                            ${availableUsers.map(user => `
                                <div class="chat-item" onclick="startNewChat('${user.id}')">
                                    <div class="chat-avatar">${user.avatar}</div>
                                    <div class="chat-info">
                                        <div class="chat-name">
                                            ${user.name}
                                            ${user.isOnline ? '🟢' : '⚫'}
                                        </div>
                                        <div class="chat-last-message">
                                            ${user.bio} • ${user.city} • ${user.age} лет
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

            const newChat = {
                id: 'chat_' + Date.now(),
                participants: [currentUser.id, userId],
                lastMessage: {
                    text: 'Чат начат 🚀',
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                },
                messages: [
                    {
                        id: '1',
                        text: `Привет! Я ${currentUser.name}. Рад познакомиться! 👋`,
                        senderId: currentUser.id,
                        timestamp: new Date().toISOString()
                    }
                ]
            };

            chats.push(newChat);
            openChat(newChat.id);
        }

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherUserId = currentChat.participants.find(id => id !== currentUser.id);
            const chatUser = allUsers.find(u => u.id === otherUserId);
            
            document.getElementById('chatContent').innerHTML = `
                <div style="display: flex; flex-direction: column; height: 100%;">
                    <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: between;">
                        <div style="display: flex; align-items: center;">
                            <div class="chat-avatar">${chatUser.avatar}</div>
                            <div>
                                <div style="font-weight: bold;">${chatUser.name}</div>
                                <div style="color: #888; font-size: 12px;">${chatUser.bio}</div>
                            </div>
                        </div>
                        <button class="btn" onclick="renderMainInterface()" style="padding: 8px 15px;">← Назад</button>
                    </div>
                    
                    <div class="messages-container" id="messagesContainer">
                        ${renderChatMessages()}
                    </div>
                    
                    <div class="message-input-container">
                        <input type="text" class="message-input" placeholder="💬 Введите сообщение..." id="messageInput" onkeypress="if(event.key=='Enter') sendMessage()">
                        <button class="send-btn" onclick="sendMessage()">📤</button>
                        <button class="btn btn-voice" onclick="showVoiceRecorder()" style="padding: 10px; margin-left: 10px;">🎤</button>
                    </div>
                </div>
            `;
        }

        function renderChatMessages() {
            if (!currentChat.messages) return '';
            
            return currentChat.messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                return `
                    <div class="message ${isOwn ? 'own' : ''}">
                        ${msg.text}
                    </div>
                `;
            }).join('');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (text && currentChat) {
                const newMessage = {
                    id: Date.now().toString(),
                    text: text,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                input.value = '';
                openChat(currentChat.id);
            }
        }

        function showNotification(message) {
            // Простое уведомление
            alert(message);
        }

        // Закрытие истории при клике
        document.getElementById('storyViewer').addEventListener('click', function() {
            this.style.display = 'none';
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🎃 DLtrollex с голосовыми сообщениями запущен!")
    print(f"🔗 http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
