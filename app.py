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
            
            <button class="btn btn-admin" id="adminAccessBtn">
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
            
            <button class="btn" id="registerBtn">
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
            
            <button class="btn btn-admin" id="adminLoginBtn">⚡ Войти</button>
            
            <button class="btn" id="backToMainFromAdminBtn">
                <span>← Назад</span>
            </button>
            
            <div id="adminError" class="error"></div>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <div class="chat-container">
            <div class="sidebar">
                <div class="header">
                    <div class="logo glowing-logo" style="font-size: 24px;">💜 DLtrollex</div>
                    <div class="header-actions">
                        <button class="header-btn" id="createGroupBtn" title="Создать группу">👥</button>
                        <button class="header-btn" id="themeBtn" title="Сменить тему">🎨</button>
                        <button class="header-btn" id="settingsBtn" title="Настройки"⚙️</button>
                        <button class="header-btn" id="notificationsBtn" title="Уведомления">
                            🔔
                            <div class="notification-badge" id="globalNotificationBadge" style="display: none;">0</div>
                        </button>
                        <button class="header-btn" id="moderationBtn" title="Модерация" style="display: none;">🛡️</button>
                        <button class="header-btn" id="logoutBtn" title="Выйти">🚪</button>
                    </div>
                </div>
                
                <div class="user-info" id="profileSection">
                    <div class="avatar" id="userAvatar">👤</div>
                    <div>
                        <div id="userName">Пользователь</div>
                        <div style="color: var(--accent-color); font-size: 13px;" id="userUsername">@username</div>
                        <div style="color: #10b981; font-size: 11px;" id="userStatus">● онлайн</div>
                    </div>
                </div>
                
                <div class="search-container">
                    <input type="text" class="search-input" id="searchInput" placeholder="🔍 Поиск по юзернейму...">
                </div>
                
                <div class="chats" id="chatsList">
                    <div class="chat-item active" data-chat="news">
                        <div class="chat-icon">📢</div>
                        <div class="chat-info">
                            <div class="chat-name">Новости DLtrollex</div>
                            <div class="chat-last-message">Официальные объявления</div>
                        </div>
                    </div>
                    <div class="chat-item" data-chat="favorites">
                        <div class="chat-icon">⭐</div>
                        <div class="chat-info">
                            <div class="chat-name">Избранное</div>
                            <div class="chat-last-message">Ваши личные заметки</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="chat-area">
                <div class="chat-header">
                    <div class="chat-info">
                        <div id="chatTitle" style="font-size: 20px; font-weight: bold;">📢 Новости DLtrollex</div>
                        <div style="color: var(--accent-color); font-size: 14px;" id="chatStatus">Официальный канал</div>
                    </div>
                    <div class="chat-actions">
                        <button class="header-btn" id="callBtn" title="Позвонить" style="display: none;">📞</button>
                        <button class="header-btn" id="videoCallBtn" title="Видеозвонок" style="display: none;">📹</button>
                        <button class="header-btn" id="searchChatBtn" title="Поиск в чате">🔍</button>
                        <button class="header-btn" id="userInfoBtn" title="Информация о чате">ℹ️</button>
                        <button class="header-btn" id="profileBtn" title="Профиль">👤</button>
                    </div>
                </div>
                
                <div class="messages" id="messagesContainer">
                    <div style="text-align: center; color: #666; margin-top: 100px;">
                        <div style="font-size: 64px;" class="floating">💜</div>
                        <p style="margin-top: 20px; font-size: 18px;">Добро пожаловать в DLtrollex!</p>
                        <p style="color: #888; margin-top: 10px;">Начните общение в выбранном чате</p>
                    </div>
                </div>
                
                <div class="input-area">
                    <textarea class="message-input" id="messageInput" placeholder="💬 Введите ваше сообщение..." rows="1"></textarea>
                    <button class="send-btn" id="sendBtn">
                        <span>Отправить</span>
                        <span>⚡</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно профиля -->
    <div id="profileModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">🎨 Настройки профиля</div>
                <button class="close-btn" id="closeProfileBtn">×</button>
            </div>
            
            <div style="text-align: center; margin-bottom: 30px;">
                <div class="avatar" id="modalAvatarPreview" style="width: 100px; height: 100px; margin: 0 auto 20px; font-size: 40px; border: 4px solid var(--accent-color);"></div>
                <input type="text" id="editName" class="modal-input" placeholder="💁 Ваше имя" style="text-align: center; font-size: 18px;">
                <input type="text" id="editUsername" class="modal-input" placeholder="👤 @username" style="text-align: center; margin-top: 15px;">
            </div>
            
            <div class="section-title">🎭 Выберите аватарку:</div>
            <div class="avatar-grid" id="avatarSelection">
                <!-- Аватарки будут добавлены через JS -->
            </div>
            
            <div class="file-upload">
                <div class="section-title">📁 Или загрузите свою аватарку:</div>
                <input type="file" id="avatarUpload" accept="image/*" style="margin: 15px 0; color: var(--text-color);">
                <div style="color: #888; font-size: 13px;">JPG, PNG или GIF (макс. 2MB)</div>
            </div>
            
            <div class="section-title">🔔 Настройки уведомлений:</div>
            <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="checkbox" id="notificationsEnabled" checked>
                    <span>Включить уведомления о новых сообщениях</span>
                </label>
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="checkbox" id="soundEnabled" checked>
                    <span>Включить звуковые уведомления</span>
                </label>
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="checkbox" id="onlineStatusEnabled" checked>
                    <span>Показывать статус "онлайн"</span>
                </label>
            </div>
            
            <button class="btn" id="saveProfileBtn" style="margin-top: 20px;">
                <span>💾 Сохранить изменения</span>
            </button>
        </div>
    </div>

    <!-- Модальное окно тем -->
    <div id="themeModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">🎨 Выбор темы оформления</div>
                <button class="close-btn" id="closeThemeBtn">×</button>
            </div>
            
            <div class="section-title">🌈 Выберите тему:</div>
            <div class="theme-grid" id="themeSelection">
                <!-- Темы будут добавлены через JS -->
            </div>
            
            <button class="btn" id="saveThemeBtn" style="margin-top: 20px;">
                <span>💾 Применить тему</span>
            </button>
        </div>
    </div>

    <!-- Модальное окно уведомлений -->
    <div id="notificationsModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">🔔 Уведомления</div>
                <button class="close-btn" id="closeNotificationsBtn">×</button>
            </div>
            
            <div class="section-title">📫 Непрочитанные сообщения:</div>
            <div id="notificationsList" style="max-height: 300px; overflow-y: auto;">
                <!-- Список уведомлений будет здесь -->
            </div>
            
            <div style="margin-top: 20px;">
                <button class="btn" id="clearAllNotificationsBtn">
                    <span>🗑️ Очистить все уведомления</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Модальное окно информации о чате -->
    <div id="chatInfoModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">ℹ️ Информация о чате</div>
                <button class="close-btn" id="closeChatInfoBtn">×</button>
            </div>
            <div id="chatInfoContent">
                <!-- Информация будет загружена здесь -->
            </div>
        </div>
    </div>

    <!-- Модальное окно модерации -->
    <div id="moderationModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">🛡️ Панель модерации</div>
                <button class="close-btn" id="closeModerationBtn">×</button>
            </div>
            
            <div class="section-title">👥 Управление пользователями</div>
            <div style="margin-bottom: 20px;">
                <select id="userSelect" class="modal-input" style="width: 100%; margin-bottom: 10px;">
                    <option value="">Выберите пользователя</option>
                </select>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button class="btn" id="banUserBtn" style="flex: 1; min-width: 120px;">🚫 Забанить</button>
                    <button class="btn" id="unbanUserBtn" style="flex: 1; min-width: 120px;">✅ Разбанить</button>
                    <button class="btn" id="muteUserBtn" style="flex: 1; min-width: 120px;">🔇 Заглушить</button>
                    <button class="btn" id="unmuteUserBtn" style="flex: 1; min-width: 120px;">🔊 Разглушить</button>
                    <button class="btn" id="makeModeratorBtn" style="flex: 1; min-width: 120px;">👑 Сделать модератором</button>
                    <button class="btn" id="viewUserInfoBtn" style="flex: 1; min-width: 120px;">📊 Инфо</button>
                </div>
            </div>
            
            <div class="section-title">📊 Статистика системы</div>
            <div id="moderationStats" style="background: var(--secondary-color); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <!-- Статистика будет загружена здесь -->
            </div>
            
            <div class="section-title">🗑️ Управление сообщениями</div>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="messageIdInput" class="modal-input" placeholder="ID сообщения" style="flex: 1;">
                <button class="btn" id="deleteMessageBtn">🗑️ Удалить</button>
            </div>
            
            <div style="margin-top: 20px;">
                <button class="btn" id="clearAllDataBtn" style="background: linear-gradient(135deg, #dc2626, #b91c1c);">
                    <span>💥 Очистить все данные</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Окно информации о пользователе -->
    <div id="userInfoModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">📊 Информация о пользователе</div>
                <button class="close-btn" id="closeUserInfoBtn">×</button>
            </div>
            <div id="userInfoContent">
                <!-- Информация будет загружена здесь -->
            </div>
        </div>
    </div>

    <!-- Окно входящего звонка -->
    <div id="incomingCallModal" class="modal call-modal hidden">
        <div class="call-content">
            <div class="call-header ringing">
                <div class="call-title">📞 Входящий звонок</div>
                <div class="call-status" id="incomingCallerInfo">...</div>
            </div>
            <div class="call-body">
                <div class="video-remote">
                    <div class="video-placeholder">
                        <div class="avatar" id="incomingCallAvatar">👤</div>
                        <div id="incomingCallName">Пользователь</div>
                    </div>
                </div>
            </div>
            <div class="call-controls">
                <button class="call-control-btn btn-end-call" id="declineCallBtn">
                    <span>❌</span>
                </button>
                <button class="call-control-btn btn-call" id="acceptCallBtn">
                    <span>📞</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Окно исходящего звонка -->
    <div id="outgoingCallModal" class="modal call-modal hidden">
        <div class="call-content">
            <div class="call-header">
                <div class="call-title">📞 Исходящий звонок</div>
                <div class="call-status" id="outgoingCallStatus">Звонок...</div>
            </div>
            <div class="call-body">
                <div class="video-remote">
                    <div class="video-placeholder">
                        <div class="avatar" id="outgoingCallAvatar">👤</div>
                        <div id="outgoingCallName">Пользователь</div>
                    </div>
                </div>
            </div>
            <div class="call-controls">
                <button class="call-control-btn btn-end-call" id="cancelCallBtn">
                    <span>❌</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Окно активного звонка -->
    <div id="activeCallModal" class="modal call-modal hidden">
        <div class="call-content">
            <div class="call-header">
                <div class="call-title">📞 Звонок</div>
                <div class="call-status" id="activeCallStatus">Соединено</div>
                <div class="call-timer" id="callTimer">00:00</div>
            </div>
            <div class="call-body">
                <div class="video-remote" id="remoteVideoContainer">
                    <div class="video-placeholder">
                        <div class="avatar" id="activeCallAvatar">👤</div>
                        <div id="activeCallName">Пользователь</div>
                    </div>
                </div>
                <div class="video-self" id="localVideoContainer">
                    <video id="localVideo" autoplay muted playsinline style="width: 100%; height: 100%; border-radius: 10px;"></video>
                </div>
            </div>
            <div class="call-controls">
                <button class="call-control-btn" id="muteBtn" title="Микрофон">
                    <span>🎤</span>
                </button>
                <button class="call-control-btn" id="videoBtn" title="Камера">
                    <span>📹</span>
                </button>
                <button class="call-control-btn btn-end-call" id="endCallBtn">
                    <span>❌</span>
                </button>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        // Глобальные переменные
        let socket = null;
        let currentUser = null;
        let currentChat = "news";
        let isAdmin = false;
        let isModerator = false;
        let selectedAvatar = {emoji: "👤", bg: "#6b21a8"};
        let uploadedAvatar = null;
        let currentTheme = "dark_purple";
        let allUsers = [];
        let groups = [];
        let currentMessages = [];
        let replyingTo = null;
        let editingMessage = null;
        let unreadMessages = {};
        let onlineUsers = new Set();
        let userSettings = {
            notifications: true,
            sound: true,
            onlineStatus: true
        };

        // WebRTC переменные
        let localStream = null;
        let remoteStream = null;
        let peerConnection = null;
        let currentCall = null;
        let callStartTime = null;
        let callTimerInterval = null;
        let isMuted = false;
        let isVideoOff = false;
        let currentCallId = null;

        const defaultAvatars = ''' + str(DEFAULT_AVATARS) + ''';
        const themes = ''' + str(THEMES) + ''';
        const reactions = ''' + str(REACTIONS) + ''';

        // WebRTC конфигурация (STUN серверы)
        const rtcConfig = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' },
                { urls: 'stun:stun2.l.google.com:19302' }
            ]
        };

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            checkAutoLogin();
            setupEventListeners();
            connectSocket();
            loadTheme();
            loadUserSettings();
            initThemes();
            initAvatars();
        });

        // Инициализация тем
        function initThemes() {
            const themeGrid = document.getElementById('themeSelection');
            themeGrid.innerHTML = '';
            
            for (const [themeId, theme] of Object.entries(themes)) {
                const themeOption = document.createElement('div');
                themeOption.className = `theme-option ${currentTheme === themeId ? 'selected' : ''}`;
                themeOption.setAttribute('data-theme', themeId);
                themeOption.innerHTML = `
                    <div class="theme-preview" style="background: ${theme.bg}; border-color: ${theme.border || theme.accent}"></div>
                    <div style="font-weight: bold; margin-bottom: 5px;">${theme.name}</div>
                    <div style="font-size: 12px; color: #888;">${themeId}</div>
                `;
                themeOption.onclick = () => selectTheme(themeId);
                themeGrid.appendChild(themeOption);
            }
        }

        // Инициализация аватарок
        function initAvatars() {
            const avatarGrid = document.getElementById('avatarSelection');
            avatarGrid.innerHTML = '';
            
            defaultAvatars.forEach((avatar, index) => {
                const avatarOption = document.createElement('div');
                avatarOption.className = `avatar-option ${selectedAvatar.emoji === avatar.emoji ? 'selected' : ''}`;
                avatarOption.style.background = avatar.bg;
                avatarOption.textContent = avatar.emoji;
                avatarOption.onclick = () => {
                    selectedAvatar = avatar;
                    document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
                    avatarOption.classList.add('selected');
                    
                    // Обновляем превью
                    const modalAvatar = document.getElementById('modalAvatarPreview');
                    modalAvatar.textContent = avatar.emoji;
                    modalAvatar.style.background = avatar.bg;
                    modalAvatar.style.backgroundImage = 'none';
                    uploadedAvatar = null;
                };
                avatarGrid.appendChild(avatarOption);
            });
        }
        
        function selectTheme(themeId) {
            document.querySelectorAll('.theme-option').forEach(opt => opt.classList.remove('selected'));
            document.querySelector(`[data-theme="${themeId}"]`).classList.add('selected');
            currentTheme = themeId;
        }

        // Проверка автоматического входа
        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            const savedSettings = localStorage.getItem('dluserSettings');
            
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    isAdmin = currentUser.id === 'admin';
                    isModerator = currentUser.id === 'admin' || currentUser.isModerator;
                    console.log("🔑 Автоматический вход:", currentUser);
                    showMainApp();
                } catch (e) {
                    console.log("❌ Ошибка автоматического входа:", e);
                    localStorage.removeItem('dlcurrentUser');
                }
            }
            
            if (savedSettings) {
                try {
                    userSettings = {...userSettings, ...JSON.parse(savedSettings)};
                } catch (e) {
                    console.log("❌ Ошибка загрузки настроек:", e);
                }
            }
        }

        // Загрузка настроек пользователя
        function loadUserSettings() {
            document.getElementById('notificationsEnabled').checked = userSettings.notifications;
            document.getElementById('soundEnabled').checked = userSettings.sound;
            document.getElementById('onlineStatusEnabled').checked = userSettings.onlineStatus;
        }

        // Сохранение настроек пользователя
        function saveUserSettings() {
            userSettings.notifications = document.getElementById('notificationsEnabled').checked;
            userSettings.sound = document.getElementById('soundEnabled').checked;
            userSettings.onlineStatus = document.getElementById('onlineStatusEnabled').checked;
            
            localStorage.setItem('dluserSettings', JSON.stringify(userSettings));
            
            if (socket && currentUser) {
                socket.emit('update_online_status', {
                    is_online: userSettings.onlineStatus,
                    user_id: currentUser.id
                });
            }
        }

        // Настройка всех обработчиков событий
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
            
            // Кнопки чата
            document.getElementById('sendBtn').addEventListener('click', sendMessage);
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            // Кнопки интерфейса
            document.getElementById('profileBtn').addEventListener('click', showProfileModal);
            document.getElementById('themeBtn').addEventListener('click', showThemeModal);
            document.getElementById('notificationsBtn').addEventListener('click', showNotificationsModal);
            document.getElementById('moderationBtn').addEventListener('click', showModerationModal);
            document.getElementById('logoutBtn').addEventListener('click', logout);
            document.getElementById('createGroupBtn').addEventListener('click', showCreateGroupModal);
            document.getElementById('searchChatBtn').addEventListener('click', showSearchChatModal);
            document.getElementById('userInfoBtn').addEventListener('click', showChatInfoModal);
            document.getElementById('profileSection').addEventListener('click', showProfileModal);
            document.getElementById('settingsBtn').addEventListener('click', showProfileModal);
            
            // Кнопки звонков
            document.getElementById('callBtn').addEventListener('click', startAudioCall);
            document.getElementById('videoCallBtn').addEventListener('click', startVideoCall);
            
            // Поиск
            document.getElementById('searchInput').addEventListener('input', searchUsers);
            
            // Модальные окна
            document.getElementById('closeProfileBtn').addEventListener('click', hideProfileModal);
            document.getElementById('closeThemeBtn').addEventListener('click', hideThemeModal);
            document.getElementById('closeNotificationsBtn').addEventListener('click', hideNotificationsModal);
            document.getElementById('closeModerationBtn').addEventListener('click', hideModerationModal);
            document.getElementById('closeUserInfoBtn').addEventListener('click', hideUserInfoModal);
            document.getElementById('closeChatInfoBtn').addEventListener('click', hideChatInfoModal);
            
            document.getElementById('saveProfileBtn').addEventListener('click', saveProfile);
            document.getElementById('saveThemeBtn').addEventListener('click', saveTheme);
            document.getElementById('clearAllNotificationsBtn').addEventListener('click', clearAllNotifications);
            
            // Загрузка аватарки
            document.getElementById('avatarUpload').addEventListener('change', handleAvatarUpload);
            
            // Обработчики чатов
            document.getElementById('chatsList').addEventListener('click', function(e) {
                const chatItem = e.target.closest('.chat-item');
                if (chatItem) {
                    document.querySelectorAll('.chat-item').forEach(item => item.classList.remove('active'));
                    chatItem.classList.add('active');
                    const chatType = chatItem.getAttribute('data-chat');
                    selectChat(chatType);
                }
            });

            // Модерация
            document.getElementById('banUserBtn').addEventListener('click', banUser);
            document.getElementById('unbanUserBtn').addEventListener('click', unbanUser);
            document.getElementById('muteUserBtn').addEventListener('click', muteUser);
            document.getElementById('unmuteUserBtn').addEventListener('click', unmuteUser);
            document.getElementById('makeModeratorBtn').addEventListener('click', makeModerator);
            document.getElementById('viewUserInfoBtn').addEventListener('click', viewUserInfo);
            document.getElementById('deleteMessageBtn').addEventListener('click', deleteMessageById);
            document.getElementById('clearAllDataBtn').addEventListener('click', clearAllData);

            // Обработчик клика по фону модального окна для закрытия
            document.addEventListener('click', function(e) {
                if (e.target.classList.contains('modal')) {
                    e.target.classList.add('hidden');
                    // При закрытии модального окна звонка - завершаем звонок
                    if (e.target.id === 'activeCallModal' || e.target.id === 'outgoingCallModal' || e.target.id === 'incomingCallModal') {
                        if (currentCall) {
                            endCall();
                        }
                    }
                }
            });

            // Предотвращаем закрытие при клике на содержимое модального окна
            document.querySelectorAll('.modal-content').forEach(content => {
                content.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });

            // Обработчики звонков
            document.getElementById('acceptCallBtn').addEventListener('click', acceptCall);
            document.getElementById('declineCallBtn').addEventListener('click', declineCall);
            document.getElementById('cancelCallBtn').addEventListener('click', cancelCall);
            document.getElementById('endCallBtn').addEventListener('click', endCall);
            document.getElementById('muteBtn').addEventListener('click', toggleMute);
            document.getElementById('videoBtn').addEventListener('click', toggleVideo);

            // Обработчик изменения настроек
            document.getElementById('notificationsEnabled').addEventListener('change', saveUserSettings);
            document.getElementById('soundEnabled').addEventListener('change', saveUserSettings);
            document.getElementById('onlineStatusEnabled').addEventListener('change', saveUserSettings);

            // Обработчик видимости страницы для уведомлений
            document.addEventListener('visibilitychange', function() {
                if (document.visibilityState === 'visible' && currentChat) {
                    // Помечаем сообщения как прочитанные при возвращении на вкладку
                    markMessagesAsRead(currentChat);
                }
            });
        }

        // Подключение к серверу
        function connectSocket() {
            socket = io();
            
            socket.on('connect', function() {
                console.log("✅ Подключено к серверу");
                if (currentUser) {
                    socket.emit('restore_session', {user_id: currentUser.id});
                    socket.emit('get_all_users');
                    socket.emit('get_unread_messages');
                    socket.emit('get_online_users');
                    
                    // Обновляем онлайн статус
                    if (userSettings.onlineStatus) {
                        socket.emit('update_online_status', {
                            is_online: true,
                            user_id: currentUser.id
                        });
                    }
                    
                    if (currentChat === 'news') {
                        loadNews();
                    } else if (currentChat === 'favorites') {
                        loadFavorites();
                    }
                }
            });
            
            socket.on('registration_success', function(user) {
                console.log("✅ Регистрация успешна:", user);
                currentUser = user;
                localStorage.setItem('dlcurrentUser', JSON.stringify(user));
                showMainApp();
                socket.emit('get_all_users');
                
                // Обновляем онлайн статус
                if (userSettings.onlineStatus) {
                    socket.emit('update_online_status', {
                        is_online: true,
                        user_id: currentUser.id
                    });
                }
            });
            
            socket.on('registration_error', function(message) {
                document.getElementById('registerError').textContent = message;
                document.getElementById('registerBtn').disabled = false;
                document.getElementById('registerBtn').innerHTML = '<span>🚀 Начать общение</span>';
            });
            
            socket.on('private_message', function(data) {
                console.log("📨 Получено сообщение:", data);
                
                // Добавляем в историю сообщений
                if (currentChat === data.chat_id || currentChat === data.sender_id) {
                    addMessageToChat(data);
                    // Помечаем как прочитанное если открыт этот чат
                    if (currentChat === data.sender_id) {
                        markMessagesAsRead(data.sender_id);
                    }
                } else {
                    // Добавляем непрочитанное сообщение
                    addUnreadMessage(data);
                    
                    // Показываем уведомление
                    if (userSettings.notifications) {
                        showMessageNotification(data);
                    }
                }
            });
            
            socket.on('news_message', function(data) {
                if (currentChat === 'news') {
                    addMessageToChat(data);
                } else {
                    addUnreadMessage(data, 'news');
                }
            });
            
            socket.on('profile_updated', function(user) {
                currentUser = user;
                localStorage.setItem('dlcurrentUser', JSON.stringify(user));
                updateUserInfo();
                showNotification('Профиль обновлен', 'success');
            });
            
            socket.on('all_news_messages', function(messages) {
                displayMessages(messages);
            });
            
            socket.on('all_users', function(users) {
                console.log("👥 Получены пользователи:", users);
                allUsers = users.filter(user => user.id !== currentUser?.id && user.id !== 'admin');
                updateUsersList();
                updateModerationUserList();
            });
            
            socket.on('favorites_data', function(data) {
                displayFavorites(data);
            });
            
            socket.on('user_data', function(data) {
                console.log("📂 Данные пользователя загружены:", data);
            });
            
            socket.on('chat_messages', function(messages) {
                console.log("💬 Получены сообщения:", messages);
                displayMessages(messages);
            });
            
            socket.on('message_updated', function(message) {
                updateMessage(message);
            });
            
            socket.on('message_deleted', function(data) {
                deleteMessageFromUI(data.message_id);
            });
            
            socket.on('reaction_added', function(data) {
                updateMessageReactions(data);
            });
            
            socket.on('session_restored', function(data) {
                console.log("🔑 Сессия восстановлена:", data);
            });

            socket.on('user_banned', function(data) {
                showNotification(`Пользователь ${data.username} забанен`, 'warning');
                if (data.user_id === currentUser.id) {
                    alert('Вы были забанены администратором');
                    logout();
                }
            });

            socket.on('user_unbanned', function(data) {
                showNotification(`Пользователь ${data.username} разбанен`, 'success');
            });

            socket.on('user_muted', function(data) {
                showNotification(`Пользователь ${data.username} заглушен`, 'warning');
            });

            socket.on('user_unmuted', function(data) {
                showNotification(`Пользователь ${data.username} разглушен`, 'success');
            });

            socket.on('moderator_added', function(data) {
                showNotification(`Пользователь ${data.username} стал модератором`, 'success');
                if (data.user_id === currentUser.id) {
                    isModerator = true;
                    document.getElementById('moderationBtn').style.display = 'flex';
                }
            });

            socket.on('moderation_stats', function(stats) {
                displayModerationStats(stats);
            });

            socket.on('user_info', function(info) {
                displayUserInfo(info);
            });

            socket.on('unread_messages', function(data) {
                console.log("📫 Получены непрочитанные сообщения:", data);
                unreadMessages = data.unread_messages || {};
                updateUnreadBadges();
                updateNotificationsList();
            });

            socket.on('online_users', function(data) {
                console.log("👥 Онлайн пользователи:", data.users);
                onlineUsers = new Set(data.users);
                updateOnlineStatuses();
            });

            socket.on('user_online', function(data) {
                onlineUsers.add(data.user_id);
                updateOnlineStatuses();
                showNotification(`${data.username} сейчас онлайн`, 'success');
            });

            socket.on('user_offline', function(data) {
                onlineUsers.delete(data.user_id);
                updateOnlineStatuses();
                showNotification(`${data.username} вышел из сети`, 'warning');
            });

            socket.on('messages_read', function(data) {
                // Обновляем счетчик непрочитанных сообщений
                if (unreadMessages[data.chat_id]) {
                    unreadMessages[data.chat_id] = 0;
                    updateUnreadBadges();
                }
            });

            // WebRTC события
            socket.on('incoming_call', function(data) {
                handleIncomingCall(data);
            });

            socket.on('call_accepted', function(data) {
                handleCallAccepted(data);
            });

            socket.on('call_rejected', function(data) {
                handleCallRejected(data);
            });

            socket.on('call_ended', function(data) {
                handleCallEnded(data);
            });

            socket.on('webrtc_offer', function(data) {
                handleWebRTCOffer(data);
            });

            socket.on('webrtc_answer', function(data) {
                handleWebRTCAnswer(data);
            });

            socket.on('webrtc_ice_candidate', function(data) {
                handleWebRTCIceCandidate(data);
            });

            socket.on('disconnect', function() {
                console.log("❌ Отключено от сервера");
                showNotification('Потеряно соединение с сервером', 'error');
            });

            socket.on('reconnect', function() {
                console.log("🔁 Переподключено к серверу");
                showNotification('Соединение восстановлено', 'success');
                
                // Восстанавливаем сессию
                if (currentUser) {
                    socket.emit('restore_session', {user_id: currentUser.id});
                    socket.emit('get_all_users');
                    socket.emit('get_unread_messages');
                }
            });
        }

        // ==================== НОВЫЕ ФУНКЦИИ ДЛЯ УВЕДОМЛЕНИЙ ====================

        function addUnreadMessage(message, chatId = null) {
            const targetChatId = chatId || message.sender_id;
            
            if (!unreadMessages[targetChatId]) {
                unreadMessages[targetChatId] = 0;
            }
            unreadMessages[targetChatId]++;
            
            updateUnreadBadges();
            updateNotificationsList();
            
            // Сохраняем на сервере
            if (socket) {
                socket.emit('update_unread_count', {
                    chat_id: targetChatId,
                    count: unreadMessages[targetChatId]
                });
            }
        }

        function markMessagesAsRead(chatId) {
            if (unreadMessages[chatId] && unreadMessages[chatId] > 0) {
                unreadMessages[chatId] = 0;
                updateUnreadBadges();
                updateNotificationsList();
                
                // Сообщаем серверу о прочтении
                if (socket) {
                    socket.emit('mark_messages_read', {chat_id: chatId});
                }
            }
        }

        function updateUnreadBadges() {
            let totalUnread = 0;
            
            // Обновляем бейджи в списке чатов
            document.querySelectorAll('.chat-item').forEach(chatItem => {
                const chatId = chatItem.getAttribute('data-chat');
                const unreadBadge = chatItem.querySelector('.unread-badge');
                
                if (unreadMessages[chatId] > 0) {
                    if (!unreadBadge) {
                        const badge = document.createElement('div');
                        badge.className = 'unread-badge';
                        badge.textContent = unreadMessages[chatId];
                        chatItem.appendChild(badge);
                    } else {
                        unreadBadge.textContent = unreadMessages[chatId];
                    }
                    totalUnread += unreadMessages[chatId];
                } else if (unreadBadge) {
                    unreadBadge.remove();
                }
            });
            
            // Обновляем глобальный бейдж уведомлений
            const globalBadge = document.getElementById('globalNotificationBadge');
            if (totalUnread > 0) {
                globalBadge.textContent = totalUnread > 99 ? '99+' : totalUnread;
                globalBadge.style.display = 'flex';
                
                // Анимация пульсации для важных уведомлений
                if (totalUnread > 5) {
                    globalBadge.classList.add('notification-pulse');
                } else {
                    globalBadge.classList.remove('notification-pulse');
                }
            } else {
                globalBadge.style.display = 'none';
                globalBadge.classList.remove('notification-pulse');
            }
        }

        function showMessageNotification(message) {
            // Создаем уведомление
            const notification = document.createElement('div');
            notification.className = 'notification-toast';
            notification.innerHTML = `
                <div style="font-size: 24px;">💬</div>
                <div>
                    <div style="font-weight: bold;">Новое сообщение</div>
                    <div style="font-size: 14px; opacity: 0.9;">От ${message.sender_name}</div>
                    <div style="font-size: 13px; opacity: 0.7; margin-top: 5px;">${message.text.length > 50 ? message.text.substring(0, 50) + '...' : message.text}</div>
                </div>
            `;
            
            // Добавляем обработчик клика
            notification.style.cursor = 'pointer';
            notification.onclick = function() {
                // Переключаемся на чат отправителя
                if (message.sender_id !== currentUser.id) {
                    selectChat(message.sender_id);
                }
                notification.remove();
            };
            
            document.body.appendChild(notification);
            
            // Автоматическое скрытие через 5 секунд
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
            
            // Воспроизводим звук уведомления если включен
            if (userSettings.sound) {
                playNotificationSound();
            }
        }

        function playNotificationSound() {
            // Создаем простой звук уведомления
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.1);
            gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + 0.3);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        }

        function showNotificationsModal() {
            const modal = document.getElementById('notificationsModal');
            modal.classList.remove('hidden');
            updateNotificationsList();
        }

        function hideNotificationsModal() {
            document.getElementById('notificationsModal').classList.add('hidden');
        }

        function updateNotificationsList() {
            const notificationsList = document.getElementById('notificationsList');
            notificationsList.innerHTML = '';
            
            let hasNotifications = false;
            
            for (const [chatId, count] of Object.entries(unreadMessages)) {
                if (count > 0) {
                    hasNotifications = true;
                    let chatName = '';
                    let chatIcon = '💬';
                    
                    if (chatId === 'news') {
                        chatName = 'Новости DLtrollex';
                        chatIcon = '📢';
                    } else if (chatId === 'favorites') {
                        chatName = 'Избранное';
                        chatIcon = '⭐';
                    } else {
                        const user = allUsers.find(u => u.id === chatId);
                        if (user) {
                            chatName = user.name;
                            chatIcon = '👤';
                        } else {
                            continue;
                        }
                    }
                    
                    const notificationItem = document.createElement('div');
                    notificationItem.className = 'chat-item';
                    notificationItem.style.cursor = 'pointer';
                    notificationItem.innerHTML = `
                        <div class="chat-icon">${chatIcon}</div>
                        <div class="chat-info">
                            <div class="chat-name">${chatName}</div>
                            <div class="chat-last-message">${count} непрочитанных сообщений</div>
                        </div>
                        <div class="unread-badge">${count}</div>
                    `;
                    
                    notificationItem.onclick = function() {
                        selectChat(chatId);
                        hideNotificationsModal();
                    };
                    
                    notificationsList.appendChild(notificationItem);
                }
            }
            
            if (!hasNotifications) {
                notificationsList.innerHTML = `
                    <div style="text-align: center; color: #666; padding: 40px;">
                        <div style="font-size: 48px;">📭</div>
                        <p style="margin-top: 20px;">Нет непрочитанных сообщений</p>
                    </div>
                `;
            }
        }

        function clearAllNotifications() {
            unreadMessages = {};
            updateUnreadBadges();
            updateNotificationsList();
            
            if (socket) {
                socket.emit('clear_all_notifications', {user_id: currentUser.id});
            }
            
            showNotification('Все уведомления очищены', 'success');
        }

        function updateOnlineStatuses() {
            // Обновляем статусы в списке пользователей
            document.querySelectorAll('.chat-item').forEach(chatItem => {
                const chatId = chatItem.getAttribute('data-chat');
                if (chatId !== 'news' && chatId !== 'favorites') {
                    const user = allUsers.find(u => u.id === chatId);
                    if (user) {
                        const statusElement = chatItem.querySelector('.online-status');
                        if (onlineUsers.has(chatId)) {
                            if (!statusElement) {
                                const status = document.createElement('div');
                                status.className = 'online-status';
                                chatItem.querySelector('.chat-icon').appendChild(status);
                            }
                        } else if (statusElement) {
                            statusElement.remove();
                        }
                    }
                }
            });
        }

        function showChatInfoModal() {
            const modal = document.getElementById('chatInfoModal');
            const content = document.getElementById('chatInfoContent');
            
            if (currentChat === 'news') {
                content.innerHTML = `
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div class="avatar" style="width: 80px; height: 80px; margin: 0 auto 15px; font-size: 32px; background: #dc2626">📢</div>
                        <h3>Новости DLtrollex</h3>
                        <p style="color: var(--accent-color);">Официальный канал</p>
                    </div>
                    <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px;">
                        <div><strong>Тип:</strong> Публичный канал</div>
                        <div><strong>Сообщений:</strong> ${currentMessages.length}</div>
                        <div><strong>Доступ:</strong> Чтение - все, отправка - только администраторы</div>
                        <div><strong>Описание:</strong> Официальные объявления и новости платформы</div>
                    </div>
                `;
            } else if (currentChat === 'favorites') {
                content.innerHTML = `
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div class="avatar" style="width: 80px; height: 80px; margin: 0 auto 15px; font-size: 32px; background: #f59e0b">⭐</div>
                        <h3>Избранное</h3>
                        <p style="color: var(--accent-color);">Личные заметки</p>
                    </div>
                    <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px;">
                        <div><strong>Тип:</strong> Личные заметки</div>
                        <div><strong>Сообщений:</strong> ${currentMessages.length}</div>
                        <div><strong>Доступ:</strong> Только вы</div>
                        <div><strong>Описание:</strong> Сохраняйте здесь важные сообщения и заметки</div>
                    </div>
                `;
            } else {
                const user = allUsers.find(u => u.id === currentChat);
                if (user) {
                    const isOnline = onlineUsers.has(user.id);
                    content.innerHTML = `
                        <div style="text-align: center; margin-bottom: 20px;">
                            <div class="avatar" style="width: 80px; height: 80px; margin: 0 auto 15px; font-size: 32px; background: ${user.avatar_bg || '#8b5cf6'}">${user.avatar || '👤'}</div>
                            <h3>${user.name}</h3>
                            <p style="color: var(--accent-color);">${user.username}</p>
                            <p style="color: ${isOnline ? '#10b981' : '#6b7280'}; font-size: 14px;">
                                ● ${isOnline ? 'онлайн' : 'не в сети'}
                            </p>
                        </div>
                        <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px;">
                            <div><strong>ID:</strong> ${user.id}</div>
                            <div><strong>Статус:</strong> ${user.is_banned ? '🚫 Забанен' : user.is_muted ? '🔇 Заглушен' : '✅ Активен'}</div>
                            <div><strong>Роль:</strong> ${user.is_moderator ? '👑 Модератор' : '👤 Пользователь'}</div>
                            <div><strong>Сообщений в чате:</strong> ${currentMessages.length}</div>
                            <div><strong>Непрочитанные:</strong> ${unreadMessages[currentChat] || 0}</div>
                        </div>
                        <div style="margin-top: 20px; display: flex; gap: 10px;">
                            <button class="btn" onclick="startAudioCallWithUser('${user.id}')" style="flex: 1;">📞 Аудиозвонок</button>
                            <button class="btn" onclick="startVideoCallWithUser('${user.id}')" style="flex: 1;">📹 Видеозвонок</button>
                        </div>
                    `;
                }
            }
            
            modal.classList.remove('hidden');
        }

        function hideChatInfoModal() {
            document.getElementById('chatInfoModal').classList.add('hidden');
        }

        // ... (остальные функции без изменений, но добавлены вызовы markMessagesAsRead при смене чата) ...

        function selectChat(chatType) {
            currentChat = chatType;
            replyingTo = null;
            editingMessage = null;
            
            // Помечаем сообщения как прочитанные при открытии чата
            markMessagesAsRead(chatType);
            
            if (chatType === 'news') {
                document.getElementById('chatTitle').textContent = '📢 Новости DLtrollex';
                document.getElementById('chatStatus').textContent = 'Официальный канал';
                loadNews();
            } else if (chatType === 'favorites') {
                document.getElementById('chatTitle').textContent = '⭐ Избранное';
                document.getElementById('chatStatus').textContent = 'Ваши личные заметки';
                loadFavorites();
            } else {
                // Личный чат
                const user = allUsers.find(u => u.id === chatType);
                if (user) {
                    document.getElementById('chatTitle').textContent = user.name;
                    const status = onlineUsers.has(user.id) ? '● онлайн' : '○ не в сети';
                    document.getElementById('chatStatus').textContent = `${user.username} • ${status}`;
                    loadPrivateMessages(chatType);
                }
            }
            
            updateInputVisibility();
            updateCallButtons();
        }

        // ... (WebRTC функции и остальной код без изменений) ...

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
    return str(int(time.time() * 1000))

def generate_message_id():
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))

def save_avatar(user_id, avatar_data):
    """Сохраняет аватарку пользователя"""
    if avatar_data and avatar_data.startswith('data:image'):
        try:
            filename = f"{user_id}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            header, data = avatar_data.split(',', 1)
            image_data = base64.b64decode(data)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            return f"/user_avatars/{filename}"
        except Exception as e:
            print(f"Ошибка сохранения аватарки: {e}")
            return None
    return None

def is_user_banned(user_id):
    """Проверяет, забанен ли пользователь"""
    return user_id in moderation_db['banned_users']

def is_user_muted(user_id):
    """Проверяет, заглушен ли пользователь"""
    return user_id in moderation_db['muted_users']

def is_user_moderator(user_id):
    """Проверяет, является ли пользователь модератором"""
    return user_id in moderation_db['moderators'] or user_id == 'admin'

# ========== SOCKET.IO HANDLERS ==========

@socketio.on('connect')
def handle_connect():
    print(f"✅ Клиент подключен: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = user_sessions.get(request.sid)
    if user_id:
        print(f"❌ Пользователь отключен: {user_id}")
        # Обновляем статус онлайн
        emit('user_offline', {'user_id': user_id, 'username': users_db.get(user_id, {}).get('name', 'Пользователь')}, broadcast=True)
        # Завершаем активные звонки при отключении
        end_user_calls(user_id)

def end_user_calls(user_id):
    """Завершает все активные звонки пользователя"""
    calls_to_end = []
    for call_id, call_data in active_calls.items():
        if call_data['caller'] == user_id or call_data['target'] == user_id:
            calls_to_end.append(call_id)
    
    for call_id in calls_to_end:
        call_data = active_calls.pop(call_id, None)
        if call_data:
            # Уведомляем другую сторону о завершении звонка
            for sid, uid in user_sessions.items():
                if uid == call_data['caller'] or uid == call_data['target']:
                    emit('call_ended', {'call_id': call_id}, room=sid)

@socketio.on('restore_session')
def handle_restore_session(data):
    """Восстановление сессии пользователя"""
    user_id = data['user_id']
    user_sessions[request.sid] = user_id
    
    # Проверяем бан
    if is_user_banned(user_id):
        emit('user_banned', {'user_id': user_id})
        return
    
    print(f"🔑 Восстановлена сессия для: {user_id}")
    emit('session_restored', {'status': 'success', 'user_id': user_id})
    
    # Отправляем непрочитанные сообщения
    if user_id in unread_messages:
        emit('unread_messages', {'unread_messages': unread_messages[user_id]})
    else:
        unread_messages[user_id] = {}
        emit('unread_messages', {'unread_messages': {}})

# ==================== НОВЫЕ ОБРАБОТЧИКИ ДЛЯ УВЕДОМЛЕНИЙ ====================

@socketio.on('get_unread_messages')
def handle_get_unread_messages():
    """Отправляет непрочитанные сообщения пользователю"""
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    if user_id not in unread_messages:
        unread_messages[user_id] = {}
    
    emit('unread_messages', {'unread_messages': unread_messages[user_id]})

@socketio.on('update_unread_count')
def handle_update_unread_count(data):
    """Обновляет счетчик непрочитанных сообщений"""
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    chat_id = data['chat_id']
    count = data['count']
    
    if user_id not in unread_messages:
        unread_messages[user_id] = {}
    
    unread_messages[user_id][chat_id] = count
    save_user_data()

@socketio.on('mark_messages_read')
def handle_mark_messages_read(data):
    """Помечает сообщения как прочитанные"""
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    chat_id = data['chat_id']
    
    if user_id in unread_messages and chat_id in unread_messages[user_id]:
        unread_messages[user_id][chat_id] = 0
        save_user_data()
        
        # Уведомляем пользователя
        emit('messages_read', {'chat_id': chat_id})

@socketio.on('clear_all_notifications')
def handle_clear_all_notifications(data):
    """Очищает все уведомления пользователя"""
    user_id = data['user_id']
    
    if user_id in unread_messages:
        for chat_id in unread_messages[user_id]:
            unread_messages[user_id][chat_id] = 0
        save_user_data()

@socketio.on('update_online_status')
def handle_update_online_status(data):
    """Обновляет онлайн статус пользователя"""
    user_id = data['user_id']
    is_online = data['is_online']
    
    if is_online:
        # Уведомляем всех о том, что пользователь онлайн
        user_data = users_db.get(user_id)
        if user_data:
            emit('user_online', {
                'user_id': user_id,
                'username': user_data['name']
            }, broadcast=True)
    else:
        # Уведомляем о выходе из сети
        user_data = users_db.get(user_id)
        if user_data:
            emit('user_offline', {
                'user_id': user_id,
                'username': user_data['name']
            }, broadcast=True)

@socketio.on('get_online_users')
def handle_get_online_users():
    """Отправляет список онлайн пользователей"""
    online_users = list(user_sessions.values())
    emit('online_users', {'users': online_users})

# ==================== ОБНОВЛЕННЫЕ ОБРАБОТЧИКИ СООБЩЕНИЙ ====================

@socketio.on('send_private_message')
def handle_send_private_message(data):
    user_id = user_sessions.get(request.sid)
    if not user_id:
        return
    
    # Проверяем бан
    if is_user_banned(user_id):
        emit('message_error', {'error': 'Вы забанены и не можете отправлять сообщения'})
        return
    
    # Проверяем мут
    if is_user_muted(user_id):
        emit('message_error', {'error': 'Вы заглушены и не можете отправлять сообщения'})
        return
    
    sender_data = users_db.get(user_id) if user_id != 'admin' else {
        'id': 'admin',
        'name': 'Администратор',
        'username': '@admin'
    }
    
    if not sender_data:
        return
    
    recipient_id = data['chat_id']
    
    # Проверяем существование получателя
    if recipient_id != 'admin' and recipient_id not in users_db:
        emit('message_error', {'error': 'Пользователь не найден'})
        return
    
    message_id = generate_message_id()
    message = {
        'id': message_id,
        'text': data['text'],
        'sender_id': user_id,
        'sender_name': sender_data['name'],
        'timestamp': datetime.datetime.now().isoformat(),
        'edited': False,
        'reactions': {}
    }
    
    # Сохраняем сообщение в правильной структуре
    # Для отправителя
    if user_id not in messages_db:
        messages_db[user_id] = {}
    if recipient_id not in messages_db[user_id]:
        messages_db[user_id][recipient_id] = []
    messages_db[user_id][recipient_id].append(message)
    
    # Для получателя (если это не админ)
    if recipient_id != 'admin' and recipient_id in users_db:
        if recipient_id not in messages_db:
            messages_db[recipient_id] = {}
        if user_id not in messages_db[recipient_id]:
            messages_db[recipient_id][user_id] = []
        messages_db[recipient_id][user_id].append(message)
        
        # Добавляем непрочитанное сообщение получателю
        if recipient_id not in unread_messages:
            unread_messages[recipient_id] = {}
        if user_id not in unread_messages[recipient_id]:
            unread_messages[recipient_id][user_id] = 0
        unread_messages[recipient_id][user_id] += 1
    
    save_user_data()
    
    # Отправляем сообщение отправителю
    emit('private_message', {**message, 'chat_id': recipient_id})
    
    # Отправляем получателю, если он онлайн
    for sid, uid in user_sessions.items():
        if uid == recipient_id:
            emit('private_message', {**message, 'chat_id': user_id}, room=sid)
            # Обновляем счетчик непрочитанных для получателя
            if recipient_id in unread_messages and user_id in unread_messages[recipient_id]:
                emit('unread_messages', {'unread_messages': unread_messages[recipient_id]}, room=sid)
    
    print(f"📨 Сообщение от {user_id} к {recipient_id}: {data['text'][:50]}...")

# ... (остальные обработчики без изменений) ...

if __name__ == '__main__':
    print("🚀 Запуск DLtrollex с уведомлениями и улучшениями...")
    print("💜 Доступно по адресу: http://localhost:5000")
    print("📞 WebRTC звонки активированы!")
    print("🛡️ Система модерации активирована!")
    print("🔔 Система уведомлений активирована!")
    print("👥 Онлайн статусы активированы!")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
