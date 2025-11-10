# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramodern2024'

class AdvancedChatManager:
    def __init__(self):
        self.users = []
        self.chats = []
        self.messages = []
    
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

chat_manager = AdvancedChatManager()

def generate_username():
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(1000, 9999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(12))

def get_user_rank(level):
    if level < 10: return "Новичок 🌱"
    elif level < 25: return "Исследователь 🚀"
    elif level < 50: return "Эксперт 💫"
    elif level < 75: return "Мастер 🏆"
    else: return "Легенда 👑"

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
                radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes slideInUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
        }

        @keyframes loadingSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
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
            padding: 20px;
            z-index: 1000;
            overflow-y: auto;
        }

        /* Экран загрузки */
        .loading-screen {
            background: var(--bg-primary);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2rem;
        }

        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(139, 92, 246, 0.3);
            border-top: 4px solid var(--accent-purple);
            border-radius: 50%;
            animation: loadingSpin 1s linear infinite;
        }

        .loading-text {
            text-align: center;
            font-size: 1.2rem;
            color: var(--text-secondary);
        }

        .loading-subtext {
            text-align: center;
            font-size: 1rem;
            color: var(--accent-purple);
            margin-top: 1rem;
            font-weight: 600;
        }

        .auth-container {
            background: var(--bg-card);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            max-width: 450px;
            position: relative;
            overflow: hidden;
            border: var(--border-glow);
            box-shadow: var(--shadow-glow);
            backdrop-filter: blur(20px);
            margin: 10px;
            animation: slideInUp 0.5s ease-out;
        }

        .auth-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: var(--gradient-primary);
            animation: gradientShift 8s ease infinite;
            opacity: 0.1;
            z-index: -1;
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 800;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
            text-align: center;
            margin-bottom: 1rem;
        }

        .subtitle {
            color: var(--text-secondary);
            text-align: center;
            margin-bottom: 1.5rem;
            font-size: 1rem;
            line-height: 1.5;
        }

        .btn {
            width: 100%;
            padding: 14px 20px;
            border: none;
            border-radius: 12px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            margin-bottom: 0.8rem;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(139, 92, 246, 0.4);
        }

        .btn-secondary {
            background: var(--bg-input);
            color: var(--text-primary);
            border: var(--border-glow);
        }

        .btn-secondary:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateY(-2px);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 0.8rem;
            margin: 1.5rem 0;
        }

        .feature-card {
            background: var(--bg-input);
            padding: 1.2rem;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: var(--border-glow);
        }

        .feature-card:hover {
            transform: translateY(-3px);
            background: rgba(139, 92, 246, 0.1);
            box-shadow: var(--shadow-glow);
        }

        .feature-icon {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .credential-box {
            background: var(--bg-input);
            padding: 1.2rem;
            border-radius: 12px;
            margin: 1.2rem 0;
            border: var(--border-glow);
            animation: pulse 2s infinite;
        }

        .credential-field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 0.4rem 0;
            padding: 0.6rem;
            background: var(--bg-secondary);
            border-radius: 8px;
            font-size: 0.9rem;
        }

        .credential-value {
            font-family: 'Courier New', monospace;
            color: var(--accent-purple);
            font-weight: 600;
            font-size: 0.85rem;
        }

        .copy-btn {
            background: var(--accent-purple);
            color: white;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }

        .copy-btn:hover {
            background: var(--accent-pink);
            transform: scale(1.05);
        }

        .floating-emoji {
            position: fixed;
            font-size: 1.8rem;
            z-index: 999;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
            pointer-events: none;
        }

        .hidden {
            display: none !important;
        }

        .stats-panel {
            background: var(--bg-card);
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: var(--border-glow);
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            margin: 0.4rem 0;
            padding: 0.5rem;
            background: var(--bg-input);
            border-radius: 6px;
            font-size: 0.9rem;
        }

        .progress-bar {
            width: 100%;
            height: 4px;
            background: var(--bg-input);
            border-radius: 2px;
            overflow: hidden;
            margin: 1rem 0;
        }

        .progress-fill {
            height: 100%;
            background: var(--gradient-primary);
            border-radius: 2px;
            transition: width 0.3s ease;
        }

        .notification {
            position: fixed;
            top: 15px;
            right: 15px;
            background: var(--gradient-primary);
            color: white;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            z-index: 2000;
            animation: slideInUp 0.3s ease;
            box-shadow: var(--shadow-glow);
            max-width: 300px;
            font-size: 0.9rem;
        }

        /* Чат интерфейс */
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-primary);
            width: 100%;
            overflow: hidden;
        }

        .chat-container {
            display: flex;
            height: 100vh;
            width: 100%;
            margin: 0;
            background: var(--bg-secondary);
            overflow: hidden;
        }

        .sidebar {
            width: 320px;
            background: var(--bg-card);
            border-right: var(--border-glow);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .user-header {
            padding: 1.5rem;
            background: var(--gradient-secondary);
            border-bottom: var(--border-glow);
        }

        .user-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            margin-bottom: 0.8rem;
        }

        .user-stats {
            display: flex;
            justify-content: space-between;
            margin-top: 0.8rem;
            font-size: 0.8rem;
            gap: 0.3rem;
        }

        .stat-badge {
            background: rgba(255,255,255,0.1);
            padding: 0.4rem 0.6rem;
            border-radius: 8px;
            text-align: center;
            flex: 1;
        }

        .level-badge {
            background: var(--gradient-gold);
            color: black;
            font-weight: 700;
        }

        .premium-badge {
            background: var(--gradient-premium);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 700;
            margin-top: 0.8rem;
            text-align: center;
        }

        .search-box {
            padding: 1rem;
            border-bottom: var(--border-glow);
        }

        .search-input {
            width: 100%;
            padding: 10px 12px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 0.85rem;
        }

        .chats-list {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 1rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
            background: rgba(255,255,255,0.02);
        }

        .chat-item:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateX(3px);
        }

        .chat-item.active {
            background: rgba(139, 92, 246, 0.2);
        }

        .unread-badge {
            position: absolute;
            top: 0.8rem;
            right: 0.8rem;
            background: var(--accent-pink);
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 700;
        }

        .chat-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            margin-right: 1rem;
            flex-shrink: 0;
        }

        .chat-info {
            flex: 1;
            min-width: 0;
        }

        .chat-name {
            font-weight: 600;
            margin-bottom: 0.2rem;
            font-size: 0.95rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .chat-preview {
            color: var(--text-secondary);
            font-size: 0.8rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .chat-time {
            font-size: 0.7rem;
            color: var(--accent-cyan);
            margin-top: 0.2rem;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            min-width: 0;
        }

        .chat-header {
            padding: 1.2rem 1.5rem;
            background: var(--bg-card);
            border-bottom: var(--border-glow);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }

        .chat-actions {
            display: flex;
            gap: 0.5rem;
        }

        .action-btn {
            background: rgba(255,255,255,0.1);
            border: none;
            color: var(--text-primary);
            padding: 0.5rem 0.7rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .action-btn:hover {
            background: var(--accent-purple);
            transform: scale(1.05);
        }

        .messages-container {
            flex: 1;
            padding: 1.5rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            min-height: 0;
        }

        .message {
            max-width: 80%;
            padding: 1rem 1.2rem;
            border-radius: 18px;
            position: relative;
            animation: slideInUp 0.3s ease;
            word-wrap: break-word;
        }

        .message.received {
            background: var(--bg-input);
            align-self: flex-start;
            border-bottom-left-radius: 5px;
        }

        .message.sent {
            background: var(--gradient-primary);
            align-self: flex-end;
            border-bottom-right-radius: 5px;
            color: white;
        }

        .message-time {
            font-size: 0.65rem;
            opacity: 0.7;
            margin-top: 0.3rem;
            text-align: right;
        }

        .message-input-container {
            padding: 1.2rem 1.5rem;
            background: var(--bg-card);
            border-top: var(--border-glow);
            display: flex;
            gap: 0.8rem;
            align-items: center;
            flex-shrink: 0;
        }

        .message-input {
            flex: 1;
            padding: 12px 16px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 20px;
            color: var(--text-primary);
            font-size: 0.9rem;
            min-width: 0;
        }

        .send-btn {
            padding: 12px 20px;
            background: var(--gradient-primary);
            border: none;
            border-radius: 15px;
            color: white;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            flex-shrink: 0;
        }

        .send-btn:hover {
            transform: scale(1.05);
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin: 0.8rem 1.5rem;
            padding: 0.8rem 1rem;
            background: rgba(139, 92, 246, 0.1);
            border-radius: 12px;
            border: var(--border-glow);
        }

        .typing-dots {
            display: flex;
            margin-left: 0.8rem;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--accent-purple);
            border-radius: 50%;
            margin: 0 2px;
            animation: typingPulse 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingPulse {
            0%, 60%, 100% { transform: scale(1); opacity: 0.4; }
            30% { transform: scale(1.2); opacity: 1; }
        }

        .trust-message {
            text-align: center;
            color: var(--accent-purple);
            font-weight: 600;
            margin-top: 1.5rem;
            font-size: 0.9rem;
        }

        /* Мобильная оптимизация */
        @media (max-width: 768px) {
            .auth-container {
                padding: 1.5rem;
                margin: 0.5rem;
                border-radius: 15px;
            }
            
            .logo {
                font-size: 2rem;
            }
            
            .feature-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.5rem;
            }
            
            .feature-card {
                padding: 1rem;
            }
            
            .chat-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: 40vh;
                position: absolute;
                z-index: 1000;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .mobile-menu-btn {
                display: block !important;
            }
            
            .messages-container {
                padding: 1rem;
            }
            
            .message {
                max-width: 90%;
                padding: 0.8rem 1rem;
            }
            
            .message-input-container {
                padding: 1rem;
            }
            
            .chat-header {
                padding: 1rem;
            }
            
            .notification {
                left: 10px;
                right: 10px;
                top: 10px;
                max-width: none;
            }

            .sidebar {
                width: 85%;
            }
        }

        @media (max-width: 480px) {
            .auth-container {
                padding: 1.2rem;
            }
            
            .logo {
                font-size: 1.8rem;
            }
            
            .subtitle {
                font-size: 0.9rem;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
            }
            
            .credential-field {
                flex-direction: column;
                gap: 0.3rem;
                align-items: flex-start;
            }
            
            .message {
                max-width: 95%;
            }
            
            .user-stats {
                flex-direction: column;
                gap: 0.3rem;
            }

            .sidebar {
                width: 90%;
            }
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text-primary);
            font-size: 1.3rem;
            cursor: pointer;
            padding: 0.4rem;
            border-radius: 6px;
            transition: all 0.3s ease;
        }

        .mobile-menu-btn:hover {
            background: rgba(139, 92, 246, 0.2);
        }
    </style>
</head>
<body>
    <!-- Плавающие элементы -->
    <div class="floating-emoji" style="top: 10%; left: 5%;">💫</div>
    <div class="floating-emoji" style="top: 15%; right: 8%;">✨</div>
    <div class="floating-emoji" style="top: 85%; left: 10%;">🚀</div>
    <div class="floating-emoji" style="top: 80%; right: 5%;">🌟</div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen loading-screen">
        <div class="loading-spinner"></div>
        <div class="loading-text">Запускаем DL-TrolledX...</div>
        <div class="loading-subtext">Спасибо, что доверяете нам! 💫</div>
    </div>

    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">DL-TrolledX</div>
            <div class="subtitle">Ультра-современный мессенджер с AI и космическим дизайном</div>
            
            <div class="stats-panel">
                <h4 style="margin-bottom: 0.8rem; text-align: center; font-size: 0.9rem;">📊 Статистика платформы</h4>
                <div class="stat-item">
                    <span>Онлайн:</span>
                    <span style="color: var(--accent-purple); font-weight: 600;">1,247</span>
                </div>
                <div class="stat-item">
                    <span>Сообщений:</span>
                    <span style="color: var(--accent-pink); font-weight: 600;">8,492</span>
                </div>
                <div class="stat-item">
                    <span>Чатов:</span>
                    <span style="color: var(--accent-cyan); font-weight: 600;">356</span>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="startQuickRegistration()">
                🚀 Начать путешествие
            </button>
            
            <div class="feature-grid">
                <div class="feature-card" onclick="startQuickRegistration()">
                    <div class="feature-icon">🤖</div>
                    <div>AI Ассистент</div>
                </div>
                <div class="feature-card" onclick="showThemeSelector()">
                    <div class="feature-icon">🎨</div>
                    <div>Темы</div>
                </div>
                <div class="feature-card" onclick="showStats()">
                    <div class="feature-icon">📊</div>
                    <div>Статистика</div>
                </div>
                <div class="feature-card" onclick="showFeatures()">
                    <div class="feature-icon">⚡</div>
                    <div>Функции</div>
                </div>
            </div>

            <div class="trust-message">
                Спасибо, что доверяете нам! 💫
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">Создание аккаунта</div>
            <div class="subtitle">Ваш цифровой пропуск в будущее общения</div>
            
            <div class="credential-box">
                <div class="credential-field">
                    <span>👤 Имя:</span>
                    <span class="credential-value" id="generatedName">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 Пароль:</span>
                    <span class="credential-value" id="generatedPassword">...</span>
                    <button class="copy-btn" onclick="copyToClipboard('generatedPassword')">📋</button>
                </div>
                <div class="credential-field">
                    <span>🆔 ID:</span>
                    <span class="credential-value" id="generatedUsername">...</span>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="registerProgress" style="width: 0%"></div>
            </div>
            
            <button class="btn btn-primary" onclick="quickRegister()">
                💫 Войти в DL-TrolledX
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewCredentials()">
                🔄 Обновить данные
            </button>
            
            <button class="btn btn-secondary" onclick="showScreen('welcomeScreen')">
                ← Назад
            </button>

            <div class="trust-message">
                Ваши данные в безопасности 🔒
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
                    <h3 id="userName" style="font-size: 1.1rem;">Пользователь</h3>
                    <p id="userRank" style="color: var(--accent-cyan); margin-bottom: 0.8rem; font-size: 0.8rem;">Уровень: 1</p>
                    
                    <div class="user-stats">
                        <div class="stat-badge level-badge">
                            <div>⚡ Ур. <span id="userLevel">1</span></div>
                        </div>
                        <div class="stat-badge">
                            <div>💎 <span id="userXP">0</span> XP</div>
                        </div>
                    </div>
                    
                    <div class="premium-badge" id="premiumBadge" style="display: none;">
                        🌟 PREMIUM
                    </div>
                </div>
                
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="🔍 Поиск чатов..." oninput="searchChats(this.value)">
                </div>
                
                <div class="chats-list" id="chatsList">
                    <!-- Список чатов будет здесь -->
                </div>
            </div>
            
            <!-- Область чата -->
            <div class="chat-area">
                <div class="chat-header">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                        <div class="chat-avatar" id="currentChatAvatar">👤</div>
                        <div style="min-width: 0;">
                            <h3 id="currentChatName" style="font-size: 1.1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Выберите чат</h3>
                            <p id="currentChatStatus" style="color: var(--text-secondary); font-size: 0.8rem;">для начала общения</p>
                        </div>
                    </div>
                    <div class="chat-actions">
                        <button class="action-btn" onclick="showChatInfo()" title="Информация">ℹ️</button>
                        <button class="action-btn" onclick="showSettings()" title="Настройки">⚙️</button>
                        <button class="action-btn" onclick="logout()" title="Выйти">🚪</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                        <h3 style="margin-bottom: 0.5rem; font-size: 1.2rem;">Добро пожаловать в DL-TrolledX!</h3>
                        <p style="font-size: 0.9rem;">Выберите чат для начала общения</p>
                    </div>
                </div>
                
                <div class="typing-indicator hidden" id="typingIndicator">
                    <span id="typingUser" style="font-size: 0.8rem;">Собеседник</span> печатает
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="Напишите сообщение..." id="messageInput" 
                           onkeypress="handleKeyPress(event)">
                    <button class="send-btn" onclick="sendMessage()">Отправить</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let userStats = {
            messagesSent: 0,
            chatsCreated: 0,
            logins: 0,
            timeSpent: 0,
            level: 1,
            xp: 0
        };

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DL-TrolledX запускается...");
            setTimeout(() => {
                hideLoadingScreen();
                initializeSampleData();
                checkAutoLogin();
            }, 2000);
        });

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function initializeSampleData() {
            // Создаем тестовых пользователей
            allUsers = [
                {
                    id: 'user1',
                    name: 'Алексей',
                    username: '@neuro_alex',
                    avatar: '🤖',
                    isOnline: true,
                    bio: 'AI разработчик',
                    level: 42,
                    xp: 12500,
                    premium: true
                },
                {
                    id: 'user2', 
                    name: 'София',
                    username: '@digital_queen',
                    avatar: '👑',
                    isOnline: true,
                    bio: 'Дизайнер интерфейсов',
                    level: 38,
                    xp: 9800,
                    premium: true
                },
                {
                    id: 'user3',
                    name: 'Максим',
                    username: '@code_master',
                    avatar: '💻',
                    isOnline: false,
                    bio: 'Full-stack разработчик',
                    level: 56,
                    xp: 21000,
                    premium: false
                }
            ];

            // Загружаем сохраненные данные
            const savedChats = localStorage.getItem('dl_trolledx_chats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
            
            const savedStats = localStorage.getItem('dl_trolledx_stats');
            if (savedStats) {
                userStats = JSON.parse(savedStats);
            }
        }

        function createSampleChats() {
            chats = []; // Очищаем старые чаты
            
            const sampleMessages = [
                "Привет! Как дела? 🚀",
                "Отлично! Работаю над новым проектом! 💫",
                "Круто! Расскажи подробнее? 🔬",
                "Создаю нейросеть для анализа данных... 📊",
                "Вау! Звучит интересно! 🌟",
                "Да, очень увлекательно! Скоро покажу результаты ⚡",
                "Жду с нетерпением! 🎯",
                "Обязательно поделюсь! 💎"
            ];

            allUsers.forEach((user, index) => {
                const chatMessages = [];
                const messageCount = 4; // Фиксированное количество сообщений
                
                for (let i = 0; i < messageCount; i++) {
                    const isUser = i % 2 === 0;
                    chatMessages.push({
                        id: `msg_${Date.now()}_${i}_${index}`,
                        text: sampleMessages[i] || "Привет! 👋",
                        senderId: isUser ? 'current_user' : user.id,
                        timestamp: new Date(Date.now() - (messageCount - i) * 600000).toISOString()
                    });
                }

                const newChat = {
                    id: `chat_${user.id}_${Date.now()}`,
                    participants: ['current_user', user.id],
                    lastMessage: chatMessages[chatMessages.length - 1],
                    messages: chatMessages,
                    unread: Math.floor(Math.random() * 3),
                    created_at: new Date().toISOString()
                };
                chats.push(newChat);
            });
            
            localStorage.setItem('dl_trolledx_chats', JSON.stringify(chats));
            return chats;
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dl_trolledx_currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                userStats.logins++;
                saveUserStats();
                
                // Показываем загрузку перед переходом в чат
                showScreen('loadingScreen');
                document.querySelector('.loading-text').textContent = 'Возвращаемся в чат...';
                document.querySelector('.loading-subtext').textContent = 'Спасибо за возвращение! 🌟';
                
                setTimeout(() => {
                    showMainApp();
                    // Автоматически открываем первый чат
                    if (chats.length > 0) {
                        openChat(chats[0].id);
                    }
                    showNotification(`С возвращением, ${currentUser.name}! 🚀`, 'success');
                }, 1500);
            } else {
                showScreen('welcomeScreen');
            }
        }

        function saveUserStats() {
            localStorage.setItem('dl_trolledx_stats', JSON.stringify(userStats));
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

        function showManualLogin() {
            showNotification('Ручной вход будет доступен в следующем обновлении! 🔄', 'info');
        }

        function showFeatures() {
            showNotification(`
                🚀 Возможности DL-TrolledX:
                • AI-ассистент в чатах
                • Система уровней и XP
                • Премиум функции
                • Красивый дизайн
            `, 'info');
        }

        function showThemeSelector() {
            showNotification('Выбор темы будет в следующем обновлении! 🎨', 'info');
        }

        function showStats() {
            showNotification('Статистика доступна в вашем профиле! 📊', 'info');
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            const username = '@' + name.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
            document.getElementById('generatedUsername').textContent = username;
            
            animateProgress('registerProgress', 100, 1000);
        }

        function generateUsername() {
            const adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой'];
            const nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк'];
            return `${randomChoice(adjectives)}${randomChoice(nouns)}${Math.floor(Math.random() * 1000)}`;
        }

        function generatePassword() {
            const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
            let password = '';
            for (let i = 0; i < 12; i++) {
                password += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            return password;
        }

        function randomChoice(array) {
            return array[Math.floor(Math.random() * array.length)];
        }

        function animateProgress(elementId, to, duration) {
            const element = document.getElementById(elementId);
            let start = 0;
            const increment = to / (duration / 10);
            
            const timer = setInterval(() => {
                start += increment;
                element.style.width = Math.min(start, to) + '%';
                if (start >= to) clearInterval(timer);
            }, 10);
        }

        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Скопировано в буфер обмена! 📋', 'success');
            });
        }

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            const username = document.getElementById('generatedUsername').textContent;
            
            if (!name || name === '...') {
                showNotification('Сначала сгенерируйте данные!', 'error');
                return;
            }
            
            const avatars = ['😎', '🤖', '👽', '🐲', '🦄'];
            const level = Math.floor(Math.random() * 50) + 1;
            const xp = level * 100 + Math.floor(Math.random() * 99);
            const premium = Math.random() > 0.7;
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                username: username,
                avatar: randomChoice(avatars),
                isOnline: true,
                bio: 'Исследователь цифровых миров 🌌',
                password: password,
                level: level,
                xp: xp,
                premium: premium,
                join_date: new Date().toISOString()
            };
            
            localStorage.setItem('dl_trolledx_currentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            userStats.level = level;
            userStats.xp = xp;
            saveUserStats();
            
            // СОЗДАЕМ ЧАТЫ СРАЗУ ПОСЛЕ РЕГИСТРАЦИИ
            createSampleChats();
            
            // Показываем загрузку перед переходом
            showScreen('loadingScreen');
            document.querySelector('.loading-text').textContent = 'Создаем ваше пространство...';
            document.querySelector('.loading-subtext').textContent = 'Спасибо за доверие! 💫';
            
            setTimeout(() => {
                showMainApp();
                // АВТОМАТИЧЕСКИ ОТКРЫВАЕМ ПЕРВЫЙ ЧАТ
                if (chats.length > 0) {
                    openChat(chats[0].id);
                }
                showNotification(`Добро пожаловать, ${name}! 🚀`, 'success');
            }, 1500);
        }

        function get_user_rank(level) {
            if (level < 10) return "Новичок 🌱";
            else if (level < 25) return "Исследователь 🚀";
            else if (level < 50) return "Эксперт 💫";
            else if (level < 75) return "Мастер 🏆";
            else return "Легенда 👑";
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById('mainApp').classList.remove('hidden');
            
            // Обновляем интерфейс пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userLevel').textContent = currentUser.level;
            document.getElementById('userXP').textContent = currentUser.xp;
            document.getElementById('userRank').textContent = `Ранг: ${get_user_rank(currentUser.level)}`;
            
            if (currentUser.premium) {
                document.getElementById('premiumBadge').style.display = 'block';
            }
            
            renderChatsList();
            startTimeTracking();
        }

        function renderChatsList() {
            const chatsList = document.getElementById('chatsList');
            
            if (chats.length === 0) {
                chatsList.innerHTML = `
                    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
                        <p style="font-size: 0.9rem;">Чатов пока нет</p>
                    </div>
                `;
                return;
            }
            
            chatsList.innerHTML = chats.map(chat => {
                const otherUser = allUsers.find(u => u.id === chat.participants.find(p => p !== 'current_user'));
                if (!otherUser) return '';
                
                const lastMessageTime = new Date(chat.lastMessage.timestamp);
                const timeString = lastMessageTime.toLocaleTimeString('ru-RU', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
                
                return `
                    <div class="chat-item" onclick="openChat('${chat.id}')" style="position: relative;">
                        <div class="chat-avatar">${otherUser.avatar}</div>
                        <div class="chat-info">
                            <div class="chat-name">${otherUser.name}</div>
                            <div class="chat-preview">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                            <div class="chat-time">${timeString}</div>
                        </div>
                        ${chat.unread > 0 ? `<div class="unread-badge">${chat.unread}</div>` : ''}
                    </div>
                `;
            }).join('');
        }

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== 'current_user'));
            if (!otherUser) return;
            
            // Убираем непрочитанные сообщения
            currentChat.unread = 0;
            localStorage.setItem('dl_trolledx_chats', JSON.stringify(chats));
            renderChatsList();
            
            document.getElementById('currentChatName').textContent = otherUser.name;
            document.getElementById('currentChatAvatar').textContent = otherUser.avatar;
            document.getElementById('currentChatStatus').textContent = otherUser.isOnline ? 
                '● онлайн' : '● был(а) недавно';
            
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = currentChat.messages.map(msg => {
                const isOwn = msg.senderId === 'current_user';
                const messageTime = new Date(msg.timestamp);
                const timeString = messageTime.toLocaleTimeString('ru-RU', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
                
                return `
                    <div class="message ${isOwn ? 'sent' : 'received'}">
                        ${msg.text}
                        <div class="message-time">${timeString}</div>
                    </div>
                `;
            }).join('');
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                const newMessage = {
                    id: 'msg_' + Date.now(),
                    text: message,
                    senderId: 'current_user',
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                
                localStorage.setItem('dl_trolledx_chats', JSON.stringify(chats));
                
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                const timeString = new Date().toLocaleTimeString('ru-RU', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
                messageElement.innerHTML = `
                    ${message}
                    <div class="message-time">${timeString}</div>
                `;
                messagesContainer.appendChild(messageElement);
                
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                userStats.messagesSent++;
                userStats.xp += 5;
                // Проверяем повышение уровня
                const newLevel = Math.floor(userStats.xp / 100) + 1;
                if (newLevel > userStats.level) {
                    userStats.level = newLevel;
                    showNotification(`🎉 Поздравляем! Вы достигли уровня ${newLevel}!`, 'success');
                    document.getElementById('userLevel').textContent = userStats.level;
                    document.getElementById('userRank').textContent = `Ранг: ${get_user_rank(userStats.level)}`;
                }
                saveUserStats();
                
                // Обновляем список чатов
                renderChatsList();
            }
        }

        function searchChats(query) {
            const chatItems = document.querySelectorAll('.chat-item');
            chatItems.forEach(item => {
                const chatName = item.querySelector('.chat-name').textContent.toLowerCase();
                if (chatName.includes(query.toLowerCase())) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('active');
        }

        function showChatInfo() {
            if (currentChat) {
                const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== 'current_user'));
                if (otherUser) {
                    showNotification(`
                        💬 Информация о чате:
                        👤 Имя: ${otherUser.name}
                        🆔 ID: ${otherUser.username}
                        📝 Статус: ${otherUser.bio}
                        ⚡ Уровень: ${otherUser.level}
                        ${otherUser.premium ? '🌟 Статус: PREMIUM' : '🔹 Статус: Базовый'}
                    `, 'info');
                }
            } else {
                showNotification('Выберите чат для просмотра информации', 'error');
            }
        }

        function showSettings() {
            showNotification(`
                ⚙️ Настройки:
                • Тема: Космическая
                • Уведомления: Включены
                • Уровень: ${userStats.level}
                • Опыт: ${userStats.xp} XP
                • Сообщений: ${userStats.messagesSent}
            `, 'info');
        }

        function logout() {
            if (confirm('Выйти из аккаунта?')) {
                currentUser = null;
                localStorage.removeItem('dl_trolledx_currentUser');
                showScreen('welcomeScreen');
                showNotification('До скорой встречи! 👋', 'info');
            }
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.style.background = type === 'error' ? 'var(--accent-pink)' : 
                                           type === 'success' ? 'var(--accent-green)' : 
                                           'var(--gradient-primary)';
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 4000);
        }

        function startTimeTracking() {
            setInterval(() => {
                if (currentUser) {
                    userStats.timeSpent++;
                    if (userStats.timeSpent % 10 === 0) {
                        saveUserStats();
                    }
                }
            }, 60000);
        }

        // Авто-сохранение
        setInterval(() => {
            if (currentUser) {
                localStorage.setItem('dl_trolledx_chats', JSON.stringify(chats));
                localStorage.setItem('dl_trolledx_stats', JSON.stringify(userStats));
            }
        }, 30000);
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
        'users_online': random.randint(50, 100),
        'version': '1.0',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'DL-TrolledX'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 DL-TrolledX запущен!")
    print("💫 Ультра-современный дизайн")
    print("📱 Оптимизирован для мобильных")
    print("🎯 Рабочие чаты сразу после регистрации")
    print(f"🔗 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
