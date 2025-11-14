# app.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
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
    text = re.sub(r'&amp;([#a-zA-Z0-9]+);', r'&\1;', text)
    
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
    if re.match(r'^(.)\1{10,}$', text):
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
    """Инициализация тестовых данных"""
    global all_users
    
    if all_users:
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
    
    # Инициализация чатов
    for user in sample_users:
        user_messages.set(user['id'], {})
        for other_user in sample_users:
            if user['id'] != other_user['id']:
                user_msgs = user_messages.get(user['id'], {})
                user_msgs[other_user['id']] = [
                    {
                        'id': str(uuid.uuid4()),
                        'sender': other_user['id'],
                        'text': sanitize_input('Привет! 👋 Рад познакомиться!'),
                        'timestamp': datetime.datetime.now().isoformat(),
                        'type': 'text'
                    }
                ]
                user_messages.set(user['id'], user_msgs)

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
        user_messages.set(user_id, user_msgs)
    
    return True

def get_user_by_friend_code(friend_code: str) -> Optional[str]:
    """Найти пользователя по friend code"""
    for user_id in user_profiles.keys():
        profile = user_profiles.get(user_id)
        if profile and profile.get('friend_code') == friend_code:
            return user_id
    return None

def get_user_by_id(user_id: str) -> Optional[dict]:
    """Найти пользователя по ID"""
    for user in all_users:
        if user['id'] == user_id:
            return user
    return None

# Создаем статические директории
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# CSS файл (оставляем оригинальный)
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
'''

# JavaScript с исправлениями
JS_CONTENT = '''
// static/js/app.js - ИСПРАВЛЕННАЯ ВЕРСИЯ
"use strict";

class TrollexApp {
    constructor() {
        this.currentUser = null;
        this.currentTab = 'chats';
        this.currentChat = null;
        this.sessionToken = null;
        this.allUsers = [];
        this.isLoading = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAutoLogin();
    }

    setupEventListeners() {
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
    }

    async checkAutoLogin() {
        try {
            const savedUser = localStorage.getItem('trollexUser');
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                this.currentUser = JSON.parse(savedUser);
                this.sessionToken = savedToken;
                await this.loadUsers();
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

    async loadUsers() {
        try {
            const response = await fetch('/api/get_users');
            const data = await response.json();
            
            if (data.success) {
                this.allUsers = data.users;
                this.renderUserList();
            }
        } catch (error) {
            console.error('Failed to load users:', error);
            // Используем тестовых пользователей если API недоступно
            this.allUsers = [
                {'id': 'user1', 'name': 'Alex_Quantum', 'avatar': '👨‍💻', 'online': true, 'last_seen': 'только что', 'status': 'Разрабатываю квантовый мессенджер'},
                {'id': 'user2', 'name': 'Sarah_Cyber', 'avatar': '👩‍🎨', 'online': true, 'last_seen': '2 мин назад', 'status': 'Создаю цифровое искусство'},
                {'id': 'user3', 'name': 'Mike_Neon', 'avatar': '👨‍🚀', 'online': false, 'last_seen': '1 час назад', 'status': 'Исследую космос'},
                {'id': 'user4', 'name': 'Emma_Digital', 'avatar': '👩‍💼', 'online': true, 'last_seen': 'только что', 'status': 'Работаю над AI проектами'},
            ];
            this.renderUserList();
        }
    }

    showWelcomeScreen() {
        this.hideAllScreens();
        document.getElementById('welcomeScreen').classList.remove('hidden');
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
        if (!contentList) return;

        if (!this.allUsers || this.allUsers.length === 0) {
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
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${user.online ? 'var(--neon)' : 'var(--text-secondary)'}; margin-right: 5px;"></span>
                        ${user.online ? 'В сети' : user.last_seen}
                    </p>
                    <p style="color: var(--text-secondary); font-size: 0.8rem;">
                        ${user.status}
                    </p>
                </div>
                <button class="control-btn" onclick="event.stopPropagation(); app.startVideoCall('${user.id}')" 
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
        
        try {
            const response = await fetch(`/api/get_messages?user_id=${this.currentUser.id}&target_id=${userId}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMessages(data.messages);
            } else {
                this.displayMessages([]);
            }
        } catch (error) {
            console.error('Failed to load messages:', error);
            this.displayMessages([]);
        }
    }

    displayMessages(messages) {
        const messagesContainer = document.getElementById('messagesContainer');
        
        if (!messages || messages.length === 0) {
            messagesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💬</div>
                    <h3>Начните общение</h3>
                    <p>Отправьте первое сообщение</p>
                </div>
            `;
            return;
        }

        messagesContainer.innerHTML = messages.map(msg => `
            <div class="message ${msg.sender === this.currentUser.id ? 'sent' : 'received'}">
                <div class="message-text">${this.escapeHtml(msg.text)}</div>
                <div class="message-time">
                    ${new Date(msg.timestamp).toLocaleTimeString('ru-RU', {
                        hour: '2-digit',
                        minute: '2-digit'
                    })}
                </div>
            </div>
        `).join('');

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || !this.currentChat) {
            this.showNotification('Введите сообщение', 'warning');
            return;
        }

        const sendBtn = document.getElementById('sendBtn');
        sendBtn.disabled = true;
        
        try {
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    target_user_id: this.currentChat,
                    message: message,
                    session_token: this.sessionToken
                })
            });

            const data = await response.json();

            if (data.success) {
                // Добавляем сообщение в чат
                this.addMessageToChat({
                    id: data.message_id,
                    sender: this.currentUser.id,
                    text: message,
                    timestamp: new Date().toISOString(),
                    type: 'text'
                });
                
                messageInput.value = '';
                this.adjustTextareaHeight(messageInput);
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            this.showNotification('Ошибка отправки сообщения: ' + error.message, 'error');
        } finally {
            sendBtn.disabled = false;
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
        
        event.currentTarget.classList.add('active');
        
        this.renderUserList();
    }

    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    }

    startVideoCall(userId) {
        this.showNotification('Функция видеозвонков в разработке 🚧', 'info');
    }

    showCallPanel() {
        this.showNotification('Создание видеозвонка...', 'info');
    }

    showSettings() {
        this.showNotification('Настройки в разработке 🚧', 'info');
    }

    showDonatePanel() {
        this.showNotification('Премиум функции в разработке 🚧', 'info');
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

    handleOnline() {
        this.showNotification('Соединение восстановлено ✅', 'success');
    }

    handleOffline() {
        this.showNotification('Отсутствует интернет-соединение 📶', 'warning');
    }

    adjustTextareaHeight(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
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
}

// Глобальные функции
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
    document.getElementById('sidebar').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
}

// Инициализация приложения
let app;

document.addEventListener('DOMContentLoaded', function() {
    app = new TrollexApp();
});
'''

# Сохраняем файлы
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(CSS_CONTENT)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(JS_CONTENT)

# HTML шаблон (оставляем оригинальный)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0a0a2a">
    <meta name="description" content="TrollexDL - защищенный мессенджер с квантовым шифрованием">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <link rel="stylesheet" href="/static/css/style.css">
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
            <div style="color: var(--neon); margin: 10px 0; display: flex; align-items: center; justify-content: center; gap: 8px;">
                <span>🔒</span>
                <span>Квантовое шифрование активировано</span>
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
                <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                </div>
                <button class="control-btn" onclick="app.startVideoCall(app.currentChat)" style="background: var(--success);" 
                        aria-label="Начать видеозвонок" id="callBtn">📞</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <button class="btn btn-primary" onclick="app.showCallPanel()" style="margin-top: 20px;">
                        🎥 Создать видеозвонок
                    </button>
                </div>
            </div>

            <div class="message-input-container">
                <textarea class="message-input" placeholder="Введите сообщение..." id="messageInput" 
                       onkeydown="handleKeyPress(event)" oninput="handleTyping()" 
                       aria-label="Введите сообщение" maxlength="2000" rows="1"></textarea>
                <button class="send-btn" onclick="app.sendMessage()" aria-label="Отправить сообщение" id="sendBtn">🚀</button>
            </div>
        </div>
    </div>

    <!-- Уведомления -->
    <div id="notification" class="notification hidden"></div>
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

# API endpoints
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
        
        # Проверяем существование пользователя
        if any(user['id'] == user_id for user in all_users):
            return jsonify({'success': False, 'error': 'User already exists'}), 409
        
        # Создаем нового пользователя
        new_user = {
            'id': user_id,
            'name': data.get('name'),
            'avatar': data.get('avatar', '👤'),
            'online': True,
            'last_seen': 'только что',
            'status': 'Новый пользователь TrollexDL'
        }
        all_users.append(new_user)
        
        # Создаем профиль
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
        
        # Создаем сессию
        session_token = generate_session_token()
        user_sessions.set(user_id, session_token)
        update_user_activity(user_id)
        
        # Инициализируем чаты для нового пользователя
        user_messages.set(user_id, {})
        for other_user in all_users:
            if other_user['id'] != user_id:
                user_msgs = user_messages.get(user_id, {})
                user_msgs[other_user['id']] = [
                    {
                        'id': str(uuid.uuid4()),
                        'sender': other_user['id'],
                        'text': sanitize_input('Привет! 👋 Рад познакомиться!'),
                        'timestamp': datetime.datetime.now().isoformat(),
                        'type': 'text'
                    }
                ]
                user_messages.set(user_id, user_msgs)
        
        logger.info(f"Зарегистрирован новый пользователь: {user_id}")
        return jsonify({
            'success': True, 
            'message': 'User registered successfully',
            'session_token': session_token
        })
        
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
        
        # Сохраняем сообщение для отправителя
        user_msgs = user_messages.get(user_id, {})
        if target_user_id not in user_msgs:
            user_msgs[target_user_id] = []
        user_msgs[target_user_id].append(message)
        user_messages.set(user_id, user_msgs)
        
        # Сохраняем сообщение для получателя
        target_msgs = user_messages.get(target_user_id, {})
        if user_id not in target_msgs:
            target_msgs[user_id] = []
        target_msgs[user_id].append(message)
        user_messages.set(target_user_id, target_msgs)
        
        # Ограничение количества сообщений
        if len(user_msgs[target_user_id]) > MAX_MESSAGES_PER_CHAT:
            user_msgs[target_user_id] = user_msgs[target_user_id][-MAX_MESSAGES_PER_CHAT:]
        
        update_user_activity(user_id)
        
        logger.info(f"Сообщение отправлено от {user_id} к {target_user_id}")
        return jsonify({'success': True, 'message_id': message['id']})
        
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_messages')
def api_get_messages():
    try:
        user_id = request.args.get('user_id')
        target_id = request.args.get('target_id')
        
        if not user_id or not target_id:
            return jsonify({'success': False, 'error': 'Missing user_id or target_id'}), 400
        
        user_msgs = user_messages.get(user_id, {})
        messages = user_msgs.get(target_id, [])
        
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
