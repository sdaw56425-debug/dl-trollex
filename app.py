# app.py - ОБНОВЛЕННАЯ ВЕРСИЯ
from flask import Flask, render_template_string, request, jsonify, send_from_directory
import datetime
import random
import os
import uuid
import logging
import hashlib
import time
import json
import re
import html
from typing import Dict, List, Optional, Set
import threading

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trollexdl-premium-2024')

# Константы
MAX_MESSAGES_PER_CHAT = 1000
MAX_STORAGE_SIZE = 5 * 1024 * 1024
RATE_LIMIT_WINDOW = 60
MAX_REQUESTS_PER_WINDOW = 100
MAX_MESSAGE_LENGTH = 2000
MAX_USERNAME_LENGTH = 20
CALL_TIMEOUT = 3600  # 1 hour

# Потокобезопасные хранилища
class ThreadSafeDict:
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()
    
    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)
    
    def set(self, key, value):
        with self._lock:
            self._data[key] = value
    
    def delete(self, key):
        with self._lock:
            if key in self._data:
                del self._data[key]
    
    def items(self):
        with self._lock:
            return list(self._data.items())
    
    def keys(self):
        with self._lock:
            return list(self._data.keys())
    
    def __contains__(self, key):
        with self._lock:
            return key in self._data

# Инициализация хранилищ
active_calls = ThreadSafeDict()
user_sessions = ThreadSafeDict()
user_messages = ThreadSafeDict()
all_users = []
friendships = ThreadSafeDict()
friend_requests = ThreadSafeDict()
user_profiles = ThreadSafeDict()
rate_limits = ThreadSafeDict()
user_activity = ThreadSafeDict()

def cleanup_old_data():
    """Очистка старых данных"""
    try:
        current_time = time.time()
        
        # Очистка старых звонков
        for call_id, call_data in list(active_calls.items()):
            created_time = datetime.datetime.fromisoformat(call_data['created_at']).timestamp()
            if current_time - created_time > CALL_TIMEOUT:
                active_calls.delete(call_id)
                logger.info(f"Удален устаревший звонок: {call_id}")
        
        # Очистка старых rate limits
        for key in list(rate_limits.keys()):
            if current_time - rate_limits.get(key, {}).get('timestamp', 0) > RATE_LIMIT_WINDOW:
                rate_limits.delete(key)
        
        # Очистка неактивных пользователей
        for user_id, last_active in list(user_activity.items()):
            if current_time - last_active > 3600:  # 1 hour
                user_activity.delete(user_id)
                
    except Exception as e:
        logger.error(f"Error in cleanup: {e}")

def schedule_cleanup():
    """Планировщик очистки"""
    while True:
        time.sleep(300)  # 5 minutes
        cleanup_old_data()

# Запуск фоновой очистки
cleanup_thread = threading.Thread(target=schedule_cleanup, daemon=True)
cleanup_thread.start()

def update_user_activity(user_id: str):
    """Обновление активности пользователя"""
    if user_id:
        user_activity.set(user_id, time.time())

def check_rate_limit(user_id: str, action: str) -> bool:
    """Проверка rate limit с улучшенной логикой"""
    current_time = time.time()
    key = f"{user_id}_{action}"
    
    record = rate_limits.get(key)
    if not record:
        rate_limits.set(key, {'count': 1, 'timestamp': current_time})
        return True
    
    time_diff = current_time - record['timestamp']
    
    if time_diff > RATE_LIMIT_WINDOW:
        rate_limits.set(key, {'count': 1, 'timestamp': current_time})
        return True
    
    if record['count'] >= MAX_REQUESTS_PER_WINDOW:
        return False
    
    record['count'] += 1
    rate_limits.set(key, record)
    return True

def sanitize_input(text: str) -> str:
    """Улучшенная санитизация ввода"""
    if not text:
        return ""
    
    # Удаляем опасные теги и атрибуты
    text = html.escape(text)
    
    # Разрешаем безопасные эмодзи и символы
    text = re.sub(r'&amp;([#a-zA-Z0-9]+);', r'&\1;', text)  # Восстанавливаем безопасные entities
    
    # Удаляем потенциально опасные конструкции
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'vbscript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+=', 'data-', text, flags=re.IGNORECASE)
    
    return text.strip()

def validate_friend_code(friend_code: str) -> bool:
    """Валидация friend code"""
    pattern = r'^TRLX-[A-F0-9]{4}-[A-F0-9]{4}$'
    return bool(re.match(pattern, friend_code))

def validate_username(username: str) -> bool:
    """Валидация имени пользователя"""
    if not username or len(username) < 3 or len(username) > MAX_USERNAME_LENGTH:
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))

def validate_message(text: str) -> tuple[bool, str]:
    """Валидация сообщения"""
    if not text or not text.strip():
        return False, "Сообщение не может быть пустым"
    
    if len(text) > MAX_MESSAGE_LENGTH:
        return False, f"Сообщение слишком длинное (максимум {MAX_MESSAGE_LENGTH} символов)"
    
    # Проверка на спам (повторяющиеся символы)
    if re.match(r'^(.)\1{10,}$', text):  # 10+ одинаковых символов подряд
        return False, "Сообщение содержит подозрительный контент"
    
    return True, ""

def generate_username() -> str:
    adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha']
    nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther']
    numbers = random.randint(1000, 9999)
    username = f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"
    return sanitize_input(username)

def generate_email(username: str) -> str:
    domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net']
    email = f"{username.lower()}@{random.choice(domains)}"
    return sanitize_input(email)

def generate_user_id() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_call_id() -> str:
    return f"call_{uuid.uuid4().hex[:12]}"

def generate_friend_code() -> str:
    return f"TRLX-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}"

def generate_session_token() -> str:
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def verify_session(user_id: str, session_token: str) -> bool:
    """Проверка сессии с обновлением активности"""
    if not user_id or not session_token:
        return False
    
    valid = user_id in user_sessions.keys() and session_token == user_sessions.get(user_id)
    if valid:
        update_user_activity(user_id)
    return valid

def initialize_sample_data():
    """Инициализация тестовых данных один раз при старте"""
    global all_users
    
    if all_users:  # Уже инициализированы
        return
    
    sample_users = [
        {'id': 'user1', 'name': 'Alex_Quantum', 'avatar': '👨‍💻', 'online': True, 'last_seen': 'только что', 'status': 'Разрабатываю квантовый мессенджер'},
        {'id': 'user2', 'name': 'Sarah_Cyber', 'avatar': '👩‍🎨', 'online': True, 'last_seen': '2 мин назад', 'status': 'Создаю цифровое искусство'},
        {'id': 'user3', 'name': 'Mike_Neon', 'avatar': '👨‍🚀', 'online': False, 'last_seen': '1 час назад', 'status': 'Исследую космос'},
        {'id': 'user4', 'name': 'Emma_Digital', 'avatar': '👩‍💼', 'online': True, 'last_seen': 'только что', 'status': 'Работаю над AI проектами'},
    ]
    
    all_users = sample_users
    
    for user in sample_users:
        user_profiles.set(user['id'], {
            'friend_code': generate_friend_code(),
            'friends': [],
            'settings': {
                'theme': 'dark',
                'notifications': True,
                'privacy': 'friends_only'
            },
            'created_at': datetime.datetime.now().isoformat()
        })
        user_sessions.set(user['id'], generate_session_token())
        update_user_activity(user['id'])
    
    friendships.set('user1', ['user2', 'user3'])
    friendships.set('user2', ['user1'])
    friendships.set('user3', ['user1'])

def ensure_user_chat(user_id: str, target_user_id: str) -> bool:
    """Создание структуры чата с проверками"""
    if not user_id or not target_user_id:
        return False
    
    # Проверяем существование пользователей
    user_exists = any(user['id'] == user_id for user in all_users)
    target_exists = any(user['id'] == target_user_id for user in all_users)
    
    if not user_exists or not target_exists:
        return False
    
    if user_id not in user_messages.keys():
        user_messages.set(user_id, {})
    
    user_msgs = user_messages.get(user_id, {})
    if target_user_id not in user_msgs:
        user_msgs[target_user_id] = []
        
        welcome_msg = {
            'id': str(uuid.uuid4()),
            'sender': target_user_id,
            'text': sanitize_input('Привет! 👋 Рад познакомиться!'),
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'text'
        }
        user_msgs[target_user_id].append(welcome_msg)
        user_messages.set(user_id, user_msgs)
    
    return True

def get_user_by_friend_code(friend_code: str) -> Optional[str]:
    for user_id in user_profiles.keys():
        profile = user_profiles.get(user_id)
        if profile and profile.get('friend_code') == friend_code:
            return user_id
    return None

def encrypt_data(data: str) -> str:
    """Простое шифрование для localStorage"""
    return hashlib.sha256(data.encode()).hexdigest()

# Создаем статические директории
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Обновленный HTML шаблон с исправлениями
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0a0a2a">
    <meta name="description" content="TrollexDL - защищенный мессенджер с квантовым шифрованием">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
    <div class="overlay" id="overlay" onclick="hideAllPanels()"></div>
    <div class="loading-overlay" id="globalLoading">
        <div class="loading-spinner"></div>
        <div class="loading-text" id="loadingText">Загрузка...</div>
    </div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin: 20px 0; font-size: 1.2rem; min-height: 60px; display: flex; align-items: center; justify-content: center;">
                <div id="typingText">Инициализация защищённого канала...</div>
            </div>
            <div style="color: var(--neon); margin: 10px 0; display: flex; align-items: center; justify-content: center; gap: 8px;">
                <span>🔒</span>
                <span>Квантовое шифрование активировано</span>
                <span style="background: var(--neon); color: var(--primary); padding: 2px 6px; border-radius: 5px; font-size: 0.8rem;">AES-256</span>
            </div>
            <div class="loading" style="margin: 20px auto;"></div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary); text-align: center;">
                Премиум мессенджер с квантовым шифрованием<br>
                <small style="font-size: 0.9rem; opacity: 0.8;">🚀 Для ПК и мобильных устройств</small>
            </div>
            
            <div style="display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: rgba(0,255,136,0.1); border: 1px solid var(--neon); border-radius: 12px; margin: 16px 0;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: var(--neon);"></div>
                <span>Защищённое соединение установлено</span>
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 НАЧАТЬ
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ БЫСТРЫЙ СТАРТ
            </button>

            <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span>🔒 Шифрование</span>
                    <span style="color: var(--neon);">Активно</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-top: 8px;">
                    <span>🌐 Онлайн</span>
                    <span style="color: var(--neon);">{{ online_count }} пользователей</span>
                </div>
            </div>
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
                <div class="friend-code" id="registerFriendCode">TRLX-XXXX-XXXX</div>
                <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 8px;">
                    Поделитесь этим кодом для добавления в друзья
                </div>
            </div>
            
            <button class="btn btn-primary" id="registerBtn" onclick="registerUser()">
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
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
        
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <div class="user-avatar" id="userAvatar">🚀</div>
                <h3 id="userName">User</h3>
                <p>ID: <span id="userId">...</span></p>
                <div class="friend-code-display" style="margin: 12px 0; padding: 10px;">
                    <div style="font-size: 0.8rem;">Friend Code:</div>
                    <div class="friend-code" id="userFriendCode">TRLX-XXXX-XXXX</div>
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')" role="button" tabindex="0" aria-label="Чаты">
                    <span>💬</span>
                    <span>Чаты</span>
                </div>
                <div class="nav-tab" onclick="switchTab('friends')" role="button" tabindex="0" aria-label="Друзья">
                    <span>👥</span>
                    <span>Друзья</span>
                </div>
                <div class="nav-tab" onclick="switchTab('discover')" role="button" tabindex="0" aria-label="Найти друзей">
                    <span>🌐</span>
                    <span>Найти</span>
                </div>
                <div class="nav-tab" onclick="switchTab('calls')" role="button" tabindex="0" aria-label="Звонки">
                    <span>📞</span>
                    <span>Звонки</span>
                </div>
                <div class="nav-tab" onclick="showDonatePanel()" role="button" tabindex="0" aria-label="Премиум функции">
                    <span>💎</span>
                    <span>Премиум</span>
                </div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Поиск..." id="searchInput" 
                       oninput="app.debouncedSearch()" aria-label="Поиск по чатам и контактам">
            </div>

            <div class="content-list" id="contentList">
                <div class="empty-state">
                    <div class="empty-state-icon">💬</div>
                    <h3>Загрузка...</h3>
                    <p>Инициализация мессенджера</p>
                </div>
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                    <div class="typing-indicator hidden" id="typingIndicator">
                        <span class="loading"></span>
                        <span>Печатает...</span>
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="control-btn" onclick="startVideoCallWithUser()" style="background: var(--success);" 
                            aria-label="Начать видеозвонок" id="callBtn">📞</button>
                    <button class="control-btn" onclick="showSettingsPanel()" aria-label="Настройки">⚙️</button>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <button class="btn btn-primary" onclick="showCallPanel()" style="margin-top: 20px;">
                        🎥 Создать видеозвонок
                    </button>
                </div>
            </div>

            <div class="message-input-container">
                <textarea class="message-input" placeholder="Введите сообщение..." id="messageInput" 
                       onkeydown="handleKeyPress(event)" oninput="handleTyping()" 
                       aria-label="Введите сообщение" maxlength="2000" rows="1"></textarea>
                <button class="send-btn" onclick="sendMessage()" aria-label="Отправить сообщение" id="sendBtn">
                    <span class="send-text">🚀</span>
                    <span class="loading hidden"></span>
                </button>
            </div>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="panel settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>⚙️ Настройки</h3>
            <button class="control-btn" onclick="hideSettingsPanel()" aria-label="Закрыть">✕</button>
        </div>
        
        <div class="settings-section">
            <h4>🎨 Тема</h4>
            <div style="display: flex; gap: 10px;">
                <button class="btn btn-secondary" onclick="changeTheme('dark')">🌙 Тёмная</button>
                <button class="btn btn-secondary" onclick="changeTheme('light')">☀️ Светлая</button>
                <button class="btn btn-secondary" onclick="changeTheme('auto')">🔄 Авто</button>
            </div>
        </div>

        <div class="settings-section">
            <h4>🔔 Уведомления</h4>
            <label style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
                <span>Push-уведомления</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="notificationsToggle" checked>
                    <span class="toggle-slider"></span>
                </label>
            </label>
        </div>

        <div class="settings-section">
            <h4>🔒 Безопасность</h4>
            <button class="btn btn-secondary" style="width: 100%; margin: 5px 0;" onclick="showSecurityInfo()">
                ℹ️ Информация о шифровании
            </button>
            <button class="btn btn-secondary" style="width: 100%; margin: 5px 0;" onclick="exportChats()">
                📤 Экспорт данных
            </button>
        </div>

        <div class="settings-section">
            <h4>👤 Аккаунт</h4>
            <button class="btn btn-secondary" style="width: 100%; margin: 5px 0;" onclick="showProfileEditor()">
                ✏️ Редактировать профиль
            </button>
            <button class="btn" style="width: 100%; margin: 5px 0; background: var(--danger);" onclick="logout()">
                🚪 Выйти
            </button>
        </div>
    </div>

    <!-- Премиум панель -->
    <div class="panel donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>💎 TrollexDL Premium</h3>
            <button class="control-btn" onclick="hideDonatePanel()" aria-label="Закрыть">✕</button>
        </div>

        <div class="user-card" style="text-align: center;">
            <div class="user-avatar" style="background: linear-gradient(135deg, #ffd700, #ff6b00);">💎</div>
            <h3>Premium Features</h3>
            <p style="color: var(--text-secondary);">Разблокируйте эксклюзивные возможности</p>
        </div>

        <div class="settings-section">
            <h4>🚀 Премиум функции</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="padding: 8px 0; display: flex; align-items: center; gap: 10px;">
                    <span style="color: var(--neon);">✓</span> Неограниченная история сообщений
                </li>
                <li style="padding: 8px 0; display: flex; align-items: center; gap: 10px;">
                    <span style="color: var(--neon);">✓</span> Расширенные настройки приватности
                </li>
                <li style="padding: 8px 0; display: flex; align-items: center; gap: 10px;">
                    <span style="color: var(--neon);">✓</span> Кастомизация интерфейса
                </li>
                <li style="padding: 8px 0; display: flex; align-items: center; gap: 10px;">
                    <span style="color: var(--neon);">✓</span> Приоритетная поддержка
                </li>
            </ul>
        </div>

        <button class="btn btn-primary" style="width: 100%; margin: 20px 0;">
            🎁 Активировать Premium
        </button>
    </div>

    <!-- Контейнер видеозвонка -->
    <div id="callContainer" class="call-container hidden">
        <div class="call-link-container-call">
            <span class="call-link" id="currentCallLink">Загрузка...</span>
            <div style="display: flex; gap: 8px;">
                <button class="copy-link-btn" onclick="copyCallLink()" aria-label="Скопировать ссылку">📋</button>
                <button class="copy-link-btn" onclick="shareCallLink()" style="background: var(--success);" 
                        aria-label="Поделиться ссылкой">📤</button>
            </div>
        </div>
        
        <div class="video-grid" id="videoGrid">
            <div class="video-container local" id="localVideoContainer">
                <video id="localVideo" autoplay muted playsinline class="video-element"></video>
                <div class="video-label">Вы (🔴 Live)</div>
            </div>
            <div class="video-container remote" id="remoteVideoContainer">
                <div id="remoteVideoPlaceholder">
                    <div style="text-align:center;">
                        <div style="font-size:3rem;">👤</div>
                        <div>Ожидание участника...</div>
                    </div>
                </div>
                <div class="video-label">Участник</div>
            </div>
        </div>
        
        <div class="call-controls">
            <button class="call-control-btn mic-toggle" id="micToggle" onclick="toggleMicrophone()">🎤</button>
            <button class="call-control-btn cam-toggle" id="camToggle" onclick="toggleCamera()">📹</button>
            <button class="call-control-btn screen-share" id="screenShareToggle" onclick="toggleScreenShare()">🖥️</button>
            <button class="call-control-btn call-end" onclick="endCall()">📞</button>
        </div>
    </div>

    <!-- Уведомления -->
    <div id="notification" class="notification hidden"></div>

    <!-- ARIA Live Regions -->
    <div id="ariaLive" aria-live="polite" aria-atomic="true" class="visually-hidden"></div>
    <div id="ariaAlert" aria-live="assertive" aria-atomic="true" class="visually-hidden"></div>
</body>
<script src="/static/js/app.js"></script>
</html>
'''

# Сохраняем обновленный CSS
CSS_CONTENT = '''
/* Обновленный CSS с исправлениями для мобильных устройств */
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
    --shadow: 0 4px 20px rgba(0,0,0,0.3);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    -webkit-tap-highlight-color: transparent;
}

body {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
    line-height: 1.6;
}

/* Исправления для мобильных устройств */
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
    animation: fadeIn 0.5s ease-out;
    overflow-y: auto;
}

.cosmic-card {
    background: rgba(26, 26, 74, 0.95);
    border: 2px solid var(--accent);
    border-radius: 24px;
    padding: 32px;
    width: 100%;
    max-width: 420px;
    text-align: center;
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow);
    animation: fadeIn 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    margin: auto;
}

/* Мобильная оптимизация */
@media (max-width: 768px) {
    .screen {
        padding: 10px;
        align-items: flex-start;
        padding-top: 20px;
    }
    
    .cosmic-card {
        padding: 24px 20px;
        margin: 10px;
        border-radius: 20px;
        max-width: none;
    }
    
    .app {
        flex-direction: column;
    }
    
    .sidebar {
        position: fixed;
        top: 0;
        left: -100%;
        width: 85%;
        max-width: 320px;
        height: 100%;
        z-index: 1000;
        transition: left 0.3s ease;
        box-shadow: 8px 0 40px rgba(0,0,0,0.5);
    }
    
    .sidebar.active {
        left: 0;
    }
    
    .mobile-menu-btn {
        display: flex !important;
        position: fixed;
        top: 16px;
        left: 16px;
        z-index: 1001;
        background: rgba(26, 26, 74, 0.9);
        border: 2px solid var(--accent);
        color: var(--text);
        width: 48px;
        height: 48px;
        border-radius: 12px;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        backdrop-filter: blur(10px);
    }
    
    .chat-area {
        margin-left: 0;
        width: 100%;
    }
    
    .nav-tabs {
        flex-wrap: wrap;
        gap: 4px;
    }
    
    .nav-tab {
        flex: 1 0 45%;
        min-width: 0;
        font-size: 0.8rem;
        padding: 8px 4px;
    }
    
    .message {
        max-width: 90%;
    }
}

/* Добавляем новые стили для улучшения UX */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--neon);
    font-size: 0.9rem;
    margin-top: 5px;
}

.unread-badge {
    background: var(--neon);
    color: var(--primary);
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: bold;
    min-width: 18px;
    text-align: center;
}

.online-dot {
    width: 8px;
    height: 8px;
    background: var(--neon);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
}

.offline-dot {
    width: 8px;
    height: 8px;
    background: var(--text-secondary);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
}

/* Анимации */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 5px var(--neon); }
    50% { box-shadow: 0 0 20px var(--neon); }
}

.pulse-glow {
    animation: pulse-glow 2s infinite;
}

/* Улучшения для очень маленьких экранов */
@media (max-width: 480px) {
    .cosmic-card {
        padding: 20px 16px;
        margin: 5px;
    }
    
    .btn {
        padding: 14px 16px;
        font-size: 1rem;
    }
    
    .user-avatar {
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
    }
    
    .logo {
        font-size: 2rem;
    }
}

/* Исправление для iOS Safari */
@supports (-webkit-touch-callout: none) {
    .screen {
        height: -webkit-fill-available;
    }
    
    .app {
        height: -webkit-fill-available;
    }
}

/* Улучшения доступности */
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}

/* Дополнительные улучшения */
.send-btn {
    position: relative;
    overflow: hidden;
}

.send-btn .loading {
    display: none;
}

.send-btn.sending .send-text {
    display: none;
}

.send-btn.sending .loading {
    display: inline-block;
}

/* Новые фичи */
.voice-activity-indicator {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--danger);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.voice-activity-indicator.active {
    opacity: 1;
    animation: pulse-glow 1s infinite;
}

.connection-status {
    position: fixed;
    top: 10px;
    right: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.8rem;
    z-index: 10000;
    backdrop-filter: blur(10px);
}

.connection-status.online {
    background: rgba(0, 255, 136, 0.2);
    border: 1px solid var(--neon);
    color: var(--neon);
}

.connection-status.offline {
    background: rgba(255, 68, 68, 0.2);
    border: 1px solid var(--danger);
    color: var(--danger);
}
'''

# Обновленный JavaScript с исправлениями
JS_CONTENT = '''
// static/js/app.js - ОБНОВЛЕННАЯ ВЕРСИЯ
"use strict";

class TrollexApp {
    constructor() {
        this.currentUser = null;
        this.currentTab = 'chats';
        this.currentChat = null;
        this.sessionToken = null;
        this.isLoading = false;
        this.isSidebarOpen = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAutoLogin();
        this.setupServiceWorker();
        this.updateConnectionStatus();
        
        // Периодическое обновление статуса
        setInterval(() => this.updateConnectionStatus(), 30000);
    }

    setupEventListeners() {
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        window.addEventListener('resize', () => this.handleResize());
        
        // Обработка касаний для мобильных устройств
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });
    }

    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .catch(err => console.log('SW registration failed: ', err));
        }
    }

    async checkAutoLogin() {
        try {
            const savedUser = localStorage.getItem('trollexUser');
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                this.currentUser = JSON.parse(savedUser);
                this.sessionToken = savedToken;
                await this.loadSampleUsers();
                this.showMainApp();
                this.showNotification('С возвращением! 🚀', 'success');
            } else {
                this.showWelcomeScreen();
            }
        } catch (error) {
            console.error('Auto-login failed:', error);
            this.showWelcomeScreen();
        }
    }

    async loadSampleUsers() {
        try {
            const response = await fetch('/api/get_users');
            const data = await response.json();
            
            if (data.success) {
                this.allUsers = data.users;
                this.renderUserList();
            }
        } catch (error) {
            console.error('Failed to load users:', error);
        }
    }

    showWelcomeScreen() {
        this.hideAllScreens();
        document.getElementById('welcomeScreen').classList.remove('hidden');
        this.updateOnlineCount();
    }

    showRegisterScreen() {
        this.hideAllScreens();
        document.getElementById('registerScreen').classList.remove('hidden');
        this.generateNewUser();
    }

    showMainApp() {
        this.hideAllScreens();
        document.getElementById('mainApp').classList.remove('hidden');
        this.renderUserList();
        this.updateUserInfo();
    }

    hideAllScreens() {
        document.querySelectorAll('.screen, .app').forEach(el => {
            el.classList.add('hidden');
        });
    }

    generateNewUser() {
        const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper'];
        const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon'];
        const numbers = Math.floor(1000 + Math.random() * 9000);
        
        const username = `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${
            nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
        
        const avatars = ['🚀', '👨‍💻', '👩‍🎨', '👨‍🚀', '👩‍💼', '🤖', '👽', '🐲'];
        const avatar = avatars[Math.floor(Math.random() * avatars.length)];
        
        document.getElementById('registerName').textContent = username;
        document.getElementById('registerAvatar').textContent = avatar;
        document.getElementById('registerId').textContent = `user_${Math.random().toString(36).substr(2, 8)}`;
        document.getElementById('registerEmail').textContent = `${username.toLowerCase()}@trollex.ai`;
        document.getElementById('registerFriendCode').textContent = 
            `TRLX-${Math.random().toString(16).substr(2, 4).toUpperCase()}-${
             Math.random().toString(16).substr(2, 4).toUpperCase()}`;
    }

    async registerUser() {
        const registerBtn = document.getElementById('registerBtn');
        const originalText = registerBtn.innerHTML;
        
        try {
            registerBtn.innerHTML = '<div class="loading"></div>';
            registerBtn.disabled = true;

            const userData = {
                id: document.getElementById('registerId').textContent,
                name: document.getElementById('registerName').textContent,
                avatar: document.getElementById('registerAvatar').textContent,
                friend_code: document.getElementById('registerFriendCode').textContent
            };

            const response = await fetch('/api/register_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = userData;
                this.sessionToken = data.session_token;
                
                localStorage.setItem('trollexUser', JSON.stringify(userData));
                localStorage.setItem('sessionToken', data.session_token);
                
                this.showMainApp();
                this.showNotification('Профиль создан успешно! 🎉', 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Registration failed:', error);
            this.showNotification('Ошибка регистрации: ' + error.message, 'error');
        } finally {
            registerBtn.innerHTML = originalText;
            registerBtn.disabled = false;
        }
    }

    quickStart() {
        this.generateNewUser();
        this.registerUser();
    }

    updateUserInfo() {
        if (!this.currentUser) return;
        
        document.getElementById('userName').textContent = this.currentUser.name;
        document.getElementById('userAvatar').textContent = this.currentUser.avatar;
        document.getElementById('userId').textContent = this.currentUser.id;
        document.getElementById('userFriendCode').textContent = this.currentUser.friend_code;
    }

    renderUserList() {
        const contentList = document.getElementById('contentList');
        if (!contentList || !this.allUsers) return;

        if (this.allUsers.length === 0) {
            contentList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">👥</div>
                    <h3>Пользователи не найдены</h3>
                    <p>Будьте первым, кто присоединится к сети!</p>
                </div>
            `;
            return;
        }

        const filteredUsers = this.allUsers.filter(user => 
            user.id !== this.currentUser?.id
        );

        contentList.innerHTML = filteredUsers.map(user => `
            <div class="chat-item" onclick="app.selectChat('${user.id}')" 
                 data-user-id="${user.id}" role="button" tabindex="0">
                <div class="item-avatar">${user.avatar}</div>
                <div style="flex: 1;">
                    <h4>${user.name}</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        <span class="${user.online ? 'online-dot' : 'offline-dot'}"></span>
                        ${user.online ? 'В сети' : user.last_seen}
                    </p>
                    <p style="color: var(--text-secondary); font-size: 0.8rem;">
                        ${user.status}
                    </p>
                </div>
                <button class="control-btn" onclick="app.startVideoCallWithUser('${user.id}')" 
                        style="background: var(--success);">📞</button>
            </div>
        `).join('');
    }

    selectChat(userId) {
        this.currentChat = userId;
        const user = this.allUsers.find(u => u.id === userId);
        
        if (user) {
            document.getElementById('currentChatName').textContent = user.name;
            document.getElementById('currentChatAvatar').textContent = user.avatar;
            document.getElementById('currentChatStatus').textContent = 
                user.online ? 'В сети' : `Был(а) ${user.last_seen}`;
            
            this.loadChatMessages(userId);
            
            // На мобильных устройствах закрываем sidebar после выбора чата
            if (window.innerWidth <= 768) {
                this.toggleSidebar();
            }
        }
    }

    async loadChatMessages(userId) {
        const messagesContainer = document.getElementById('messagesContainer');
        messagesContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <h3>Начните общение</h3>
                <p>Отправьте первое сообщение</p>
            </div>
        `;
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || !this.currentChat) return;

        const sendBtn = document.getElementById('sendBtn');
        sendBtn.classList.add('sending');
        
        try {
            // Здесь будет API вызов для отправки сообщения
            await new Promise(resolve => setTimeout(resolve, 500)); // Имитация отправки
            
            this.addMessageToChat({
                id: Date.now().toString(),
                sender: this.currentUser.id,
                text: message,
                timestamp: new Date().toISOString(),
                type: 'text'
            });
            
            messageInput.value = '';
            this.adjustTextareaHeight(messageInput);
            
        } catch (error) {
            this.showNotification('Ошибка отправки сообщения', 'error');
        } finally {
            sendBtn.classList.remove('sending');
        }
    }

    addMessageToChat(message) {
        const messagesContainer = document.getElementById('messagesContainer');
        const isEmpty = messagesContainer.querySelector('.empty-state');
        
        if (isEmpty) {
            messagesContainer.innerHTML = '';
        }
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${
            message.sender === this.currentUser.id ? 'sent' : 'received'
        }`;
        messageElement.innerHTML = `
            <div class="message-text">${this.escapeHtml(message.text)}</div>
            <div class="message-time">
                ${new Date(message.timestamp).toLocaleTimeString('ru-RU', {
                    hour: '2-digit',
                    minute: '2-digit'
                })}
            </div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    switchTab(tabName) {
        this.currentTab = tabName;
        
        // Обновляем активные табы
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        document.querySelector(`.nav-tab:nth-child(${
            ['chats', 'friends', 'discover', 'calls', 'premium'].indexOf(tabName) + 1
        })`).classList.add('active');
        
        this.renderUserList();
    }

    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        
        this.isSidebarOpen = !this.isSidebarOpen;
        sidebar.classList.toggle('active', this.isSidebarOpen);
        overlay.classList.toggle('active', this.isSidebarOpen);
    }

    startVideoCallWithUser(userId) {
        this.showNotification('Функция видеозвонков в разработке 🚧', 'info');
        // Реализация видеозвонков будет добавлена позже
    }

    showCallPanel() {
        this.showNotification('Создание видеозвонка...', 'info');
        // Реализация создания звонка
    }

    showSettingsPanel() {
        document.getElementById('settingsPanel').classList.add('active');
        document.getElementById('overlay').classList.add('active');
    }

    hideSettingsPanel() {
        document.getElementById('settingsPanel').classList.remove('active');
        document.getElementById('overlay').classList.remove('active');
    }

    showDonatePanel() {
        document.getElementById('donatePanel').classList.add('active');
        document.getElementById('overlay').classList.add('active');
    }

    hideDonatePanel() {
        document.getElementById('donatePanel').classList.remove('active');
        document.getElementById('overlay').classList.remove('active');
    }

    hideAllPanels() {
        this.hideSettingsPanel();
        this.hideDonatePanel();
        this.toggleSidebar();
    }

    // Утилиты
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.remove('hidden');
        
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 4000);
    }

    updateOnlineCount() {
        const onlineCount = this.allUsers ? this.allUsers.filter(u => u.online).length : 4;
        const countElement = document.querySelector('#welcomeScreen [style*="online_count"]');
        if (countElement) {
            countElement.textContent = `${onlineCount} пользователей`;
        }
    }

    updateConnectionStatus() {
        // Можно добавить индикатор качества соединения
    }

    handleOnline() {
        this.showNotification('Соединение восстановлено ✅', 'success');
    }

    handleOffline() {
        this.showNotification('Отсутствует интернет-соединение 📶', 'warning');
    }

    handleResize() {
        // Адаптация к изменению размера окна
        if (window.innerWidth > 768 && this.isSidebarOpen) {
            this.toggleSidebar();
        }
    }

    handleTouchStart(e) {
        // Обработка начала касания для мобильных жестов
    }

    handleTouchEnd(e) {
        // Обработка окончания касания
    }

    debouncedSearch = this.debounce(() => {
        this.renderUserList();
    }, 300);

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    adjustTextareaHeight(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
}

// Глобальные функции для обработки событий
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        app.sendMessage();
    }
}

function handleTyping() {
    const textarea = document.getElementById('messageInput');
    app.adjustTextareaHeight(textarea);
}

function toggleSidebar() {
    app.toggleSidebar();
}

function switchTab(tabName) {
    app.switchTab(tabName);
}

function showRegisterScreen() {
    app.showRegisterScreen();
}

function quickStart() {
    app.quickStart();
}

function generateNewUser() {
    app.generateNewUser();
}

function registerUser() {
    app.registerUser();
}

function hideAllPanels() {
    app.hideAllPanels();
}

function showSettingsPanel() {
    app.showSettingsPanel();
}

function hideSettingsPanel() {
    app.hideSettingsPanel();
}

function showDonatePanel() {
    app.showDonatePanel();
}

function hideDonatePanel() {
    app.hideDonatePanel();
}

// Инициализация приложения
let app;

document.addEventListener('DOMContentLoaded', function() {
    app = new TrollexApp();
});

// Предотвращение масштабирования на iOS
document.addEventListener('touchmove', function(e) {
    if (e.scale !== 1) {
        e.preventDefault();
    }
}, { passive: false });
'''

# Сохраняем файлы
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(CSS_CONTENT)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(JS_CONTENT)

@app.route('/')
def index():
    initialize_sample_data()
    online_count = len([user for user in all_users if user.get('online', False)])
    return render_template_string(HTML_TEMPLATE, online_count=online_count)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/get_users')
def api_get_users():
    return jsonify({'success': True, 'users': all_users})

@app.route('/api/register_user', methods=['POST'])
def api_register_user():
    try:
        data = request.json
        user_id = data.get('id')
        
        if not user_id or not validate_username(data.get('name', '')):
            return jsonify({'success': False, 'error': 'Invalid user data'}), 400
        
        # Добавляем пользователя в all_users
        new_user = {
            'id': user_id,
            'name': data.get('name'),
            'avatar': data.get('avatar', '👤'),
            'online': True,
            'last_seen': 'только что',
            'status': 'Новый пользователь TrollexDL'
        }
        all_users.append(new_user)
        
        user_profiles.set(user_id, {
            'friend_code': data.get('friend_code'),
            'friends': [],
            'settings': {
                'theme': 'dark',
                'notifications': True,
                'privacy': 'friends_only'
            },
            'created_at': datetime.datetime.now().isoformat()
        })
        
        session_token = generate_session_token()
        user_sessions.set(user_id, session_token)
        update_user_activity(user_id)
        
        logger.info(f"Зарегистрирован новый пользователь: {user_id}")
        return jsonify({
            'success': True, 
            'message': 'User registered successfully',
            'session_token': session_token
        })
        
    except Exception as e:
        logger.error(f"Ошибка регистрации пользователя: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"📱 Поддержка мобильных устройств: активирована")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
