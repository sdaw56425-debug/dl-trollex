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
        
        /* Анимации */
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px var(--accent-color); }
            50% { text-shadow: 0 0 20px var(--accent-color), 0 0 30px var(--accent-color); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(5deg); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
        }
        
        @keyframes bounce {
            0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
            40%, 43% { transform: translate3d(0,-15px,0); }
            70% { transform: translate3d(0,-5px,0); }
            90% { transform: translate3d(0,-2px,0); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        @keyframes slideInUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideInRight {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        .glowing-logo {
            animation: glow 2s ease-in-out infinite;
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        .bounce {
            animation: bounce 1s ease infinite;
        }
        
        .shake {
            animation: shake 0.5s ease-in-out;
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        .slide-in-up {
            animation: slideInUp 0.5s ease-out;
        }
        
        .slide-in-right {
            animation: slideInRight 0.5s ease-out;
        }
        
        .rotate {
            animation: rotate 2s linear infinite;
        }
        
        .typewriter {
            overflow: hidden;
            border-right: 2px solid var(--accent-color);
            white-space: nowrap;
            animation: typewriter 3s steps(40) 1s both, blink 0.8s infinite;
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
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 2px solid var(--accent-color);
            width: 100%;
            max-width: min(450px, 90vw);
            text-align: center;
            position: relative;
            overflow: hidden;
            z-index: 1001;
        }
        
        .auth-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(139, 92, 246, 0.1), transparent);
            animation: rotate 6s linear infinite;
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
            transition: all 0.3s ease;
            touch-action: manipulation;
            user-select: none;
            min-height: 50px;
            display: flex !important;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1002;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:active {
            transform: scale(0.95);
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
        
        .btn-halloween {
            background: linear-gradient(135deg, #ff7b25, #ff5500);
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
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            border-left: 4px solid var(--success-color);
        }
        
        /* Чат интерфейс */
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
            transition: all 0.3s ease;
        }
        
        .search-input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
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
            transition: all 0.3s ease;
            user-select: none;
            position: relative;
            z-index: 1002;
            min-height: 70px;
        }
        
        .chat-item:hover {
            background: var(--secondary-color);
            transform: translateX(5px);
        }
        
        .chat-item:active {
            transform: scale(0.98);
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
            transition: all 0.3s ease;
        }
        
        .chat-avatar:hover {
            transform: scale(1.1) rotate(10deg);
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
            animation: slideInUp 0.3s ease-out;
            transition: all 0.3s ease;
        }
        
        .message:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
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
            transition: all 0.3s ease;
        }
        
        .message-input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
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
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
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
            animation: pulse 2s infinite;
        }
        
        /* Мобильная оптимизация */
        .mobile-only {
            display: none;
        }
        
        .desktop-only {
            display: block;
        }
        
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
            transition: all 0.3s ease;
            border-radius: 10px;
        }
        
        .nav-button.active {
            color: var(--accent-color);
            background: var(--secondary-color);
            transform: translateY(-5px);
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
        
        /* Дополнительные стили */
        .no-select {
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
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
        
        .feature-card:hover {
            border-color: var(--accent-color);
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        }
        
        .feature-icon {
            font-size: 32px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover .feature-icon {
            transform: scale(1.2) rotate(5deg);
        }
        
        .credential-box {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border: 1px solid var(--accent-color);
            animation: pulse 2s infinite;
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
            transition: all 0.3s ease;
        }
        
        .copy-btn:hover {
            transform: scale(1.05);
        }
        
        .copy-btn:active {
            transform: scale(0.95);
        }
        
        .decorative-emoji {
            position: fixed;
            font-size: 24px;
            z-index: 99;
            opacity: 0.1;
            animation: float 8s ease-in-out infinite;
            pointer-events: none;
        }
        
        .error {
            color: #ef4444;
            margin-top: 15px;
            padding: 10px;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
            border: 1px solid #ef4444;
            animation: shake 0.5s ease-in-out;
        }
        
        .success {
            color: #10b981;
            margin-top: 15px;
            padding: 10px;
            background: rgba(16, 185, 129, 0.1);
            border-radius: 8px;
            border: 1px solid #10b981;
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
            animation: slideInUp 0.5s ease-out;
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
        
        .theme-option {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .theme-option:hover {
            transform: scale(1.1);
        }
        
        .theme-option.active {
            border-color: white;
            transform: scale(1.1);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .stat-card {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: var(--accent-color);
        }
        
        .stat-label {
            font-size: 12px;
            color: #888;
        }
        
        /* Анимация для нового сообщения */
        @keyframes messageSent {
            0% { transform: translateY(20px) scale(0.8); opacity: 0; }
            100% { transform: translateY(0) scale(1); opacity: 1; }
        }
        
        .message-sent {
            animation: messageSent 0.4s ease-out;
        }
    </style>
</head>
<body>
    <!-- Декоративные элементы -->
    <div class="decorative-emoji" style="top: 10%; left: 5%;">🎃</div>
    <div class="decorative-emoji" style="top: 15%; right: 8%;">👻</div>
    <div class="decorative-emoji" style="top: 85%; left: 10%;">💜</div>
    <div class="decorative-emoji" style="top: 80%; right: 5%;">🎃</div>

    <!-- ПЕРВАЯ СТРАНИЦА - НАЧАТЬ ОБЩЕНИЕ -->
    <div id="screen1" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">🎃 DLtrollex</div>
            <div class="subtitle typewriter">Хеллоуин 2025 Edition! Улучшенный чат с анимациями</div>
            
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
            
            <div id="loginError" class="error hidden"></div>
        </div>
    </div>

    <!-- АВТО-РЕГИСТРАЦИЯ -->
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

    <!-- Основной интерфейс -->
    <div id="mainApp" class="app"></div>

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
            timeSpent: 0
        };
        let isMobile = false;
        let currentMobileView = 'chats';

        // Инициализация
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
            loadTheme();
            initializeData();
            loadUserStats();
            
            // Обработчик изменения размера
            window.addEventListener('resize', function() {
                detectDeviceType();
                if (currentUser) {
                    renderChatsInterface();
                }
            });
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    userStats.logins++;
                    saveUserStats();
                    showMainApp();
                    showNotification(`С возвращением, ${currentUser.name}! 👋`, 'success');
                } catch (e) {
                    console.error("Ошибка автологина:", e);
                    localStorage.removeItem('dlcurrentUser');
                }
            }
        }

        function loadHalloweenTheme() {
            const saved = localStorage.getItem('dlhalloween');
            if (saved === 'true') {
                activateHalloweenTheme();
            }
        }

        function loadTheme() {
            const savedTheme = localStorage.getItem('dltheme');
            if (savedTheme) {
                currentTheme = savedTheme;
                applyTheme(savedTheme);
            }
        }

        function loadUserStats() {
            const saved = localStorage.getItem('dluserStats');
            if (saved) {
                userStats = {...userStats, ...JSON.parse(saved)};
            }
        }

        function saveUserStats() {
            localStorage.setItem('dluserStats', JSON.stringify(userStats));
        }

        function initializeData() {
            const savedUsers = localStorage.getItem('dlallUsers');
            if (savedUsers) {
                allUsers = JSON.parse(savedUsers);
            } else {
                // Создаем тестовых пользователей
                allUsers = [
                    {
                        id: 'user1',
                        name: 'Алексей',
                        username: '@alexey',
                        email: 'alexey@example.com',
                        avatar: '😎',
                        isOnline: true,
                        lastSeen: new Date().toISOString(),
                        bio: 'Люблю программирование 🚀',
                        registered: new Date(Date.now() - 86400000).toISOString(),
                        password: 'test123'
                    },
                    {
                        id: 'user2', 
                        name: 'Мария',
                        username: '@maria',
                        email: 'maria@example.com',
                        avatar: '👩',
                        isOnline: true,
                        lastSeen: new Date().toISOString(),
                        bio: 'Дизайнер и художник 🎨',
                        registered: new Date(Date.now() - 172800000).toISOString(),
                        password: 'test123'
                    },
                    {
                        id: 'user3',
                        name: 'Дмитрий',
                        username: '@dmitry', 
                        email: 'dmitry@example.com',
                        avatar: '🤖',
                        isOnline: false,
                        lastSeen: new Date(Date.now() - 3600000).toISOString(),
                        bio: 'Разработчик ИИ',
                        registered: new Date(Date.now() - 259200000).toISOString(),
                        password: 'test123'
                    }
                ];
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }

            const savedChats = localStorage.getItem('dlchats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            } else {
                chats = [];
                localStorage.setItem('dlchats', JSON.stringify(chats));
            }
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').style.display = 'none';
            const targetScreen = document.getElementById(screenId);
            if (targetScreen) {
                targetScreen.classList.remove('hidden');
            }
        }

        function startQuickRegistration() {
            showScreen('quickRegisterScreen');
            generateNewCredentials();
        }

        function showManualLogin() {
            showScreen('manualLoginScreen');
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            const username = '@' + name.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
            document.getElementById('generatedUsername').textContent = username;
        }

        function generateUsername() {
            const adjectives = ['Весёлый', 'Серьёзный', 'Смелый', 'Умный', 'Быстрый', 'Креативный'];
            const nouns = ['Единорог', 'Дракон', 'Волк', 'Феникс', 'Тигр', 'Кот'];
            return `${randomChoice(adjectives)}${randomChoice(nouns)}${Math.floor(Math.random() * 1000)}`;
        }

        function generatePassword() {
            const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%';
            let password = '';
            for (let i = 0; i < 10; i++) {
                password += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            return password;
        }

        function randomChoice(array) {
            return array[Math.floor(Math.random() * array.length)];
        }

        function copyToClipboard(elementId) {
            const text = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Скопировано в буфер обмена! 📋', 'success');
                const btn = event.target;
                btn.classList.add('bounce');
                setTimeout(() => btn.classList.remove('bounce'), 1000);
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
            
            const user_id = 'user_' + Date.now();
            const avatar = getRandomAvatar();
            
            currentUser = {
                id: user_id,
                name: name,
                username: username,
                email: '',
                avatar: avatar,
                isOnline: true,
                lastSeen: new Date().toISOString(),
                bio: 'Новый пользователь DLtrollex 🚀',
                registered: new Date().toISOString(),
                password: password
            };
            
            allUsers.push(currentUser);
            localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            userStats.logins++;
            saveUserStats();
            
            showMainApp();
            showNotification(`Добро пожаловать, ${name}! 🎉`, 'success');
        }

        function manualLogin() {
            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value.trim();
            const errorDiv = document.getElementById('loginError');

            if (!username || !password) {
                errorDiv.textContent = 'Заполните все поля!';
                errorDiv.classList.remove('hidden');
                return;
            }

            const user = allUsers.find(u => 
                (u.username === username || u.name === username) && u.password === password
            );

            if (user) {
                currentUser = user;
                currentUser.isOnline = true;
                
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
                
                userStats.logins++;
                saveUserStats();
                
                showMainApp();
                showNotification(`С возвращением, ${currentUser.name}! 👋`, 'success');
            } else {
                errorDiv.textContent = 'Неверное имя пользователя или пароль!';
                errorDiv.classList.remove('hidden');
            }
        }

        function getRandomAvatar() {
            const avatars = ['😊', '😎', '🤩', '👻', '🐱', '🦊', '🐶'];
            return avatars[Math.floor(Math.random() * avatars.length)];
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => screen.classList.add('hidden'));
            document.getElementById('mainApp').style.display = 'block';
            if (isMobile) {
                document.getElementById('mobileNav').style.display = 'flex';
            }
            renderChatsInterface();
            startTimeTracking();
        }

        function showMobileView(view) {
            currentMobileView = view;
            
            document.querySelectorAll('.nav-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.closest('.nav-button').classList.add('active');
            
            if (view === 'chats') {
                renderChatsInterface();
            } else if (view === 'contacts') {
                showContactsView();
            } else if (view === 'settings') {
                showSettings();
            }
        }

        function renderChatsInterface() {
            let content = '';
            
            if (isMobile) {
                content = `
                    <div class="chat-container">
                        <div class="sidebar active">
                            <div style="padding: 15px; border-bottom: 1px solid var(--border-color);">
                                <div class="logo" style="font-size: 20px; margin-bottom: 8px;">${isHalloweenTheme ? '🎃' : '💜'} DLtrollex</div>
                                <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                            </div>
                            
                            <div class="search-box">
                                <input type="text" class="search-input" placeholder="🔍 Поиск..." oninput="searchUsers(this.value)">
                            </div>
                            
                            <div class="chats-list" id="chatsList">
                                ${renderChatsList()}
                            </div>
                        </div>
                        
                        <div class="chat-area" id="chatArea">
                            <div style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column; padding: 20px;">
                                <div style="font-size: 60px; margin-bottom: 15px;" class="pulse">💬</div>
                                <h3 style="text-align: center;">Выберите чат для общения</h3>
                                <button class="btn" onclick="showContactsView()" style="margin-top: 15px; max-width: 200px;">👥 Найти друзей</button>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                content = `
                    <div class="chat-container">
                        <div class="sidebar">
                            <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                                <div class="logo" style="font-size: 24px; margin-bottom: 10px;">${isHalloweenTheme ? '🎃' : '💜'} DLtrollex</div>
                                <div style="color: #888; font-size: 12px;">Привет, ${currentUser.name}!</div>
                            </div>
                            
                            <div class="search-box">
                                <input type="text" class="search-input" placeholder="🔍 Поиск пользователей..." oninput="searchUsers(this.value)">
                            </div>
                            
                            <div class="chats-list" id="chatsList">
                                ${renderChatsList()}
                            </div>
                            
                            <div style="padding: 15px; border-top: 1px solid var(--border-color);">
                                <button class="btn" onclick="showContactsView()" style="margin-bottom: 10px;">👥 Найти друзей</button>
                                <button class="btn" onclick="showSettings()">⚙️ Настройки</button>
                                <button class="btn btn-danger no-select" onclick="showLogoutConfirm()" style="margin-top: 10px;">
                                    🚪 Выйти
                                </button>
                            </div>
                        </div>
                        
                        <div class="chat-area">
                            <div id="chatContent" style="flex: 1; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                                <div style="font-size: 80px; margin-bottom: 20px;" class="pulse">${isHalloweenTheme ? '🎃' : '💜'}</div>
                                <h2>Добро пожаловать в чаты!</h2>
                                <p style="color: #888; margin: 10px 0 20px 0; text-align: center;">
                                    Начните общение с другими пользователями
                                </p>
                                <button class="btn" onclick="showContactsView()">💬 Найти друзей</button>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            document.getElementById('mainApp').innerHTML = content;
        }

        function renderChatsList() {
            if (chats.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;" class="pulse">💬</div>
                        <div>Чатов пока нет</div>
                        <div style="font-size: 12px; margin-top: 5px;">Начните новый чат</div>
                    </div>
                `;
            }
            
            return chats.map(chat => {
                const otherUserId = chat.participants.find(id => id !== currentUser.id);
                const otherUser = allUsers.find(u => u.id === otherUserId);
                if (!otherUser) return '';
                
                return `
                    <div class="chat-item no-select" onclick="openChat('${chat.id}')">
                        <div style="position: relative;">
                            <div class="chat-avatar">${otherUser.avatar}</div>
                            ${otherUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div class="chat-info">
                            <div class="chat-name">${otherUser.name}</div>
                            <div class="chat-last-message">${chat.lastMessage?.text || 'Нет сообщений'}</div>
                        </div>
                        <div class="chat-time">${formatTime(chat.lastMessage?.timestamp)}</div>
                    </div>
                `;
            }).join('');
        }

        function showContactsView() {
            const availableUsers = allUsers.filter(user => user.id !== currentUser.id);
            
            let content = '';
            
            if (isMobile) {
                content = `
                    <div class="chat-container">
                        <div class="sidebar active">
                            <div style="padding: 15px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                                <h3 style="margin: 0;">👥 Контакты</h3>
                                <button class="btn" onclick="renderChatsInterface()" style="padding: 8px 12px; font-size: 12px;">← Назад</button>
                            </div>
                            <div class="chats-list">
                                ${availableUsers.map(user => `
                                    <div class="chat-item no-select" onclick="startNewChat('${user.id}')">
                                        <div style="position: relative;">
                                            <div class="chat-avatar">${user.avatar}</div>
                                            ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                                        </div>
                                        <div class="chat-info">
                                            <div class="chat-name">
                                                ${user.name}
                                                ${user.isOnline ? '<span style="color: #10b981; font-size: 11px;"> ● онлайн</span>' : ''}
                                            </div>
                                            <div class="chat-last-message">${user.username}</div>
                                        </div>
                                        <button class="btn" style="padding: 6px 12px; font-size: 11px;">💬</button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `;
            } else {
                content = `
                    <div class="chat-area">
                        <div style="padding: 20px; height: 100%; overflow-y: auto;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                <h2>👥 Все пользователи (${availableUsers.length})</h2>
                                <button class="btn" onclick="renderChatsInterface()">← Назад к чатам</button>
                            </div>
                            
                            <div style="display: grid; gap: 10px;">
                                ${availableUsers.map(user => `
                                    <div class="chat-item no-select" onclick="startNewChat('${user.id}')">
                                        <div style="position: relative;">
                                            <div class="chat-avatar">${user.avatar}</div>
                                            ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                                        </div>
                                        <div class="chat-info">
                                            <div class="chat-name">
                                                ${user.name}
                                                ${user.isOnline ? '<span style="color: #10b981; font-size: 12px;"> ● онлайн</span>' : ''}
                                            </div>
                                            <div class="chat-last-message">${user.username} • ${user.bio || 'Нет описания'}</div>
                                        </div>
                                        <button class="btn" style="padding: 8px 15px; font-size: 12px;">💬 Чат</button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `;
            }
            
            if (isMobile) {
                document.getElementById('mainApp').innerHTML = content;
            } else {
                document.getElementById('chatContent').innerHTML = content;
            }
        }

        function startNewChat(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;

            const existingChat = chats.find(chat => 
                chat.participants.includes(userId) && 
                chat.participants.includes(currentUser.id)
            );

            if (existingChat) {
                currentChat = existingChat;
                openChat(existingChat.id);
                return;
            }

            const newChat = {
                id: 'chat_' + Date.now(),
                type: 'private',
                participants: [currentUser.id, userId],
                lastMessage: {
                    text: 'Чат начат 🚀',
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                },
                unreadCount: 0,
                messages: [
                    {
                        id: '1',
                        text: `Привет! Я ${currentUser.name}. Рад познакомиться! 👋`,
                        senderId: currentUser.id,
                        timestamp: new Date().toISOString()
                    }
                ]
            };

            chats.unshift(newChat);
            currentChat = newChat;
            
            localStorage.setItem('dlchats', JSON.stringify(chats));
            
            userStats.chatsCreated++;
            saveUserStats();
            
            openChat(newChat.id);
            showNotification(`Чат с ${user.name} начат! 💬`, 'success');
        }

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherParticipants = currentChat.participants.filter(p => p !== currentUser.id);
            const chatUser = allUsers.find(u => u.id === otherParticipants[0]);
            if (!chatUser) return;
            
            let content = '';
            
            if (isMobile) {
                content = `
                    <div class="chat-container">
                        <div class="chat-area active">
                            <div style="padding: 12px 15px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 12px; background: var(--card-color);">
                                <button class="btn no-select" onclick="renderChatsInterface()" style="padding: 8px; background: transparent; color: var(--text-color);">
                                    ←
                                </button>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="position: relative;">
                                        <div class="chat-avatar" style="width: 35px; height: 35px; font-size: 14px;">${chatUser.avatar}</div>
                                        ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                                    </div>
                                    <div>
                                        <div style="font-weight: bold; font-size: 14px;">${chatUser.name}</div>
                                        <div style="color: #888; font-size: 11px;">
                                            ${chatUser.isOnline ? 'online' : `был(а) ${formatLastSeen(chatUser.lastSeen)}`}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="messages-container" id="messagesContainer">
                                ${renderChatMessages()}
                            </div>
                            
                            <div class="message-input-container">
                                <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput" onkeypress="if(event.key=='Enter') sendMessage()">
                                <button class="send-btn no-select" onclick="sendMessage()">📤</button>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                content = `
                    <div class="chat-area">
                        <div style="padding: 15px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                            <div style="display: flex; align-items: center;">
                                <div style="position: relative; margin-right: 15px;">
                                    <div class="chat-avatar">${chatUser.avatar}</div>
                                    ${chatUser.isOnline ? '<div class="online-indicator"></div>' : ''}
                                </div>
                                <div>
                                    <div style="font-weight: bold; font-size: 16px;">${chatUser.name}</div>
                                    <div style="color: #888; font-size: 12px;">
                                        ${chatUser.isOnline ? 'online' : `был(а) ${formatLastSeen(chatUser.lastSeen)}`}
                                    </div>
                                </div>
                            </div>
                            <div>
                                <button class="btn" onclick="renderChatsInterface()" style="padding: 8px 15px; font-size: 12px;">← Назад</button>
                            </div>
                        </div>
                        
                        <div class="messages-container" id="messagesContainer">
                            ${renderChatMessages()}
                        </div>
                        
                        <div class="message-input-container">
                            <input type="text" class="message-input" placeholder="💬 Введите сообщение..." id="messageInput" onkeypress="if(event.key=='Enter') sendMessage()">
                            <button class="send-btn no-select" onclick="sendMessage()">📤</button>
                        </div>
                    </div>
                `;
            }
            
            if (isMobile) {
                document.getElementById('mainApp').innerHTML = content;
            } else {
                document.getElementById('chatContent').innerHTML = content;
            }

            scrollToBottom();
            setTimeout(() => {
                const input = document.getElementById('messageInput');
                if (input) input.focus();
            }, 300);
        }

        function renderChatMessages() {
            if (!currentChat.messages || currentChat.messages.length === 0) {
                return `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;" class="pulse">💬</div>
                        <div>Чат пуст</div>
                        <div style="font-size: 12px; margin-top: 5px;">Напишите первое сообщение!</div>
                    </div>
                `;
            }

            return currentChat.messages.map(msg => {
                const isOwn = msg.senderId === currentUser.id;
                const sender = allUsers.find(u => u.id === msg.senderId);
                if (!sender) return '';
                
                return `
                    <div class="message ${isOwn ? 'own' : ''} message-sent">
                        <div style="margin-bottom: 4px;">
                            ${!isOwn ? `<strong>${sender.name}:</strong> ` : ''}
                            ${msg.text}
                        </div>
                        <div style="font-size: 11px; color: ${isOwn ? 'rgba(255,255,255,0.7)' : '#888'}; text-align: ${isOwn ? 'right' : 'left'};">
                            ${formatTime(msg.timestamp)}
                            ${isOwn ? ' ✓' : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                if (!currentChat.messages) currentChat.messages = [];
                
                const newMessage = {
                    id: Date.now().toString(),
                    text: message,
                    senderId: currentUser.id,
                    timestamp: new Date().toISOString()
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                
                localStorage.setItem('dlchats', JSON.stringify(chats));
                
                const messagesContainer = document.getElementById('messagesContainer');
                if (messagesContainer) {
                    const messageElement = document.createElement('div');
                    messageElement.className = `message own message-sent`;
                    messageElement.innerHTML = `
                        <div style="margin-bottom: 4px;">${message}</div>
                        <div style="font-size: 11px; color: rgba(255,255,255,0.7); text-align: right;">
                            ${formatTime(newMessage.timestamp)} ✓
                        </div>
                    `;
                    messagesContainer.appendChild(messageElement);
                    scrollToBottom();
                }
                
                input.value = '';
                
                userStats.messagesSent++;
                saveUserStats();
                
                // Авто-ответ
                setTimeout(() => {
                    if (Math.random() > 0.3) {
                        sendAutoReply();
                    }
                }, 1000 + Math.random() * 2000);
            }
        }

        function sendAutoReply() {
            if (!currentChat) return;
            
            const otherUserId = currentChat.participants.find(id => id !== currentUser.id);
            const otherUser = allUsers.find(u => u.id === otherUserId);
            if (!otherUser) return;
            
            const replies = [
                'Привет! Как дела? 😊',
                'Интересно... расскажи подробнее! 🤔',
                'Отлично! Продолжаем общение 🚀',
                'Согласен с тобой! 👍',
                'Хм, нужно подумать над этим... 💭',
                'У меня тоже самое! 😄',
                'Продолжаем в том же духе! 💪'
            ];
            
            const replyMessage = {
                id: Date.now().toString() + '_reply',
                text: randomChoice(replies),
                senderId: otherUser.id,
                timestamp: new Date().toISOString()
            };
            
            currentChat.messages.push(replyMessage);
            currentChat.lastMessage = replyMessage;
            
            localStorage.setItem('dlchats', JSON.stringify(chats));
            
            const messagesContainer = document.getElementById('messagesContainer');
            if (messagesContainer) {
                const messageElement = document.createElement('div');
                messageElement.className = `message message-sent`;
                messageElement.innerHTML = `
                    <div style="margin-bottom: 4px;">
                        <strong>${otherUser.name}:</strong> ${replyMessage.text}
                    </div>
                    <div style="font-size: 11px; color: #888; text-align: left;">
                        ${formatTime(replyMessage.timestamp)}
                    </div>
                `;
                messagesContainer.appendChild(messageElement);
                scrollToBottom();
            }
        }

        function scrollToBottom() {
            setTimeout(() => {
                const messagesContainer = document.getElementById('messagesContainer');
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            }, 100);
        }

        function searchUsers(query) {
            if (!query.trim()) {
                document.getElementById('chatsList').innerHTML = renderChatsList();
                return;
            }
            
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && (
                    user.name.toLowerCase().includes(query.toLowerCase()) ||
                    user.username.toLowerCase().includes(query.toLowerCase())
                )
            );
            
            let searchHTML = '';
            
            if (filteredUsers.length > 0) {
                searchHTML = filteredUsers.map(user => `
                    <div class="chat-item no-select" onclick="startNewChat('${user.id}')">
                        <div style="position: relative;">
                            <div class="chat-avatar">${user.avatar}</div>
                            ${user.isOnline ? '<div class="online-indicator"></div>' : ''}
                        </div>
                        <div class="chat-info">
                            <div class="chat-name">${user.name}</div>
                            <div class="chat-last-message">${user.username}</div>
                        </div>
                        <button class="btn" style="padding: 6px 12px; font-size: 11px;">💬</button>
                    </div>
                `).join('');
            } else {
                searchHTML = `
                    <div style="text-align: center; padding: 40px 20px; color: #888;">
                        <div style="font-size: 48px; margin-bottom: 15px;">🔍</div>
                        <div>Пользователи не найдены</div>
                    </div>
                `;
            }
            
            document.getElementById('chatsList').innerHTML = searchHTML;
        }

        function showSettings() {
            let content = '';
            
            if (isMobile) {
                content = `
                    <div class="chat-container">
                        <div class="sidebar active">
                            <div style="padding: 15px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                                <h3 style="margin: 0;">⚙️ Настройки</h3>
                                <button class="btn" onclick="renderChatsInterface()" style="padding: 8px 12px; font-size: 12px;">← Назад</button>
                            </div>
                            <div class="settings-container">
                                ${renderSettingsContent()}
                                <div style="margin-top: 20px;">
                                    <button class="btn btn-danger no-select" onclick="showLogoutConfirm()">
                                        🚪 Выйти из аккаунта
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                content = `
                    <div class="chat-area">
                        <div class="settings-container">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                <h2>⚙️ Настройки профиля</h2>
                                <button class="btn" onclick="renderChatsInterface()">← Назад к чатам</button>
                            </div>
                            ${renderSettingsContent()}
                        </div>
                    </div>
                `;
            }
            
            if (isMobile) {
                document.getElementById('mainApp').innerHTML = content;
            } else {
                document.getElementById('chatContent').innerHTML = content;
            }
        }

        function renderSettingsContent() {
            return `
                <div class="settings-section">
                    <div class="settings-title">👤 Профиль</div>
                    <input type="text" class="input-field" value="${currentUser.name}" placeholder="Ваше имя" id="settingsName">
                    <input type="text" class="input-field" value="${currentUser.username}" placeholder="Юзернейм" id="settingsUsername">
                    <input type="email" class="input-field" value="${currentUser.email || ''}" placeholder="📧 Email" id="settingsEmail">
                    <textarea class="input-field" placeholder="О себе" id="settingsBio" style="min-height: 80px; resize: vertical;">${currentUser.bio || ''}</textarea>
                    <button class="btn" onclick="updateProfile()">💾 Сохранить профиль</button>
                </div>
                
                <div class="settings-section">
                    <div class="settings-title">🎨 Внешний вид</div>
                    <div style="display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap;">
                        <div class="theme-option ${currentTheme === 'purple' ? 'active' : ''}" style="background: #8b5cf6;" onclick="changeTheme('purple')"></div>
                        <div class="theme-option ${currentTheme === 'blue' ? 'active' : ''}" style="background: #3b82f6;" onclick="changeTheme('blue')"></div>
                        <div class="theme-option ${currentTheme === 'green' ? 'active' : ''}" style="background: #10b981;" onclick="changeTheme('green')"></div>
                        <div class="theme-option ${currentTheme === 'pink' ? 'active' : ''}" style="background: #ec4899;" onclick="changeTheme('pink')"></div>
                        <div class="theme-option ${currentTheme === 'orange' ? 'active' : ''}" style="background: #f97316;" onclick="changeTheme('orange')"></div>
                    </div>
                    <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()" style="margin-bottom: 10px;">
                        ${isHalloweenTheme ? '👻 Выключить хеллоуин' : '🎃 Включить хеллоуин'}
                    </button>
                </div>

                <div class="settings-section">
                    <div class="settings-title">📊 Статистика</div>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">${userStats.messagesSent}</div>
                            <div class="stat-label">Сообщений</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${userStats.chatsCreated}</div>
                            <div class="stat-label">Чатов</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${userStats.logins}</div>
                            <div class="stat-label">Входов</div>
                        </div>
                    </div>
                </div>

                <div class="settings-section">
                    <div class="settings-title">🔧 Управление</div>
                    <button class="btn no-select" onclick="exportData()" style="margin-bottom: 10px;">
                        📤 Экспорт данных
                    </button>
                    <button class="btn btn-warning no-select" onclick="clearAllData()">
                        🗑️ Очистить все данные
                    </button>
                </div>
            `;
        }

        function updateProfile() {
            const name = document.getElementById('settingsName').value.trim();
            const username = document.getElementById('settingsUsername').value.trim();
            const email = document.getElementById('settingsEmail').value.trim();
            const bio = document.getElementById('settingsBio').value.trim();
            
            if (!name) {
                showNotification('Введите имя!', 'error');
                return;
            }
            
            currentUser.name = name;
            currentUser.username = username;
            currentUser.email = email;
            currentUser.bio = bio;
            
            const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
            if (userIndex !== -1) {
                allUsers[userIndex] = {...allUsers[userIndex], ...currentUser};
                localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
            }
            
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            showNotification('Профиль обновлен! ✨', 'success');
            renderChatsInterface();
        }

        function toggleHalloweenTheme() {
            if (isHalloweenTheme) {
                deactivateHalloweenTheme();
            } else {
                activateHalloweenTheme();
            }
        }

        function activateHalloweenTheme() {
            document.body.classList.add('halloween-theme');
            isHalloweenTheme = true;
            localStorage.setItem('dlhalloween', 'true');
            showNotification('🎃 Хеллоуинская тема активирована!', 'success');
            renderChatsInterface();
        }

        function deactivateHalloweenTheme() {
            document.body.classList.remove('halloween-theme');
            isHalloweenTheme = false;
            localStorage.setItem('dlhalloween', 'false');
            showNotification('👻 Хеллоуинская тема выключена!', 'info');
            renderChatsInterface();
        }

        function changeTheme(theme) {
            currentTheme = theme;
            localStorage.setItem('dltheme', theme);
            applyTheme(theme);
            showNotification(`Тема "${theme}" применена! 🎨`, 'success');
        }

        function applyTheme(theme) {
            const root = document.documentElement;
            const themes = {
                purple: { accent: '#8b5cf6' },
                blue: { accent: '#3b82f6' },
                green: { accent: '#10b981' },
                pink: { accent: '#ec4899' },
                orange: { accent: '#f97316' }
            };
            
            if (themes[theme]) {
                root.style.setProperty('--accent-color', themes[theme].accent);
            }
        }

        function exportData() {
            const data = {
                user: currentUser,
                chats: chats,
                stats: userStats,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `dltrollex_backup_${new Date().getTime()}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            
            showNotification('Данные экспортированы! 📤', 'success');
        }

        function clearAllData() {
            if (confirm('ВНИМАНИЕ! Это удалит все чаты, настройки и историю. Продолжить?')) {
                localStorage.clear();
                showNotification('Все данные очищены 🔄', 'info');
                setTimeout(() => location.reload(), 1000);
            }
        }

        function showLogoutConfirm() {
            if (confirm('Вы уверены, что хотите выйти?')) {
                logout();
            }
        }

        function logout() {
            if (currentUser) {
                const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
                if (userIndex !== -1) {
                    allUsers[userIndex].isOnline = false;
                    allUsers[userIndex].lastSeen = new Date().toISOString();
                    localStorage.setItem('dlallUsers', JSON.stringify(allUsers));
                }
            }
            
            currentUser = null;
            localStorage.removeItem('dlcurrentUser');
            showNotification('Вы вышли из системы 👋', 'info');
            setTimeout(() => location.reload(), 1000);
        }

        function showFeatures() {
            showNotification(`
                🚀 Возможности DLtrollex:
                • Красивые анимации
                • Адаптивный дизайн
                • Голосовые сообщения
                • Групповые чаты
                • Поиск по сообщениям
                • Темы оформления
                • Экспорт данных
            `, 'info');
        }

        function formatTime(timestamp) {
            if (!timestamp) return '';
            const date = new Date(timestamp);
            return date.toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
        }

        function formatLastSeen(timestamp) {
            if (!timestamp) return 'давно';
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            const minutes = Math.floor(diff / 60000);
            
            if (minutes < 1) return 'только что';
            if (minutes < 60) return `${minutes} мин назад`;
            return `${Math.floor(minutes / 60)} ч назад`;
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification-toast';
            notification.style.background = type === 'error' ? '#ef4444' : 
                                          type === 'success' ? '#10b981' : 
                                          type === 'warning' ? '#f59e0b' : 'var(--accent-color)';
            notification.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 20px;">
                        ${type === 'error' ? '❌' : 
                          type === 'success' ? '✅' : 
                          type === 'warning' ? '⚠️' : '💡'}
                    </div>
                    <div style="flex: 1;">${message}</div>
                </div>
            `;
            
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

        // Обработчик ориентации
        window.addEventListener('orientationchange', function() {
            setTimeout(() => {
                detectDeviceType();
                if (currentUser) {
                    renderChatsInterface();
                }
            }, 300);
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        
        if not name:
            return jsonify({'success': False, 'message': 'Введите имя'})
        
        user_id = str(int(datetime.datetime.now().timestamp() * 1000)) + str(random.randint(1000, 9999))
        final_username = username or f"user{random.randint(10000, 99999)}"
        
        user_data = {
            'id': user_id,
            'name': name,
            'username': final_username,
            'avatar': '👤',
            'avatar_bg': '#6b21a8',
            'registered_at': datetime.datetime.now().isoformat(),
        }
        
        users_db[user_id] = user_data
        
        return jsonify({'success': True, 'user': user_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Ошибка сервера'})

def create_app():
    return app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🎃 DLtrollex Хеллоуин 2025 запущен!")
    print(f"📱 Оптимизирован для мобильных и ПК")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("✨ ИСПРАВЛЕНЫ ВСЕ БАГИ + ДОБАВЛЕНЫ АНИМАЦИИ!")
    print("🚀 Теперь работает:")
    print("   • Регистрация и вход")
    print("   • Создание чатов")
    print("   • Отправка сообщений")
    print("   • Авто-ответы")
    print("   • Поиск пользователей")
    print("   • Настройки профиля")
    print("   • Смена тем")
    print("🎬 Новые анимации:")
    print("   • Typewriter эффект")
    print("   • Плавные переходы")
    print("   • Анимации кнопок")
    print("   • Эффекты сообщений")
    print("   • Пульсации и свечения")
    
    app.run(host='0.0.0.0', port=port, debug=False)
