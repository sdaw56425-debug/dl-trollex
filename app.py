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
news_messages = [
    {
        'id': '1',
        'text': 'Добро пожаловать в DLtrollex! 🎉',
        'sender_name': 'Система',
        'timestamp': datetime.datetime.now().isoformat(),
    },
    {
        'id': '2', 
        'text': 'Это фиолетовый мессенджер с максимальной кастомизацией! 💜',
        'sender_name': 'Система', 
        timestamp': datetime.datetime.now().isoformat(),
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎃</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
            -webkit-text-size-adjust: 100%;
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
            --safe-area-top: env(safe-area-inset-top, 0px);
            --safe-area-bottom: env(safe-area-inset-bottom, 0px);
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            height: 100dvh;
            overflow: hidden;
            transition: all 0.3s ease;
            touch-action: manipulation;
            padding: var(--safe-area-top) 0 var(--safe-area-bottom) 0;
        }
        
        body.halloween-theme {
            --accent-color: #ff7b25;
            --bg-color: #1a0f00;
            --card-color: #2a1a00;
            --secondary-color: #3a2a00;
        }
        
        /* Оптимизированные анимации */
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 10px var(--accent-color);
            }
            50% {
                text-shadow: 0 0 20px var(--accent-color);
            }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .glowing-logo {
            animation: glow 3s ease-in-out infinite;
            will-change: text-shadow;
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
            will-change: transform;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
            will-change: transform;
        }
        
        .fade-in {
            animation: fadeIn 0.4s ease-out;
            will-change: opacity, transform;
        }
        
        /* Базовые компоненты */
        .screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            height: 100dvh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--bg-color) 0%, var(--card-color) 100%);
            z-index: 1000;
            padding: 20px;
            padding-top: calc(20px + var(--safe-area-top));
            padding-bottom: calc(20px + var(--safe-area-bottom));
        }
        
        .auth-box {
            background: var(--card-color);
            padding: 30px 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 2px solid var(--accent-color);
            width: 100%;
            max-width: min(450px, 90vw);
            text-align: center;
            position: relative;
            overflow: hidden;
            z-index: 1001;
        }
        
        .logo {
            font-size: clamp(32px, 8vw, 42px);
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 12px;
        }
        
        .subtitle {
            color: #888;
            margin-bottom: 25px;
            font-size: clamp(14px, 4vw, 16px);
            line-height: 1.4;
        }
        
        .input-field {
            width: 100%;
            padding: 16px;
            margin-bottom: 15px;
            background: var(--secondary-color);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-color);
            font-size: 16px;
            transition: all 0.2s ease;
            -webkit-appearance: none;
        }
        
        .input-field:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
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
            margin-bottom: 12px;
            transition: all 0.2s ease;
            touch-action: manipulation;
            user-select: none;
            min-height: 50px;
            display: flex !important;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1002;
            -webkit-user-select: none;
        }
        
        .btn:active {
            transform: scale(0.98);
        }
        
        .btn-halloween {
            background: linear-gradient(135deg, #ff7b25, #ff5500);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #10b981, #059669);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f59e0b, #d97706);
        }
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            height: 100dvh;
            background: var(--bg-color);
            position: relative;
            z-index: 1000;
        }
        
        /* Уведомления */
        .notification-toast {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 3000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        /* Оптимизированный чат-интерфейс */
        .chat-container {
            display: flex;
            height: 100%;
            width: 100%;
            position: relative;
            z-index: 1000;
        }
        
        .sidebar {
            width: 100%;
            max-width: 400px;
            background: var(--card-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 1001;
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 1001;
            min-width: 0;
        }
        
        .search-box {
            padding: 15px;
            border-bottom: 1px solid var(--border-color);
            flex-shrink: 0;
        }
        
        .search-input {
            width: 100%;
            padding: 12px 15px;
            background: var(--secondary-color);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 14px;
        }
        
        .chats-list {
            flex: 1;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .chat-item {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
            position: relative;
            z-index: 1002;
            min-height: 70px;
        }
        
        .chat-item:active {
            background: var(--secondary-color);
        }
        
        .chat-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            margin-right: 12px;
            flex-shrink: 0;
        }
        
        .chat-info {
            flex: 1;
            min-width: 0;
        }
        
        .chat-name {
            font-weight: bold;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 15px;
        }
        
        .chat-last-message {
            color: #888;
            font-size: 13px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .chat-time {
            color: #888;
            font-size: 11px;
            flex-shrink: 0;
            margin-left: 8px;
        }
        
        .messages-container {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            display: flex;
            flex-direction: column;
            gap: 8px;
            position: relative;
            z-index: 1001;
        }
        
        .message {
            background: var(--secondary-color);
            padding: 10px 12px;
            border-radius: 15px;
            max-width: 85%;
            word-wrap: break-word;
            position: relative;
            z-index: 1002;
            animation: fadeIn 0.2s ease-out;
        }
        
        .message.own {
            background: var(--accent-color);
            align-self: flex-end;
        }
        
        .message-input-container {
            padding: 15px;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 8px;
            align-items: center;
            position: relative;
            z-index: 1001;
            flex-shrink: 0;
        }
        
        .message-input {
            flex: 1;
            padding: 12px 15px;
            background: var(--secondary-color);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            color: var(--text-color);
            font-size: 14px;
        }
        
        .send-btn {
            padding: 12px 18px;
            background: var(--accent-color);
            border: none;
            border-radius: 25px;
            color: white;
            cursor: pointer;
            min-width: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1002;
            flex-shrink: 0;
        }
        
        .online-indicator {
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            position: absolute;
            bottom: 2px;
            right: 2px;
            border: 2px solid var(--card-color);
        }
        
        /* Мобильная оптимизация */
        .mobile-only {
            display: none;
        }
        
        .desktop-only {
            display: block;
        }
        
        /* Навигация для мобильных */
        .mobile-nav {
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--card-color);
            border-top: 1px solid var(--border-color);
            padding: 10px 15px;
            padding-bottom: calc(10px + var(--safe-area-bottom));
            z-index: 2000;
        }
        
        .nav-button {
            flex: 1;
            padding: 12px;
            background: transparent;
            border: none;
            color: var(--text-color);
            text-align: center;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .nav-button.active {
            color: var(--accent-color);
            transform: translateY(-2px);
        }
        
        /* Адаптивные стили */
        @media (max-width: 768px) {
            .screen {
                padding: 15px;
                padding-top: calc(15px + var(--safe-area-top));
                padding-bottom: calc(15px + var(--safe-area-bottom));
            }
            
            .auth-box {
                padding: 25px 20px;
                max-width: 95vw;
            }
            
            .mobile-only {
                display: block;
            }
            
            .desktop-only {
                display: none;
            }
            
            .chat-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                max-width: none;
                display: none;
            }
            
            .sidebar.active {
                display: flex;
            }
            
            .chat-area {
                display: none;
            }
            
            .chat-area.active {
                display: flex;
            }
            
            .mobile-nav {
                display: flex;
                justify-content: space-around;
            }
            
            .message {
                max-width: 90%;
            }
            
            .chat-item {
                padding: 10px 12px;
                min-height: 60px;
            }
            
            .chat-avatar {
                width: 40px;
                height: 40px;
                font-size: 16px;
            }
            
            .btn {
                min-height: 44px;
                padding: 14px;
            }
        }
        
        @media (min-width: 769px) {
            .sidebar {
                display: flex !important;
            }
            
            .chat-area {
                display: flex !important;
            }
        }
        
        /* Оптимизация производительности */
        .will-change {
            will-change: transform, opacity;
        }
        
        .no-animation {
            animation: none !important;
        }
        
        /* Улучшенный скроллбар */
        .chats-list::-webkit-scrollbar,
        .messages-container::-webkit-scrollbar {
            width: 4px;
        }
        
        .chats-list::-webkit-scrollbar-track,
        .messages-container::-webkit-scrollbar-track {
            background: transparent;
        }
        
        .chats-list::-webkit-scrollbar-thumb,
        .messages-container::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 2px;
        }
        
        /* Предотвращение выделения текста на мобильных */
        .no-select {
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Новые компоненты для функций */
        .emoji-picker {
            position: absolute;
            bottom: 70px;
            right: 15px;
            background: var(--card-color);
            border: 1px solid var(--border-color);
            border-radius: 15px;
            padding: 10px;
            display: none;
            grid-template-columns: repeat(6, 1fr);
            gap: 5px;
            max-width: 250px;
            z-index: 2000;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .emoji-btn {
            padding: 8px;
            background: transparent;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s ease;
        }
        
        .emoji-btn:hover, .emoji-btn:active {
            background: var(--secondary-color);
            transform: scale(1.1);
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: var(--secondary-color);
            border-radius: 15px;
            max-width: 100px;
            font-size: 12px;
            color: #888;
        }
        
        .typing-dots {
            display: flex;
            gap: 3px;
        }
        
        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--accent-color);
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        
        .context-menu {
            position: fixed;
            background: var(--card-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 8px 0;
            z-index: 3000;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            display: none;
        }
        
        .context-item {
            padding: 10px 15px;
            background: transparent;
            border: none;
            color: var(--text-color);
            text-align: left;
            width: 100%;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .context-item:hover, .context-item:active {
            background: var(--secondary-color);
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 6px;
        }
        
        .status-online { background: #10b981; }
        .status-offline { background: #6b7280; }
        .status-away { background: #f59e0b; }
        
        /* Стили для настроек с прокруткой */
        .settings-container {
            height: 100%;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            padding: 20px;
        }
        
        .settings-section {
            background: var(--card-color);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            border: 1px solid var(--border-color);
        }
        
        .settings-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: var(--accent-color);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Стили для новых функций */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .feature-card {
            background: var(--secondary-color);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }
        
        .feature-card:hover, .feature-card:active {
            border-color: var(--accent-color);
            transform: translateY(-3px);
        }
        
        .feature-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .credential-box {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border: 1px solid var(--accent-color);
        }
        
        .credential-field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 8px 0;
            gap: 10px;
        }
        
        .credential-value {
            font-family: monospace;
            background: var(--card-color);
            padding: 5px 10px;
            border-radius: 5px;
            flex: 1;
            word-break: break-all;
            font-size: 14px;
        }
        
        .copy-btn {
            background: var(--accent-color);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            flex-shrink: 0;
            transition: all 0.2s ease;
        }
        
        .copy-btn:active {
            transform: scale(0.95);
        }
        
        /* Стили для декоративных элементов */
        .decorative-emoji {
            position: fixed;
            font-size: 24px;
            z-index: 99;
            opacity: 0.1;
            animation: float 8s ease-in-out infinite;
            pointer-events: none;
        }
        
        /* Стили для новых функций чата */
        .message-actions {
            position: absolute;
            top: -10px;
            right: 10px;
            display: none;
            gap: 5px;
        }
        
        .message:hover .message-actions {
            display: flex;
        }
        
        .action-btn {
            background: var(--card-color);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 12px;
        }
        
        .voice-message-btn {
            background: var(--accent-color);
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            margin-left: 10px;
        }
        
        .voice-recording {
            animation: pulse 1s infinite;
            background: #ef4444 !important;
        }
        
        /* Стили для групп */
        .group-avatar {
            background: linear-gradient(135deg, #8b5cf6, #7e22ce);
            position: relative;
        }
        
        .group-members {
            font-size: 11px;
            color: #888;
        }
        
        /* Оптимизация для медленных устройств */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        /* Стили для ошибок */
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
    </style>
</head>
<body>
    <!-- Декоративные элементы (только тыква, призрак и сердечко) -->
    <div class="decorative-emoji" style="top: 10%; left: 5%;">🎃</div>
    <div class="decorative-emoji" style="top: 15%; right: 8%;">👻</div>
    <div class="decorative-emoji" style="top: 85%; left: 10%;">💜</div>
    <div class="decorative-emoji" style="top: 80%; right: 5%;">🎃</div>

    <!-- ПЕРВАЯ СТРАНИЦА - НАЧАТЬ ОБЩЕНИЕ -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle">Хеллоуин 2025 Edition! Улучшенный чат с новыми функциями</div>
            
            <button class="btn pulse no-select" onclick="startQuickRegistration()">
                <span>💬 Начать общение</span>
            </button>
            
            <div class="feature-grid">
                <div class="feature-card no-select" onclick="startQuickRegistration()">
                    <div class="feature-icon">🚀</div>
                    <div>Быстрый старт</div>
                </div>
                <div class="feature-card no-select" onclick="showManualLogin()">
                    <div class="feature-icon">🔐</div>
                    <div>Ручной вход</div>
                </div>
                <div class="feature-card no-select" onclick="showFeatures()">
                    <div class="feature-icon">⭐</div>
                    <div>Возможности</div>
                </div>
            </div>
        </div>
    </div>

    <!-- РУЧНОЙ ВХОД -->
    <div id="manualLoginScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🔐 Вход</div>
            <div class="subtitle">Войдите в существующий аккаунт</div>
            
            <input type="text" class="input-field" id="loginUsername" placeholder="👤 Имя пользователя">
            <input type="password" class="input-field" id="loginPassword" placeholder="🔐 Пароль">
            
            <button class="btn btn-success no-select" onclick="manualLogin()">
                <span>🚀 Войти в аккаунт</span>
            </button>
            
            <button class="btn no-select" onclick="showScreen('screen1')">
                <span>← Назад</span>
            </button>
            
            <div id="loginError" class="error hidden" style="margin-top: 15px;"></div>
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
                    <button class="copy-btn no-select" onclick="copyToClipboard('generatedPassword')">📋</button>
                </div>
                <div class="credential-field">
                    <span>🆔 Юзернейм:</span>
                    <span class="credential-value" id="generatedUsername">...</span>
                </div>
            </div>
            
            <button class="btn btn-success pulse no-select" onclick="quickRegister()">
                <span>🚀 Продолжить в чат!</span>
            </button>
            
            <button class="btn no-select" onclick="generateNewCredentials()">
                <span>🔄 Сгенерировать заново</span>
            </button>
            
            <button class="btn no-select" onclick="showScreen('screen1')">
                <span>← Назад</span>
            </button>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <!-- Интерфейс будет генерироваться JavaScript -->
    </div>

    <!-- Мобильная навигация -->
    <div class="mobile-nav" id="mobileNav" style="display: none;">
        <button class="nav-button active no-select" onclick="showMobileView('chats')">
            <div style="font-size: 20px;">💬</div>
            <div>Чаты</div>
        </button>
        <button class="nav-button no-select" onclick="showMobileView('contacts')">
            <div style="font-size: 20px;">👥</div>
            <div>Контакты</div>
        </button>
        <button class="nav-button no-select" onclick="showMobileView('settings')">
            <div style="font-size: 20px;">⚙️</div>
            <div>Настройки</div>
        </button>
    </div>

    <!-- Emoji Picker -->
    <div class="emoji-picker" id="emojiPicker">
        <button class="emoji-btn" onclick="addEmoji('😊')">😊</button>
        <button class="emoji-btn" onclick="addEmoji('😂')">😂</button>
        <button class="emoji-btn" onclick="addEmoji('🥰')">🥰</button>
        <button class="emoji-btn" onclick="addEmoji('😎')">😎</button>
        <button class="emoji-btn" onclick="addEmoji('🤔')">🤔</button>
        <button class="emoji-btn" onclick="addEmoji('🎉')">🎉</button>
        <button class="emoji-btn" onclick="addEmoji('🚀')">🚀</button>
        <button class="emoji-btn" onclick="addEmoji('💜')">💜</button>
        <button class="emoji-btn" onclick="addEmoji('🎃')">🎃</button>
        <button class="emoji-btn" onclick="addEmoji('👻')">👻</button>
        <button class="emoji-btn" onclick="addEmoji('⭐')">⭐</button>
        <button class="emoji-btn" onclick="addEmoji('🔥')">🔥</button>
    </div>

    <!-- Context Menu -->
    <div class="context-menu" id="contextMenu">
        <button class="context-item no-select" onclick="copyMessage()">📋 Копировать</button>
        <button class="context-item no-select" onclick="deleteMessage()">🗑️ Удалить</button>
        <button class="context-item no-select" onclick="replyToMessage()">↩️ Ответить</button>
        <button class="context-item no-select" onclick="hideContextMenu()">✖️ Закрыть</button>
    </div>

    <script>
        let currentUser = null;
        let currentChat = null;
        let chats = [];
        let allUsers = [];
        let isHalloweenTheme = false;
        let currentTheme = 'purple';
        let userStats = {
            messagesSent: 0,
            chatsCreated: 0,
            logins: 0,
            timeSpent: 0,
            voiceMessages: 0,
            groupsCreated: 0
        };
        let isMobile = false;
        let currentMobileView = 'chats';
        let selectedMessage = null;
        let onlineUsers = new Set();
        let isRecording = false;
        let mediaRecorder = null;
        let audioChunks = [];

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🎃 DLtrollex Хеллоуин 2025 загружен!");
            detectDeviceType();
            initializeApp();
        });

        function detectDeviceType() {
            isMobile = window.innerWidth <= 768;
            console.log(`📱 Устройство: ${isMobile ? 'Мобильное' : 'Десктоп'}`);
        }

        function initializeApp() {
            checkAutoLogin();
            loadHalloweenTheme();
           
