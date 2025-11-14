# app.py
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
    # В продакшене используйте библиотеки типа cryptography
    return hashlib.sha256(data.encode()).hexdigest()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0a0a2a">
    <meta name="description" content="TrollexDL - защищенный мессенджер с квантовым шифрованием">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <style>
        /* CSS будет в отдельном файле */
    </style>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- HTML структура -->
</body>
<script src="/static/js/app.js"></script>
</html>
'''

# Создаем статические директории
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Создаем CSS файл
CSS_CONTENT = '''
/* static/css/style.css */
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

/* Анимации */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes bounce {
    0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
    40%, 43% { transform: translate3d(0,-8px,0); }
    70% { transform: translate3d(0,-4px,0); }
    90% { transform: translate3d(0,-2px,0); }
}

/* Основные компоненты */
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
}

.hidden {
    display: none !important;
}

.visually-hidden {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    padding: 0 !important;
    margin: -1px !important;
    overflow: hidden !important;
    clip: rect(0, 0, 0, 0) !important;
    white-space: nowrap !important;
    border: 0 !important;
}

/* Космическая карточка */
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
}

.logo {
    font-size: 2.75rem;
    font-weight: 900;
    margin-bottom: 24px;
    background: linear-gradient(135deg, var(--neon), var(--accent-glow));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 40px rgba(107, 43, 217, 0.6);
}

/* Кнопки */
.btn {
    width: 100%;
    padding: 16px 24px;
    border: none;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    margin: 10px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    min-height: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
}

.btn:focus-visible {
    outline: 3px solid var(--neon);
    outline-offset: 2px;
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-glow));
    color: white;
    box-shadow: 0 4px 15px rgba(107, 43, 217, 0.4);
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(107, 43, 217, 0.6);
}

.btn-primary:active:not(:disabled) {
    transform: translateY(0);
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.08);
    color: var(--text);
    border: 2px solid var(--accent);
    backdrop-filter: blur(10px);
}

.btn-secondary:hover:not(:disabled) {
    background: rgba(107, 43, 217, 0.2);
    transform: translateY(-1px);
}

/* Карточка пользователя */
.user-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 24px;
    border-radius: 20px;
    margin: 20px 0;
    border: 1px solid var(--accent);
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease-out;
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
    margin: 0 auto 16px;
    box-shadow: 0 8px 25px rgba(107, 43, 217, 0.4);
    transition: transform 0.3s ease;
}

.user-avatar:hover {
    transform: scale(1.05) rotate(5deg);
}

/* Friend Code */
.friend-code-display {
    background: rgba(255,255,255,0.1);
    padding: 16px;
    border-radius: 16px;
    margin: 16px 0;
    text-align: center;
    border: 1px solid var(--accent);
    backdrop-filter: blur(10px);
}

.friend-code {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 1.2rem;
    color: var(--neon);
    margin: 8px 0;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}

/* Основное приложение */
.app {
    width: 100%;
    height: 100vh;
    display: flex;
    position: relative;
    background: var(--primary);
}

/* Sidebar */
.sidebar {
    width: 320px;
    background: rgba(26, 26, 74, 0.95);
    border-right: 2px solid var(--accent);
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(20px);
    z-index: 100;
    box-shadow: 4px 0 20px rgba(0,0,0,0.3);
}

.user-header {
    padding: 24px;
    background: linear-gradient(135deg, var(--accent), var(--accent-glow));
    text-align: center;
    position: relative;
    box-shadow: 0 4px 15px rgba(107, 43, 217, 0.4);
}

.user-header .user-avatar {
    width: 64px;
    height: 64px;
    font-size: 1.5rem;
    margin: 0 auto 12px;
}

/* Навигационные табы */
.nav-tabs {
    display: flex;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 6px;
    margin: 16px;
    flex-wrap: wrap;
    gap: 4px;
    backdrop-filter: blur(10px);
}

.nav-tab {
    flex: 1;
    padding: 12px 8px;
    text-align: center;
    cursor: pointer;
    border-radius: 12px;
    transition: all 0.3s ease;
    font-size: 0.9rem;
    min-width: 70px;
    min-height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 4px;
    touch-action: manipulation;
    border: 1px solid transparent;
}

.nav-tab:hover:not(.active) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--accent);
}

.nav-tab.active {
    background: var(--accent);
    box-shadow: 0 4px 12px rgba(107, 43, 217, 0.4);
    transform: translateY(-1px);
}

.nav-tab:focus-visible {
    outline: 2px solid var(--neon);
    outline-offset: 2px;
}

/* Поиск */
.search-box {
    padding: 16px;
}

.search-input {
    width: 100%;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid var(--accent);
    border-radius: 16px;
    color: var(--text);
    font-size: 1rem;
    min-height: 52px;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.search-input:focus {
    outline: none;
    border-color: var(--neon);
    box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.2);
    transform: translateY(-1px);
}

.search-input::placeholder {
    color: var(--text-secondary);
}

/* Список контента */
.content-list {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    scrollbar-width: thin;
    scrollbar-color: var(--accent) transparent;
}

.content-list::-webkit-scrollbar {
    width: 6px;
}

.content-list::-webkit-scrollbar-track {
    background: transparent;
}

.content-list::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 3px;
}

.content-list::-webkit-scrollbar-thumb:hover {
    background: var(--accent-glow);
}

/* Элементы чата */
.chat-item {
    display: flex;
    align-items: center;
    padding: 16px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    min-height: 72px;
    animation: fadeIn 0.4s ease-out;
}

.chat-item:hover {
    background: rgba(107, 43, 217, 0.2);
    border-color: var(--accent);
    transform: translateX(4px);
}

.chat-item:active {
    transform: scale(0.98);
}

.chat-item:focus-visible {
    outline: 2px solid var(--neon);
    outline-offset: 2px;
}

.item-avatar {
    width: 52px;
    height: 52px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent-glow));
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 14px;
    flex-shrink: 0;
    font-size: 1.3rem;
    box-shadow: 0 4px 12px rgba(107, 43, 217, 0.4);
}

/* Область чата */
.chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--primary);
    position: relative;
}

.chat-header {
    padding: 20px;
    background: rgba(26, 26, 74, 0.9);
    border-bottom: 2px solid var(--accent);
    display: flex;
    align-items: center;
    gap: 14px;
    min-height: 80px;
    backdrop-filter: blur(20px);
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.chat-header .item-avatar {
    width: 48px;
    height: 48px;
    font-size: 1.2rem;
    margin: 0;
}

/* Контейнер сообщений */
.messages-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
    scroll-behavior: smooth;
}

.message {
    max-width: 78%;
    padding: 14px 18px;
    border-radius: 20px;
    position: relative;
    word-wrap: break-word;
    animation: fadeIn 0.4s ease-out;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.message.received {
    background: rgba(107, 43, 217, 0.25);
    align-self: flex-start;
    border-bottom-left-radius: 6px;
    backdrop-filter: blur(10px);
}

.message.sent {
    background: linear-gradient(135deg, var(--accent), var(--accent-glow));
    align-self: flex-end;
    color: white;
    border-bottom-right-radius: 6px;
}

.message-time {
    font-size: 0.75rem;
    opacity: 0.8;
    margin-top: 6px;
    text-align: right;
}

.message-status {
    font-size: 0.7rem;
    margin-left: 6px;
}

/* Ввод сообщения */
.message-input-container {
    padding: 20px;
    background: rgba(26, 26, 74, 0.9);
    border-top: 2px solid var(--accent);
    display: flex;
    gap: 14px;
    align-items: flex-end;
    backdrop-filter: blur(20px);
}

.message-input {
    flex: 1;
    padding: 16px 20px;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid var(--accent);
    border-radius: 24px;
    color: var(--text);
    font-size: 1rem;
    min-height: 56px;
    max-height: 120px;
    resize: none;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.message-input:focus {
    outline: none;
    border-color: var(--neon);
    box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.2);
}

.message-input::placeholder {
    color: var(--text-secondary);
}

.send-btn {
    padding: 16px 20px;
    background: linear-gradient(135deg, var(--accent), var(--accent-glow));
    color: white;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    font-size: 1.1rem;
    min-height: 56px;
    min-width: 64px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(107, 43, 217, 0.4);
}

.send-btn:hover:not(:disabled) {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 20px rgba(107, 43, 217, 0.6);
}

.send-btn:active:not(:disabled) {
    transform: translateY(0) scale(1);
}

.send-btn:disabled {
    opacity: 0.6;
    transform: none;
    box-shadow: none;
}

/* Empty states */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
    animation: fadeIn 0.6s ease-out;
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 20px;
    opacity: 0.7;
}

.empty-state h3 {
    margin-bottom: 12px;
    font-weight: 600;
}

.empty-state p {
    margin-bottom: 24px;
    opacity: 0.8;
}

/* Уведомления */
.notification {
    position: fixed;
    top: 24px;
    right: 24px;
    background: linear-gradient(135deg, var(--accent), var(--accent-glow));
    color: white;
    padding: 16px 24px;
    border-radius: 16px;
    z-index: 4000;
    animation: slideIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    max-width: 380px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
}

.notification.error {
    background: linear-gradient(135deg, var(--danger), #ff6b6b);
}

.notification.warning {
    background: linear-gradient(135deg, var(--warning), #ffd93d);
}

.notification.success {
    background: linear-gradient(135deg, var(--success), #6bff8f);
}

/* Кнопки управления */
.control-btn {
    padding: 12px 16px;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.95rem;
    min-height: 48px;
    min-width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
    backdrop-filter: blur(10px);
}

.control-btn:hover:not(:disabled) {
    background: rgba(107, 43, 217, 0.3);
    transform: scale(1.05);
}

.control-btn:active:not(:disabled) {
    transform: scale(0.95);
}

.control-btn:focus-visible {
    outline: 2px solid var(--neon);
    outline-offset: 2px;
}

.control-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

/* Мобильное меню */
.mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.5rem;
    cursor: pointer;
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    min-height: 48px;
    min-width: 48px;
    z-index: 101;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.mobile-menu-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}

.mobile-menu-btn:active {
    transform: translateY(-50%) scale(0.9);
}

/* Панели */
.panel {
    position: fixed;
    top: 0;
    width: 90%;
    max-width: 420px;
    height: 100%;
    background: rgba(26, 26, 74, 0.98);
    border: 2px solid var(--accent);
    z-index: 2000;
    transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    padding: 24px;
    overflow-y: auto;
    backdrop-filter: blur(30px);
    box-shadow: -8px 0 40px rgba(0,0,0,0.5);
}

.settings-panel {
    right: -100%;
}

.settings-panel.active {
    right: 0;
}

.donate-panel {
    left: -100%;
}

.donate-panel.active {
    left: 0;
}

.call-panel {
    left: -100%;
}

.call-panel.active {
    left: 0;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    z-index: 1999;
    display: none;
    backdrop-filter: blur(5px);
}

.overlay.active {
    display: block;
    animation: fadeIn 0.3s ease-out;
}

/* Видеозвонки */
.call-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--primary);
    z-index: 3000;
    display: none;
    flex-direction: column;
}

.call-container.active {
    display: flex;
    animation: fadeIn 0.4s ease-out;
}

.video-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
    padding: 24px;
}

.video-container {
    position: relative;
    background: var(--secondary);
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid var(--accent);
    min-height: 240px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.video-container:hover {
    border-color: var(--neon);
    transform: translateY(-2px);
}

.video-element {
    width: 100%;
    height: 100%;
    object-fit: cover;
    background: var(--secondary);
}

.video-label {
    position: absolute;
    bottom: 16px;
    left: 16px;
    background: rgba(0,0,0,0.8);
    padding: 10px 16px;
    border-radius: 12px;
    font-size: 0.95rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Элементы управления звонком */
.call-controls {
    padding: 24px;
    background: rgba(26, 26, 74, 0.95);
    display: flex;
    justify-content: center;
    gap: 20px;
    border-top: 2px solid var(--accent);
    flex-wrap: wrap;
    backdrop-filter: blur(20px);
}

.call-control-btn {
    width: 68px;
    height: 68px;
    border-radius: 50%;
    border: none;
    font-size: 1.4rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 68px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.call-control-btn:hover:not(:disabled) {
    transform: translateY(-3px) scale(1.1);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}

.call-control-btn:active:not(:disabled) {
    transform: translateY(-1px) scale(1.05);
}

.call-control-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.call-control-btn.call-end {
    background: var(--danger);
    color: white;
}

.call-control-btn.call-end:hover:not(:disabled) {
    background: #ff6b6b;
    transform: translateY(-3px) scale(1.15);
}

.call-control-btn.mic-toggle {
    background: var(--success);
    color: white;
}

.call-control-btn.mic-toggle.muted {
    background: var(--danger);
}

.call-control-btn.cam-toggle {
    background: var(--accent);
    color: white;
}

.call-control-btn.cam-toggle.off {
    background: var(--warning);
}

.call-control-btn.screen-share {
    background: var(--warning);
    color: white;
}

.call-control-btn.screen-share.active {
    background: var(--neon);
    color: var(--primary);
}

/* Контейнер ссылки звонка */
.call-link-container-call {
    position: absolute;
    top: 24px;
    left: 24px;
    background: rgba(0,0,0,0.85);
    padding: 14px 20px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 10;
    max-width: calc(100% - 48px);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
}

.call-link {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    color: var(--neon);
    word-break: break-all;
    margin: 0;
    font-size: 0.9rem;
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}

.copy-link-btn {
    background: var(--accent);
    color: white;
    border: none;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
    min-height: 40px;
    transition: all 0.3s ease;
    flex-shrink: 0;
}

.copy-link-btn:hover {
    background: var(--accent-glow);
    transform: translateY(-1px);
}

.copy-link-btn:active {
    transform: translateY(0);
}

/* Индикаторы загрузки */
.loading {
    display: inline-block;
    width: 22px;
    height: 22px;
    border: 3px solid rgba(255,255,255,.2);
    border-radius: 50%;
    border-top-color: var(--neon);
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 5000;
    backdrop-filter: blur(10px);
}

.loading-overlay.active {
    display: flex;
    animation: fadeIn 0.3s ease-out;
}

.loading-spinner {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255,255,255,.1);
    border-radius: 50%;
    border-top-color: var(--neon);
    animation: spin 1s ease-in-out infinite;
}

.loading-text {
    color: var(--text);
    margin-top: 20px;
    font-size: 1.1rem;
    text-align: center;
}

/* Секции настроек */
.settings-section {
    margin-bottom: 24px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

.settings-section h4 {
    margin-bottom: 16px;
    color: var(--neon);
    font-size: 1.2rem;
}

/* Переключатели */
.toggle-switch {
    position: relative;
    display: inline-block;
    width: 54px;
    height: 28px;
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
    border-radius: 28px;
    border: 2px solid var(--accent);
}

.toggle-slider:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

input:checked + .toggle-slider {
    background-color: var(--success);
    border-color: var(--neon);
}

input:checked + .toggle-slider:before {
    transform: translateX(26px);
}

/* Сообщения об ошибках */
.error-message {
    color: var(--danger);
    font-size: 0.85rem;
    margin-top: 6px;
    display: none;
    animation: fadeIn 0.3s ease-out;
}

.input-error {
    border-color: var(--danger) !important;
    box-shadow: 0 0 0 3px rgba(255, 68, 68, 0.2) !important;
}

.input-error:focus {
    border-color: var(--danger) !important;
}

/* Адаптивность */
@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        height: 100%;
        transform: translateX(-100%);
        transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        z-index: 1000;
        width: 85%;
        max-width: 320px;
        box-shadow: 8px 0 40px rgba(0,0,0,0.5);
    }
    
    .sidebar.active {
        transform: translateX(0);
    }
    
    .mobile-menu-btn {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .nav-tab {
        font-size: 0.85rem;
        padding: 10px 6px;
        min-height: 56px;
    }

    .panel {
        width: 90%;
        max-width: none;
    }

    .video-grid {
        grid-template-columns: 1fr;
        padding: 16px;
        gap: 12px;
    }

    .video-container {
        min-height: 200px;
    }

    .call-control-btn {
        width: 56px;
        height: 56px;
        font-size: 1.2rem;
    }

    .call-link-container-call {
        top: 16px;
        left: 16px;
        right: 16px;
        max-width: none;
        flex-direction: column;
        gap: 8px;
        text-align: center;
    }

    .message {
        max-width: 88%;
    }

    .control-btn {
        min-height: 44px;
        min-width: 44px;
        padding: 10px;
    }

    .cosmic-card {
        margin: 10px;
        padding: 24px;
    }

    .notification {
        right: 16px;
        left: 16px;
        max-width: none;
    }

    /* Мобильная оптимизация звонков */
    .mobile-call-layout .video-container.local {
        position: fixed;
        top: 80px;
        right: 16px;
        width: 120px;
        height: 160px;
        z-index: 10;
        border: 2px solid var(--neon);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
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
        padding: 20px 16px;
        gap: 12px;
    }

    .mobile-call-layout .call-link-container-call {
        top: 100px;
    }
}

/* Улучшения для очень маленьких экранов */
@media (max-width: 480px) {
    .cosmic-card {
        padding: 20px;
        margin: 8px;
        border-radius: 20px;
    }
    
    .nav-tabs {
        flex-direction: column;
        gap: 4px;
    }
    
    .nav-tab {
        margin: 2px 0;
        min-height: 52px;
    }
    
    .call-controls {
        gap: 8px;
        padding: 16px 12px;
    }
    
    .call-control-btn {
        width: 50px;
        height: 50px;
        font-size: 1.1rem;
    }

    .user-header {
        padding: 20px;
    }

    .chat-header {
        padding: 16px;
        min-height: 72px;
    }

    .message-input-container {
        padding: 16px;
    }

    .empty-state {
        padding: 40px 16px;
    }

    .empty-state-icon {
        font-size: 3rem;
    }
}

/* Улучшения доступности */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* High contrast mode */
@media (prefers-contrast: high) {
    :root {
        --primary: #000000;
        --secondary: #111111;
        --text: #ffffff;
        --text-secondary: #cccccc;
    }

    .cosmic-card,
    .user-card,
    .settings-section {
        border-width: 3px;
    }
}

/* Dark mode (по умолчанию) */
@media (prefers-color-scheme: dark) {
    :root {
        --primary: #0a0a2a;
        --secondary: #1a1a4a;
    }
}

/* Поддержка Safari */
@supports (-webkit-touch-callout: none) {
    .message-input {
        font-size: 16px; /* Предотвращает zoom в iOS */
    }
    
    .sidebar {
        -webkit-overflow-scrolling: touch;
    }
}

/* Поддержка старых браузеров */
@supports not (backdrop-filter: blur(10px)) {
    .cosmic-card,
    .sidebar,
    .notification,
    .call-link-container-call {
        background: rgba(26, 26, 74, 0.98);
    }
}

/* Print styles */
@media print {
    .call-container,
    .panel,
    .overlay,
    .mobile-menu-btn,
    .message-input-container {
        display: none !important;
    }
    
    .app {
        display: block;
    }
    
    .sidebar {
        position: static;
        width: 100%;
    }
}

/* Focus styles for keyboard navigation */
.focus-visible {
    outline: 3px solid var(--neon);
    outline-offset: 2px;
}

/* Selection styles */
::selection {
    background: rgba(107, 43, 217, 0.3);
    color: white;
}

::-moz-selection {
    background: rgba(107, 43, 217, 0.3);
    color: white;
}

/* Scrollbar styling for Firefox */
* {
    scrollbar-width: thin;
    scrollbar-color: var(--accent) transparent;
}

/* Custom properties for theming */
[data-theme="light"] {
    --primary: #ffffff;
    --secondary: #f0f0f0;
    --text: #333333;
    --text-secondary: #666666;
    --accent: #6c2bd9;
    --accent-glow: #8b5cf6;
    --neon: #00a86b;
}

[data-theme="auto"] {
    /* Автоматическая тема будет применена через JavaScript */
}

/* RTL support */
[dir="rtl"] {
    text-align: right;
}

[dir="rtl"] .sidebar {
    border-right: none;
    border-left: 2px solid var(--accent);
}

[dir="rtl"] .chat-item:hover {
    transform: translateX(-4px);
}

/* Loading states */
.is-loading {
    pointer-events: none;
    opacity: 0.7;
}

.is-loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid transparent;
    border-top-color: currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Error states */
.has-error {
    border-color: var(--danger);
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

/* Success states */
.has-success {
    border-color: var(--success);
}

/* Warning states */
.has-warning {
    border-color: var(--warning);
}

/* Disabled states */
.is-disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}

/* Hidden content for screen readers */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
'''

# Создаем JavaScript файл
JS_CONTENT = '''
// static/js/app.js
"use strict";

// Константы приложения
const APP_CONSTANTS = {
    MAX_MESSAGE_LENGTH: 2000,
    MAX_USERNAME_LENGTH: 20,
    DEBOUNCE_DELAY: 300,
    RATE_LIMIT_WINDOW: 1000,
    MAX_RATE_LIMIT: 5,
    API_TIMEOUT: 10000,
    TYPING_INDICATOR_TIMEOUT: 3000,
    MESSAGE_PAGE_SIZE: 50,
    CACHE_TTL: 5 * 60 * 1000, // 5 minutes
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000
};

// Утилиты
class Utils {
    static sanitizeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    static escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\\\$&');
    }

    static debounce(func, wait, immediate = false) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    }

    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    static generateId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    static formatTime(date) {
        return new Date(date).toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    static formatDate(date) {
        return new Date(date).toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }

    static isToday(date) {
        const today = new Date();
        const target = new Date(date);
        return today.toDateString() === target.toDateString();
    }

    static isYesterday(date) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const target = new Date(date);
        return yesterday.toDateString() === target.toDateString();
    }

    static async copyToClipboard(text) {
        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(text);
                return true;
            } else {
                // Fallback для старых браузеров
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                const successful = document.execCommand('copy');
                document.body.removeChild(textArea);
                return successful;
            }
        } catch (err) {
            console.error('Failed to copy text: ', err);
            return false;
        }
    }

    static async shareContent(data) {
        if (navigator.share) {
            try {
                await navigator.share(data);
                return true;
            } catch (err) {
                if (err.name !== 'AbortError') {
                    console.error('Share failed:', err);
                }
                return false;
            }
        }
        return false;
    }

    static validateFriendCode(code) {
        return /^TRLX-[A-F0-9]{4}-[A-F0-9]{4}$/.test(code);
    }

    static validateUsername(username) {
        return /^[a-zA-Z0-9_]{3,20}$/.test(username);
    }

    static validateMessage(text) {
        if (!text || !text.trim()) {
            return { isValid: false, error: 'Сообщение не может быть пустым' };
        }
        
        if (text.length > APP_CONSTANTS.MAX_MESSAGE_LENGTH) {
            return { 
                isValid: false, 
                error: `Сообщение слишком длинное (максимум ${APP_CONSTANTS.MAX_MESSAGE_LENGTH} символов)` 
            };
        }

        // Проверка на спам
        if (/(.)\\1{10,}/.test(text)) {
            return { isValid: false, error: 'Сообщение содержит подозрительный контент' };
        }

        return { isValid: true, error: '' };
    }

    static getBrowserInfo() {
        const ua = navigator.userAgent;
        return {
            isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua),
            isIOS: /iPad|iPhone|iPod/.test(ua),
            isSafari: /^((?!chrome|android).)*safari/i.test(ua),
            isChrome: /chrome|chromium|crios/i.test(ua),
            isFirefox: /firefox|fxios/i.test(ua)
        };
    }

    static supportsWebRTC() {
        return !!(navigator.mediaDevices && 
                 navigator.mediaDevices.getUserMedia &&
                 window.RTCPeerConnection);
    }

    static supportsScreenShare() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia);
    }

    static async checkCameraAccess() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            stream.getTracks().forEach(track => track.stop());
            return true;
        } catch (err) {
            return false;
        }
    }

    static async checkMicrophoneAccess() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            return true;
        } catch (err) {
            return false;
        }
    }
}

// Менеджер кэширования
class CacheManager {
    constructor() {
        this.cache = new Map();
        this.defaultTTL = APP_CONSTANTS.CACHE_TTL;
    }

    set(key, value, ttl = this.defaultTTL) {
        const item = {
            value,
            expiry: Date.now() + ttl
        };
        this.cache.set(key, item);
    }

    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;

        if (Date.now() > item.expiry) {
            this.cache.delete(key);
            return null;
        }

        return item.value;
    }

    delete(key) {
        this.cache.delete(key);
    }

    clear() {
        this.cache.clear();
    }

    cleanup() {
        const now = Date.now();
        for (const [key, item] of this.cache.entries()) {
            if (now > item.expiry) {
                this.cache.delete(key);
            }
        }
    }
}

// Менеджер состояния приложения
class AppState {
    constructor() {
        this.currentUser = null;
        this.currentTab = 'chats';
        this.currentChat = null;
        this.sessionToken = null;
        this.allUsers = [];
        this.friends = [];
        this.friendRequests = [];
        this.currentCallLink = '';
        this.isLoading = false;
        this.pendingRequests = new Set();
        this.typingUsers = new Map();
        this.unreadCounts = new Map();
        this.messagePages = new Map();
        
        // Video call state
        this.localStream = null;
        this.currentCallId = null;
        this.isInCall = false;
        this.isMicMuted = false;
        this.isCamOff = false;
        this.isScreenSharing = false;
        this.isRecording = false;
        this.isBackgroundBlurred = false;
        this.screenStream = null;

        // Rate limiting
        this.rateLimitMap = new Map();
        
        // Cache
        this.cache = new CacheManager();
        
        // Network state
        this.isOnline = navigator.onLine;
        this.retryCounts = new Map();
        
        // UI state
        this.scrollPosition = new Map();
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        const loader = document.getElementById('globalLoading');
        if (loader) {
            if (loading) {
                loader.classList.add('active');
            } else {
                loader.classList.remove('active');
            }
        }
        this.updateButtonStates();
    }
    
    addPendingRequest(requestId) {
        this.pendingRequests.add(requestId);
        this.updateButtonStates();
    }
    
    removePendingRequest(requestId) {
        this.pendingRequests.delete(requestId);
        this.updateButtonStates();
    }
    
    updateButtonStates() {
        const isBusy = this.pendingRequests.size > 0 || this.isLoading;
        document.querySelectorAll('.btn, .control-btn, .call-control-btn').forEach(btn => {
            if (!btn.classList.contains('call-end') && !btn.classList.contains('mobile-menu-btn')) {
                btn.disabled = isBusy;
                btn.classList.toggle('is-loading', isBusy);
            }
        });
    }

    checkRateLimit(action, limit = APP_CONSTANTS.MAX_RATE_LIMIT, windowMs = APP_CONSTANTS.RATE_LIMIT_WINDOW) {
        const key = `${action}_${this.currentUser?.id || 'anonymous'}`;
        const now = Date.now();
        const record = this.rateLimitMap.get(key);
        
        if (!record || now - record.timestamp > windowMs) {
            this.rateLimitMap.set(key, { count: 1, timestamp: now });
            return true;
        }
        
        if (record.count >= limit) {
            return false;
        }
        
        record.count++;
        this.rateLimitMap.set(key, record);
        return true;
    }

    cleanupRateLimits() {
        const now = Date.now();
        for (const [key, record] of this.rateLimitMap.entries()) {
            if (now - record.timestamp > APP_CONSTANTS.RATE_LIMIT_WINDOW) {
                this.rateLimitMap.delete(key);
            }
        }
    }

    setUnreadCount(chatId, count) {
        this.unreadCounts.set(chatId, count);
        this.updateUnreadBadges();
    }

    incrementUnreadCount(chatId) {
        const current = this.unreadCounts.get(chatId) || 0;
        this.setUnreadCount(chatId, current + 1);
    }

    clearUnreadCount(chatId) {
        this.unreadCounts.set(chatId, 0);
        this.updateUnreadBadges();
    }

    updateUnreadBadges() {
        // Implementation for updating UI badges
        document.querySelectorAll('.chat-item').forEach(item => {
            const userId = item.dataset.userId;
            if (userId) {
                const count = this.unreadCounts.get(userId) || 0;
                let badge = item.querySelector('.unread-badge');
                
                if (count > 0) {
                    if (!badge) {
                        badge = document.createElement('div');
                        badge.className = 'unread-badge';
                        item.appendChild(badge);
                    }
                    badge.textContent = count > 99 ? '99+' : count.toString();
                } else if (badge) {
                    badge.remove();
                }
            }
        });
    }

    saveScrollPosition(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            this.scrollPosition.set(containerId, container.scrollTop);
        }
    }

    restoreScrollPosition(containerId) {
        const position = this.scrollPosition.get(containerId);
        const container = document.getElementById(containerId);
        if (container && position !== undefined) {
            container.scrollTop = position;
        }
    }

    async retryOperation(operation, operationName, maxAttempts = APP_CONSTANTS.RETRY_ATTEMPTS) {
        let lastError;
        
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return await operation();
            } catch (error) {
                lastError = error;
                console.warn(`${operationName} attempt ${attempt} failed:`, error);
                
                if (attempt < maxAttempts) {
                    await new Promise(resolve => 
                        setTimeout(resolve, APP_CONSTANTS.RETRY_DELAY * attempt)
                    );
                }
            }
        }
        
        throw lastError;
    }
}

// Менеджер сетевых запросов
class NetworkManager {
    constructor() {
        this.baseURL = window.location.origin;
        this.pendingRequests = new Map();
        this.requestTimeouts = new Map();
    }

    async request(endpoint, options = {}) {
        const controller = new AbortController();
        const requestId = Utils.generateId();
        
        const config = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            signal: controller.signal,
            ...options
        };

        // Добавляем timeout
        const timeoutId = setTimeout(() => {
            controller.abort();
            this.pendingRequests.delete(requestId);
        }, APP_CONSTANTS.API_TIMEOUT);

        this.requestTimeouts.set(requestId, timeoutId);
        this.pendingRequests.set(requestId, controller);

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } finally {
            clearTimeout(timeoutId);
            this.requestTimeouts.delete(requestId);
            this.pendingRequests.delete(requestId);
        }
    }

    cancelAllRequests() {
        for (const [requestId, controller] of this.pendingRequests) {
            controller.abort();
            const timeoutId = this.requestTimeouts.get(requestId);
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
        }
        this.pendingRequests.clear();
        this.requestTimeouts.clear();
    }

    async get(endpoint) {
        return this.request(endpoint);
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
}

// Менеджер уведомлений
class NotificationManager {
    constructor() {
        this.notificationQueue = [];
        this.isShowing = false;
        this.container = null;
        this.init();
    }

    init() {
        this.container = document.getElementById('notification');
        if (!this.container) {
            this.createContainer();
        }
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'notification';
        this.container.className = 'notification hidden';
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 4000) {
        this.notificationQueue.push({ message, type, duration });
        this.processQueue();
    }

    processQueue() {
        if (this.isShowing || this.notificationQueue.length === 0) {
            return;
        }

        this.isShowing = true;
        const { message, type, duration } = this.notificationQueue.shift();

        this.container.textContent = message;
        this.container.className = `notification ${type}`;
        this.container.classList.remove('hidden');

        // Анимация появления
        this.container.style.animation = 'slideIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';

        setTimeout(() => {
            this.hide();
        }, duration);
    }

    hide() {
        this.container.classList.add('hidden');
        this.container.style.animation = '';
        
        setTimeout(() => {
            this.isShowing = false;
            this.processQueue();
        }, 300);
    }

    success(message, duration = 4000) {
        this.show(message, 'success', duration);
    }

    error(message, duration = 5000) {
        this.show(message, 'error', duration);
    }

    warning(message, duration = 4500) {
        this.show(message, 'warning', duration);
    }

    info(message, duration = 4000) {
        this.show(message, 'info', duration);
    }
}

// Менеджер медиа (камера, микрофон, экран)
class MediaManager {
    constructor() {
        this.localStream = null;
        this.screenStream = null;
        this.audioContext = null;
        this.analyser = null;
        this.isSpeaking = false;
    }

    async getUserMedia(constraints) {
        try {
            return await navigator.mediaDevices.getUserMedia(constraints);
        } catch (error) {
            this.handleMediaError(error);
            throw error;
        }
    }

    async getDisplayMedia(constraints) {
        try {
            return await navigator.mediaDevices.getDisplayMedia(constraints);
        } catch (error) {
            if (error.name !== 'NotAllowedError') {
                this.handleMediaError(error);
            }
            throw error;
        }
    }

    handleMediaError(error) {
        let message = 'Ошибка доступа к медиаустройствам';
        
        switch (error.name) {
            case 'NotAllowedError':
                message = 'Доступ к камере/микрофону запрещен. Разрешите доступ в настройках браузера.';
                break;
            case 'NotFoundError':
                message = 'Камера или микрофон не найдены. Проверьте подключение устройств.';
                break;
            case 'NotReadableError':
                message = 'Ошибка доступа к камере/микрофону. Устройство может быть занято другим приложением.';
                break;
            case 'OverconstrainedError':
                message = 'Запрошенные настройки камеры/микрофона не поддерживаются.';
                break;
            default:
                message = `Ошибка медиаустройства: ${error.message}`;
        }
        
        app.notifications.error(message);
    }

    stopStream(stream) {
        if (stream) {
            stream.getTracks().forEach(track => {
                track.stop();
                stream.removeTrack(track);
            });
        }
    }

    stopAllStreams() {
        this.stopStream(this.localStream);
        this.stopStream(this.screenStream);
        this.localStream = null;
        this.screenStream = null;
    }

    async switchCamera() {
        if (!this.localStream) return null;

        const videoTrack = this.localStream.getVideoTracks()[0];
        if (!videoTrack) return null;

        const constraints = videoTrack.getConstraints();
        const facingMode = constraints.facingMode === 'user' ? 'environment' : 'user';

        this.stopStream(this.localStream);

        try {
            this.localStream = await this.getUserMedia({
                video: { facingMode },
                audio: true
            });
            return this.localStream;
        } catch (error) {
            console.error('Error switching camera:', error);
            return null;
        }
    }

    async takeSnapshot(videoElement) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        ctx.drawImage(videoElement, 0, 0);
        
        return canvas.toDataURL('image/jpeg', 0.8);
    }

    initAudioAnalysis(stream) {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        
        this.analyser = this.audioContext.createAnalyser();
        const source = this.audioContext.createMediaStreamSource(stream);
        source.connect(this.analyser);
        
        this.analyser.fftSize = 256;
        this.startVoiceDetection();
    }

    startVoiceDetection() {
        if (!this.analyser) return;

        const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
        
        const detect = () => {
            this.analyser.getByteFrequencyData(dataArray);
            
            let sum = 0;
            for (let i = 0; i < dataArray.length; i++) {
                sum += dataArray[i];
            }
            const average = sum / dataArray.length;
            
            const speaking = average > 30; // Пороговое значение
            if (speaking !== this.isSpeaking) {
                this.isSpeaking = speaking;
                this.onSpeakingStateChange(speaking);
            }
            
            requestAnimationFrame(detect);
        };
        
        detect();
    }

    onSpeakingStateChange(speaking) {
        // Можно обновлять UI при изменении состояния голосовой активности
        const indicator = document.getElementById('voiceActivityIndicator');
        if (indicator) {
            indicator.classList.toggle('active', speaking);
        }
    }

    // Адаптивное качество видео based on network conditions
    async getAdaptiveVideoConstraints() {
        const browserInfo = Utils.getBrowserInfo();
        const isMobile = browserInfo.isMobile;
        const isSlowNetwork = !navigator.connection || 
                             navigator.connection.effectiveType === 'slow-2g' || 
                             navigator.connection.effectiveType === '2g';

        if (isSlowNetwork) {
            return {
                width: { ideal: 640 },
                height: { ideal: 480 },
                frameRate: { ideal: 15, max: 20 }
            };
        }

        if (isMobile) {
            return {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                frameRate: { ideal: 24, max: 30 }
            };
        }

        return {
            width: { ideal: 1920 },
            height: { ideal: 1080 },
            frameRate: { ideal: 30, max: 60 }
        };
    }
}

// Главный класс приложения
class TrollexApp {
    constructor() {
        this.state = new AppState();
        this.network = new NetworkManager();
        this.notifications = new NotificationManager();
        this.media = new MediaManager();
        this.cache = new CacheManager();
        
        this.debouncedSearch = Utils.debounce(() => this.loadContent(), APP_CONSTANTS.DEBOUNCE_DELAY);
        this.typingTimeout = null;
        this.cleanupInterval = null;
        this.reconnectTimeout = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupServiceWorker();
        this.setupNetworkMonitoring();
        this.startCleanupInterval();
        this.initializeApp();
    }

    setupEventListeners() {
        // Window events
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        window.addEventListener('beforeunload', () => this.cleanup());
        window.addEventListener('unload', () => this.cleanup());
        window.addEventListener('resize', Utils.throttle(() => this.handleResize(), 250));
        window.addEventListener('keydown', (e) => this.handleGlobalKeydown(e));
        
        // Visibility change
        document.addEventListener('visibilitychange', () => this.handleVisibilityChange());
        
        // Touch events for mobile
        document.addEventListener('touchstart', () => {}, { passive: true });
        
        // Context menu prevention on mobile
        document.addEventListener('contextmenu', (e) => {
            if (Utils.getBrowserInfo().isMobile) {
                e.preventDefault();
            }
        });
    }

    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        }
    }

    setupNetworkMonitoring() {
        if (navigator.connection) {
            navigator.connection.addEventListener('change', () => {
                this.handleConnectionChange();
            });
        }
    }

    startCleanupInterval() {
        this.cleanupInterval = setInterval(() => {
            this.state.cleanupRateLimits();
            this.cache.cleanup();
        }, 60000); // Cleanup every minute
    }

    async initializeApp() {
        try {
            await this.showLoadingScreen();
            await this.checkAutoLogin();
        } catch (error) {
            console.error('App initialization failed:', error);
            this.notifications.error('Ошибка инициализации приложения');
            this.showWelcomeScreen();
        }
    }

    async showLoadingScreen() {
        const texts = [
            "Инициализация квантового интерфейса...",
            "Загрузка защищённого канала...", 
            "Подключение к нейросети...",
            "Активация протокола шифрования...",
            "Готово! Запускаем TrollexDL..."
        ];
        
        const typingElement = document.getElementById('typingText');
        if (!typingElement) return;

        for (let i = 0; i < texts.length; i++) {
            typingElement.textContent = texts[i];
            await new Promise(resolve => setTimeout(resolve, 800));
        }

        await new Promise(resolve => setTimeout(resolve, 500));
        document.getElementById('loadingScreen').classList.add('hidden');
    }

    // ... остальные методы класса TrollexApp

    handleOnline() {
        this.state.isOnline = true;
        this.notifications.success('Соединение восстановлено ✅');
        this.retryPendingOperations();
    }

    handleOffline() {
        this.state.isOnline = false;
        this.notifications.warning('Отсутствует интернет-соединение 📶');
    }

    handleResize() {
        // Адаптация UI при изменении размера окна
        if (this.state.isInCall && window.innerWidth <= 768) {
            document.getElementById('videoGrid').classList.add('mobile-call-layout');
        } else {
            document.getElementById('videoGrid').classList.remove('mobile-call-layout');
        }
    }

    handleGlobalKeydown(e) {
        // Глобальные горячие клавиши
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'k':
                    e.preventDefault();
                    document.getElementById('searchInput')?.focus();
                    break;
                case '/':
                    e.preventDefault();
                    document.getElementById('messageInput')?.focus();
                    break;
                case 'n':
                    e.preventDefault();
                    this.showAddFriendByLink();
                    break;
            }
        }

        // Escape key
        if (e.key === 'Escape') {
            this.hideAllPanels();
            if (this.state.isInCall) {
                this.endCall();
            }
        }
    }

    handleVisibilityChange() {
        if (document.hidden) {
            // Страница скрыта
            this.state.saveScrollPosition('messagesContainer');
        } else {
            // Страница видима
            setTimeout(() => {
                this.state.restoreScrollPosition('messagesContainer');
            }, 100);
        }
    }

    handleConnectionChange() {
        if (navigator.connection) {
            const effectiveType = navigator.connection.effectiveType;
            if (effectiveType === 'slow-2g' || effectiveType === '2g') {
                this.notifications.warning('Медленное соединение ⚠️');
            }
        }
    }

    async retryPendingOperations() {
        // Повторная отправка неудачных операций
        // Implementation depends on specific operations
    }

    cleanup() {
        this.media.stopAllStreams();
        this.network.cancelAllRequests();
        
        if (this.cleanupInterval) {
            clearInterval(this.cleanupInterval);
        }
        
        if (this.reconnectTimeout) {
            clearTimeout(this.reconnectTimeout);
        }
        
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }
    }

    // Основные методы приложения...
    async checkAutoLogin() {
        try {
            const savedUser = this.getEncryptedItem('trollexUser');
            const savedToken = this.getEncryptedItem('sessionToken');
            
            if (savedUser && savedToken) {
                this.state.currentUser = savedUser;
                this.state.sessionToken = savedToken;
                await this.loadSampleUsers();
                this.showMainApp();
                this.notifications.success('С возвращением! 🚀');
            } else {
                this.showWelcomeScreen();
            }
        } catch (error) {
            console.error('Auto-login failed:', error);
            this.showWelcomeScreen();
        }
    }

    getEncryptedItem(key) {
        try {
            const encrypted = localStorage.getItem(key);
            if (!encrypted) return null;
            
            // В продакшене используйте proper encryption
            return JSON.parse(encrypted);
        } catch (error) {
            console.error('Error reading encrypted item:', error);
            return null;
        }
    }

    setEncryptedItem(key, value) {
        try {
            // В продакшене используйте proper encryption
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error setting encrypted item:', error);
        }
    }

    // ... остальная реализация методов приложения
}

// Инициализация приложения
let app;

document.addEventListener('DOMContentLoaded', function() {
    try {
        app = new TrollexApp();
        
        // Предотвращение выхода без сохранения
        window.addEventListener('beforeunload', function(e) {
            if (app.state.pendingRequests.size > 0) {
                e.preventDefault();
                e.returnValue = '';
                return '';
            }
        });
        
    } catch (error) {
        console.error('Failed to initialize app:', error);
        // Fallback to basic functionality
        const errorScreen = document.createElement('div');
        errorScreen.innerHTML = `
            <div class="screen">
                <div class="cosmic-card">
                    <div class="logo">TrollexDL</div>
                    <div style="color: var(--danger); margin: 20px 0;">
                        Ошибка загрузки приложения. Пожалуйста, обновите страницу.
                    </div>
                    <button class="btn btn-primary" onclick="window.location.reload()">
                        🔄 Обновить
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(errorScreen);
    }
});

// Глобальные функции для HTML атрибутов
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
}

function switchTab(tabName) {
    if (app) {
        app.switchTab(tabName);
    }
}

function showRegisterScreen() {
    if (app) {
        app.showRegisterScreen();
    }
}

function quickStart() {
    if (app) {
        app.quickStart();
    }
}

// Fallback для старых браузеров
if (!window.Promise) {
    // Load polyfills
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.min.js';
    document.head.appendChild(script);
}

if (!window.fetch) {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/whatwg-fetch@3.6.2/dist/fetch.umd.min.js';
    document.head.appendChild(script);
}
'''

# Создаем файлы
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(CSS_CONTENT)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(JS_CONTENT)

# Обновленный HTML шаблон
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
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary);">
                Премиум мессенджер с квантовым шифрованием
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
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
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
                    <span>Донат</span>
                </div>
                <div class="nav-tab" onclick="showSettings()" role="button" tabindex="0" aria-label="Настройки">
                    <span>⚙️</span>
                    <span>Настройки</span>
                </div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Поиск..." id="searchInput" 
                       oninput="debouncedSearch()" aria-label="Поиск по чатам и контактам">
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
                <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                    <div class="typing-indicator hidden" id="typingIndicator">
                        <span class="loading"></span>
                        <span>Печатает...</span>
                    </div>
                </div>
                <button class="control-btn" onclick="startVideoCallWithUser()" style="background: var(--success);" 
                        aria-label="Начать видеозвонок" id="callBtn">📞</button>
                <button class="control-btn" onclick="showFileShare()" style="background: var(--warning);" 
                        aria-label="Поделиться файлом" id="fileShareBtn">📎</button>
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
                <button class="send-btn" onclick="sendMessage()" aria-label="Отправить сообщение" id="sendBtn">🚀</button>
            </div>
        </div>
    </div>

    <!-- Контейнер видеозвонка -->
    <div id="callContainer" class="call-container">
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
                <div class="voice-activity-indicator hidden" id="voiceActivityIndicator"></div>
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
            <button class="call-control-btn mic-toggle" id="micToggle" onclick="toggleMicrophone()" 
                    aria-label="Включить/выключить микрофон">🎤</button>
            <button class="call-control-btn cam-toggle" id="camToggle" onclick="toggleCamera()" 
                    aria-label="Включить/выключить камеру">📹</button>
            <button class="call-control-btn screen-share" id="screenShareToggle" onclick="toggleScreenShare()" 
                    aria-label="Демонстрация экрана">🖥️</button>
            <button class="call-control-btn" onclick="toggleRecording()" style="background: var(--cyber);" 
                    aria-label="Начать/остановить запись" id="recordBtn">⏺️</button>
            <button class="call-control-btn" onclick="switchCamera()" style="background: var(--accent-glow);" 
                    aria-label="Переключить камеру" id="switchCameraBtn">🔄</button>
            <button class="call-control-btn call-end" onclick="endCall()" aria-label="Завершить звонок">📞</button>
        </div>
    </div>

    <!-- Уведомления -->
    <div id="notification" class="notification hidden"></div>

    <!-- ARIA Live Regions для accessibility -->
    <div id="ariaLive" aria-live="polite" aria-atomic="true" class="visually-hidden"></div>
    <div id="ariaAlert" aria-live="assertive" aria-atomic="true" class="visually-hidden"></div>
</body>
<script src="/static/js/app.js"></script>
</html>
'''

@app.route('/')
def index():
    initialize_sample_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Остальные API endpoints остаются аналогичными, но с улучшенной валидацией
@app.route('/api/register_user', methods=['POST'])
def api_register_user():
    try:
        data = request.json
        user_id = data.get('id')
        
        if not user_id or not validate_username(data.get('name', '')):
            return jsonify({'success': False, 'error': 'Invalid user data'}), 400
        
        if user_id in user_profiles.keys():
            return jsonify({'success': False, 'error': 'User already exists'}), 409
        
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
        
        user_sessions.set(user_id, generate_session_token())
        update_user_activity(user_id)
        
        logger.info(f"Зарегистрирован новый пользователь: {user_id}")
        return jsonify({'success': True, 'message': 'User registered successfully'})
        
    except Exception as e:
        logger.error(f"Ошибка регистрации пользователя: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    try:
        data = request.json
        user_id = data.get('user_id')
        target_user_id = data.get('target_user_id')
        message_text = data.get('message')
        session_token = data.get('session_token')
        
        if not all([user_id, target_user_id, message_text, session_token]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        if not verify_session(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
        
        if not check_rate_limit(user_id, 'send_message'):
            return jsonify({'success': False, 'error': 'Rate limit exceeded'}), 429
        
        # Валидация сообщения
        is_valid, error_msg = validate_message(message_text)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Санитизация
        message_text = sanitize_input(message_text)
        
        if not ensure_user_chat(user_id, target_user_id):
            return jsonify({'success': False, 'error': 'Chat not found'}), 404
        
        message = {
            'id': str(uuid.uuid4()),
            'sender': user_id,
            'text': message_text,
            'timestamp': datetime.datetime.now().isoformat(),
            'type': 'text',
            'status': 'delivered'
        }
        
        user_msgs = user_messages.get(user_id, {})
        user_msgs[target_user_id].append(message)
        
        # Ограничение количества сообщений
        if len(user_msgs[target_user_id]) > MAX_MESSAGES_PER_CHAT:
            user_msgs[target_user_id] = user_msgs[target_user_id][-MAX_MESSAGES_PER_CHAT:]
        
        user_messages.set(user_id, user_msgs)
        update_user_activity(user_id)
        
        logger.info(f"Сообщение отправлено от {user_id} к {target_user_id}")
        return jsonify({'success': True, 'message_id': message['id']})
        
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
