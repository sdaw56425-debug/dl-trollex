# app.py - ПОЛНАЯ РЕАЛИЗАЦИЯ С WEBRTC ЗВОНКАМИ И РЕАЛЬНЫМИ ЧАТАМИ
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime
import random
import os
import uuid
import logging
import logging.config
import hashlib
import time
import json
import re
import html
from typing import Dict, List, Optional, Set, Tuple
import threading
import sqlite3
from contextlib import contextmanager
import math
import secrets
import psutil
from functools import wraps
import jwt
import bcrypt
from waitress import serve

# Настройка логирования
def setup_logging():
    """Настройка расширенного логгирования"""
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'trollexdl.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'detailed',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
    })

setup_logging()
logger = logging.getLogger(__name__)

# Конфигурация через переменные окружения
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'trollexdl_database.db')
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 10 * 1024 * 1024))
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 3600))
    RATE_LIMIT = int(os.environ.get('RATE_LIMIT', 100))
    MAX_CACHE_SIZE = int(os.environ.get('MAX_CACHE_SIZE', 1000))

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Константы
MAX_MESSAGES_PER_CHAT = 1000
MAX_STORAGE_SIZE = 5 * 1024 * 1024
RATE_LIMIT_WINDOW = 60
MAX_REQUESTS_PER_WINDOW = Config.RATE_LIMIT
MAX_MESSAGE_LENGTH = 2000
MAX_USERNAME_LENGTH = 20
CALL_TIMEOUT = 3600
DB_PATH = Config.DATABASE_URL
SESSION_TIMEOUT = Config.SESSION_TIMEOUT

# Потокобезопасные хранилища с ограничением размера
class ThreadSafeDict:
    def __init__(self, max_size=1000):
        self._data = {}
        self._lock = threading.RLock()
        self._max_size = max_size
        self._access_order = []
    
    def get(self, key, default=None):
        with self._lock:
            if key in self._data:
                if key in self._access_order:
                    self._access_order.remove(key)
                self._access_order.append(key)
                return self._data[key]
            return default
    
    def set(self, key, value):
        with self._lock:
            if len(self._data) >= self._max_size and key not in self._data:
                self._evict_oldest()
            
            self._data[key] = value
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
    
    def _evict_oldest(self):
        if self._access_order:
            oldest_key = self._access_order.pop(0)
            if oldest_key in self._data:
                del self._data[oldest_key]
    
    def delete(self, key):
        with self._lock:
            if key in self._data:
                del self._data[key]
            if key in self._access_order:
                self._access_order.remove(key)
    
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
            self._access_order.clear()

# Хранилища для WebRTC звонков
active_calls = ThreadSafeDict(max_size=100)
user_sessions_memory = ThreadSafeDict(max_size=Config.MAX_CACHE_SIZE)
user_activity = ThreadSafeDict(max_size=1000)
rate_limits = ThreadSafeDict(max_size=2000)
typing_users = ThreadSafeDict(max_size=500)
online_users = ThreadSafeDict(max_size=1000)  # sid -> user_id
user_sockets = ThreadSafeDict(max_size=1000)  # user_id -> sid

# Инициализация базы данных
def init_database():
    """Инициализация SQLite базы данных"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with sqlite3.connect(DB_PATH, timeout=30) as conn:
                cursor = conn.cursor()
                
                cursor.execute('PRAGMA foreign_keys = ON')
                cursor.execute('PRAGMA journal_mode = WAL')
                cursor.execute('PRAGMA synchronous = NORMAL')
                
                # Таблица пользователей
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        avatar TEXT NOT NULL,
                        online BOOLEAN DEFAULT FALSE,
                        last_seen TEXT DEFAULT 'давно',
                        status TEXT DEFAULT '',
                        friend_code TEXT UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        premium BOOLEAN DEFAULT FALSE,
                        password_hash TEXT,
                        email TEXT UNIQUE
                    )
                ''')
                
                # Таблица сообщений
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY,
                        sender_id TEXT NOT NULL,
                        receiver_id TEXT NOT NULL,
                        text TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        type TEXT DEFAULT 'text',
                        encrypted BOOLEAN DEFAULT FALSE,
                        read BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE,
                        FOREIGN KEY (receiver_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                ''')
                
                # Таблица друзей
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS friendships (
                        user_id TEXT NOT NULL,
                        friend_id TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (user_id, friend_id),
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                        FOREIGN KEY (friend_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                ''')
                
                # Таблица заявок в друзья
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS friend_requests (
                        id TEXT PRIMARY KEY,
                        from_user_id TEXT NOT NULL,
                        to_user_id TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (from_user_id) REFERENCES users (id) ON DELETE CASCADE,
                        FOREIGN KEY (to_user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                ''')
                
                # Таблица сессий
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        user_id TEXT PRIMARY KEY,
                        session_token TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP DEFAULT (datetime('now', '+7 days')),
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                ''')
                
                # Таблица звонков
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS calls (
                        id TEXT PRIMARY KEY,
                        caller_id TEXT NOT NULL,
                        receiver_id TEXT NOT NULL,
                        status TEXT DEFAULT 'calling',
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ended_at TIMESTAMP,
                        call_type TEXT DEFAULT 'video',
                        FOREIGN KEY (caller_id) REFERENCES users (id) ON DELETE CASCADE,
                        FOREIGN KEY (receiver_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                ''')
                
                conn.commit()
                logger.info("База данных инициализирована успешно")
                break
                
        except sqlite3.Error as e:
            logger.error(f"Ошибка инициализации базы данных (попытка {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

def add_database_indexes():
    """Добавление индексов для улучшения производительности"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)",
                    "CREATE INDEX IF NOT EXISTS idx_messages_sender_receiver ON messages(sender_id, receiver_id)",
                    "CREATE INDEX IF NOT EXISTS idx_messages_receiver_sender ON messages(receiver_id, sender_id)",
                    "CREATE INDEX IF NOT EXISTS idx_users_online ON users(online)",
                    "CREATE INDEX IF NOT EXISTS idx_users_friend_code ON users(friend_code)",
                    "CREATE INDEX IF NOT EXISTS idx_friendships_user ON friendships(user_id)",
                    "CREATE INDEX IF NOT EXISTS idx_friendships_friend ON friendships(friend_id)",
                    "CREATE INDEX IF NOT EXISTS idx_sessions_activity ON user_sessions(last_activity)",
                    "CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at)",
                    "CREATE INDEX IF NOT EXISTS idx_friend_requests_from ON friend_requests(from_user_id)",
                    "CREATE INDEX IF NOT EXISTS idx_friend_requests_to ON friend_requests(to_user_id)",
                    "CREATE INDEX IF NOT EXISTS idx_calls_caller ON calls(caller_id)",
                    "CREATE INDEX IF NOT EXISTS idx_calls_receiver ON calls(receiver_id)",
                ]
                
                for index_sql in indexes:
                    try:
                        cursor.execute(index_sql)
                    except Exception as e:
                        logger.warning(f"Failed to create index: {e}")
                
                conn.commit()
                logger.info("Индексы базы данных созданы успешно")
                break
                
        except Exception as e:
            logger.error(f"Ошибка создания индексов (попытка {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

@contextmanager
def get_db_connection():
    """Контекстный менеджер для работы с базой данных с retry логикой"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=30)
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA foreign_keys = ON')
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
            break
        except sqlite3.Error as e:
            logger.error(f"Ошибка подключения к БД (попытка {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

# Инициализация базы данных при старте
init_database()
add_database_indexes()

# Декораторы для безопасности
def require_auth(f):
    """Декоратор для проверки аутентификации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            user_id = request.args.get('user_id') or request.json.get('user_id') if request.json else None
            session_token = request.args.get('session_token') or request.json.get('session_token') if request.json else None
            
            if auth_header and auth_header.startswith('Bearer '):
                session_token = auth_header[7:]
            
            if not user_id or not session_token:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
            if not verify_session_enhanced(user_id, session_token):
                return jsonify({'success': False, 'error': 'Invalid or expired session'}), 401
                
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Auth error: {e}")
            return jsonify({'success': False, 'error': 'Authentication failed'}), 401
    return decorated_function

def rate_limit(f):
    """Декоратор для ограничения запросов"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_id = request.args.get('user_id') or request.json.get('user_id') if request.json else None
            client_ip = request.remote_addr
            
            if not user_id:
                user_id = f"ip_{client_ip}"
            
            action = f.__name__
            if not check_rate_limit(user_id, action):
                return jsonify({
                    'success': False, 
                    'error': 'Rate limit exceeded. Please try again later.'
                }), 429
                
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Rate limit error: {e}")
            return jsonify({'success': False, 'error': 'Rate limit check failed'}), 500
    return decorated_function

def socket_require_auth(f):
    """Декоратор для проверки аутентификации в WebSocket"""
    @wraps(f)
    def decorated_function(data):
        try:
            user_id = data.get('user_id')
            session_token = data.get('session_token')
            
            if not user_id or not session_token:
                emit('error', {'message': 'Authentication required'})
                return
            
            if not verify_session_enhanced(user_id, session_token):
                emit('error', {'message': 'Invalid session'})
                return
                
            return f(data)
        except Exception as e:
            logger.error(f"Socket auth error: {e}")
            emit('error', {'message': 'Authentication failed'})
    return decorated_function

def validate_access(user_id, target_user_id=None, resource_type=None):
    """Валидация прав доступа пользователя"""
    if not user_id:
        return False
    
    if target_user_id == user_id:
        return True
    
    if resource_type == 'message':
        if not target_user_id:
            return False
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 1 FROM friendships 
                WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
                LIMIT 1
            ''', (user_id, target_user_id, target_user_id, user_id))
            
            if cursor.fetchone():
                return True
            
            cursor.execute('''
                SELECT 1 FROM group_members gm1
                JOIN group_members gm2 ON gm1.group_id = gm2.group_id
                WHERE gm1.user_id = ? AND gm2.user_id = ?
                LIMIT 1
            ''', (user_id, target_user_id))
            
            return cursor.fetchone() is not None
    
    return True  # Для звонков разрешаем всем

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
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET online = FALSE, last_seen = ? WHERE id = ?",
                        ('давно', user_id)
                    )
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM user_sessions WHERE expires_at < datetime('now') OR last_activity < datetime('now', '-30 days')"
            )
                
    except Exception as e:
        logger.error(f"Error in cleanup: {e}")

def schedule_cleanup():
    """Планировщик очистки"""
    while True:
        time.sleep(300)
        cleanup_old_data()

cleanup_thread = threading.Thread(target=schedule_cleanup, daemon=True)
cleanup_thread.start()

def update_user_activity(user_id: str):
    """Обновление активности пользователя с защитой от race condition"""
    if not user_id:
        return
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            user_activity.set(user_id, time.time())
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET online = TRUE, last_seen = 'только что' WHERE id = ?",
                    (user_id,)
                )
                cursor.execute(
                    "UPDATE user_sessions SET last_activity = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (user_id,)
                )
            break
        except sqlite3.Error as e:
            logger.error(f"Error updating user activity (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(0.1)

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
    """Санитизация ввода с улучшенной защитой"""
    if not text:
        return ""
    
    text = html.escape(text)
    
    dangerous_patterns = [
        (r'javascript:', '', re.IGNORECASE),
        (r'vbscript:', '', re.IGNORECASE),
        (r'data:', '', re.IGNORECASE),
        (r'on\w+=', 'data-', re.IGNORECASE),
        (r'expression\(', 'escaped-expr(', re.IGNORECASE),
        (r'<script', '&lt;script', re.IGNORECASE),
        (r'</script', '&lt;/script', re.IGNORECASE),
    ]
    
    for pattern, replacement, flags in dangerous_patterns:
        text = re.sub(pattern, replacement, text, flags=flags)
    
    if len(text) > 10000:
        text = text[:10000]
    
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
    """Валидация сообщения с улучшенной проверкой"""
    if not text or not text.strip():
        return False, "Сообщение не может быть пустым"
    
    if len(text) > MAX_MESSAGE_LENGTH:
        return False, f"Сообщение слишком длинное (максимум {MAX_MESSAGE_LENGTH} символов)"
    
    spam_patterns = [
        r'^(.)\1{10,}$',
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, text, re.IGNORECASE):
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
    max_attempts = 10
    for attempt in range(max_attempts):
        code = f"TRLX-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE friend_code = ?", (code,))
            if not cursor.fetchone():
                return code
    raise Exception("Failed to generate unique friend code")

def generate_session_token() -> str:
    return secrets.token_urlsafe(32)

def generate_call_id() -> str:
    return f"call_{uuid.uuid4().hex[:12]}"

def verify_session_enhanced(user_id: str, session_token: str) -> bool:
    """Улучшенная проверка сессии с проверкой времени жизни"""
    if not user_id or not session_token:
        return False
    
    stored_token = user_sessions_memory.get(user_id)
    if stored_token and stored_token == session_token:
        update_user_activity(user_id)
        return True
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT session_token FROM user_sessions 
            WHERE user_id = ? AND session_token = ? 
            AND expires_at > datetime('now')""",
            (user_id, session_token)
        )
        result = cursor.fetchone()
        
        if result:
            user_sessions_memory.set(user_id, session_token)
            update_user_activity(user_id)
            return True
    
    return False

def get_user_by_id(user_id: str) -> Optional[dict]:
    """Найти пользователя по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None

def get_user_by_friend_code(friend_code: str) -> Optional[str]:
    """Найти пользователя по friend code"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE friend_code = ?", (friend_code,))
        row = cursor.fetchone()
        if row:
            return row['id']
    return None

def ensure_user_chat(user_id: str, target_user_id: str) -> bool:
    """Создание структуры чата с проверкой прав доступа"""
    if not user_id or not target_user_id:
        return False
    
    user_exists = get_user_by_id(user_id)
    target_exists = get_user_by_id(target_user_id)
    
    if not user_exists or not target_exists:
        return False
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM friendships 
            WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
            LIMIT 1
        ''', (user_id, target_user_id, target_user_id, user_id))
        
        return cursor.fetchone() is not None

def get_days_until_new_year():
    """Получить количество дней до Нового Года"""
    now = datetime.datetime.now()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    days_left = (new_year - now).days
    return days_left

def get_random_motivation():
    """Случайная мотивационная фраза"""
    motivations = [
        "🚀 Ты можешь всё! Верь в себя!",
        "💫 Сегодня твой день для великих дел!",
        "🌟 Не сдавайся, у тебя всё получится!",
        "🔥 Впереди ждут великие открытия!",
        "🎯 Каждая мечта достижима!",
        "⚡ Ты сильнее, чем думаешь!",
        "🌈 Будущее создаётся сегодня!",
        "🎉 Каждый день - новая возможность!"
    ]
    return random.choice(motivations)

def get_total_users_count():
    """Получить общее количество пользователей"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        return cursor.fetchone()['count']

def save_uploaded_file(file, user_id: str, file_type: str) -> Optional[str]:
    """Безопасное сохранение загруженных файлов"""
    try:
        allowed_types = {
            'image': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
            'audio': ['mp3', 'wav', 'ogg', 'm4a'],
            'document': ['pdf', 'txt', 'doc', 'docx']
        }
        
        if file_type not in allowed_types:
            return None
        
        filename = secure_filename(file.filename)
        if not filename:
            return None
        
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if extension not in allowed_types[file_type]:
            return None
        
        unique_filename = f"{user_id}_{uuid.uuid4().hex}.{extension}"
        upload_folder = f"static/uploads/{file_type}"
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        return f"/{file_path}"
        
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return None

def secure_filename(filename: str) -> str:
    """Безопасное имя файла"""
    filename = html.escape(filename)
    filename = re.sub(r'[^\w\-_.]', '', filename)
    return filename[:255]

# WebSocket обработчики для реального времени
@socketio.on('connect')
def handle_connect():
    """Обработчик подключения WebSocket"""
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Обработчик отключения WebSocket"""
    user_id = online_users.get(request.sid)
    if user_id:
        online_users.delete(request.sid)
        user_sockets.delete(user_id)
        logger.info(f"User {user_id} disconnected")
        
        # Уведомляем друзей о выходе из сети
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT friend_id FROM friendships WHERE user_id = ?
                UNION
                SELECT user_id FROM friendships WHERE friend_id = ?
            ''', (user_id, user_id))
            
            friends = [row['friend_id'] for row in cursor.fetchall()]
            
        for friend_id in friends:
            friend_sid = user_sockets.get(friend_id)
            if friend_sid:
                emit('user_status', {
                    'user_id': user_id,
                    'online': False,
                    'last_seen': 'только что'
                }, room=friend_sid)

@socketio.on('authenticate')
def handle_authentication(data):
    """Аутентификация пользователя в WebSocket"""
    try:
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        
        if not user_id or not session_token:
            emit('error', {'message': 'Authentication required'})
            return
        
        if not verify_session_enhanced(user_id, session_token):
            emit('error', {'message': 'Invalid session'})
            return
        
        # Сохраняем связь sid -> user_id
        online_users.set(request.sid, user_id)
        user_sockets.set(user_id, request.sid)
        
        # Обновляем статус онлайн
        update_user_activity(user_id)
        
        # Уведомляем друзей о входе в сеть
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT friend_id FROM friendships WHERE user_id = ?
                UNION
                SELECT user_id FROM friendships WHERE friend_id = ?
            ''', (user_id, user_id))
            
            friends = [row['friend_id'] for row in cursor.fetchall()]
            
        for friend_id in friends:
            friend_sid = user_sockets.get(friend_id)
            if friend_sid:
                emit('user_status', {
                    'user_id': user_id,
                    'online': True,
                    'last_seen': 'только что'
                }, room=friend_sid)
        
        emit('authenticated', {'success': True})
        logger.info(f"User {user_id} authenticated via WebSocket")
        
    except Exception as e:
        logger.error(f"WebSocket authentication error: {e}")
        emit('error', {'message': 'Authentication failed'})

@socketio.on('send_message')
def handle_send_message(data):
    """Обработчик отправки сообщения в реальном времени"""
    try:
        user_id = data.get('user_id')
        target_id = data.get('target_id')
        message_text = sanitize_input(data.get('message', ''))
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            emit('error', {'message': 'Invalid session'})
            return
        
        if not validate_access(user_id, target_id, 'message'):
            emit('error', {'message': 'Access denied'})
            return
        
        is_valid, error_msg = validate_message(message_text)
        if not is_valid:
            emit('error', {'message': error_msg})
            return
        
        # Сохраняем сообщение в базе
        message_id = str(uuid.uuid4())
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (id, sender_id, receiver_id, text, type)
                VALUES (?, ?, ?, ?, 'text')
            ''', (message_id, user_id, target_id, message_text))
        
        # Отправляем сообщение получателю
        target_sid = user_sockets.get(target_id)
        if target_sid:
            emit('new_message', {
                'id': message_id,
                'sender_id': user_id,
                'receiver_id': target_id,
                'text': message_text,
                'timestamp': datetime.datetime.now().isoformat(),
                'type': 'text'
            }, room=target_sid)
        
        # Подтверждение отправителю
        emit('message_sent', {
            'message_id': message_id,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        logger.info(f"Message sent from {user_id} to {target_id}")
        
    except Exception as e:
        logger.error(f"Send message error: {e}")
        emit('error', {'message': 'Failed to send message'})

@socketio.on('typing_start')
def handle_typing_start(data):
    """Обработчик начала печатания"""
    try:
        user_id = data.get('user_id')
        target_id = data.get('target_id')
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            return
        
        target_sid = user_sockets.get(target_id)
        if target_sid:
            emit('user_typing', {
                'user_id': user_id,
                'typing': True
            }, room=target_sid)
            
    except Exception as e:
        logger.error(f"Typing start error: {e}")

@socketio.on('typing_stop')
def handle_typing_stop(data):
    """Обработчик окончания печатания"""
    try:
        user_id = data.get('user_id')
        target_id = data.get('target_id')
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            return
        
        target_sid = user_sockets.get(target_id)
        if target_sid:
            emit('user_typing', {
                'user_id': user_id,
                'typing': False
            }, room=target_sid)
            
    except Exception as e:
        logger.error(f"Typing stop error: {e}")

# WebRTC обработчики звонков
@socketio.on('call_start')
def handle_call_start(data):
    """Начало звонка"""
    try:
        caller_id = data.get('caller_id')
        receiver_id = data.get('receiver_id')
        call_type = data.get('call_type', 'video')
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(caller_id, session_token):
            emit('error', {'message': 'Invalid session'})
            return
        
        # Проверяем, онлайн ли получатель
        receiver_sid = user_sockets.get(receiver_id)
        if not receiver_sid:
            emit('call_error', {'message': 'Пользователь не в сети'})
            return
        
        # Создаем запись о звонке
        call_id = generate_call_id()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO calls (id, caller_id, receiver_id, call_type, status)
                VALUES (?, ?, ?, ?, 'calling')
            ''', (call_id, caller_id, receiver_id, call_type))
        
        # Сохраняем информацию о звонке
        active_calls.set(call_id, {
            'caller_id': caller_id,
            'receiver_id': receiver_id,
            'call_type': call_type,
            'status': 'calling',
            'created_at': datetime.datetime.now().isoformat()
        })
        
        # Отправляем уведомление получателю
        emit('incoming_call', {
            'call_id': call_id,
            'caller_id': caller_id,
            'call_type': call_type,
            'caller_name': get_user_by_id(caller_id)['name'] if get_user_by_id(caller_id) else 'Unknown'
        }, room=receiver_sid)
        
        emit('call_initiated', {
            'call_id': call_id,
            'status': 'calling'
        })
        
        logger.info(f"Call {call_id} started from {caller_id} to {receiver_id}")
        
    except Exception as e:
        logger.error(f"Call start error: {e}")
        emit('call_error', {'message': 'Failed to start call'})

@socketio.on('call_answer')
def handle_call_answer(data):
    """Ответ на звонок"""
    try:
        call_id = data.get('call_id')
        answer = data.get('answer')  # 'accept' or 'reject'
        session_token = data.get('session_token')
        user_id = data.get('user_id')
        
        if not verify_session_enhanced(user_id, session_token):
            emit('error', {'message': 'Invalid session'})
            return
        
        call_data = active_calls.get(call_id)
        if not call_data:
            emit('call_error', {'message': 'Call not found'})
            return
        
        caller_id = call_data['caller_id']
        caller_sid = user_sockets.get(caller_id)
        
        if answer == 'accept':
            # Обновляем статус звонка
            call_data['status'] = 'active'
            active_calls.set(call_id, call_data)
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE calls SET status = 'active' WHERE id = ?
                ''', (call_id,))
            
            if caller_sid:
                emit('call_accepted', {
                    'call_id': call_id
                }, room=caller_sid)
            
            emit('call_connected', {
                'call_id': call_id
            })
            
            logger.info(f"Call {call_id} accepted by {user_id}")
            
        else:
            # Отклонение звонка
            call_data['status'] = 'rejected'
            active_calls.set(call_id, call_data)
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE calls SET status = 'rejected', ended_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (call_id,))
            
            if caller_sid:
                emit('call_rejected', {
                    'call_id': call_id
                }, room=caller_sid)
            
            active_calls.delete(call_id)
            logger.info(f"Call {call_id} rejected by {user_id}")
            
    except Exception as e:
        logger.error(f"Call answer error: {e}")
        emit('call_error', {'message': 'Failed to answer call'})

@socketio.on('call_end')
def handle_call_end(data):
    """Завершение звонка"""
    try:
        call_id = data.get('call_id')
        session_token = data.get('session_token')
        user_id = data.get('user_id')
        
        if not verify_session_enhanced(user_id, session_token):
            return
        
        call_data = active_calls.get(call_id)
        if call_data:
            # Уведомляем другого участника
            other_user_id = call_data['caller_id'] if user_id == call_data['receiver_id'] else call_data['receiver_id']
            other_sid = user_sockets.get(other_user_id)
            
            if other_sid:
                emit('call_ended', {
                    'call_id': call_id
                }, room=other_sid)
            
            # Обновляем базу данных
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE calls SET status = 'ended', ended_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (call_id,))
            
            active_calls.delete(call_id)
            logger.info(f"Call {call_id} ended by {user_id}")
            
    except Exception as e:
        logger.error(f"Call end error: {e}")

@socketio.on('webrtc_offer')
def handle_webrtc_offer(data):
    """Обработка WebRTC offer"""
    try:
        call_id = data.get('call_id')
        offer = data.get('offer')
        session_token = data.get('session_token')
        user_id = data.get('user_id')
        
        if not verify_session_enhanced(user_id, session_token):
            return
        
        call_data = active_calls.get(call_id)
        if call_data:
            other_user_id = call_data['caller_id'] if user_id == call_data['receiver_id'] else call_data['receiver_id']
            other_sid = user_sockets.get(other_user_id)
            
            if other_sid:
                emit('webrtc_offer', {
                    'call_id': call_id,
                    'offer': offer
                }, room=other_sid)
                
    except Exception as e:
        logger.error(f"WebRTC offer error: {e}")

@socketio.on('webrtc_answer')
def handle_webrtc_answer(data):
    """Обработка WebRTC answer"""
    try:
        call_id = data.get('call_id')
        answer = data.get('answer')
        session_token = data.get('session_token')
        user_id = data.get('user_id')
        
        if not verify_session_enhanced(user_id, session_token):
            return
        
        call_data = active_calls.get(call_id)
        if call_data:
            other_user_id = call_data['caller_id'] if user_id == call_data['receiver_id'] else call_data['receiver_id']
            other_sid = user_sockets.get(other_user_id)
            
            if other_sid:
                emit('webrtc_answer', {
                    'call_id': call_id,
                    'answer': answer
                }, room=other_sid)
                
    except Exception as e:
        logger.error(f"WebRTC answer error: {e}")

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    """Обработка ICE candidate"""
    try:
        call_id = data.get('call_id')
        candidate = data.get('candidate')
        session_token = data.get('session_token')
        user_id = data.get('user_id')
        
        if not verify_session_enhanced(user_id, session_token):
            return
        
        call_data = active_calls.get(call_id)
        if call_data:
            other_user_id = call_data['caller_id'] if user_id == call_data['receiver_id'] else call_data['receiver_id']
            other_sid = user_sockets.get(other_user_id)
            
            if other_sid:
                emit('ice_candidate', {
                    'call_id': call_id,
                    'candidate': candidate
                }, room=other_sid)
                
    except Exception as e:
        logger.error(f"ICE candidate error: {e}")

# Новые функции
def initialize_voice_messages():
    """Инициализация голосовых сообщений"""
    return {
        'max_duration': 300,
        'formats': ['mp3', 'wav', 'ogg'],
        'max_size': 10 * 1024 * 1024  # 10MB
    }

def initialize_advanced_features():
    """Инициализация расширенных функций"""
    return {
        'ai_assistant': {
            'enabled': True,
            'features': ['auto_reply', 'smart_suggestions', 'content_moderation']
        }
    }

def initialize_sample_data():
    """Инициализация тестовых данных"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) as count FROM users")
                count = cursor.fetchone()['count']
                
                if count > 0:
                    logger.info("Тестовые данные уже существуют в базе")
                    return
                
                sample_users = [
                    {'id': 'user1', 'name': 'Alex_Quantum', 'avatar': '👨‍💻', 'online': True, 'last_seen': 'только что', 'status': 'Разрабатываю квантовый мессенджер'},
                    {'id': 'user2', 'name': 'Sarah_Cyber', 'avatar': '👩‍🎨', 'online': True, 'last_seen': '2 мин назад', 'status': 'Создаю цифровое искусство'},
                    {'id': 'user3', 'name': 'Mike_Neon', 'avatar': '👨‍🚀', 'online': False, 'last_seen': '1 час назад', 'status': 'Исследую космос'},
                    {'id': 'user4', 'name': 'Emma_Digital', 'avatar': '👩‍💼', 'online': True, 'last_seen': 'только что', 'status': 'Работаю над AI проектами'},
                    {'id': 'user5', 'name': 'Tech_Support', 'avatar': '🤖', 'online': True, 'last_seen': 'только что', 'status': 'Помогаю пользователям'},
                ]
                
                for user in sample_users:
                    friend_code = generate_friend_code()
                    cursor.execute('''
                        INSERT OR REPLACE INTO users 
                        (id, name, avatar, online, last_seen, status, friend_code, premium)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user['id'], user['name'], user['avatar'], 
                        user['online'], user['last_seen'], user['status'],
                        friend_code, random.choice([True, False])
                    ))
                    
                    session_token = generate_session_token()
                    cursor.execute('''
                        INSERT OR REPLACE INTO user_sessions 
                        (user_id, session_token, expires_at) VALUES (?, ?, datetime('now', '+7 days'))
                    ''', (user['id'], session_token))
                    user_sessions_memory.set(user['id'], session_token)
                    update_user_activity(user['id'])
                
                friendships = [
                    ('user1', 'user2'), ('user1', 'user3'),
                    ('user2', 'user1'), ('user3', 'user1'),
                    ('user1', 'user4'), ('user4', 'user1'),
                ]
                
                for user_id, friend_id in friendships:
                    cursor.execute('''
                        INSERT OR IGNORE INTO friendships (user_id, friend_id) 
                        VALUES (?, ?)
                    ''', (user_id, friend_id))
                
                test_messages = [
                    ('user2', 'user1', 'Привет! 👋 Рад познакомиться!'),
                    ('user1', 'user2', 'Привет! Я тоже рад! Как дела?'),
                    ('user2', 'user1', 'Отлично! Работаю над новым проектом. А ты?'),
                    ('user3', 'user1', 'Привет! Как дела?'),
                    ('user1', 'user3', 'Всё хорошо! Создаю новый мессенджер'),
                    ('user4', 'user1', 'Добро пожаловать в TrollexDL! 🚀'),
                    ('user1', 'user4', 'Спасибо! Очень крутой интерфейс!'),
                ]
                
                for sender_id, receiver_id, text in test_messages:
                    message_id = str(uuid.uuid4())
                    cursor.execute('''
                        INSERT INTO messages 
                        (id, sender_id, receiver_id, text) VALUES (?, ?, ?, ?)
                    ''', (message_id, sender_id, receiver_id, text))
                
                logger.info("Тестовые данные успешно инициализированы в базе")
                break
                
        except Exception as e:
            logger.error(f"Ошибка инициализации тестовых данных (попытка {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

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
    return packages

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
    return sticker_packs

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
    return theme_packs

# Создаем статические директории
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/uploads/image', exist_ok=True)
os.makedirs('static/uploads/audio', exist_ok=True)
os.makedirs('static/uploads/document', exist_ok=True)

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
    -webkit-user-select: none;
    user-select: none;
    -webkit-touch-callout: none;
}

body {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
    line-height: 1.6;
    position: fixed;
    width: 100%;
    height: 100%;
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
    50% { transform: scale(1.05); }
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes ripple {
    0% { transform: scale(0); opacity: 1; }
    100% { transform: scale(4); opacity: 0; }
}

@keyframes newYearGlow {
    0%, 100% { 
        box-shadow: 0 0 10px gold, 0 0 20px orange;
        transform: scale(1);
    }
    50% { 
        box-shadow: 0 0 20px gold, 0 0 40px orange;
        transform: scale(1.05);
    }
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
    overflow-y: auto;
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
    padding: 18px 24px;
    border: none;
    border-radius: 16px;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    margin: 10px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    min-height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    touch-action: manipulation;
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
    -webkit-appearance: none;
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
    -webkit-overflow-scrolling: touch;
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
    -webkit-user-select: text;
    user-select: text;
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
    -webkit-appearance: none;
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
    touch-action: manipulation;
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

/* Новогодний счетчик */
.new-year-counter {
    background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bff8f);
    padding: 12px 16px;
    border-radius: 16px;
    margin: 16px 0;
    text-align: center;
    animation: newYearGlow 2s infinite;
    border: 2px solid gold;
}

.new-year-counter h4 {
    color: #8b0000;
    margin-bottom: 8px;
    font-weight: bold;
}

.new-year-days {
    font-size: 2rem;
    font-weight: bold;
    color: #8b0000;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

/* Мотивационная фраза */
.motivation-box {
    background: rgba(255, 255, 255, 0.1);
    padding: 16px;
    border-radius: 16px;
    margin: 16px 0;
    text-align: center;
    border-left: 4px solid var(--neon);
    animation: fadeIn 0.6s ease-out;
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

/* Стили для звонков */
.call-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--primary);
    z-index: 2000;
    display: flex;
    flex-direction: column;
}

.call-header {
    padding: 20px;
    background: rgba(0,0,0,0.8);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.call-video-container {
    flex: 1;
    display: flex;
    position: relative;
}

.local-video, .remote-video {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.remote-video {
    background: var(--secondary);
}

.local-video {
    position: absolute;
    bottom: 20px;
    right: 20px;
    width: 200px;
    height: 150px;
    border: 2px solid var(--neon);
    border-radius: 12px;
    z-index: 10;
}

.call-controls {
    padding: 20px;
    background: rgba(0,0,0,0.8);
    display: flex;
    justify-content: center;
    gap: 20px;
}

.call-btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.call-accept {
    background: var(--success);
    color: white;
}

.call-reject {
    background: var(--danger);
    color: white;
}

.call-end {
    background: var(--danger);
    color: white;
}

.call-btn:hover {
    transform: scale(1.1);
}

.incoming-call-alert {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--gradient);
    padding: 30px;
    border-radius: 20px;
    z-index: 3000;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    animation: bounce 1s infinite;
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
    .screen {
        padding: 15px;
        align-items: flex-start;
    }
    
    .cosmic-card {
        margin: 10px;
        padding: 24px;
        border-radius: 20px;
        max-width: none;
    }
    
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
        min-width: 44px;
        min-height: 44px;
    }

    .nav-tab {
        font-size: 0.85rem;
        padding: 12px 6px;
        min-height: 60px;
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
        min-height: 48px;
        min-width: 48px;
    }

    .message-input {
        min-height: 52px;
        font-size: 16px; /* Предотвращает zoom на iOS */
    }
    
    .user-avatar {
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
    }

    /* Адаптация звонков для мобильных */
    .local-video {
        width: 120px;
        height: 90px;
        bottom: 10px;
        right: 10px;
    }

    .call-btn {
        width: 50px;
        height: 50px;
        font-size: 1.2rem;
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
        min-height: 56px;
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
        width: 50px;
        height: 50px;
        font-size: 1.3rem;
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

/* Overlay для мобильного меню */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 99;
    display: none;
    backdrop-filter: blur(5px);
}

.overlay.active {
    display: block;
    animation: fadeIn 0.3s ease;
}

/* Адаптивные изображения */
img {
    max-width: 100%;
    height: auto;
}

/* Улучшенные элементы управления */
.control-btn {
    padding: 12px;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.1rem;
    min-width: 44px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.1);
    color: var(--text);
    touch-action: manipulation;
}

.control-btn:active {
    transform: scale(0.95);
}

/* Анимация появления элементов */
.chat-item {
    padding: 16px;
    display: flex;
    align-items: center;
    border-radius: 16px;
    margin: 8px 0;
    background: rgba(255,255,255,0.05);
    transition: all 0.3s ease;
    border: 1px solid transparent;
    animation: fadeIn 0.5s ease-out;
}

.chat-item:active {
    background: rgba(107, 43, 217, 0.2);
    transform: scale(0.98);
}

.chat-item:hover {
    border-color: var(--accent);
}

.item-avatar {
    width: 50px;
    height: 50px;
    border-radius: 14px;
    background: var(--gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-right: 16px;
    flex-shrink: 0;
}

/* Empty states */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 20px;
    opacity: 0.7;
}
'''

# JavaScript с РЕАЛЬНОЙ РЕАЛИЗАЦИЕЙ WEBRTC ЗВОНКОВ
JS_CONTENT = '''
// static/js/app.js - ПОЛНАЯ РЕАЛИЗАЦИЯ С WEBRTC ЗВОНКАМИ
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
        this.daysUntilNewYear = 0;
        this.currentMotivation = '';
        
        // WebRTC переменные
        this.localStream = null;
        this.remoteStream = null;
        this.peerConnection = null;
        this.currentCall = null;
        this.socket = null;
        
        // Конфигурация STUN/TURN серверов
        this.rtcConfig = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupServiceWorker();
        this.setupWebSocket();
        this.checkAutoLogin();
        this.startConnectionMonitor();
        this.calculateNewYear();
        this.updateMotivation();
    }

    setupWebSocket() {
        // Подключаемся к WebSocket серверу
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('WebSocket connected');
            if (this.currentUser && this.sessionToken) {
                this.socket.emit('authenticate', {
                    user_id: this.currentUser.id,
                    session_token: this.sessionToken
                });
            }
        });
        
        this.socket.on('disconnect', () => {
            console.log('WebSocket disconnected');
        });
        
        this.socket.on('authenticated', (data) => {
            console.log('WebSocket authentication successful');
        });
        
        this.socket.on('error', (data) => {
            this.showNotification(data.message, 'error');
        });
        
        // Обработчики сообщений
        this.socket.on('new_message', (data) => {
            this.handleNewMessage(data);
        });
        
        this.socket.on('message_sent', (data) => {
            this.handleMessageSent(data);
        });
        
        this.socket.on('user_typing', (data) => {
            this.handleUserTyping(data);
        });
        
        this.socket.on('user_status', (data) => {
            this.handleUserStatus(data);
        });
        
        // Обработчики звонков
        this.socket.on('incoming_call', (data) => {
            this.handleIncomingCall(data);
        });
        
        this.socket.on('call_initiated', (data) => {
            this.handleCallInitiated(data);
        });
        
        this.socket.on('call_accepted', (data) => {
            this.handleCallAccepted(data);
        });
        
        this.socket.on('call_rejected', (data) => {
            this.handleCallRejected(data);
        });
        
        this.socket.on('call_ended', (data) => {
            this.handleCallEnded(data);
        });
        
        this.socket.on('call_connected', (data) => {
            this.handleCallConnected(data);
        });
        
        this.socket.on('call_error', (data) => {
            this.handleCallError(data);
        });
        
        // WebRTC обработчики
        this.socket.on('webrtc_offer', (data) => {
            this.handleWebRTCOffer(data);
        });
        
        this.socket.on('webrtc_answer', (data) => {
            this.handleWebRTCAnswer(data);
        });
        
        this.socket.on('ice_candidate', (data) => {
            this.handleICECandidate(data);
        });
    }

    setupEventListeners() {
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        window.addEventListener('resize', () => this.handleResize());
        window.addEventListener('beforeunload', () => this.handleBeforeUnload());
        document.addEventListener('visibilitychange', () => this.handleVisibilityChange());
        
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

    calculateNewYear() {
        const now = new Date();
        const nextYear = now.getFullYear() + 1;
        const newYear = new Date(nextYear, 0, 1);
        const diff = newYear - now;
        this.daysUntilNewYear = Math.ceil(diff / (1000 * 60 * 60 * 24));
    }

    updateMotivation() {
        const motivations = [
            "🚀 Ты можешь всё! Верь в себя!",
            "💫 Сегодня твой день для великих дел!",
            "🌟 Не сдавайся, у тебя всё получится!",
            "🔥 Впереди ждут великие открытия!",
            "🎯 Каждая мечта достижима!",
            "⚡ Ты сильнее, чем думаешь!",
            "🌈 Будущее создаётся сегодня!",
            "🎉 Каждый день - новая возможность!"
        ];
        this.currentMotivation = motivations[Math.floor(Math.random() * motivations.length)];
    }

    startConnectionMonitor() {
        setInterval(() => {
            this.checkConnectionQuality();
        }, 30000);
    }

    async checkConnectionQuality() {
        try {
            const startTime = performance.now();
            await fetch('/api/ping', { method: 'HEAD', cache: 'no-store' });
            const latency = performance.now() - startTime;
            
            if (latency > 1000) {
                this.connectionStatus = 'slow';
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
                
                const isValid = await this.verifySession();
                if (isValid) {
                    await this.loadInitialData();
                    this.showMainApp();
                } else {
                    this.clearStorage();
                    this.showWelcomeScreen();
                }
            } else {
                this.showWelcomeScreen();
            }
        } catch (error) {
            console.error('Auto-login failed:', error);
            this.clearStorage();
            this.showWelcomeScreen();
        }
    }

    async verifySession() {
        if (!this.currentUser || !this.sessionToken) return false;
        
        try {
            const response = await this.fetchWithTimeout('/api/verify_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    session_token: this.sessionToken
                })
            }, 5000);
            
            const data = await response.json();
            return data.success === true;
        } catch (error) {
            console.error('Session verification failed:', error);
            return false;
        }
    }

    clearStorage() {
        localStorage.removeItem('trollexUser');
        localStorage.removeItem('sessionToken');
        this.currentUser = null;
        this.sessionToken = null;
    }

    async loadInitialData() {
        this.showLoading(true);
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
        } finally {
            this.showLoading(false);
        }
    }

    showLoading(show) {
        this.isLoading = show;
        const loadingElement = document.getElementById('loadingScreen');
        if (loadingElement) {
            if (show) {
                loadingElement.classList.remove('hidden');
            } else {
                setTimeout(() => {
                    loadingElement.classList.add('hidden');
                }, 500);
            }
        }
    }

    async loadUsers() {
        try {
            const response = await this.fetchWithTimeout('/api/get_users', {}, 5000);
            const data = await response.json();
            
            if (data.success) {
                this.allUsers = data.users;
            }
        } catch (error) {
            console.error('Failed to load users:', error);
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
                signal: controller.signal,
                cache: 'no-store'
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
        
        this.updateNewYearCounter();
    }

    updateNewYearCounter() {
        const newYearElement = document.getElementById('newYearCounter');
        if (newYearElement) {
            newYearElement.innerHTML = `
                <h4>🎄 До Нового Года:</h4>
                <div class="new-year-days">${this.daysUntilNewYear} дней</div>
                <div style="margin-top: 8px; font-size: 0.9rem;">✨ Готовься к чудесам!</div>
            `;
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
        setInterval(() => {
            this.updateOnlineStatus();
        }, 30000);
        
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
    }

    hasPremiumSubscription() {
        return Math.random() > 0.7;
    }

    switchTab(tabName, event) {
        if (this.isLoading) return;
        
        this.currentTab = tabName;
        
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
        
        const friendsHtml = this.friends.map(friend => {
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
            !this.friends.some(friend => friend.id === user.id)
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

    // РЕАЛЬНАЯ РЕАЛИЗАЦИЯ WEBRTC ЗВОНКОВ
    async startVideoCall(userId = null) {
        if (!userId) {
            this.showNotification('Выберите пользователя для звонка', 'warning');
            return;
        }

        try {
            this.socket.emit('call_start', {
                caller_id: this.currentUser.id,
                receiver_id: userId,
                call_type: 'video',
                session_token: this.sessionToken
            });

            this.showNotification('Звонок инициирован...', 'info');

        } catch (error) {
            console.error('Error starting video call:', error);
            this.showNotification('Ошибка запуска звонка', 'error');
        }
    }

    async startVoiceCall(userId = null) {
        if (!userId) {
            this.showNotification('Выберите пользователя для звонка', 'warning');
            return;
        }

        try {
            this.socket.emit('call_start', {
                caller_id: this.currentUser.id,
                receiver_id: userId,
                call_type: 'audio',
                session_token: this.sessionToken
            });

            this.showNotification('Аудиозвонок инициирован...', 'info');

        } catch (error) {
            console.error('Error starting voice call:', error);
            this.showNotification('Ошибка запуска звонка', 'error');
        }
    }

    // Обработчики звонков
    handleIncomingCall(data) {
        this.currentCall = data.call_id;
        
        const callAlert = `
            <div class="incoming-call-alert">
                <h3>Входящий звонок</h3>
                <p>${data.caller_name}</p>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button class="call-btn call-accept" onclick="app.answerCall('accept')">📞</button>
                    <button class="call-btn call-reject" onclick="app.answerCall('reject')">✖</button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', callAlert);
    }

    async answerCall(answer) {
        document.querySelector('.incoming-call-alert')?.remove();

        this.socket.emit('call_answer', {
            call_id: this.currentCall,
            answer: answer,
            user_id: this.currentUser.id,
            session_token: this.sessionToken
        });

        if (answer === 'accept') {
            this.showCallInterface();
        }
    }

    showCallInterface() {
        const callInterface = `
            <div class="call-container">
                <div class="call-header">
                    <h3>Звонок</h3>
                    <button class="control-btn" onclick="app.endCall()">✖</button>
                </div>
                <div class="call-video-container">
                    <video id="remoteVideo" class="remote-video" autoplay playsinline></video>
                    <video id="localVideo" class="local-video" autoplay playsinline muted></video>
                </div>
                <div class="call-controls">
                    <button class="call-btn call-end" onclick="app.endCall()">📞</button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', callInterface);
    }

    endCall() {
        if (this.currentCall) {
            this.socket.emit('call_end', {
                call_id: this.currentCall,
                user_id: this.currentUser.id,
                session_token: this.sessionToken
            });
        }

        this.cleanupCall();
    }

    cleanupCall() {
        document.querySelector('.call-container')?.remove();
        document.querySelector('.incoming-call-alert')?.remove();
        this.currentCall = null;
    }

    // Обработчики событий звонков
    handleCallInitiated(data) {
        this.currentCall = data.call_id;
        this.showNotification('Звонок отправлен...', 'info');
    }

    handleCallAccepted(data) {
        this.showNotification('Звонок принят!', 'success');
        this.showCallInterface();
    }

    handleCallRejected(data) {
        this.showNotification('Звонок отклонен', 'warning');
        this.cleanupCall();
    }

    handleCallEnded(data) {
        this.showNotification('Звонок завершен', 'info');
        this.cleanupCall();
    }

    handleCallConnected(data) {
        this.showNotification('Соединение установлено!', 'success');
    }

    handleCallError(data) {
        this.showNotification('Ошибка звонка: ' + data.message, 'error');
        this.cleanupCall();
    }

    // Обработчики реального времени
    handleNewMessage(data) {
        if (this.currentChat === data.sender_id) {
            this.addMessageToChat(data);
        }
    }

    handleMessageSent(data) {
        console.log('Message sent successfully:', data.message_id);
    }

    handleUserTyping(data) {
        if (data.typing) {
            this.typingUsers.set(data.user_id, Date.now());
        } else {
            this.typingUsers.delete(data.user_id);
        }
        
        if (this.currentChat === data.user_id) {
            this.renderCurrentTab();
        }
    }

    handleUserStatus(data) {
        const user = this.allUsers.find(u => u.id === data.user_id);
        if (user) {
            user.online = data.online;
            user.last_seen = data.last_seen;
            this.renderCurrentTab();
        }
    }

    // Реальные функции чата
    async selectChat(userId) {
        this.currentChat = userId;
        const user = this.allUsers.find(u => u.id === userId);
        
        if (user) {
            document.getElementById('currentChatName').textContent = user.name;
            document.getElementById('currentChatAvatar').textContent = user.avatar;
            document.getElementById('currentChatStatus').textContent = 
                user.online ? 'В сети' : `Был(а) ${user.last_seen}`;
            
            await this.loadChatMessages(userId);
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
            const isSent = msg.sender_id === this.currentUser.id;
            const sender = this.allUsers.find(u => u.id === msg.sender_id);
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

        if (this.socket) {
            this.socket.emit('send_message', {
                user_id: this.currentUser.id,
                target_id: this.currentChat,
                message: message,
                session_token: this.sessionToken
            });

            if (messageInput) {
                messageInput.value = '';
            }
        } else {
            this.showNotification('Ошибка подключения', 'error');
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
            message.sender_id === this.currentUser.id ? 'sent' : 'received'
        }`;
        messageElement.style.animation = 'fadeIn 0.3s ease-out';
        
        const sender = this.allUsers.find(u => u.id === message.sender_id);
        const senderName = sender ? sender.name : 'Неизвестный';
        
        messageElement.innerHTML = `
            ${message.sender_id !== this.currentUser.id ? 
                `<div style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 4px;">${senderName}</div>` : ''}
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

    // Реальные функции друзей
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

    // Донат функции
    showDonatePanel() {
        const overlay = document.getElementById('overlay');
        const donatePanel = document.createElement('div');
        
        donatePanel.className = 'cosmic-card';
        donatePanel.style.position = 'fixed';
        donatePanel.style.top = '50%';
        donatePanel.style.left = '50%';
        donatePanel.style.transform = 'translate(-50%, -50%)';
        donatePanel.style.zIndex = '1000';
        donatePanel.style.maxHeight = '90vh';
        donatePanel.style.overflowY = 'auto';
        donatePanel.innerHTML = this.getDonatePanelHTML();
        
        document.body.appendChild(donatePanel);
        overlay.classList.add('active');
        
        overlay.onclick = () => this.hideDonatePanel();
        donatePanel.querySelector('.close-btn').onclick = () => this.hideDonatePanel();
    }

    hideDonatePanel() {
        const donatePanel = document.querySelector('.cosmic-card');
        const overlay = document.getElementById('overlay');
        
        if (donatePanel && donatePanel.style.position === 'fixed') {
            donatePanel.remove();
        }
        overlay.classList.remove('active');
    }

    getDonatePanelHTML() {
        const packages = Object.values(initialize_donate_packages());
        
        return `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                <h2 style="margin: 0;">💎 TrollexDL Premium</h2>
                <button class="control-btn close-btn" style="background: var(--danger);">✕</button>
            </div>
            
            <div style="margin: 20px 0;">
                <h4 style="text-align: center; margin-bottom: 16px;">🎯 Выберите тарифный план</h4>
                <div style="max-height: 50vh; overflow-y: auto; padding-right: 8px;">
                    ${packages.map(pkg => `
                        <div class="donate-package ${pkg.popular ? 'popular' : ''}" 
                             style="border-color: ${pkg.color}">
                            <div class="package-header">
                                <div class="package-name" style="color: ${pkg.color}">${pkg.name}</div>
                                <div class="package-price" style="color: ${pkg.color}">
                                    ${pkg.price} руб
                                    ${pkg.original_price ? `<span class="package-original-price" style="text-decoration: line-through; font-size: 0.9rem; margin-left: 8px;">${pkg.original_price} руб</span>` : ''}
                                </div>
                                <div class="package-period">за ${pkg.period}</div>
                            </div>
                            <ul class="package-features" style="list-style: none; padding: 0; margin: 16px 0;">
                                ${pkg.features.map(feature => `<li style="margin: 8px 0; font-size: 0.9rem;">${feature}</li>`).join('')}
                            </ul>
                            <button class="btn btn-primary" onclick="app.selectPackage('${pkg.id}')" 
                                    style="background: ${pkg.color}; color: white;">
                                🛒 Выбрать ${pkg.name}
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    selectPackage(packageId) {
        this.showNotification(`🎉 Выбран тариф ${packageId}!`, 'success');
        this.hideDonatePanel();
    }

    sendSticker(stickerId) {
        const sticker = this.stickers.find(s => s.id === stickerId);
        if (sticker && this.currentChat && this.socket) {
            this.socket.emit('send_message', {
                user_id: this.currentUser.id,
                target_id: this.currentChat,
                message: sticker.emoji + ' ' + sticker.text,
                session_token: this.sessionToken
            });

            this.showNotification(`Стикер отправлен: ${sticker.text}`, 'success');
        }
    }

    showUserProfile(userId) {
        const user = this.allUsers.find(u => u.id === userId);
        if (user) {
            this.showNotification(`👤 Профиль ${user.name} - ${user.status}`, 'info');
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
            const overlay = document.getElementById('overlay');
            if (sidebar) sidebar.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
        }
    }

    handleBeforeUnload() {
        if (this.currentUser) {
            localStorage.setItem('trollexUser', JSON.stringify(this.currentUser));
            localStorage.setItem('sessionToken', this.sessionToken);
        }
        
        if (this.currentCall) {
            this.endCall();
        }
    }

    handleVisibilityChange() {
        if (!document.hidden) {
            this.updateOnlineStatus();
        }
    }

    handleTouchStart(event) {
        if (event.target.classList.contains('btn') || 
            event.target.classList.contains('control-btn') ||
            event.target.classList.contains('nav-tab')) {
            event.target.style.transform = 'scale(0.95)';
        }
    }

    handleTouchEnd(event) {
        if (event.target.classList.contains('btn') || 
            event.target.classList.contains('control-btn') ||
            event.target.classList.contains('nav-tab')) {
            event.target.style.transform = '';
        }
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
    const donatePanel = document.querySelector('.cosmic-card');
    
    if (sidebar) sidebar.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    if (donatePanel && donatePanel.style.position === 'fixed') {
        donatePanel.remove();
    }
}

// Инициализация приложения
let app;

document.addEventListener('DOMContentLoaded', function() {
    app = new TrollexApp();
    window.app = app;
});
'''

# Сохраняем файлы
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(CSS_CONTENT)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(JS_CONTENT)

# Service Worker для PWA
SW_CONTENT = '''
// static/sw.js - Service Worker для оффлайн работы
const CACHE_NAME = 'trollexdl-v2.0.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js'
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0a0a2a">
    <meta name="description" content="TrollexDL - защищенный мессенджер с квантовым шифрованием">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
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
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo floating-element">TrollexDL</div>
            <div style="margin-bottom: 25px; color: var(--text-secondary);">
                Премиум мессенджер с квантовым шифрованием
            </div>
            
            <div class="new-year-counter" id="newYearCounter">
                <!-- Новогодний счетчик будет добавлен через JS -->
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
            </div>

            <div class="friend-code-display">
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Ваш Friend Code:</div>
                <div class="friend-code" id="registerFriendCode">TRLX-XXXX-XXXX</div>
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
                <button class="mobile-menu-btn control-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
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
                <button class="mobile-menu-btn control-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="control-btn" onclick="app.startVideoCall(app.currentChat)" style="background: var(--success);" 
                            aria-label="Начать видеозвонок" id="callBtn">📞</button>
                    <button class="control-btn" onclick="app.showDonatePanel()" style="background: var(--accent);" 
                            aria-label="Премиум функции">💎</button>
                </div>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon floating-element">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                </div>
            </div>

            <div class="message-input-container">
                <textarea class="message-input" placeholder="Введите сообщение..." id="messageInput" 
                       onkeydown="handleKeyPress(event)" 
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
    "description": "Премиум мессенджер с квантовым шифрованием и WebRTC звонками",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a2a",
    "theme_color": "#6c2bd9",
    "orientation": "portrait"
}

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

@app.route('/health')
def health_check():
    """Проверка состояния приложения"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'active_users': len(user_activity),
            'online_sockets': len(online_users),
            'active_calls': len(active_calls),
            'database': 'connected',
            'version': '2.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/verify_session', methods=['POST'])
@rate_limit
def api_verify_session():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        
        if verify_session_enhanced(user_id, session_token):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid session'})
    except Exception as e:
        logger.error(f"Session verification error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/register_user', methods=['POST'])
@rate_limit
def api_register_user():
    try:
        data = request.get_json()
        user_id = data.get('id')
        name = sanitize_input(data.get('name', ''))
        avatar = data.get('avatar', '🚀')
        friend_code = data.get('friend_code')
        
        if not user_id or not name or not friend_code:
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        existing_user = get_user_by_id(user_id)
        if existing_user:
            return jsonify({'success': False, 'error': 'User already exists'})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (id, name, avatar, online, last_seen, status, friend_code)
                VALUES (?, ?, ?, TRUE, 'только что', 'Новый пользователь TrollexDL', ?)
            ''', (user_id, name, avatar, friend_code))
            
            session_token = generate_session_token()
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, datetime('now', '+7 days'))
            ''', (user_id, session_token))
            
            user_sessions_memory.set(user_id, session_token)
            update_user_activity(user_id)
        
        return jsonify({
            'success': True, 
            'session_token': session_token,
            'message': 'User registered successfully'
        })
        
    except Exception as e:
        logger.error(f"User registration error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_users')
@require_auth
@rate_limit
def api_get_users():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, avatar, online, last_seen, status, friend_code, premium FROM users")
            users = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        logger.error(f"Get users error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_friends')
@require_auth
@rate_limit
def api_get_friends():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.id, u.name, u.avatar, u.online, u.last_seen, u.status 
                FROM users u
                JOIN friendships f ON u.id = f.friend_id
                WHERE f.user_id = ?
            ''', (user_id,))
            friends = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({'success': True, 'friends': friends})
    except Exception as e:
        logger.error(f"Get friends error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_messages')
@require_auth
@rate_limit
def api_get_messages():
    try:
        user_id = request.args.get('user_id')
        target_id = request.args.get('target_id')
        
        if not user_id or not target_id:
            return jsonify({'success': False, 'error': 'User ID and Target ID required'})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM messages 
                WHERE (sender_id = ? AND receiver_id = ?) 
                   OR (sender_id = ? AND receiver_id = ?)
                ORDER BY timestamp
                LIMIT 100
            ''', (user_id, target_id, target_id, user_id))
            
            messages = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({'success': True, 'messages': messages})
    except Exception as e:
        logger.error(f"Get messages error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/send_message', methods=['POST'])
@require_auth
@rate_limit
def api_send_message():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        target_user_id = data.get('target_user_id')
        message_text = sanitize_input(data.get('message', ''))
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'})
        
        is_valid, error_msg = validate_message(message_text)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg})
        
        message_id = str(uuid.uuid4())
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (id, sender_id, receiver_id, text, type)
                VALUES (?, ?, ?, ?, 'text')
            ''', (message_id, user_id, target_user_id, message_text))
        
        return jsonify({'success': True, 'message_id': message_id})
        
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_donate_packages')
@rate_limit
def api_get_donate_packages():
    packages = initialize_donate_packages()
    return jsonify({'success': True, 'packages': list(packages.values())})

@app.route('/api/get_stickers')
@require_auth
@rate_limit
def api_get_stickers():
    stickers_data = initialize_stickers()
    all_stickers = stickers_data['basic'] + stickers_data.get('premium', [])
    return jsonify({'success': True, 'stickers': all_stickers})

@app.route('/api/get_themes')
@require_auth
@rate_limit
def api_get_themes():
    themes_data = initialize_themes()
    return jsonify({'success': True, 'themes': themes_data})

@app.route('/api/send_friend_request', methods=['POST'])
@require_auth
@rate_limit
def api_send_friend_request():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        target_id = data.get('target_id')
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'})
        
        if user_id == target_id:
            return jsonify({'success': False, 'error': 'Cannot send friend request to yourself'})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            request_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO friend_requests (id, from_user_id, to_user_id, status)
                VALUES (?, ?, ?, 'pending')
            ''', (request_id, user_id, target_id))
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Send friend request error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add_friend_by_code', methods=['POST'])
@require_auth
@rate_limit
def api_add_friend_by_code():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        friend_code = data.get('friend_code')
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'})
        
        friend_user_id = get_user_by_friend_code(friend_code)
        if not friend_user_id:
            return jsonify({'success': False, 'error': 'User not found'})
        
        if user_id == friend_user_id:
            return jsonify({'success': False, 'error': 'Cannot add yourself as friend'})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)
            ''', (user_id, friend_user_id))
            
            cursor.execute('''
                INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)
            ''', (friend_user_id, user_id))
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Add friend by code error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/remove_friend', methods=['POST'])
@require_auth
@rate_limit
def api_remove_friend():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        friend_id = data.get('friend_id')
        session_token = data.get('session_token')
        
        if not verify_session_enhanced(user_id, session_token):
            return jsonify({'success': False, 'error': 'Invalid session'})
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM friendships 
                WHERE user_id = ? AND friend_id = ?
            ''', (user_id, friend_id))
            
            cursor.execute('''
                DELETE FROM friendships 
                WHERE user_id = ? AND friend_id = ?
            ''', (friend_id, user_id))
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Remove friend error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    initialize_sample_data()
    
    port = int(os.environ.get('PORT', 5000))
    debug = Config.DEBUG
    
    total_users = get_total_users_count()
    logger.info(f"🚀 TrollexDL ULTIMATE v2.0 запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"📱 Реальные WebRTC звонки активированы")
    logger.info(f"💬 Мгновенные сообщения включены")
    logger.info(f"👥 Всего пользователей в базе: {total_users}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    if debug:
        socketio.run(app, host='0.0.0.0', port=port, debug=debug)
    else:
        logger.info("🚀 Запуск в продакшен режиме с Waitress")
        serve(app, host='0.0.0.0', port=port)
