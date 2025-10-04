# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ С ЗВОНКАМИ (УЛУЧШЕННЫЙ)
from flask import Flask, render_template_string, request, send_from_directory
from flask_socketio import SocketIO, emit
import datetime
import random
import os
import base64
import time
import json
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'
app.config['UPLOAD_FOLDER'] = 'user_avatars'
app.config['DATA_FOLDER'] = 'user_data'
socketio = SocketIO(app, cors_allowed_origins="*")

# Создаем папки
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# База данных
users_db = {}
messages_db = {}  # Структура: {user_id: {target_user_id: [messages]}}
user_sessions = {}
news_messages = []
user_settings = {}
favorites_db = {}
groups_db = {}
message_reactions = {}
active_calls = {}
moderation_db = {
    'banned_users': [],
    'muted_users': [],
    'deleted_messages': [],
    'moderators': []
}
unread_messages = {}  # Новое: непрочитанные сообщения {user_id: {chat_id: count}}

# Админ
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "dltrollex123"

# Стандартные аватарки
DEFAULT_AVATARS = [
    {"emoji": "👻", "bg": "#6b21a8"}, {"emoji": "😊", "bg": "#7e22ce"},
    {"emoji": "😎", "bg": "#9333ea"}, {"emoji": "🤠", "bg": "#a855f7"},
    {"emoji": "🧑", "bg": "#c084fc"}, {"emoji": "👨", "bg": "#6b21a8"},
    {"emoji": "👩", "bg": "#7e22ce"}, {"emoji": "🦊", "bg": "#9333ea"},
    {"emoji": "🐱", "bg": "#a855f7"}, {"emoji": "🐶", "bg": "#c084fc"}
]

# Темы с фиолетовой основой
THEMES = {
    "dark_purple": {
        "name": "Темный фиолетовый", 
        "bg": "#0f0f0f", 
        "card": "#1a1a1a", 
        "accent": "#8b5cf6", 
        "text": "#ffffff",
        "secondary": "#2d2d2d",
        "border": "#3d3d3d"
    },
    "blue_purple": {
        "name": "Сине-фиолетовый", 
        "bg": "#0a0a1f", 
        "card": "#151533", 
        "accent": "#6366f1", 
        "text": "#ffffff",
        "secondary": "#1e1e3f",
        "border": "#2d2d5a"
    },
    "pink_purple": {
        "name": "Розово-фиолетовый", 
        "bg": "#1a0a1a", 
        "card": "#2d152d", 
        "accent": "#ec4899", 
        "text": "#ffffff",
        "secondary": "#3d1f3d",
        "border": "#5a2d5a"
    }
}

# Реакции - ТОЛЬКО ЛАЙК
REACTIONS = ["👍"]

# Функции для сохранения/загрузки данных
def save_user_data():
    """Сохраняет все данные пользователей"""
    data = {
        'users_db': users_db,
        'messages_db': messages_db,
        'news_messages': news_messages,
        'user_settings': user_settings,
        'favorites_db': favorites_db,
        'groups_db': groups_db,
        'message_reactions': message_reactions,
        'moderation_db': moderation_db,
        'unread_messages': unread_messages
    }
    try:
        with open(os.path.join(app.config['DATA_FOLDER'], 'data.pkl'), 'wb') as f:
            pickle.dump(data, f)
        print("💾 Данные сохранены")
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

def load_user_data():
    """Загружает данные пользователей"""
    global users_db, messages_db, news_messages, user_settings, favorites_db, groups_db, message_reactions, moderation_db, unread_messages
    try:
        with open(os.path.join(app.config['DATA_FOLDER'], 'data.pkl'), 'rb') as f:
            data = pickle.load(f)
            users_db = data.get('users_db', {})
            messages_db = data.get('messages_db', {})
            news_messages = data.get('news_messages', [])
            user_settings = data.get('user_settings', {})
            favorites_db = data.get('favorites_db', {})
            groups_db = data.get('groups_db', {})
            message_reactions = data.get('message_reactions', {})
            moderation_db = data.get('moderation_db', {
                'banned_users': [],
                'muted_users': [],
                'deleted_messages': [],
                'moderators': []
            })
            unread_messages = data.get('unread_messages', {})
        print("📂 Данные загружены")
    except FileNotFoundError:
        print("📂 Файл данных не найден, создаем новую базу")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")

# Загружаем данные при запуске
load_user_data()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        :root {
            --bg-color: #0f0f0f;
            --card-color: #1a1a1a;
            --accent-color: #8b5cf6;
            --text-color: #ffffff;
            --secondary-color: #2d2d2d;
            --border-color: #3d3d3d;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        /* Анимация свечения */
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
        
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes ringing {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        @keyframes notificationPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); background: #ef4444; }
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
        
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        
        .ringing {
            animation: ringing 1s ease-in-out infinite;
        }
        
        .notification-pulse {
            animation: notificationPulse 1s ease-in-out infinite;
        }
        
        /* Экраны входа */
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
        }
        
        .auth-box {
            background: var(--card-color);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 2px solid var(--accent-color);
            width: 450px;
            text-align: center;
            position: relative;
            overflow: hidden;
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
            font-size: 48px;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 15px;
        }
        
        .subtitle {
            color: #888;
            margin-bottom: 40px;
            font-size: 16px;
        }
        
        .input-field {
            width: 100%;
            padding: 18px;
            margin-bottom: 20px;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-color);
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .input-field:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
            transform: translateY(-2px);
        }
        
        .optional {
            color: #888;
            font-size: 12px;
            margin-top: -15px;
            margin-bottom: 20px;
            text-align: left;
        }
        
        .btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-admin {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        
        .btn-admin:hover {
            box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4);
        }
        
        .btn-call {
            background: linear-gradient(135deg, #10b981, #059669);
        }
        
        .btn-call:hover {
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
        }
        
        .btn-video {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
        }
        
        .btn-video:hover {
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        }
        
        .btn-end-call {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }
        
        .btn-end-call:hover {
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
        }
        
        .link {
            color: var(--accent-color);
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .link:hover {
            text-shadow: 0 0 10px var(--accent-color);
        }
        
        .error {
            color: #ef4444;
            margin-top: 15px;
            padding: 10px;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
            border: 1px solid #ef4444;
        }
        
        .success {
            color: #10b981;
            margin-top: 15px;
            padding: 10px;
            background: rgba(16, 185, 129, 0.1);
            border-radius: 8px;
            border: 1px solid #10b981;
        }
        
        /* Основной интерфейс чата */
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
        }
        
        .chat-container {
            display: flex;
            height: 100vh;
            background: var(--bg-color);
        }
        
        .sidebar {
            width: 350px;
            background: var(--card-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .header {
            padding: 25px;
            background: var(--card-color);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
        }
        
        .header-btn {
            background: var(--secondary-color);
            border: none;
            border-radius: 10px;
            width: 45px;
            height: 45px;
            color: var(--accent-color);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .header-btn:hover {
            background: var(--accent-color);
            color: white;
            transform: scale(1.1);
        }
        
        .notification-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #ef4444;
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px;
            background: var(--secondary-color);
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .user-info:hover {
            background: var(--accent-color);
        }
        
        .avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 20px;
            background-size: cover;
            background-position: center;
            border: 3px solid var(--accent-color);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }
        
        .search-container {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .search-input {
            width: 100%;
            padding: 15px 15px 15px 45px;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 14px;
            transition: all 0.3s ease;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23888" width="20px" height="20px"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>');
            background-repeat: no-repeat;
            background-position: 15px center;
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }
        
        .chats {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }
        
        .chat-item {
            padding: 20px;
            margin-bottom: 8px;
            background: var(--secondary-color);
            border-radius: 15px;
            cursor: pointer;
            border: 2px solid transparent;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .chat-item:hover {
            background: var(--accent-color);
            transform: translateX(5px);
            border-color: var(--accent-color);
        }
        
        .chat-item.active {
            background: var(--accent-color);
            border-color: var(--accent-color);
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        }
        
        .chat-call-buttons {
            position: absolute;
            right: 15px;
            display: flex;
            gap: 8px;
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .chat-item:hover .chat-call-buttons {
            opacity: 1;
        }
        
        .call-btn-small {
            background: var(--accent-color);
            border: none;
            border-radius: 8px;
            width: 32px;
            height: 32px;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .call-btn-small:hover {
            transform: scale(1.1);
        }
        
        .audio-call-btn {
            background: #10b981;
        }
        
        .video-call-btn {
            background: #3b82f6;
        }
        
        .chat-icon {
            font-size: 24px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            position: relative;
        }
        
        .chat-info {
            flex: 1;
            min-width: 0;
        }
        
        .chat-name {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 16px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .chat-last-message {
            color: #888;
            font-size: 13px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .unread-badge {
            background: #ef4444;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            font-size: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .online-status {
            position: absolute;
            bottom: -2px;
            right: -2px;
            width: 12px;
            height: 12px;
            background: #10b981;
            border: 2px solid var(--card-color);
            border-radius: 50%;
        }
        
        /* Основная область чата */
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-color);
        }
        
        .chat-header {
            padding: 25px;
            background: var(--card-color);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .chat-actions {
            display: flex;
            gap: 12px;
        }
        
        .messages {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            background: var(--bg-color);
        }
        
        .message {
            max-width: 65%;
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 18px;
            word-wrap: break-word;
            position: relative;
            animation: messageAppear 0.3s ease-out;
        }
        
        @keyframes messageAppear {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message-in {
            background: var(--card-color);
            margin-right: auto;
            border-bottom-left-radius: 5px;
        }
        
        .message-out {
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        
        .message-sender {
            font-size: 13px;
            color: var(--accent-color);
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        .message-time {
            font-size: 11px;
            color: rgba(255,255,255,0.6);
            text-align: right;
            margin-top: 8px;
        }
        
        .message-edited {
            font-size: 11px;
            color: rgba(255,255,255,0.5);
            font-style: italic;
            margin-left: 5px;
        }
        
        .message-actions {
            position: absolute;
            top: 10px;
            right: 10px;
            display: none;
            gap: 5px;
            background: rgba(0,0,0,0.7);
            padding: 5px;
            border-radius: 8px;
        }
        
        .message:hover .message-actions {
            display: flex;
        }
        
        .message-action-btn {
            background: none;
            border: none;
            color: white;
            padding: 5px;
            font-size: 12px;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .message-action-btn:hover {
            background: var(--accent-color);
        }
        
        .reactions-container {
            display: flex;
            gap: 8px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .reaction {
            background: var(--secondary-color);
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .reaction:hover {
            background: var(--accent-color);
            transform: scale(1.1);
        }
        
        .input-area {
            padding: 25px;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }
        
        .message-input {
            flex: 1;
            padding: 18px;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 16px;
            resize: none;
            max-height: 120px;
            min-height: 50px;
            transition: all 0.3s ease;
        }
        
        .message-input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 25px rgba(139, 92, 246, 0.3);
        }
        
        .send-btn {
            padding: 18px 25px;
            background: linear-gradient(135deg, var(--accent-color), #7e22ce);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        }
        
        /* Модальные окна */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: var(--card-color);
            padding: 40px;
            border-radius: 20px;
            width: 600px;
            max-width: 90%;
            max-height: 90%;
            overflow-y: auto;
            border: 2px solid var(--accent-color);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            animation: slideIn 0.3s ease-out;
            position: relative;
            z-index: 10001;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .modal-title {
            font-size: 24px;
            font-weight: bold;
            color: var(--text-color);
        }
        
        .close-btn {
            background: none;
            border: none;
            color: #888;
            font-size: 28px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }
        
        .close-btn:hover {
            color: var(--accent-color);
            background: var(--secondary-color);
            transform: scale(1.1);
        }
        
        .section-title {
            color: var(--accent-color);
            margin-bottom: 20px;
            font-weight: bold;
            font-size: 18px;
        }
        
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .avatar-option {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
            border: 3px solid transparent;
            transition: all 0.3s ease;
        }
        
        .avatar-option:hover {
            transform: scale(1.1);
        }
        
        .avatar-option.selected {
            border-color: var(--accent-color);
            transform: scale(1.1);
            box-shadow: 0 0 20px var(--accent-color);
        }
        
        .file-upload {
            margin: 25px 0;
            padding: 25px;
            background: var(--secondary-color);
            border-radius: 15px;
            border: 2px dashed var(--accent-color);
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .file-upload:hover {
            background: var(--accent-color);
        }
        
        .file-upload input[type="file"] {
            width: 100%;
            padding: 10px;
            cursor: pointer;
        }
        
        .theme-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .theme-option {
            padding: 20px;
            border-radius: 15px;
            cursor: pointer;
            border: 3px solid transparent;
            text-align: center;
            transition: all 0.3s ease;
            background: var(--secondary-color);
        }
        
        .theme-option:hover {
            transform: translateY(-5px);
            background: var(--accent-color);
        }
        
        .theme-option.selected {
            border-color: var(--accent-color);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
            background: var(--accent-color);
        }
        
        .theme-preview {
            width: 100%;
            height: 80px;
            border-radius: 10px;
            margin-bottom: 10px;
            border: 2px solid var(--border-color);
        }
        
        .hidden {
            display: none !important;
        }
        
        /* Окно звонка */
        .call-modal {
            z-index: 20000;
        }
        
        .call-content {
            width: 90%;
            max-width: 800px;
            height: 80%;
            display: flex;
            flex-direction: column;
            background: var(--card-color);
            border-radius: 20px;
            overflow: hidden;
            border: 3px solid var(--accent-color);
        }
        
        .call-header {
            padding: 25px;
            background: var(--secondary-color);
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }
        
        .call-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .call-status {
            color: var(--accent-color);
            font-size: 16px;
        }
        
        .call-body {
            flex: 1;
            display: flex;
            position: relative;
            background: #000;
        }
        
        .video-container {
            flex: 1;
            position: relative;
            background: #000;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .video-self {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 200px;
            height: 150px;
            border: 2px solid var(--accent-color);
            border-radius: 10px;
            background: #333;
            z-index: 10;
        }
        
        .video-remote {
            width: 100%;
            height: 100%;
            background: #111;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .video-placeholder {
            text-align: center;
            color: #666;
        }
        
        .video-placeholder .avatar {
            width: 120px;
            height: 120px;
            font-size: 48px;
            margin: 0 auto 20px;
        }
        
        .call-controls {
            padding: 30px;
            background: var(--secondary-color);
            display: flex;
            justify-content: center;
            gap: 20px;
            border-top: 1px solid var(--border-color);
        }
        
        .call-control-btn {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: none;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .call-control-btn:hover {
            transform: scale(1.1);
        }
        
        .call-timer {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 16px;
            z-index: 20;
        }
        
        /* Улучшенные стили для полей ввода в модальных окнах */
        .modal-input {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-color);
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .modal-input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
            transform: translateY(-2px);
        }
        
        /* Кастомизация скроллбара */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--secondary-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #7e22ce;
        }
        
        /* Убираем выделение при клике */
        * {
            -webkit-tap-highlight-color: transparent;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Разрешаем выделение для полей ввода */
        input, textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
        
        /* Новые стили для статусов */
        .status-online {
            color: #10b981;
        }
        
        .status-offline {
            color: #6b7280;
        }
        
        .status-away {
            color: #f59e0b;
        }
        
        /* Стили для уведомлений */
        .notification-toast {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            z-index: 3000;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease-out;
            display: flex;
            align-items: center;
            gap: 10px;
            max-width: 400px;
        }
        
        .notification-toast.error {
            background: #ef4444;
        }
        
        .notification-toast.success {
            background: #10b981;
        }
        
        .notification-toast.warning {
            background: #f59e0b;
        }
        
        /* Анимация для новых сообщений */
        .new-message-indicator {
            text-align: center;
            margin: 10px 0;
            color: var(--accent-color);
            font-size: 12px;
            font-weight: bold;
        }
        
        /* Стили для системных сообщений */
        .system-message {
            text-align: center;
            color: #888;
            font-style: italic;
            margin: 10px 0;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <!-- Главный экран выбора -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Фиолетовый чат с максимальной кастомизацией</div>
            
            <button class="btn pulse" id="startChatBtn">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-admin pulse" id="adminAccessBtn">
                <span>👑 Войти как администратор</span>
            </button>
        </div>
    </div>

    <!-- Экран регистрации -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Создание аккаунта</div>
            
            <input type="text" id="regName" class="input-field" placeholder="💁 Ваше имя" required>
            <input type="text" id="regUsername" class="input-field" placeholder="👤 @username (не обязательно)">
            <div class="optional">✨ Юзернейм не обязателен. Если не указать, будет сгенерирован автоматически</div>
            
            <button class="btn pulse" id="registerBtn">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" id="backToMainBtn">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
            <div id="registerSuccess" class="success"></div>
        </div>
    </div>

    <!-- Экран входа админа -->
    <div id="adminScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Панель администратора</div>
            
            <input type="password" id="adminPass" class="input-field" placeholder="🔒 Введите пароль администратора">
            
            <button class="btn btn-admin pulse" id="adminLoginBtn">⚡ Войти</button>
            
            <button class="btn" id="backToMainFromAdminBtn">
                <span>← Назад</span>
            </button>
            
            <div id="adminError" class="error"></div>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <!-- ... остальная HTML структура без изменений ... -->
    </div>

    <!-- Все модальные окна остаются без изменений -->

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        // Глобальные переменные
        let socket = null;
        let currentUser = null;
        let currentChat = "news";
        let isAdmin = false;
        let isModerator = false;

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            setupEventListeners();
            connectSocket();
            checkAutoLogin();
        });

        function setupEventListeners() {
            // Главный экран
            document.getElementById('startChatBtn').addEventListener('click', showRegisterScreen);
            document.getElementById('adminAccessBtn').addEventListener('click', showAdminScreen);
            
            // Кнопки навигации
            document.getElementById('backToMainBtn').addEventListener('click', showMainScreen);
            document.getElementById('backToMainFromAdminBtn').addEventListener('click', showMainScreen);
            
            // Кнопки авторизации
            document.getElementById('registerBtn').addEventListener('click', register);
            document.getElementById('adminLoginBtn').addEventListener('click', adminLogin);
            
            // Остальные обработчики...
            document.getElementById('sendBtn').addEventListener('click', sendMessage);
            document.getElementById('logoutBtn').addEventListener('click', logout);
        }

        function connectSocket() {
            socket = io();
            
            socket.on('connect', function() {
                console.log("✅ Подключено к серверу");
            });
            
            socket.on('registration_success', function(user) {
                console.log("✅ Регистрация успешна:", user);
                currentUser = user;
                localStorage.setItem('dlcurrentUser', JSON.stringify(user));
                showMainApp();
            });
            
            socket.on('registration_error', function(data) {
                document.getElementById('registerError').textContent = data.message;
                document.getElementById('registerBtn').disabled = false;
                document.getElementById('registerBtn').innerHTML = '<span>🚀 Начать общение</span>';
            });
            
            socket.on('private_message', function(data) {
                console.log("📨 Получено сообщение:", data);
                if (currentChat === data.chat_id) {
                    addMessageToChat(data);
                }
            });
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    showMainApp();
                } catch (e) {
                    console.log("❌ Ошибка автоматического входа:", e);
                    localStorage.removeItem('dlcurrentUser');
                }
            }
        }

        function showMainScreen() {
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
        }

        function showRegisterScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            // Инициализация интерфейса
            if (currentUser) {
                document.getElementById('userName').textContent = currentUser.name;
                document.getElementById('userUsername').textContent = currentUser.username;
            }
            
            // Загрузка начальных данных
            socket.emit('get_all_users');
            socket.emit('get_news_messages');
        }

        function register() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            document.getElementById('registerBtn').disabled = true;
            document.getElementById('registerBtn').innerHTML = '<span>⏳ Регистрация...</span>';
            document.getElementById('registerError').textContent = '';
            
            socket.emit('register', {
                name: name,
                username: username || undefined
            });
        }

        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    is_admin: true
                };
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
        }

        function logout() {
            currentUser = null;
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const text = messageInput.value.trim();
            
            if (!text || !currentUser) return;
            
            socket.emit('send_private_message', {
                text: text,
                chat_id: currentChat
            });
            
            messageInput.value = '';
        }

        function addMessageToChat(message) {
            const container = document.getElementById('messagesContainer');
            const messageDiv = document.createElement('div');
            
            const isOwnMessage = message.sender_id === currentUser?.id;
            const messageTime = new Date(message.timestamp).toLocaleTimeString('ru-RU', {
                hour: '2-digit',
                minute: '2-digit'
            });
            
            messageDiv.className = `message ${isOwnMessage ? 'message-out' : 'message-in'}`;
            messageDiv.innerHTML = `
                ${!isOwnMessage ? `<div class="message-sender">${message.sender_name}</div>` : ''}
                <div class="message-text">${message.text}</div>
                <div class="message-time">${messageTime}</div>
            `;
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }

        // Остальные функции...
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/user_avatars/<filename>')
def serve_avatar(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def generate_user_id():
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

def generate_message_id():
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

@socketio.on('connect')
def handle_connect():
    print(f"✅ Клиент подключен: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = user_sessions.get(request.sid)
    if user_id:
        print(f"❌ Пользователь отключен: {user_id}")
        del user_sessions[request.sid]

@socketio.on('register')
def handle_register(data):
    """Регистрация нового пользователя - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    try:
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        
        print(f"📝 Попытка регистрации: name={name}, username={username}")
        
        if not name:
            emit('registration_error', {'message': 'Введите имя'})
            return
        
        # Генерируем user_id
        user_id = generate_user_id()
        
        # Если username не указан, генерируем автоматически
        if not username:
            username = f"user{random.randint(10000, 99999)}"
        else:
            # Проверяем уникальность username
            for user in users_db.values():
                if user.get('username') == username:
                    emit('registration_error', {'message': 'Этот юзернейм уже занят'})
                    return
        
        # Создаем пользователя
        user_data = {
            'id': user_id,
            'name': name,
            'username': username,
            'avatar': '👤',
            'avatar_bg': '#6b21a8',
            'registered_at': datetime.datetime.now().isoformat(),
            'is_banned': False,
            'is_muted': False,
            'is_moderator': False
        }
        
        # Сохраняем в базу
        users_db[user_id] = user_data
        user_sessions[request.sid] = user_id
        
        # Инициализируем непрочитанные сообщения
        unread_messages[user_id] = {}
        
        # Сохраняем данные
        save_user_data()
        
        print(f"👤 Новый пользователь: {name} (@{username})")
        
        # Отправляем успешный ответ
        emit('registration_success', user_data)
        
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")
        emit('registration_error', {'message': 'Ошибка сервера при регистрации'})

@socketio.on('send_private_message')
def handle_send_private_message(data):
    """Отправка приватного сообщения"""
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    text = data.get('text', '').strip()
    target_id = data.get('chat_id')
    
    if not text or not target_id:
        return
    
    # Создаем сообщение
    message_id = generate_message_id()
    sender_name = users_db[user_id]['name'] if user_id in users_db else 'Неизвестный'
    
    message = {
        'id': message_id,
        'text': text,
        'sender_id': user_id,
        'sender_name': sender_name,
        'timestamp': datetime.datetime.now().isoformat(),
        'edited': False,
        'reactions': {}
    }
    
    # Сохраняем сообщение
    if user_id not in messages_db:
        messages_db[user_id] = {}
    if target_id not in messages_db[user_id]:
        messages_db[user_id][target_id] = []
    messages_db[user_id][target_id].append(message)
    
    save_user_data()
    
    # Отправляем сообщение отправителю
    emit('private_message', {**message, 'chat_id': target_id})
    
    # Отправляем получателю, если он онлайн
    for sid, uid in user_sessions.items():
        if uid == target_id:
            emit('private_message', {**message, 'chat_id': user_id}, room=sid)
    
    print(f"📨 Сообщение от {user_id} к {target_id}")

@socketio.on('get_all_users')
def handle_get_all_users():
    """Получение списка всех пользователей"""
    users_list = []
    
    # Добавляем обычных пользователей
    for user_id, user_data in users_db.items():
        if user_id != 'admin':
            users_list.append(user_data)
    
    # Добавляем админа
    users_list.append({
        'id': 'admin',
        'name': 'Администратор',
        'username': '@admin',
        'avatar': '👑',
        'avatar_bg': '#dc2626',
        'is_admin': True
    })
    
    emit('all_users', users_list)

@socketio.on('get_news_messages')
def handle_get_news_messages():
    """Получение новостей"""
    # Для демонстрации создаем несколько тестовых новостей
    if not news_messages:
        news_messages.extend([
            {
                'id': '1',
                'text': 'Добро пожаловать в DLtrollex! 🎉',
                'sender_id': 'admin',
                'sender_name': 'Администратор',
                'timestamp': datetime.datetime.now().isoformat(),
                'edited': False
            },
            {
                'id': '2', 
                'text': 'Это фиолетовый мессенджер с максимальной кастомизацией! 💜',
                'sender_id': 'admin',
                'sender_name': 'Администратор', 
                'timestamp': datetime.datetime.now().isoformat(),
                'edited': False
            }
        ])
    
    emit('all_news_messages', news_messages)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Запуск DLtrollex с исправленной регистрацией...")
    print(f"💜 Доступно по адресу: http://localhost:{port}")
    print("🎯 Анимации кнопок 'Войти' и 'Войти как администратор' восстановлены!")
    print("🐛 Баги регистрации исправлены!")
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
