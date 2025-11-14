# app.py - ПОЛНОСТЬЮ ПЕРЕРАБОТАННАЯ ВЕРСИЯ
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
from typing import Dict, List, Optional, Set, Tuple
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
CALL_TIMEOUT = 3600

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
    
    def values(self):
        with self._lock:
            return list(self._data.values())
    
    def __contains__(self, key):
        with self._lock:
            return key in self._data
    
    def __len__(self):
        with self._lock:
            return len(self._data)
    
    def clear(self):
        with self._lock:
            self._data.clear()

# Инициализация хранилищ
active_calls = ThreadSafeDict()
user_sessions = ThreadSafeDict()
user_messages = ThreadSafeDict()
all_users = ThreadSafeDict()
friendships = ThreadSafeDict()
friend_requests = ThreadSafeDict()
user_profiles = ThreadSafeDict()
rate_limits = ThreadSafeDict()
user_activity = ThreadSafeDict()
groups = ThreadSafeDict()
donate_packages = ThreadSafeDict()
user_subscriptions = ThreadSafeDict()
stickers = ThreadSafeDict()
themes = ThreadSafeDict()
voice_messages = ThreadSafeDict()

def cleanup_old_data():
    """Очистка старых данных"""
    try:
        current_time = time.time()
        
        for call_id, call_data in list(active_calls.items()):
            if 'created_at' in call_data:
                try:
                    created_time = datetime.datetime.fromisoformat(call_data['created_at']).timestamp()
                    if current_time - created_time > CALL_TIMEOUT:
                        active_calls.delete(call_id)
                except (ValueError, KeyError):
                    active_calls.delete(call_id)
        
        for key in list(rate_limits.keys()):
            record = rate_limits.get(key)
            if record and current_time - record.get('timestamp', 0) > RATE_LIMIT_WINDOW:
                rate_limits.delete(key)
        
        for user_id, last_active in list(user_activity.items()):
            if current_time - last_active > 3600:
                user_activity.delete(user_id)
                user = all_users.get(user_id)
                if user:
                    user['online'] = False
                    user['last_seen'] = 'давно'
                
    except Exception as e:
        logger.error(f"Error in cleanup: {e}")

def schedule_cleanup():
    """Планировщик очистки"""
    while True:
        time.sleep(300)
        cleanup_old_data()

# Запуск фоновой очистки
cleanup_thread = threading.Thread(target=schedule_cleanup, daemon=True)
cleanup_thread.start()

def update_user_activity(user_id: str):
    """Обновление активности пользователя"""
    if user_id:
        user_activity.set(user_id, time.time())
        user = all_users.get(user_id)
        if user:
            user['online'] = True
            user['last_seen'] = 'только что'

def check_rate_limit(user_id: str, action: str) -> bool:
    """Проверка rate limit"""
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
    """Санитизация ввода"""
    if not text:
        return ""
    
    text = html.escape(text)
    text = re.sub(r'&amp;([#a-zA-Z0-9]+);', r'&\1;', text)
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

def validate_message(text: str) -> Tuple[bool, str]:
    """Валидация сообщения"""
    if not text or not text.strip():
        return False, "Сообщение не может быть пустым"
    
    if len(text) > MAX_MESSAGE_LENGTH:
        return False, f"Сообщение слишком длинное (максимум {MAX_MESSAGE_LENGTH} символов)"
    
    if re.match(r'^(.)\1{10,}$', text):
        return False, "Сообщение содержит подозрительный контент"
    
    return True, ""

def generate_username() -> str:
    adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha']
    nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther']
    numbers = random.randint(1000, 9999)
    username = f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"
    return sanitize_input(username)

def generate_user_id() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_friend_code() -> str:
    """Генерация уникального friend code"""
    while True:
        code = f"TRLX-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}"
        if not any(profile.get('friend_code') == code for profile in user_profiles.values()):
            return code

def generate_session_token() -> str:
    return hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

def verify_session(user_id: str, session_token: str) -> bool:
    """Проверка сессии"""
    if not user_id or not session_token:
        return False
    
    if user_id not in all_users:
        return False
    
    stored_token = user_sessions.get(user_id)
    if not stored_token:
        return False
    
    valid = stored_token == session_token
    if valid:
        update_user_activity(user_id)
    return valid

def get_user_by_id(user_id: str) -> Optional[dict]:
    """Найти пользователя по ID"""
    return all_users.get(user_id)

def get_user_by_friend_code(friend_code: str) -> Optional[str]:
    """Найти пользователя по friend code"""
    for user_id, profile in user_profiles.items():
        if profile and profile.get('friend_code') == friend_code:
            return user_id
    return None

def ensure_user_chat(user_id: str, target_user_id: str) -> bool:
    """Создание структуры чата"""
    if not user_id or not target_user_id:
        return False
    
    user_exists = user_id in all_users
    target_exists = target_user_id in all_users
    
    if not user_exists or not target_exists:
        return False
    
    if user_id not in user_messages:
        user_messages.set(user_id, {})
    
    user_msgs = user_messages.get(user_id)
    if user_msgs is None:
        user_messages.set(user_id, {})
        user_msgs = user_messages.get(user_id)
    
    if target_user_id not in user_msgs:
        user_msgs[target_user_id] = []
    
    return True

# Новые функции
def initialize_voice_messages():
    """Инициализация голосовых сообщений"""
    voice_messages.set('default', {
        'max_duration': 300,
        'formats': ['mp3', 'wav', 'ogg'],
        'max_size': 10 * 1024 * 1024  # 10MB
    })

def initialize_advanced_features():
    """Инициализация расширенных функций"""
    # Инициализация AI помощника
    user_subscriptions.set('ai_assistant', {
        'enabled': True,
        'features': ['auto_reply', 'smart_suggestions', 'content_moderation']
    })

def initialize_sample_data():
    """Инициализация тестовых данных"""
    for storage in [all_users, user_profiles, user_sessions, user_messages, 
                   friend_requests, friendships, groups]:
        storage.clear()
    
    sample_users = [
        {'id': 'user1', 'name': 'Alex_Quantum', 'avatar': '👨‍💻', 'online': True, 'last_seen': 'только что', 'status': 'Разрабатываю квантовый мессенджер'},
        {'id': 'user2', 'name': 'Sarah_Cyber', 'avatar': '👩‍🎨', 'online': True, 'last_seen': '2 мин назад', 'status': 'Создаю цифровое искусство'},
        {'id': 'user3', 'name': 'Mike_Neon', 'avatar': '👨‍🚀', 'online': False, 'last_seen': '1 час назад', 'status': 'Исследую космос'},
        {'id': 'user4', 'name': 'Emma_Digital', 'avatar': '👩‍💼', 'online': True, 'last_seen': 'только что', 'status': 'Работаю над AI проектами'},
        {'id': 'user5', 'name': 'Tech_Support', 'avatar': '🤖', 'online': True, 'last_seen': 'только что', 'status': 'Помогаю пользователям'},
    ]
    
    for user in sample_users:
        all_users.set(user['id'], user)
        
        user_profiles.set(user['id'], {
            'friend_code': generate_friend_code(),
            'friends': [],
            'settings': {
                'theme': 'dark',
                'notifications': True,
                'privacy': 'friends_only',
                'language': 'ru'
            },
            'created_at': datetime.datetime.now().isoformat(),
            'premium': random.choice([True, False])
        })
        
        user_sessions.set(user['id'], generate_session_token())
        update_user_activity(user['id'])
        user_messages.set(user['id'], {})
    
    # Создаем связи между пользователями
    for user in sample_users:
        for other_user in sample_users:
            if user['id'] != other_user['id']:
                ensure_user_chat(user['id'], other_user['id'])
                
                user_msgs = user_messages.get(user['id'], {})
                if other_user['id'] in user_msgs and len(user_msgs[other_user['id']]) == 0:
                    welcome_msg = {
                        'id': str(uuid.uuid4()),
                        'sender': other_user['id'],
                        'text': sanitize_input('Привет! 👋 Рад познакомиться!'),
                        'timestamp': datetime.datetime.now().isoformat(),
                        'type': 'text'
                    }
                    user_msgs[other_user['id']].append(welcome_msg)
        
        # Создаем дружеские связи
        if user['id'] == 'user1':
            user_profiles.get('user1')['friends'] = ['user2', 'user3']
            user_profiles.get('user2')['friends'] = ['user1']
            user_profiles.get('user3')['friends'] = ['user1']
    
    # Создаем группы
    groups.set('group1', {
        'id': 'group1',
        'name': 'TrollexDL Community',
        'avatar': '👥',
        'members': ['user1', 'user2', 'user3'],
        'created_by': 'user1',
        'created_at': datetime.datetime.now().isoformat(),
        'messages': []
    })
    
    groups.set('group2', {
        'id': 'group2',
        'name': 'Разработчики',
        'avatar': '⚙️',
        'members': ['user1', 'user4'],
        'created_by': 'user4',
        'created_at': datetime.datetime.now().isoformat(),
        'messages': []
    })
    
    initialize_donate_packages()
    initialize_stickers()
    initialize_themes()
    initialize_voice_messages()
    initialize_advanced_features()
    
    logger.info("Инициализированы тестовые данные")

def initialize_donate_packages():
    """Инициализация донат пакетов"""
    packages = {
        'basic': {
            'id': 'basic',
            'name': 'Basic',
            'price': 149,
            'original_price': 299,
            'period': 'месяц',
            'color': '#00ff88',
            'popular': False,
            'features': [
                '🎨 5 кастомных тем',
                '🔔 Расширенные уведомления',
                '💾 Хранилище 1GB',
                '👥 До 5 участников в группе',
                '📱 10 анимированных стикеров',
                '⚡ Ускоренная отправка',
                '🎯 Приоритет в очереди'
            ]
        },
        'vip': {
            'id': 'vip',
            'name': 'VIP',
            'price': 299,
            'original_price': 599,
            'period': 'месяц',
            'color': '#8b5cf6',
            'popular': True,
            'features': [
                '⭐ Все функции Basic',
                '🎭 15 анимированных аватаров',
                '🔒 Приватные чаты',
                '👥 До 15 участников',
                '🎵 Голосовые сообщения',
                '💾 Хранилище 5GB',
                '🚀 Приоритетная поддержка'
            ]
        },
        'premium': {
            'id': 'premium',
            'name': 'Premium',
            'price': 599,
            'original_price': 1199,
            'period': 'месяц',
            'color': '#ff6b6b',
            'popular': False,
            'features': [
                '⭐ Все функции VIP',
                '🎬 Видео сообщения',
                '👥 До 50 участников',
                '🎮 Игровые приложения',
                '🤖 AI-помощник',
                '💾 Хранилище 20GB',
                '🌐 Собственный домен'
            ]
        }
    }
    
    for package_id, package in packages.items():
        donate_packages.set(package_id, package)

def initialize_stickers():
    """Инициализация стикеров"""
    sticker_packs = {
        'basic': [
            {'id': 's1', 'emoji': '😊', 'text': 'Привет!'},
            {'id': 's2', 'emoji': '👍', 'text': 'OK'},
            {'id': 's3', 'emoji': '❤️', 'text': 'Любовь'},
            {'id': 's4', 'emoji': '🎉', 'text': 'Поздравляю!'},
            {'id': 's5', 'emoji': '😂', 'text': 'Смех'},
            {'id': 's6', 'emoji': '😢', 'text': 'Грусть'},
            {'id': 's7', 'emoji': '🎯', 'text': 'Цель'},
            {'id': 's8', 'emoji': '🚀', 'text': 'Запуск!'}
        ],
        'premium': [
            {'id': 'p1', 'emoji': '⭐', 'text': 'Звезда'},
            {'id': 'p2', 'emoji': '🎨', 'text': 'Креатив'},
            {'id': 'p3', 'emoji': '⚡', 'text': 'Энергия'},
            {'id': 'p4', 'emoji': '🔮', 'text': 'Магия'},
            {'id': 'p5', 'emoji': '🌙', 'text': 'Луна'},
            {'id': 'p6', 'emoji': '🔥', 'text': 'Огонь'}
        ]
    }
    stickers.set('default', sticker_packs)

def initialize_themes():
    """Инициализация тем"""
    theme_packs = {
        'dark': {'primary': '#0a0a2a', 'accent': '#6c2bd9', 'text': '#ffffff'},
        'light': {'primary': '#ffffff', 'accent': '#007acc', 'text': '#333333'},
        'cyber': {'primary': '#001122', 'accent': '#00ff88', 'text': '#00ffff'},
        'neon': {'primary': '#1a0033', 'accent': '#ff00ff', 'text': '#ffff00'},
        'ocean': {'primary': '#002233', 'accent': '#00aaff', 'text': '#88ddff'},
        'sunset': {'primary': '#1a0b2c', 'accent': '#ff6b6b', 'text': '#ffd93d'}
    }
    themes.set('default', theme_packs)

# Создаем статические директории
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/images', exist_ok=True)

# CSS с улучшенным дизайном и мобильной оптимизацией
CSS_CONTENT = '''
/* static/css/style.css - УЛУЧШЕННЫЙ ДИЗАЙН */
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
    --gradient: linear-gradient(135deg, var(--accent), var(--accent-glow));
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

/* Улучшенные анимации */
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

@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px currentColor; }
    50% { box-shadow: 0 0 20px currentColor; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes bounce {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes ripple {
    0% { transform: scale(0); opacity: 1; }
    100% { transform: scale(4); opacity: 0; }
}

/* Базовые стили */
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

/* Улучшенная космическая карточка */
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
    position: relative;
    overflow: hidden;
}

.cosmic-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shimmer 2s infinite;
}

.logo {
    font-size: 2.75rem;
    font-weight: 900;
    margin-bottom: 24px;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 40px rgba(107, 43, 217, 0.6);
}

/* Улучшенные кнопки */
.btn {
    width: 100%;
    padding: 16px 24px;
    border: none;
    border-radius: 16px;
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

.btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn:active::before {
    width: 300px;
    height: 300px;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
}

.btn-primary {
    background: var(--gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(107, 43, 217, 0.4);
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(107, 43, 217, 0.6);
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

/* Улучшенная карточка пользователя */
.user-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 24px;
    border-radius: 20px;
    margin: 20px 0;
    border: 1px solid var(--accent);
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease-out;
    position: relative;
}

.user-avatar {
    width: 80px;
    height: 80px;
    border-radius: 20px;
    background: var(--gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin: 0 auto 16px;
    box-shadow: 0 8px 25px rgba(107, 43, 217, 0.4);
    transition: all 0.3s ease;
    position: relative;
}

.user-avatar.premium::after {
    content: '⭐';
    position: absolute;
    top: -5px;
    right: -5px;
    background: gold;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.user-avatar:hover {
    transform: scale(1.05) rotate(5deg);
}

/* Friend Code с анимацией */
.friend-code-display {
    background: rgba(255,255,255,0.1);
    padding: 16px;
    border-radius: 16px;
    margin: 16px 0;
    text-align: center;
    border: 1px solid var(--accent);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.friend-code {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 1.2rem;
    color: var(--neon);
    margin: 8px 0;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    animation: glow 2s infinite;
}

/* Основное приложение */
.app {
    width: 100%;
    height: 100vh;
    display: flex;
    position: relative;
    background: var(--primary);
}

/* Улучшенный Sidebar */
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
    background: var(--gradient);
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

/* Улучшенные навигационные табы */
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
    position: relative;
}

.nav-tab::after {
    content: '';
    position: absolute;
    bottom: 2px;
    left: 50%;
    width: 0;
    height: 2px;
    background: var(--neon);
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

.nav-tab:hover:not(.active) {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--accent);
}

.nav-tab:hover::after {
    width: 20px;
}

.nav-tab.active {
    background: var(--accent);
    box-shadow: 0 4px 12px rgba(107, 43, 217, 0.4);
    transform: translateY(-1px);
}

.nav-tab.active::after {
    width: 30px;
}

/* Улучшенный поиск */
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

/* Улучшенные сообщения */
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
    max-width: 85%;
    padding: 14px 18px;
    border-radius: 20px;
    position: relative;
    word-wrap: break-word;
    animation: fadeIn 0.4s ease-out;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.message:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.message.received {
    background: rgba(107, 43, 217, 0.25);
    align-self: flex-start;
    border-bottom-left-radius: 6px;
    backdrop-filter: blur(10px);
}

.message.sent {
    background: var(--gradient);
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

/* Улучшенный ввод сообщения */
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

.send-btn {
    padding: 16px 20px;
    background: var(--gradient);
    color: white;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    font-size: 1.1rem;
    min-height: 56px;
    min-width: 64px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(107, 43, 217, 0.4);
    position: relative;
    overflow: hidden;
}

.send-btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    transform: translate(-50%, -50%);
    transition: width 0.3s, height 0.3s;
}

.send-btn:active::before {
    width: 100px;
    height: 100px;
}

.send-btn:hover:not(:disabled) {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 6px 20px rgba(107, 43, 217, 0.6);
}

.send-btn:disabled {
    opacity: 0.6;
    transform: none;
    box-shadow: none;
}

/* Новые компоненты для улучшенного UX */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--neon);
    animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}

.voice-message {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
    border: 1px solid var(--accent);
}

.voice-waveform {
    display: flex;
    align-items: center;
    gap: 2px;
    height: 20px;
}

.voice-bar {
    width: 3px;
    height: 100%;
    background: var(--neon);
    border-radius: 2px;
    animation: voiceWave 1s infinite;
}

@keyframes voiceWave {
    0%, 100% { height: 20%; }
    50% { height: 100%; }
}

/* Улучшенные уведомления */
.notification {
    position: fixed;
    top: 24px;
    right: 24px;
    background: var(--gradient);
    color: white;
    padding: 16px 24px;
    border-radius: 16px;
    z-index: 4000;
    animation: slideIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    max-width: 380px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    gap: 12px;
}

.notification::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
    animation: bounce 1s infinite;
}

.notification.success {
    background: linear-gradient(135deg, var(--success), #6bff8f);
}

.notification.error {
    background: linear-gradient(135deg, var(--danger), #ff6b6b);
}

.notification.warning {
    background: linear-gradient(135deg, var(--warning), #ffd93d);
}

/* Улучшенные донат пакеты */
.donate-package {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid;
    border-radius: 20px;
    padding: 24px;
    margin: 16px 0;
    position: relative;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    overflow: hidden;
}

.donate-package::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient);
}

.donate-package:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

.donate-package.popular {
    border-width: 3px;
    animation: glow 2s infinite;
    transform: scale(1.05);
}

.donate-package.popular::before {
    height: 6px;
    background: linear-gradient(90deg, #ff6b6b, #ffd93d, #00ff88);
}

.donate-package.popular::after {
    content: '🔥 ПОПУЛЯРНЫЙ';
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #ff6b6b, #ffd93d);
    color: var(--primary);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
    z-index: 1;
    box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
}

/* Анимации */
.floating-element {
    animation: float 3s ease-in-out infinite;
}

.bounce-animation {
    animation: bounce 0.5s ease infinite;
}

.spin-animation {
    animation: spin 2s linear infinite;
}

.loading-spinner {
    width: 24px;
    height: 24px;
    border: 3px solid rgba(255,255,255,0.3);
    border-top: 3px solid var(--neon);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Статусы */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: bold;
    margin-left: 8px;
}

.status-online {
    background: var(--success);
    color: var(--primary);
}

.status-offline {
    background: var(--text-secondary);
    color: var(--primary);
}

.status-busy {
    background: var(--warning);
    color: var(--primary);
}

.status-away {
    background: var(--cyber);
    color: var(--primary);
}

.online-dot {
    width: 8px;
    height: 8px;
    background: var(--neon);
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

.offline-dot {
    width: 8px;
    height: 8px;
    background: var(--text-secondary);
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}

/* Улучшенная мобильная оптимизация */
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

    .message {
        max-width: 90%;
        padding: 12px 16px;
    }

    .message-input-container {
        padding: 16px;
        gap: 10px;
    }

    .send-btn {
        min-height: 52px;
        min-width: 60px;
        padding: 14px 18px;
    }

    .cosmic-card {
        margin: 10px;
        padding: 24px;
        border-radius: 20px;
    }

    .notification {
        right: 16px;
        left: 16px;
        max-width: none;
        top: 16px;
    }

    .user-header {
        padding: 20px;
    }

    .chat-header {
        padding: 16px;
        min-height: 72px;
    }

    /* Улучшения для touch devices */
    .btn, .control-btn, .nav-tab {
        min-height: 44px;
    }

    .message-input {
        min-height: 52px;
        font-size: 16px; /* Предотвращает zoom на iOS */
    }
}

@media (max-width: 480px) {
    .cosmic-card {
        padding: 20px;
        margin: 8px;
        border-radius: 18px;
    }
    
    .nav-tabs {
        flex-direction: column;
        gap: 4px;
    }
    
    .nav-tab {
        margin: 2px 0;
        min-height: 52px;
        font-size: 0.8rem;
    }
    
    .donate-package {
        padding: 16px;
        margin: 10px 0;
    }

    .package-name {
        font-size: 1.2rem;
    }

    .package-price {
        font-size: 1.5rem;
    }

    .message {
        max-width: 95%;
        padding: 10px 14px;
    }

    .empty-state {
        padding: 40px 16px;
    }

    .empty-state-icon {
        font-size: 3rem;
    }

    .user-avatar {
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
    }

    /* Улучшения для очень маленьких экранов */
    .chat-item {
        padding: 12px;
        min-height: 64px;
    }

    .item-avatar {
        width: 44px;
        height: 44px;
        font-size: 1.1rem;
        margin-right: 12px;
    }
}

/* Поддержка landscape режима */
@media (max-height: 500px) and (orientation: landscape) {
    .screen {
        padding: 10px;
        align-items: flex-start;
        overflow-y: auto;
    }
    
    .cosmic-card {
        margin: 20px auto;
        max-height: 90vh;
        overflow-y: auto;
    }
}

/* Улучшения для темной темы */
@media (prefers-color-scheme: dark) {
    :root {
        --primary: #0a0a2a;
        --secondary: #1a1a4a;
    }
}

/* Улучшения для высокой контрастности */
@media (prefers-contrast: high) {
    :root {
        --accent: #8b5cf6;
        --neon: #00ff88;
        --text: #ffffff;
    }
    
    .btn, .control-btn, .nav-tab {
        border-width: 2px;
    }
}

/* Улучшения для reduced motion */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Улучшенная доступность */
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

/* Фокус для клавиатурной навигации */
.btn:focus-visible,
.control-btn:focus-visible,
.nav-tab:focus-visible,
.search-input:focus-visible,
.message-input:focus-visible {
    outline: 3px solid var(--neon);
    outline-offset: 2px;
}

/* Улучшенный скроллбар */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-glow);
}
'''

# JavaScript с полной оптимизацией и новыми функциями
JS_CONTENT = '''
// static/js/app.js - ПОЛНОСТЬЮ ОПТИМИЗИРОВАННАЯ ВЕРСИЯ
"use strict";

class TrollexApp {
    constructor() {
        this.currentUser = null;
        this.currentTab = 'chats';
        this.currentChat = null;
        this.sessionToken = null;
        this.allUsers = [];
        this.friends = [];
        this.friendRequests = [];
        this.groups = [];
        this.donatePackages = [];
        this.stickers = [];
        this.themes = [];
        this.isLoading = false;
        this.typingUsers = new Map();
        this.connectionStatus = 'online';
        this.audioContext = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupServiceWorker();
        this.checkAutoLogin();
        this.startConnectionMonitor();
    }

    setupEventListeners() {
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        window.addEventListener('resize', () => this.handleResize());
        window.addEventListener('beforeunload', () => this.handleBeforeUnload());
        document.addEventListener('visibilitychange', () => this.handleVisibilityChange());
        
        // Touch events для мобильных устройств
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });
    }

    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('ServiceWorker registered');
                })
                .catch(error => {
                    console.log('ServiceWorker registration failed:', error);
                });
        }
    }

    startConnectionMonitor() {
        setInterval(() => {
            this.checkConnectionQuality();
        }, 30000);
    }

    async checkConnectionQuality() {
        try {
            const startTime = performance.now();
            await fetch('/api/ping', { method: 'HEAD' });
            const latency = performance.now() - startTime;
            
            if (latency > 1000) {
                this.connectionStatus = 'slow';
                this.showNotification('Медленное соединение', 'warning');
            } else {
                this.connectionStatus = 'online';
            }
        } catch (error) {
            this.connectionStatus = 'offline';
        }
    }

    async checkAutoLogin() {
        try {
            const savedUser = localStorage.getItem('trollexUser');
            const savedToken = localStorage.getItem('sessionToken');
            
            if (savedUser && savedToken) {
                this.currentUser = JSON.parse(savedUser);
                this.sessionToken = savedToken;
                await this.loadInitialData();
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

    async loadInitialData() {
        try {
            await Promise.allSettled([
                this.loadUsers(),
                this.loadFriends(),
                this.loadFriendRequests(),
                this.loadGroups(),
                this.loadDonatePackages(),
                this.loadStickers(),
                this.loadThemes()
            ]);
        } catch (error) {
            console.error('Failed to load initial data:', error);
            this.showNotification('Ошибка загрузки данных', 'error');
        }
    }

    async loadUsers() {
        try {
            const response = await this.fetchWithTimeout('/api/get_users', {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.allUsers = data.users;
            } else {
                throw new Error(data.error || 'Failed to load users');
            }
        } catch (error) {
            console.error('Failed to load users:', error);
            throw error;
        }
    }

    async loadFriends() {
        try {
            if (!this.currentUser) return;
            
            const response = await this.fetchWithTimeout(`/api/get_friends?user_id=${this.currentUser.id}`, {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.friends = data.friends || [];
            }
        } catch (error) {
            console.error('Failed to load friends:', error);
            this.friends = [];
        }
    }

    async loadFriendRequests() {
        try {
            if (!this.currentUser) return;
            
            const response = await this.fetchWithTimeout(`/api/get_friend_requests?user_id=${this.currentUser.id}`, {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.friendRequests = data.requests || [];
            }
        } catch (error) {
            console.error('Failed to load friend requests:', error);
            this.friendRequests = [];
        }
    }

    async loadGroups() {
        try {
            if (!this.currentUser) return;
            
            const response = await this.fetchWithTimeout(`/api/get_groups?user_id=${this.currentUser.id}`, {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.groups = data.groups || [];
            }
        } catch (error) {
            console.error('Failed to load groups:', error);
            this.groups = [];
        }
    }

    async loadDonatePackages() {
        try {
            const response = await this.fetchWithTimeout('/api/get_donate_packages', {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.donatePackages = data.packages || [];
            }
        } catch (error) {
            console.error('Failed to load donate packages:', error);
            this.donatePackages = [];
        }
    }

    async loadStickers() {
        try {
            const response = await this.fetchWithTimeout('/api/get_stickers', {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.stickers = data.stickers || [];
            }
        } catch (error) {
            console.error('Failed to load stickers:', error);
            this.stickers = [];
        }
    }

    async loadThemes() {
        try {
            const response = await this.fetchWithTimeout('/api/get_themes', {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.themes = data.themes || [];
            }
        } catch (error) {
            console.error('Failed to load themes:', error);
            this.themes = [];
        }
    }

    async fetchWithTimeout(url, options = {}, timeout = 5000) {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);
        
        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(id);
            return response;
        } catch (error) {
            clearTimeout(id);
            throw error;
        }
    }

    showWelcomeScreen() {
        this.hideAllScreens();
        document.getElementById('welcomeScreen').classList.remove('hidden');
        this.animateWelcomeScreen();
    }

    animateWelcomeScreen() {
        const logo = document.querySelector('.logo');
        if (logo) {
            logo.classList.add('floating-element');
        }
    }

    showRegisterScreen() {
        this.hideAllScreens();
        document.getElementById('registerScreen').classList.remove('hidden');
        this.generateNewUser();
    }

    showMainApp() {
        this.hideAllScreens();
        document.getElementById('mainApp').classList.remove('hidden');
        this.updateUserInfo();
        this.renderCurrentTab();
        this.startRealTimeUpdates();
    }

    startRealTimeUpdates() {
        // Симуляция реальных обновлений
        setInterval(() => {
            this.updateOnlineStatus();
        }, 30000);
        
        // Периодическая синхронизация данных
        setInterval(() => {
            this.syncData();
        }, 60000);
    }

    async syncData() {
        if (this.connectionStatus !== 'online') return;
        
        try {
            await Promise.allSettled([
                this.loadUsers(),
                this.loadFriends(),
                this.loadGroups()
            ]);
            this.renderCurrentTab();
        } catch (error) {
            console.error('Sync failed:', error);
        }
    }

    updateOnlineStatus() {
        this.allUsers.forEach(user => {
            if (user.id !== this.currentUser.id) {
                user.online = Math.random() > 0.3;
                if (!user.online) {
                    const times = ['2 мин назад', '5 мин назад', '10 мин назад', '1 час назад'];
                    user.last_seen = times[Math.floor(Math.random() * times.length)];
                }
            }
        });
        this.renderCurrentTab();
    }

    hideAllScreens() {
        const screens = ['welcomeScreen', 'registerScreen', 'mainApp', 'loadingScreen'];
        screens.forEach(screenId => {
            const element = document.getElementById(screenId);
            if (element) element.classList.add('hidden');
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
            registerBtn.innerHTML = '<div class="loading-spinner"></div>';
            registerBtn.disabled = true;

            const userData = {
                id: document.getElementById('registerId').textContent,
                name: document.getElementById('registerName').textContent,
                avatar: document.getElementById('registerAvatar').textContent,
                friend_code: document.getElementById('registerFriendCode').textContent
            };

            const response = await this.fetchWithTimeout('/api/register_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            }, 10000);

            const data = await response.json();

            if (data.success) {
                this.currentUser = userData;
                this.sessionToken = data.session_token;
                
                // Сохраняем в localStorage
                localStorage.setItem('trollexUser', JSON.stringify(userData));
                localStorage.setItem('sessionToken', data.session_token);
                
                await this.loadInitialData();
                this.showMainApp();
                this.showNotification('Профиль создан успешно! 🎉', 'success');
            } else {
                throw new Error(data.error || 'Registration failed');
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
        
        // Добавляем премиум эффекты если есть подписка
        const userAvatar = document.getElementById('userAvatar');
        if (this.hasPremiumSubscription()) {
            userAvatar.classList.add('premium');
        }
    }

    hasPremiumSubscription() {
        const profile = this.currentUser ? user_profiles.get(this.currentUser.id) : null;
        return profile ? profile.get('premium', false) : false;
    }

    switchTab(tabName, event) {
        this.currentTab = tabName;
        
        // Обновляем активные табы
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        if (event && event.currentTarget) {
            event.currentTarget.classList.add('active');
        }
        
        this.renderCurrentTab();
    }

    renderCurrentTab() {
        const contentList = document.getElementById('contentList');
        if (!contentList) return;
        
        switch (this.currentTab) {
            case 'chats':
                this.renderChatsList();
                break;
            case 'friends':
                this.renderFriendsList();
                break;
            case 'discover':
                this.renderDiscoverList();
                break;
            case 'calls':
                this.renderCallsList();
                break;
            case 'stickers':
                this.renderStickersList();
                break;
            default:
                this.renderChatsList();
        }
    }

    renderChatsList() {
        const contentList = document.getElementById('contentList');
        if (!contentList) return;
        
        const chatItems = [];
        
        // Личные чаты
        this.allUsers
            .filter(user => user.id !== this.currentUser.id)
            .forEach(user => {
                const statusClass = user.online ? 'status-online' : 'status-offline';
                const statusText = user.online ? 'В сети' : user.last_seen;
                
                chatItems.push(`
                    <div class="chat-item" onclick="app.selectChat('${user.id}')" 
                         data-user-id="${user.id}" role="button" tabindex="0">
                        <div class="item-avatar ${this.hasPremiumSubscription() ? 'premium' : ''}">${user.avatar}</div>
                        <div style="flex: 1;">
                            <h4>${user.name} 
                                <span class="status-badge ${statusClass}">${statusText}</span>
                            </h4>
                            <p style="color: var(--text-secondary); font-size: 0.9rem;">
                                ${user.status}
                            </p>
                            ${this.typingUsers.has(user.id) ? `
                                <div class="typing-indicator">
                                    <span>печатает</span>
                                    <div class="typing-dots">
                                        <div class="typing-dot"></div>
                                        <div class="typing-dot"></div>
                                        <div class="typing-dot"></div>
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button class="control-btn" onclick="event.stopPropagation(); app.startVideoCall('${user.id}')" 
                                    style="background: var(--success);">📞</button>
                            <button class="control-btn" onclick="event.stopPropagation(); app.showUserProfile('${user.id}')" 
                                    style="background: var(--accent);">👤</button>
                        </div>
                    </div>
                `);
            });
        
        // Групповые чаты
        this.groups.forEach(group => {
            chatItems.push(`
                <div class="chat-item" onclick="app.selectGroup('${group.id}')">
                    <div class="item-avatar">${group.avatar}</div>
                    <div style="flex: 1;">
                        <h4>${group.name}</h4>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            ${group.members ? group.members.length : 0} участников
                        </p>
                    </div>
                </div>
            `);
        });
        
        if (chatItems.length === 0) {
            contentList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon floating-element">💬</div>
                    <h3>Нет чатов</h3>
                    <p>Начните общение с другими пользователями</p>
                    <button class="btn btn-primary" onclick="app.switchTab('discover')" style="margin-top: 20px;">
                        👥 Найти друзей
                    </button>
                </div>
            `;
        } else {
            contentList.innerHTML = chatItems.join('');
        }
    }

    renderFriendsList() {
        const contentList = document.getElementById('contentList');
        if (!contentList) return;
        
        if (this.friends.length === 0) {
            contentList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon bounce-animation">👥</div>
                    <h3>Нет друзей</h3>
                    <p>Добавьте друзей чтобы начать общение</p>
                    <button class="btn btn-primary" onclick="app.switchTab('discover')" style="margin-top: 20px;">
                        🔍 Найти друзей
                    </button>
                </div>
            `;
            return;
        }
        
        const friendsHtml = this.friends.map(friendId => {
            const friend = this.allUsers.find(u => u.id === friendId);
            if (!friend) return '';
            
            const statusClass = friend.online ? 'status-online' : 'status-offline';
            const statusText = friend.online ? 'В сети' : friend.last_seen;
            
            return `
                <div class="chat-item" onclick="app.selectChat('${friend.id}')">
                    <div class="item-avatar ${this.hasPremiumSubscription() ? 'premium' : ''}">${friend.avatar}</div>
                    <div style="flex: 1;">
                        <h4>${friend.name} 
                            <span class="status-badge ${statusClass}">${statusText}</span>
                        </h4>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            ${friend.status}
                        </p>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="control-btn" onclick="event.stopPropagation(); app.startVideoCall('${friend.id}')" 
                                style="background: var(--success);">📞</button>
                        <button class="control-btn" onclick="event.stopPropagation(); app.removeFriend('${friend.id}')" 
                                style="background: var(--danger);">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');
        
        contentList.innerHTML = friendsHtml;
    }

    renderDiscoverList() {
        const contentList = document.getElementById('contentList');
        if (!contentList) return;
        
        const nonFriends = this.allUsers.filter(user => 
            user.id !== this.currentUser.id && 
            !this.friends.includes(user.id)
        );
        
        let discoverHtml = `
            <div style="margin-bottom: 20px;">
                <h4 style="margin-bottom: 16px;">Добавить по Friend Code</h4>
                <div style="display: flex; gap: 8px;">
                    <input type="text" class="search-input" id="friendCodeInput" 
                           placeholder="TRLX-XXXX-XXXX" style="flex: 1;">
                    <button class="btn btn-primary" onclick="app.addFriendByCode()">Добавить</button>
                </div>
            </div>
        `;
        
        if (nonFriends.length === 0) {
            discoverHtml += `
                <div class="empty-state" style="padding: 20px;">
                    <div class="empty-state-icon spin-animation">🌐</div>
                    <h3>Нет пользователей</h3>
                    <p>Все пользователи уже в вашем списке друзей</p>
                </div>
            `;
        } else {
            discoverHtml += `
                <h4 style="margin-bottom: 16px;">Рекомендуемые пользователи</h4>
                ${nonFriends.map(user => {
                    const statusClass = user.online ? 'status-online' : 'status-offline';
                    const statusText = user.online ? 'В сети' : user.last_seen;
                    
                    return `
                    <div class="chat-item">
                        <div class="item-avatar ${this.hasPremiumSubscription() ? 'premium' : ''}">${user.avatar}</div>
                        <div style="flex: 1;">
                            <h4>${user.name} 
                                <span class="status-badge ${statusClass}">${statusText}</span>
                            </h4>
                            <p style="color: var(--text-secondary); font-size: 0.9rem;">
                                ${user.status}
                            </p>
                        </div>
                        <button class="control-btn" onclick="app.sendFriendRequest('${user.id}')" 
                                style="background: var(--success);">➕</button>
                    </div>
                `}).join('')}
            `;
        }
        
        contentList.innerHTML = discoverHtml;
    }

    renderCallsList() {
        const contentList = document.getElementById('contentList');
        if (!contentList) return;
        
        contentList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon floating-element">📞</div>
                <h3>История звонков</h3>
                <p>Здесь будет отображаться история ваших звонков</p>
                <div style="display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap;">
                    <button class="btn btn-primary" onclick="app.startVideoCall()">
                        🎥 Видеозвонок
                    </button>
                    <button class="btn btn-secondary" onclick="app.startVoiceCall()">
                        🔊 Аудиозвонок
                    </button>
                    <button class="btn btn-secondary" onclick="app.startVoiceMessage()">
                        🎤 Голосовое сообщение
                    </button>
                </div>
            </div>
        `;
    }

    renderStickersList() {
        const contentList = document.getElementById('contentList');
        if (!contentList) return;
        
        if (this.stickers.length === 0) {
            contentList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">😊</div>
                    <h3>Стикеры</h3>
                    <p>Здесь будут ваши стикерпаки</p>
                </div>
            `;
            return;
        }
        
        contentList.innerHTML = `
            <div style="padding: 16px;">
                <h4 style="margin-bottom: 16px;">Мои стикеры</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 10px;">
                    ${this.stickers.map(sticker => `
                        <div class="sticker-item" onclick="app.sendSticker('${sticker.id}')" 
                             style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 12px; text-align: center; cursor: pointer; transition: all 0.3s ease; border: 1px solid var(--accent);">
                            <div style="font-size: 2rem;">${sticker.emoji}</div>
                            <div style="font-size: 0.8rem; margin-top: 8px; color: var(--text-secondary);">${sticker.text}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Новые функции
    async startVoiceMessage() {
        if (!this.hasPremiumSubscription()) {
            this.showNotification('Голосовые сообщения доступны в премиум тарифах!', 'warning');
            this.showDonatePanel();
            return;
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.showNotification('🎤 Запись началась...', 'info');
            
            // Здесь будет логика записи голосового сообщения
            setTimeout(() => {
                this.showNotification('Голосовое сообщение записано!', 'success');
            }, 3000);
        } catch (error) {
            this.showNotification('Ошибка доступа к микрофону', 'error');
        }
    }

    simulateTyping(userId) {
        this.typingUsers.set(userId, Date.now());
        this.renderCurrentTab();
        
        setTimeout(() => {
            this.typingUsers.delete(userId);
            this.renderCurrentTab();
        }, 3000);
    }

    // Донат функции
    showDonatePanel() {
        const overlay = document.getElementById('overlay');
        const donatePanel = document.createElement('div');
        
        donatePanel.className = 'panel donate-panel active';
        donatePanel.innerHTML = this.getDonatePanelHTML();
        
        document.body.appendChild(donatePanel);
        overlay.classList.add('active');
        
        overlay.onclick = () => this.hideDonatePanel();
        donatePanel.querySelector('.close-btn').onclick = () => this.hideDonatePanel();
    }

    hideDonatePanel() {
        const donatePanel = document.querySelector('.donate-panel');
        const overlay = document.getElementById('overlay');
        
        if (donatePanel) {
            donatePanel.remove();
        }
        overlay.classList.remove('active');
    }

    getDonatePanelHTML() {
        return `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                <h2 style="margin: 0;">💎 TrollexDL Premium</h2>
                <button class="control-btn close-btn" style="background: var(--danger);">✕</button>
            </div>
            
            <div class="telegram-contact" style="background: var(--gradient); padding: 20px; border-radius: 16px; margin: 20px 0;">
                <h4 style="color: white; margin-bottom: 8px;">🚀 Для покупки подписки</h4>
                <p style="color: white; margin-bottom: 12px;">Обратитесь в наш Telegram канал</p>
                <a href="https://t.me/Trollex_official" target="_blank" class="telegram-link">
                    @Trollex_official
                </a>
            </div>

            <div style="margin: 20px 0;">
                <h4 style="text-align: center; margin-bottom: 16px;">🎯 Выберите тарифный план</h4>
                <div style="max-height: 60vh; overflow-y: auto; padding-right: 8px;">
                    ${this.donatePackages.map(pkg => `
                        <div class="donate-package ${pkg.popular ? 'popular' : ''}" 
                             style="border-color: ${pkg.color}">
                            <div class="package-header">
                                <div class="package-name" style="color: ${pkg.color}">${pkg.name}</div>
                                <div class="package-price" style="color: ${pkg.color}">
                                    ${pkg.price} руб
                                    ${pkg.original_price ? `<span class="package-original-price">${pkg.original_price} руб</span>` : ''}
                                </div>
                                <div class="package-period">за ${pkg.period}</div>
                            </div>
                            <ul class="package-features">
                                ${pkg.features.map(feature => `<li>${feature}</li>`).join('')}
                            </ul>
                            <button class="donate-btn" onclick="app.selectPackage('${pkg.id}')" 
                                    style="background: ${pkg.color}; color: white;">
                                🛒 Выбрать ${pkg.name}
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div style="text-align: center; margin-top: 20px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 16px;">
                <h4>🎁 Что вы получаете?</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 16px;">
                    <div style="text-align: left;">
                        <p style="margin: 8px 0; font-size: 0.9rem;">⭐ Эксклюзивные функции</p>
                        <p style="margin: 8px 0; font-size: 0.9rem;">🚀 Приоритетная поддержка</p>
                        <p style="margin: 8px 0; font-size: 0.9rem;">🔒 Улучшенная безопасность</p>
                    </div>
                    <div style="text-align: left;">
                        <p style="margin: 8px 0; font-size: 0.9rem;">🎨 Расширенные возможности</p>
                        <p style="margin: 8px 0; font-size: 0.9rem;">📱 Эксклюзивный контент</p>
                        <p style="margin: 8px 0; font-size: 0.9rem;">⚡ Максимальная скорость</p>
                    </div>
                </div>
            </div>
        `;
    }

    selectPackage(packageId) {
        const pkg = this.donatePackages.find(p => p.id === packageId);
        if (!pkg) return;

        this.showNotification(`🎉 Выбран тариф ${pkg.name}! Для покупки обратитесь в @Trollex_official`, 'success');
        
        // Анимация выбора
        const selectedPackage = document.querySelector(`.donate-package[style*="${pkg.color}"]`);
        if (selectedPackage) {
            selectedPackage.classList.add('bounce-animation');
            setTimeout(() => {
                selectedPackage.classList.remove('bounce-animation');
            }, 1000);
        }
        
        window.open(`https://t.me/Trollex_official?start=subscribe_${packageId}`, '_blank');
        this.hideDonatePanel();
    }

    showSettings() {
        this.showNotification('⚙️ Панель настроек в разработке', 'info');
    }

    showUserProfile(userId) {
        const user = this.allUsers.find(u => u.id === userId);
        if (user) {
            this.showNotification(`👤 Профиль ${user.name} - ${user.status}`, 'info');
        }
    }

    async selectChat(userId) {
        this.currentChat = userId;
        const user = this.allUsers.find(u => u.id === userId);
        
        if (user) {
            document.getElementById('currentChatName').textContent = user.name;
            document.getElementById('currentChatAvatar').textContent = user.avatar;
            document.getElementById('currentChatStatus').textContent = 
                user.online ? 'В сети' : `Был(а) ${user.last_seen}`;
            
            await this.loadChatMessages(userId);
            
            // Симулируем печатание
            setTimeout(() => {
                this.simulateTyping(userId);
            }, 1000);
            
            if (window.innerWidth <= 768) {
                this.toggleSidebar();
            }
        }
    }

    selectGroup(groupId) {
        const group = this.groups.find(g => g.id === groupId);
        if (group) {
            this.showNotification(`Выбрана группа: ${group.name}`, 'info');
        }
    }

    async loadChatMessages(userId) {
        const messagesContainer = document.getElementById('messagesContainer');
        if (!messagesContainer) return;
        
        try {
            messagesContainer.innerHTML = '<div class="loading-spinner" style="margin: 20px auto;"></div>';
            
            const response = await this.fetchWithTimeout(`/api/get_messages?user_id=${this.currentUser.id}&target_id=${userId}`, {}, 5000);
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
        if (!messagesContainer) return;
        
        if (!messages || messages.length === 0) {
            messagesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon floating-element">💬</div>
                    <h3>Начните общение</h3>
                    <p>Отправьте первое сообщение</p>
                </div>
            `;
            return;
        }

        messagesContainer.innerHTML = messages.map(msg => {
            const isSent = msg.sender === this.currentUser.id;
            const sender = this.allUsers.find(u => u.id === msg.sender);
            const senderName = sender ? sender.name : 'Неизвестный';
            
            return `
                <div class="message ${isSent ? 'sent' : 'received'}">
                    ${!isSent ? `<div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 4px;">${senderName}</div>` : ''}
                    <div class="message-text">${this.escapeHtml(msg.text)}</div>
                    <div class="message-time">
                        ${new Date(msg.timestamp).toLocaleTimeString('ru-RU', {
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                        ${isSent ? '<span class="message-status">✓</span>' : ''}
                    </div>
                </div>
            `;
        }).join('');

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput ? messageInput.value.trim() : '';
        
        if (!message || !this.currentChat) {
            this.showNotification('Введите сообщение', 'warning');
            return;
        }

        const sendBtn = document.getElementById('sendBtn');
        const originalHTML = sendBtn ? sendBtn.innerHTML : '🚀';
        
        if (sendBtn) {
            sendBtn.innerHTML = '<div class="loading-spinner"></div>';
            sendBtn.disabled = true;
        }
        
        try {
            const response = await this.fetchWithTimeout('/api/send_message', {
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
            }, 10000);

            const data = await response.json();

            if (data.success) {
                this.addMessageToChat({
                    id: data.message_id,
                    sender: this.currentUser.id,
                    text: message,
                    timestamp: new Date().toISOString(),
                    type: 'text'
                });
                
                if (messageInput) {
                    messageInput.value = '';
                    this.adjustTextareaHeight(messageInput);
                }
                
                // Анимация успешной отправки
                if (sendBtn) {
                    sendBtn.innerHTML = '✓';
                    setTimeout(() => {
                        sendBtn.innerHTML = originalHTML;
                    }, 1000);
                }
            } else {
                throw new Error(data.error || 'Failed to send message');
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            this.showNotification('Ошибка отправки сообщения: ' + error.message, 'error');
        } finally {
            if (sendBtn) {
                sendBtn.disabled = false;
            }
        }
    }

    sendSticker(stickerId) {
        const sticker = this.stickers.find(s => s.id === stickerId);
        if (sticker && this.currentChat) {
            this.addMessageToChat({
                id: 'sticker_' + Date.now(),
                sender: this.currentUser.id,
                text: sticker.emoji + ' ' + sticker.text,
                timestamp: new Date().toISOString(),
                type: 'sticker'
            });
            
            this.showNotification(`Стикер отправлен: ${sticker.text}`, 'success');
        }
    }

    addMessageToChat(message) {
        const messagesContainer = document.getElementById('messagesContainer');
        if (!messagesContainer) return;
        
        const isEmpty = messagesContainer.querySelector('.empty-state');
        
        if (isEmpty) {
            messagesContainer.innerHTML = '';
        }
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${
            message.sender === this.currentUser.id ? 'sent' : 'received'
        }`;
        messageElement.style.animation = 'fadeIn 0.3s ease-out';
        
        const sender = this.allUsers.find(u => u.id === message.sender);
        const senderName = sender ? sender.name : 'Неизвестный';
        
        messageElement.innerHTML = `
            ${message.sender !== this.currentUser.id ? 
                `<div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 4px;">${senderName}</div>` : ''}
            <div class="message-text">${this.escapeHtml(message.text)}</div>
            <div class="message-time">
                ${new Date(message.timestamp).toLocaleTimeString('ru-RU', {
                    hour: '2-digit',
                    minute: '2-digit'
                })}
                ${message.sender === this.currentUser.id ? '<span class="message-status">✓</span>' : ''}
            </div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Анимация появления сообщения
        setTimeout(() => {
            messageElement.style.transform = 'translateY(0)';
            messageElement.style.opacity = '1';
        }, 10);
    }

    // Функции друзей
    async sendFriendRequest(userId) {
        try {
            const response = await this.fetchWithTimeout('/api/send_friend_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    target_id: userId,
                    session_token: this.sessionToken
                })
            }, 5000);

            const data = await response.json();

            if (data.success) {
                this.showNotification('Запрос в друзья отправлен! 📨', 'success');
                this.renderDiscoverList();
            } else {
                throw new Error(data.error || 'Failed to send friend request');
            }
        } catch (error) {
            console.error('Failed to send friend request:', error);
            this.showNotification('Ошибка отправки запроса: ' + error.message, 'error');
        }
    }

    async addFriendByCode() {
        const friendCodeInput = document.getElementById('friendCodeInput');
        const friendCode = friendCodeInput ? friendCodeInput.value.trim() : '';
        
        if (!friendCode) {
            this.showNotification('Введите Friend Code', 'warning');
            return;
        }

        try {
            const response = await this.fetchWithTimeout('/api/add_friend_by_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    friend_code: friendCode,
                    session_token: this.sessionToken
                })
            }, 5000);

            const data = await response.json();

            if (data.success) {
                this.showNotification('Друг добавлен! 🎉', 'success');
                if (friendCodeInput) friendCodeInput.value = '';
                await this.loadFriends();
                this.renderDiscoverList();
            } else {
                throw new Error(data.error || 'Failed to add friend');
            }
        } catch (error) {
            console.error('Failed to add friend by code:', error);
            this.showNotification('Ошибка добавления друга: ' + error.message, 'error');
        }
    }

    async removeFriend(friendId) {
        if (!confirm('Удалить пользователя из друзей?')) return;

        try {
            const response = await this.fetchWithTimeout('/api/remove_friend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    friend_id: friendId,
                    session_token: this.sessionToken
                })
            }, 5000);

            const data = await response.json();

            if (data.success) {
                this.showNotification('Друг удален', 'info');
                await this.loadFriends();
                this.renderFriendsList();
            } else {
                throw new Error(data.error || 'Failed to remove friend');
            }
        } catch (error) {
            console.error('Failed to remove friend:', error);
            this.showNotification('Ошибка удаления друга: ' + error.message, 'error');
        }
    }

    // Звонки
    startVideoCall(userId = null) {
        if (this.hasPremiumSubscription()) {
            this.showNotification('🎥 Запуск видеозвонка...', 'success');
        } else {
            this.showNotification('🎥 Видеозвонки доступны в премиум тарифах!', 'warning');
            this.showDonatePanel();
        }
    }

    startVoiceCall() {
        if (this.hasPremiumSubscription()) {
            this.showNotification('🔊 Запуск аудиозвонка...', 'success');
        } else {
            this.showNotification('🔊 Аудиозвонки доступны в премиум тарифах!', 'warning');
            this.showDonatePanel();
        }
    }

    // Touch events
    handleTouchStart(event) {
        // Добавляем визуальную обратную связь для touch
        if (event.target.classList.contains('btn') || 
            event.target.classList.contains('control-btn') ||
            event.target.classList.contains('nav-tab')) {
            event.target.style.transform = 'scale(0.95)';
        }
    }

    handleTouchEnd(event) {
        // Восстанавливаем размер после touch
        if (event.target.classList.contains('btn') || 
            event.target.classList.contains('control-btn') ||
            event.target.classList.contains('nav-tab')) {
            event.target.style.transform = '';
        }
    }

    // Утилиты
    toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        
        if (sidebar) sidebar.classList.toggle('active');
        if (overlay) overlay.classList.toggle('active');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        if (!notification) return;
        
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.remove('hidden');
        
        // Анимация появления
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 4000);
    }

    handleOnline() {
        this.connectionStatus = 'online';
        this.showNotification('Соединение восстановлено ✅', 'success');
        this.syncData();
    }

    handleOffline() {
        this.connectionStatus = 'offline';
        this.showNotification('Отсутствует интернет-соединение 📶', 'warning');
    }

    handleResize() {
        if (window.innerWidth > 768) {
            const sidebar = document.getElementById('sidebar');
            if (sidebar) sidebar.classList.remove('active');
        }
    }

    handleBeforeUnload() {
        // Сохраняем состояние при закрытии
        if (this.currentUser) {
            localStorage.setItem('trollexUser', JSON.stringify(this.currentUser));
            localStorage.setItem('sessionToken', this.sessionToken);
        }
    }

    handleVisibilityChange() {
        if (!document.hidden) {
            this.updateOnlineStatus();
        }
    }

    adjustTextareaHeight(textarea) {
        if (!textarea) return;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    debouncedSearch = this.debounce(() => {
        this.renderCurrentTab();
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
        if (window.app) {
            window.app.sendMessage();
        }
    }
}

function handleTyping() {
    const textarea = document.getElementById('messageInput');
    if (window.app && textarea) {
        window.app.adjustTextareaHeight(textarea);
    }
}

function toggleSidebar() {
    if (window.app) {
        window.app.toggleSidebar();
    }
}

function switchTab(tabName, event) {
    if (window.app) {
        window.app.switchTab(tabName, event);
    }
}

function showRegisterScreen() {
    if (window.app) {
        window.app.showRegisterScreen();
    }
}

function quickStart() {
    if (window.app) {
        window.app.quickStart();
    }
}

function generateNewUser() {
    if (window.app) {
        window.app.generateNewUser();
    }
}

function registerUser() {
    if (window.app) {
        window.app.registerUser();
    }
}

function hideAllPanels() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const donatePanel = document.querySelector('.donate-panel');
    
    if (sidebar) sidebar.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    if (donatePanel) {
        donatePanel.remove();
    }
}

// Инициализация приложения
let app;

document.addEventListener('DOMContentLoaded', function() {
    app = new TrollexApp();
    window.app = app;
    
    // Скрываем экран загрузки
    setTimeout(() => {
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
            }, 500);
        }
    }, 1500);
});

// PWA функциональность
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed: ', error);
            });
    });
}
'''

# Сохраняем файлы
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(CSS_CONTENT)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(JS_CONTENT)

# Service Worker для PWA
SW_CONTENT = '''
// static/sw.js - Service Worker для оффлайн работы
const CACHE_NAME = 'trollexdl-v1.2.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/images/icon-192.png',
    '/static/images/icon-512.png'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});
'''

with open('static/sw.js', 'w', encoding='utf-8') as f:
    f.write(SW_CONTENT)

# HTML с улучшенной разметкой для PWA
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
    <link rel="manifest" href="/static/manifest.json">
    <link rel="icon" type="image/png" href="/static/images/icon-192.png">
</head>
<body>
    <div class="overlay" id="overlay" onclick="hideAllPanels()"></div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="margin: 20px 0; font-size: 1.2rem; min-height: 60px; display: flex; align-items: center; justify-content: center;">
                <div class="loading-spinner"></div>
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
            <div class="logo floating-element">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary);">
                Премиум мессенджер с квантовым шифрованием
            </div>
            
            <div style="display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: rgba(0,255,136,0.1); border: 1px solid var(--neon); border-radius: 12px; margin: 16px 0;">
                <div class="bounce-animation" style="width: 10px; height: 10px; border-radius: 50%; background: var(--neon);"></div>
                <span>Защищённое соединение установлено</span>
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 НАЧАТЬ
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ БЫСТРЫЙ СТАРТ
            </button>
            
            <div style="margin-top: 20px; padding: 16px; background: rgba(255,255,255,0.05); border-radius: 12px;">
                <h4>🎯 Новые возможности</h4>
                <p style="font-size: 0.9rem; margin: 8px 0;">• Голосовые сообщения</p>
                <p style="font-size: 0.9rem; margin: 8px 0;">• Улучшенные стикеры</p>
                <p style="font-size: 0.9rem; margin: 8px 0;">• Оптимизация для телефонов</p>
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
                <div class="nav-tab active" onclick="switchTab('chats', event)" role="button" tabindex="0" aria-label="Чаты">
                    <span>💬</span>
                    <span>Чаты</span>
                </div>
                <div class="nav-tab" onclick="switchTab('friends', event)" role="button" tabindex="0" aria-label="Друзья">
                    <span>👥</span>
                    <span>Друзья</span>
                </div>
                <div class="nav-tab" onclick="switchTab('discover', event)" role="button" tabindex="0" aria-label="Найти друзей">
                    <span>🌐</span>
                    <span>Найти</span>
                </div>
                <div class="nav-tab" onclick="switchTab('calls', event)" role="button" tabindex="0" aria-label="Звонки">
                    <span>📞</span>
                    <span>Звонки</span>
                </div>
                <div class="nav-tab" onclick="switchTab('stickers', event)" role="button" tabindex="0" aria-label="Стикеры">
                    <span>😊</span>
                    <span>Стикеры</span>
                </div>
                <div class="nav-tab" onclick="app.showDonatePanel()" role="button" tabindex="0" aria-label="Премиум функции">
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
                <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="control-btn" onclick="app.startVideoCall(app.currentChat)" style="background: var(--success);" 
                            aria-label="Начать видеозвонок" id="callBtn">📞</button>
                    <button class="control-btn" onclick="app.startVoiceMessage()" style="background: var(--warning);" 
                            aria-label="Голосовое сообщение">🎤</button>
                    <button class="control-btn" onclick="app.showDonatePanel()" style="background: var(--accent);" 
                            aria-label="Премиум функции">💎</button>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon floating-element">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <div style="display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap;">
                        <button class="btn btn-primary" onclick="app.startVideoCall()">
                            🎥 Видеозвонок
                        </button>
                        <button class="btn btn-secondary" onclick="app.showDonatePanel()">
                            💎 Премиум
                        </button>
                    </div>
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

# Manifest для PWA
MANIFEST_CONTENT = {
    "name": "TrollexDL Messenger",
    "short_name": "TrollexDL",
    "description": "Премиум мессенджер с квантовым шифрованием",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a2a",
    "theme_color": "#6c2bd9",
    "orientation": "portrait",
    "icons": [
        {
            "src": "/static/images/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/static/images/icon-512.png", 
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

import json
with open('static/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(MANIFEST_CONTENT, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    initialize_sample_data()
    return render_template_string(HTML_TEMPLATE)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/static/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/static/sw.js')
def serve_sw():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/api/ping')
def api_ping():
    return jsonify({'success': True, 'timestamp': datetime.datetime.now().isoformat()})

# Все остальные API endpoints остаются без изменений...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL ULTIMATE запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"📱 Оптимизировано для мобильных устройств")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
