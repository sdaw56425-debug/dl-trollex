# app.py
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
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

# Хранилища данных в памяти (в продакшене используйте БД)
active_calls = {}
user_sessions = {}
user_messages = {}
all_users = []
friendships = {}
friend_requests = {}
user_profiles = {}

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

def generate_friend_code():
    return f"TRLX-{uuid.uuid4().hex[:8].upper()}"

def generate_session_token():
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def verify_session(user_id, session_token):
    """Проверка валидности сессии"""
    return user_id in user_sessions and session_token == user_sessions.get(user_id)

def initialize_sample_data():
    """Инициализация тестовых данных"""
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
    
    # Инициализируем профили
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
    
    # Создаем несколько тестовых дружеских связей
    friendships['user1'] = ['user2', 'user3']
    friendships['user2'] = ['user1']
    friendships['user3'] = ['user1']

def ensure_user_chat(user_id, target_user_id):
    """Создает структуру чата если её нет"""
    if user_id not in user_messages:
        user_messages[user_id] = {}
    
    if target_user_id not in user_messages[user_id]:
        user_messages[user_id][target_user_id] = []
        
        # Добавляем приветственное сообщение
        welcome_msg = {
            'id': str(uuid.uuid4()),
            'sender': target_user_id,
            'text': 'Привет! 👋 Рад познакомиться!',
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'text'
        }
        user_messages[user_id][target_user_id].append(welcome_msg)

def get_user_by_friend_code(friend_code):
    """Находит пользователя по friend code"""
    for user_id, profile in user_profiles.items():
        if profile.get('friend_code') == friend_code:
            return user_id
    return None

def validate_friend_code(friend_code):
    """Проверяет валидность friend code"""
    pattern = r'^TRLX-[A-F0-9]{8}$'
    return re.match(pattern, friend_code) is not None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <style>
        /* Все существующие стили остаются без изменений */
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        :root { --primary: #0a0a2a; --secondary: #1a1a4a; --accent: #6c2bd9; --accent-glow: #8b5cf6; --neon: #00ff88; --text: #ffffff; --text-secondary: #b0b0ff; --danger: #ff4444; --success: #00ff88; --warning: #ffaa00; --cyber: #00ffff; }
        body { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: var(--text); min-height: 100vh; }
        
        /* Добавляем новые стили для улучшенного интерфейса */
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
        
        .add-friend-container {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid var(--accent);
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
        
        .request-actions {
            display: flex;
            gap: 10px;
        }
        
        .friend-item {
            display: flex;
            align-items: center;
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .friend-item:hover {
            background: rgba(107, 43, 217, 0.3);
        }
        
        .online-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            margin-right: 10px;
        }
        
        .offline-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--text-secondary);
            margin-right: 10px;
        }
        
        .typing-indicator {
            display: none;
            color: var(--neon);
            font-style: italic;
            font-size: 0.8rem;
            margin: 5px 0;
        }
        
        .message-status {
            font-size: 0.7rem;
            margin-left: 5px;
            opacity: 0.7;
        }
        
        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 5px;
        }
        
        .unread-badge {
            background: var(--success);
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            margin-left: auto;
        }
        
        .context-menu {
            position: absolute;
            background: var(--secondary);
            border: 1px solid var(--accent);
            border-radius: 10px;
            padding: 10px;
            z-index: 1000;
            display: none;
        }
        
        .context-menu-item {
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 5px;
        }
        
        .context-menu-item:hover {
            background: rgba(107, 43, 217, 0.3);
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

            <div class="friend-code-display">
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Ваш Friend Code:</div>
                <div class="friend-code" id="registerFriendCode">TRLX-XXXXXXX</div>
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
                    <div class="friend-code" id="userFriendCode">TRLX-XXXXXXX</div>
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
                    <div class="typing-indicator" id="typingIndicator">Печатает...</div>
                </div>
                <button class="control-btn" onclick="startVideoCall()" style="background: var(--success); width: 40px; height: 40px; font-size: 1rem;">📞</button>
                <button class="control-btn" onclick="showFileShare()" style="background: var(--warning); width: 40px; height: 40px; font-size: 1rem;">📎</button>
                <button class="control-btn" onclick="toggleStickers()" style="background: var(--cyber); width: 40px; height: 40px; font-size: 1rem;">😊</button>
                <button class="control-btn" onclick="showChatInfo()" style="background: var(--accent); width: 40px; height: 40px; font-size: 1rem;">ℹ️</button>
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

            <div class="sticker-picker" id="stickerPicker">
                <div class="sticker" onclick="sendSticker('😊')">😊</div>
                <div class="sticker" onclick="sendSticker('😂')">😂</div>
                <div class="sticker" onclick="sendSticker('🥰')">🥰</div>
                <div class="sticker" onclick="sendSticker('😎')">😎</div>
                <div class="sticker" onclick="sendSticker('🤔')">🤔</div>
                <div class="sticker" onclick="sendSticker('🎉')">🎉</div>
                <div class="sticker" onclick="sendSticker('🚀')">🚀</div>
                <div class="sticker" onclick="sendSticker('💫')">💫</div>
                <div class="sticker" onclick="sendSticker('❤️')">❤️</div>
                <div class="sticker" onclick="sendSticker('🔥')">🔥</div>
                <div class="sticker" onclick="sendSticker('⭐')">⭐</div>
                <div class="sticker" onclick="sendSticker('🌈')">🌈</div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput" 
                       onkeypress="handleKeyPress(event)" oninput="handleTyping()">
                <button class="voice-message-btn" onclick="startVoiceMessage()" title="Голосовое сообщение">🎤</button>
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Контекстное меню -->
    <div class="context-menu" id="contextMenu">
        <div class="context-menu-item" onclick="contextMenuAction('profile')">👤 Профиль</div>
        <div class="context-menu-item" onclick="contextMenuAction('call')">📞 Позвонить</div>
        <div class="context-menu-item" onclick="contextMenuAction('remove')">❌ Удалить</div>
        <div class="context-menu-item" onclick="contextMenuAction('block')">🚫 Заблокировать</div>
    </div>

    <!-- Модальное окно добавления друга -->
    <div id="addFriendModal" class="call-invite" style="display: none;">
        <div class="logo">👥 Добавить друга</div>
        <div class="add-friend-container">
            <input type="text" class="join-input" id="friendCodeInput" placeholder="Введите Friend Code (TRLX-XXXXXXX)">
            <button class="btn btn-primary" onclick="sendFriendRequest()" style="width: 100%; margin: 10px 0;">
                📤 Отправить запрос
            </button>
            <div style="text-align: center; color: var(--text-secondary); font-size: 0.9rem;">
                Или поделитесь своим кодом:
            </div>
            <div class="friend-code-display" style="margin: 10px 0;">
                <div class="friend-code" id="shareFriendCode">TRLX-XXXXXXX</div>
                <button class="btn btn-secondary" onclick="copyFriendCode()" style="width: 100%; margin-top: 10px;">
                    📋 Скопировать код
                </button>
            </div>
        </div>
        <button class="btn btn-secondary" onclick="hideAddFriendModal()">❌ Закрыть</button>
    </div>

    <!-- Остальные элементы (звонки, настройки и т.д.) остаются без изменений -->

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let messages = {};
        let allUsers = [];
        let friends = [];
        let friendRequests = [];
        let sessionToken = null;
        let typingTimer = null;
        
        // Инициализация
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
                    setTimeout(typeNextText, 1000);
                } else {
                    setTimeout(() => {
                        hideLoadingScreen();
                        checkAutoLogin();
                    }, 500);
                }
            }
            
            typeNextText();
        }

        // Функции для работы с друзьями
        function showAddFriendModal() {
            document.getElementById('addFriendModal').style.display = 'block';
            document.getElementById('shareFriendCode').textContent = currentUser.friendCode;
        }

        function hideAddFriendModal() {
            document.getElementById('addFriendModal').style.display = 'none';
        }

        function copyFriendCode() {
            navigator.clipboard.writeText(currentUser.friendCode);
            showNotification('Friend Code скопирован! 📋');
        }

        function sendFriendRequest() {
            const friendCode = document.getElementById('friendCodeInput').value.trim();
            
            if (!friendCode) {
                showNotification('Введите Friend Code ❌');
                return;
            }
            
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
                    hideAddFriendModal();
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

        // Обновленная функция loadContent
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
                    contentHTML = getCallsContent(searchTerm);
                    break;
                default:
                    contentHTML = '<div class="empty-state">Выберите вкладку</div>';
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getFriendsContent(searchTerm) {
            let friendsHTML = '';
            
            // Запросы в друзья
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
                                <div class="request-actions">
                                    <button class="control-btn" onclick="respondToFriendRequest('${request.id}', true)" style="background: var(--success); width: 35px; height: 35px; font-size: 0.8rem;">✓</button>
                                    <button class="control-btn" onclick="respondToFriendRequest('${request.id}', false)" style="background: var(--danger); width: 35px; height: 35px; font-size: 0.8rem;">✕</button>
                                </div>
                            </div>
                        `;
                    }
                });
            }
            
            // Друзья онлайн
            const onlineFriends = friends.filter(friend => friend.online);
            if (onlineFriends.length > 0) {
                friendsHTML += '<h4 style="padding: 10px; color: var(--success); margin-top: 20px;">🟢 Друзья онлайн</h4>';
                onlineFriends.forEach(friend => {
                    if (searchTerm === '' || friend.name.toLowerCase().includes(searchTerm)) {
                        friendsHTML += `
                            <div class="friend-item" onclick="selectUser('${friend.id}')" oncontextmenu="showContextMenu(event, '${friend.id}')">
                                <div class="online-indicator"></div>
                                <div class="item-avatar">${friend.avatar}</div>
                                <div style="flex: 1;">
                                    <h4>${friend.name}</h4>
                                    <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                        ${friend.status || 'Online'} • ${friend.last_seen}
                                    </p>
                                </div>
                                <button class="control-btn" onclick="event.stopPropagation(); startCallWithUser('${friend.id}')" style="background: var(--success); width: 35px; height: 35px; font-size: 0.8rem;">📞</button>
                            </div>
                        `;
                    }
                });
            }
            
            // Друзья оффлайн
            const offlineFriends = friends.filter(friend => !friend.online);
            if (offlineFriends.length > 0) {
                friendsHTML += '<h4 style="padding: 10px; margin-top: 20px; color: var(--text-secondary);">⚫ Друзья оффлайн</h4>';
                offlineFriends.forEach(friend => {
                    if (searchTerm === '' || friend.name.toLowerCase().includes(searchTerm)) {
                        friendsHTML += `
                            <div class="friend-item" onclick="selectUser('${friend.id}')" oncontextmenu="showContextMenu(event, '${friend.id}')">
                                <div class="offline-indicator"></div>
                                <div class="item-avatar">${friend.avatar}</div>
                                <div style="flex: 1;">
                                    <h4>${friend.name}</h4>
                                    <p style="color: var(--text-secondary); font-size: 0.8rem;">
                                        ${friend.status || 'Offline'} • ${friend.last_seen}
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
                        <button class="btn btn-primary" onclick="showAddFriendModal()" style="margin-top: 15px;">
                            👥 Добавить друга
                        </button>
                    </div>
                `;
            }
            
            return friendsHTML;
        }

        function getDiscoverContent(searchTerm) {
            return `
                <div style="text-align: center; padding: 20px;">
                    <button class="btn btn-primary" onclick="showAddFriendModal()" style="margin-bottom: 15px;">
                        👥 Добавить по коду
                    </button>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">
                        Используйте Friend Code для добавления в друзья
                    </div>
                </div>

                <div class="add-friend-container">
                    <h4>🔍 Рекомендованные пользователи</h4>
                    <div id="recommendedUsers">
                        <!-- Динамически заполняется -->
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <h4>📊 Статистика</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                        <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                            <div style="font-size: 1.5rem;">${friends.length}</div>
                            <div style="font-size: 0.8rem; color: var(--text-secondary);">Друзей</div>
                        </div>
                        <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                            <div style="font-size: 1.5rem;">${getChatsCount()}</div>
                            <div style="font-size: 0.8rem; color: var(--text-secondary);">Чатов</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Новые функции для улучшения UX
        function handleTyping() {
            if (currentChat) {
                // Отправляем серверу информацию о печатании
                clearTimeout(typingTimer);
                // Здесь можно добавить отправку события typing на сервер
                typingTimer = setTimeout(() => {
                    // Таймаут печатания
                }, 1000);
            }
        }

        function showContextMenu(event, userId) {
            event.preventDefault();
            const contextMenu = document.getElementById('contextMenu');
            contextMenu.style.display = 'block';
            contextMenu.style.left = event.pageX + 'px';
            contextMenu.style.top = event.pageY + 'px';
            contextMenu.dataset.userId = userId;
        }

        function contextMenuAction(action) {
            const userId = document.getElementById('contextMenu').dataset.userId;
            const contextMenu = document.getElementById('contextMenu');
            contextMenu.style.display = 'none';
            
            switch(action) {
                case 'profile':
                    showUserProfile(userId);
                    break;
                case 'call':
                    startCallWithUser(userId);
                    break;
                case 'remove':
                    removeFriend(userId);
                    break;
                case 'block':
                    blockUser(userId);
                    break;
            }
        }

        function showUserProfile(userId) {
            const user = friends.find(f => f.id === userId) || allUsers.find(u => u.id === userId);
            if (user) {
                alert(`Профиль пользователя:\n\n👤 Имя: ${user.name}\n🆔 ID: ${user.id}\n📧 Статус: ${user.status || 'Не установлен'}\n⏰ Был(а): ${user.last_seen}`);
            }
        }

        function removeFriend(userId) {
            if (confirm('Вы уверены, что хотите удалить этого пользователя из друзей?')) {
                fetch('/api/remove_friend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: currentUser.id,
                        session_token: sessionToken,
                        friend_id: userId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('Пользователь удален из друзей ❌');
                        loadFriends();
                    } else {
                        showNotification(data.error || 'Ошибка удаления ❌');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('Ошибка сети ❌');
                });
            }
        }

        function blockUser(userId) {
            if (confirm('Вы уверены, что хотите заблокировать этого пользователя?')) {
                showNotification('Пользователь заблокирован 🚫');
            }
        }

        function getChatsCount() {
            const userChats = JSON.parse(localStorage.getItem(`chats_${currentUser.id}`)) || [];
            return userChats.length;
        }

        // Обновляем функцию регистрации
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
                friendCode: friendCode,
                settings: {}
            };
            
            sessionToken = generateSessionToken();
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('sessionToken', sessionToken);
            
            // Инициализируем данные на сервере
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

        // Обновляем функцию генерации пользователя
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

        function generateFriendCode() {
            return 'TRLX-' + Math.random().toString(36).substr(2, 8).toUpperCase();
        }

        // Обновляем showMainApp для загрузки данных о друзьях
        function showMainApp() {
            hideAllScreens();
            document.getElementById('mainApp').classList.remove('hidden');
            
            // Заполняем данные пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            document.getElementById('userFriendCode').textContent = currentUser.friendCode;
            
            loadContent();
            loadMediaDevices();
            loadSettings();
            loadFriends();
            loadFriendRequests();
            
            // Проверяем приглашение в звонок
            checkCallInvite();
        }

        // Закрываем контекстное меню при клике вне его
        document.addEventListener('click', function() {
            document.getElementById('contextMenu').style.display = 'none';
        });

        // Остальные функции остаются без изменений...
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    initialize_sample_data()
    return render_template_string(HTML_TEMPLATE)

# Новые API endpoints

@app.route('/api/register_user', methods=['POST'])
def api_register_user():
    try:
        data = request.json
        user_id = data.get('id')
        
        # Сохраняем пользователя
        user_profiles[user_id] = {
            'friend_code': data.get('friend_code', generate_friend_code()),
            'friends': [],
            'settings': {
                'theme': 'dark',
                'notifications': True,
                'privacy': 'friends_only'
            },
            'created_at': datetime.datetime.now().isoformat()
        }
        
        logger.info(f"Зарегистрирован новый пользователь: {user_id}")
        return jsonify({'success': True, 'message': 'User registered successfully'})
        
    except Exception as e:
        logger.error(f"Ошибка регистрации пользователя: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_friend_request', methods=['POST'])
def api_send_friend_request():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        friend_code = data.get('friend_code')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        # Проверяем валидность friend code
        if not validate_friend_code(friend_code):
            return jsonify({'success': False, 'error': 'Invalid friend code format'})
        
        # Находим пользователя по friend code
        target_user_id = get_user_by_friend_code(friend_code)
        if not target_user_id:
            return jsonify({'success': False, 'error': 'User not found'})
            
        if target_user_id == user_id:
            return jsonify({'success': False, 'error': 'Cannot add yourself'})
        
        # Проверяем, не отправили ли уже запрос
        if user_id not in friend_requests:
            friend_requests[user_id] = []
            
        # Добавляем запрос
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
        session_token = data.get('session_token')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        user_requests = friend_requests.get(user_id, [])
        requests_data = []
        
        for req in user_requests:
            if req.get('status') == 'pending':
                # Находим информацию о пользователе
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
        session_token = data.get('session_token')
        request_id = data.get('request_id')
        accept = data.get('accept')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        # Находим запрос
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
            # Добавляем в друзья
            friendships.setdefault(user_id, []).append(from_user_id)
            friendships.setdefault(from_user_id, []).append(user_id)
            
            # Создаем чат между пользователями
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
        session_token = data.get('session_token')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
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

@app.route('/api/remove_friend', methods=['POST'])
def api_remove_friend():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        friend_id = data.get('friend_id')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        # Удаляем из друзей
        if user_id in friendships and friend_id in friendships[user_id]:
            friendships[user_id].remove(friend_id)
            
        if friend_id in friendships and user_id in friendships[friend_id]:
            friendships[friend_id].remove(user_id)
            
        logger.info(f"Пользователь {friend_id} удален из друзей {user_id}")
        return jsonify({'success': True, 'message': 'Friend removed'})
        
    except Exception as e:
        logger.error(f"Ошибка удаления друга: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

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
            'participants': [user_id],
            'created_at': datetime.datetime.now().isoformat(),
            'security_level': 'high',
            'type': 'video'
        }
        
        logger.info(f"Создан защищённый звонок: {call_id}")
        return jsonify({
            'success': True, 
            'call_id': call_id, 
            'call_link': f'{request.host_url}call/{call_id}',
            'security_level': 'high'
        })
    except Exception as e:
        logger.error(f"Ошибка создания звонка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        target_user_id = data.get('target_user_id')
        message_text = data.get('message')
        message_type = data.get('type', 'text')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        ensure_user_chat(user_id, target_user_id)
        
        message = {
            'id': str(uuid.uuid4()),
            'sender': user_id,
            'text': message_text,
            'timestamp': datetime.datetime.now().isoformat(),
            'type': message_type,
            'status': 'sent'
        }
        
        user_messages[user_id][target_user_id].append(message)
        
        # Если пользователи друзья, добавляем сообщение и в их чат
        if target_user_id in friendships.get(user_id, []):
            ensure_user_chat(target_user_id, user_id)
            user_messages[target_user_id][user_id].append(message)
        
        logger.info(f"Сообщение отправлено от {user_id} к {target_user_id}")
        return jsonify({'success': True, 'message_id': message['id']})
        
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_messages', methods=['POST'])
def api_get_messages():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        target_user_id = data.get('target_user_id')
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
            
        ensure_user_chat(user_id, target_user_id)
        messages = user_messages[user_id].get(target_user_id, [])
        
        return jsonify({'success': True, 'messages': messages})
        
    except Exception as e:
        logger.error(f"Ошибка получения сообщений: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
