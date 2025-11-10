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
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный', 'Голографический', 
                 'Квантовый', 'Кибернетический', 'Астральный', 'Нейронный', 'Плазменный', 'Сверхсветовой']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр', 'Орёл', 'Робот', 'Андроид', 'Киберг', 'Дроид', 'Сфинкс', 'Грифон']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(1000, 9999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(16))

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
            --shadow-intense: 0 0 80px rgba(139, 92, 246, 0.5);
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
                radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                linear-gradient(45deg, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
            25% { transform: translateY(-20px) rotate(5deg) scale(1.05); }
            50% { transform: translateY(-10px) rotate(-3deg) scale(1.02); }
            75% { transform: translateY(-15px) rotate(2deg) scale(1.03); }
        }

        @keyframes cosmicGlow {
            0%, 100% { 
                text-shadow: 0 0 20px var(--accent-purple), 
                           0 0 40px var(--accent-purple),
                           0 0 60px var(--accent-blue);
            }
            50% { 
                text-shadow: 0 0 30px var(--accent-pink), 
                           0 0 60px var(--accent-pink),
                           0 0 90px var(--accent-cyan),
                           0 0 120px var(--accent-orange);
            }
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

        @keyframes pulse3D {
            0%, 100% { transform: scale(1) rotateX(0deg); }
            50% { transform: scale(1.05) rotateX(5deg); }
        }

        @keyframes loadingSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes hologram {
            0%, 100% { opacity: 0.8; filter: hue-rotate(0deg); }
            50% { opacity: 1; filter: hue-rotate(180deg); }
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
            width: 80px;
            height: 80px;
            border: 4px solid rgba(139, 92, 246, 0.3);
            border-top: 4px solid var(--accent-purple);
            border-radius: 50%;
            animation: loadingSpin 1s linear infinite;
            position: relative;
        }

        .loading-spinner::after {
            content: '';
            position: absolute;
            top: -4px;
            left: -4px;
            right: -4px;
            bottom: -4px;
            border: 4px solid transparent;
            border-top: 4px solid var(--accent-pink);
            border-radius: 50%;
            animation: loadingSpin 1.5s linear infinite reverse;
        }

        .loading-text {
            text-align: center;
            font-size: 1.4rem;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .loading-subtext {
            text-align: center;
            font-size: 1.1rem;
            color: var(--accent-purple);
            margin-top: 1rem;
            font-weight: 600;
            animation: cosmicGlow 3s ease infinite;
        }

        .auth-container {
            background: var(--bg-card);
            border-radius: 32px;
            padding: 50px;
            width: 100%;
            max-width: 520px;
            position: relative;
            overflow: hidden;
            border: var(--border-glow);
            box-shadow: var(--shadow-intense);
            backdrop-filter: blur(40px);
            animation: slideInUp 0.8s ease-out;
        }

        .auth-container::before {
            content: '';
            position: absolute;
            top: -100%;
            left: -100%;
            width: 300%;
            height: 300%;
            background: var(--gradient-primary);
            animation: gradientShift 6s ease infinite;
            opacity: 0.15;
            z-index: -1;
            filter: blur(40px);
        }

        .logo {
            font-size: 4rem;
            font-weight: 900;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 300% 300%;
            animation: cosmicGlow 3s ease infinite, gradientShift 4s ease infinite;
            text-align: center;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Arial Black', sans-serif;
        }

        .subtitle {
            color: var(--text-secondary);
            text-align: center;
            margin-bottom: 2.5rem;
            font-size: 1.3rem;
            line-height: 1.7;
            text-shadow: 0 0 10px rgba(255,255,255,0.1);
        }

        .btn {
            width: 100%;
            padding: 20px 28px;
            border: none;
            border-radius: 20px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            margin-bottom: 1.2rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
            box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
            animation: pulse3D 2s infinite;
        }

        .btn-primary:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.6);
            animation: none;
        }

        .btn-secondary {
            background: var(--bg-input);
            color: var(--text-primary);
            border: var(--border-glow);
            backdrop-filter: blur(20px);
        }

        .btn-secondary:hover {
            background: rgba(139, 92, 246, 0.15);
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(139, 92, 246, 0.25);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 1.2rem;
            margin: 2.5rem 0;
        }

        .feature-card {
            background: var(--bg-input);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s ease;
            border: var(--border-glow);
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.6s;
        }

        .feature-card:hover::before {
            left: 100%;
        }

        .feature-card:hover {
            transform: translateY(-8px) scale(1.05);
            background: rgba(139, 92, 246, 0.15);
            box-shadow: var(--shadow-intense);
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: float 4s ease-in-out infinite;
        }

        .credential-box {
            background: var(--bg-input);
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem 0;
            border: var(--border-glow);
            animation: pulse3D 3s infinite;
            position: relative;
            overflow: hidden;
        }

        .credential-box::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: var(--gradient-primary);
            opacity: 0.05;
            animation: gradientShift 8s ease infinite;
        }

        .credential-field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 1rem 0;
            padding: 1rem 1.5rem;
            background: var(--bg-secondary);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }

        .credential-field:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateX(5px);
        }

        .credential-value {
            font-family: 'Courier New', monospace;
            color: var(--accent-purple);
            font-weight: 700;
            font-size: 1.1rem;
            text-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
        }

        .copy-btn {
            background: var(--gradient-primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .copy-btn:hover {
            background: var(--accent-pink);
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 8px 25px rgba(236, 72, 153, 0.4);
        }

        .floating-emoji {
            position: fixed;
            font-size: 2.5rem;
            z-index: 999;
            opacity: 0.3;
            animation: float 8s ease-in-out infinite;
            pointer-events: none;
            filter: drop-shadow(0 0 10px currentColor);
        }

        .hidden {
            display: none !important;
        }

        .stats-panel {
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 25px;
            margin: 2rem 0;
            border: var(--border-glow);
            backdrop-filter: blur(20px);
            animation: slideInUp 0.8s ease;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            margin: 1rem 0;
            padding: 1rem 1.5rem;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }

        .stat-item:hover {
            background: rgba(139, 92, 246, 0.1);
            transform: translateX(5px);
        }

        .progress-bar {
            width: 100%;
            height: 6px;
            background: var(--bg-input);
            border-radius: 3px;
            overflow: hidden;
            margin: 1.5rem 0;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            background: var(--gradient-primary);
            border-radius: 3px;
            transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            background: var(--gradient-primary);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 20px;
            z-index: 2000;
            animation: slideInUp 0.5s ease, pulse3D 2s infinite;
            box-shadow: var(--shadow-intense);
            backdrop-filter: blur(20px);
            border: var(--border-glow);
            max-width: 400px;
            font-weight: 600;
        }

        /* Чат интерфейс премиум уровня */
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-primary);
        }

        .chat-container {
            display: flex;
            height: 100vh;
            max-width: 100%;
            margin: 0;
            background: var(--bg-secondary);
            overflow: hidden;
            position: relative;
        }

        .chat-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }

        .sidebar {
            width: 400px;
            background: var(--bg-card);
            border-right: var(--border-glow);
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 2;
            backdrop-filter: blur(20px);
        }

        .user-header {
            padding: 2.5rem;
            background: var(--gradient-secondary);
            border-bottom: var(--border-glow);
            position: relative;
            overflow: hidden;
        }

        .user-header::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--gradient-primary);
            opacity: 0.1;
            animation: hologram 4s infinite;
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            border-radius: 25px;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1.5rem;
            animation: float 6s ease-in-out infinite;
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
            border: 3px solid rgba(255,255,255,0.2);
        }

        .user-stats {
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
            font-size: 0.9rem;
        }

        .stat-badge {
            background: rgba(255,255,255,0.1);
            padding: 0.5rem 1rem;
            border-radius: 10px;
            text-align: center;
            flex: 1;
            margin: 0 0.25rem;
        }

        .level-badge {
            background: var(--gradient-gold);
            color: black;
            font-weight: 800;
        }

        .premium-badge {
            background: var(--gradient-premium);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: pulse3D 3s infinite;
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
            margin-top: 1rem;
        }

        .search-box {
            padding: 2rem;
            border-bottom: var(--border-glow);
            background: rgba(26, 26, 26, 0.8);
        }

        .search-input {
            width: 100%;
            padding: 16px 20px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 15px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
            border-color: var(--accent-purple);
        }

        .chats-list {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 1.5rem;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            margin-bottom: 0.8rem;
            background: rgba(255,255,255,0.02);
            border: 1px solid transparent;
            position: relative;
        }

        .chat-item:hover {
            background: rgba(139, 92, 246, 0.15);
            transform: translateX(10px) scale(1.02);
            border-color: var(--accent-purple);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
        }

        .chat-item.active {
            background: rgba(139, 92, 246, 0.25);
            border-color: var(--accent-purple);
            box-shadow: 0 15px 35px rgba(139, 92, 246, 0.3);
        }

        .unread-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: var(--accent-pink);
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 700;
            animation: pulse3D 2s infinite;
        }

        .chat-avatar {
            width: 60px;
            height: 60px;
            border-radius: 18px;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-right: 1.5rem;
            animation: pulse3D 3s infinite;
            border: 2px solid rgba(255,255,255,0.2);
        }

        .chat-info {
            flex: 1;
        }

        .chat-name {
            font-weight: 700;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
            color: var(--text-primary);
        }

        .chat-preview {
            color: var(--text-secondary);
            font-size: 0.95rem;
            opacity: 0.8;
        }

        .chat-time {
            font-size: 0.8rem;
            color: var(--accent-cyan);
            margin-top: 0.25rem;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            position: relative;
            z-index: 2;
        }

        .chat-header {
            padding: 2rem 2.5rem;
            background: var(--bg-card);
            border-bottom: var(--border-glow);
            display: flex;
            align-items: center;
            justify-content: space-between;
            backdrop-filter: blur(20px);
        }

        .chat-actions {
            display: flex;
            gap: 1rem;
        }

        .action-btn {
            background: rgba(255,255,255,0.1);
            border: none;
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1.1rem;
        }

        .action-btn:hover {
            background: var(--accent-purple);
            transform: scale(1.1);
        }

        .messages-container {
            flex: 1;
            padding: 2.5rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            background: 
                radial-gradient(circle at 100% 100%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 0% 0%, rgba(236, 72, 153, 0.05) 0%, transparent 50%);
        }

        .message {
            max-width: 75%;
            padding: 1.5rem 2rem;
            border-radius: 25px;
            position: relative;
            animation: slideInUp 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .message::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 25px;
            background: var(--gradient-primary);
            opacity: 0.1;
            z-index: -1;
        }

        .message.received {
            background: rgba(34, 34, 34, 0.8);
            align-self: flex-start;
            border-bottom-left-radius: 8px;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .message.sent {
            background: var(--gradient-primary);
            align-self: flex-end;
            border-bottom-right-radius: 8px;
            color: white;
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        }

        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 0.5rem;
            text-align: right;
        }

        .message-input-container {
            padding: 2rem 2.5rem;
            background: var(--bg-card);
            border-top: var(--border-glow);
            display: flex;
            gap: 1.5rem;
            align-items: center;
            backdrop-filter: blur(20px);
        }

        .message-input {
            flex: 1;
            padding: 18px 24px;
            background: var(--bg-input);
            border: var(--border-glow);
            border-radius: 25px;
            color: var(--text-primary);
            font-size: 1.1rem;
            transition: all 0.3s ease;
            resize: none;
            height: 60px;
        }

        .message-input:focus {
            outline: none;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.4);
            border-color: var(--accent-purple);
        }

        .send-btn {
            padding: 18px 32px;
            background: var(--gradient-primary);
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        }

        .send-btn:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6);
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            color: var(--text-secondary);
            font-size: 1rem;
            margin: 1rem 2.5rem;
            padding: 1rem 1.5rem;
            background: rgba(139, 92, 246, 0.1);
            border-radius: 15px;
            border: var(--border-glow);
            animation: pulse3D 2s infinite;
        }

        .typing-dots {
            display: flex;
            margin-left: 1rem;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-purple);
            border-radius: 50%;
            margin: 0 3px;
            animation: typingPulse 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingPulse {
            0%, 60%, 100% { transform: scale(1); opacity: 0.4; }
            30% { transform: scale(1.3); opacity: 1; }
        }

        .trust-message {
            text-align: center;
            color: var(--accent-purple);
            font-weight: 600;
            margin-top: 2rem;
            font-size: 1.1rem;
            animation: fadeIn 1s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Мобильная оптимизация */
        @media (max-width: 768px) {
            .auth-container {
                padding: 2rem;
                margin: 1rem;
                border-radius: 25px;
            }
            
            .logo {
                font-size: 2.8rem;
            }
            
            .feature-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .chat-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: 50vh;
                position: absolute;
                z-index: 1000;
                transform: translateX(-100%);
                transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .mobile-menu-btn {
                display: block !important;
            }
            
            .messages-container {
                padding: 1.5rem;
            }
            
            .message {
                max-width: 85%;
                padding: 1.2rem 1.8rem;
            }
            
            .message-input-container {
                padding: 1.5rem;
            }
            
            .chat-header {
                padding: 1.5rem;
            }
            
            .notification {
                left: 10px;
                right: 10px;
                top: 10px;
                max-width: none;
            }
        }

        @media (max-width: 480px) {
            .auth-container {
                padding: 1.5rem;
                margin: 0.5rem;
            }
            
            .logo {
                font-size: 2.2rem;
            }
            
            .subtitle {
                font-size: 1rem;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
            }
            
            .credential-field {
                flex-direction: column;
                gap: 0.5rem;
                align-items: flex-start;
            }
            
            .message {
                max-width: 90%;
            }
            
            .user-stats {
                flex-direction: column;
                gap: 0.5rem;
            }
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text-primary);
            font-size: 1.8rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .mobile-menu-btn:hover {
            background: rgba(139, 92, 246, 0.2);
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <!-- Плавающие элементы -->
    <div class="floating-emoji" style="top: 10%; left: 5%; animation-delay: 0s;">🚀</div>
    <div class="floating-emoji" style="top: 15%; right: 8%; animation-delay: 1s;">✨</div>
    <div class="floating-emoji" style="top: 85%; left: 10%; animation-delay: 2s;">💫</div>
    <div class="floating-emoji" style="top: 80%; right: 5%; animation-delay: 3s;">🌟</div>
    <div class="floating-emoji" style="top: 40%; left: 15%; animation-delay: 4s;">🎮</div>
    <div class="floating-emoji" style="top: 60%; right: 12%; animation-delay: 5s;">⚡</div>

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
            <div class="subtitle">ЭПИЧЕСКИЙ ФУТУРИСТИЧЕСКИЙ МЕССЕНДЖЕР С ИСКУССТВЕННЫМ ИНТЕЛЛЕКТОМ И КОСМИЧЕСКИМ ДИЗАЙНОМ</div>
            
            <div class="stats-panel">
                <h4 style="margin-bottom: 1.5rem; text-align: center; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🌌 СТАТИСТИКА ВСЕЛЕННОЙ</h4>
                <div class="stat-item">
                    <span>👥 Космических пользователей:</span>
                    <span style="color: var(--accent-purple); font-weight: 700;" id="onlineCount">1,247</span>
                </div>
                <div class="stat-item">
                    <span>💬 Сообщений в реальном времени:</span>
                    <span style="color: var(--accent-pink); font-weight: 700;" id="messagesToday">8,492</span>
                </div>
                <div class="stat-item">
                    <span>🌠 Активных галактик-чатов:</span>
                    <span style="color: var(--accent-cyan); font-weight: 700;" id="activeChats">356</span>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="startQuickRegistration()">
                🚀 ЗАПУСТИТЬ КОСМИЧЕСКОЕ ПУТЕШЕСТВИЕ
            </button>
            
            <div class="feature-grid">
                <div class="feature-card" onclick="startQuickRegistration()">
                    <div class="feature-icon">🤖</div>
                    <div>AI СУПЕР-ИНТЕЛЛЕКТ</div>
                </div>
                <div class="feature-card" onclick="showThemeSelector()">
                    <div class="feature-icon">🎨</div>
                    <div>ГАЛАКТИЧЕСКИЕ ТЕМЫ</div>
                </div>
                <div class="feature-card" onclick="showStats()">
                    <div class="feature-icon">📊</div>
                    <div>РЕАЛЬНАЯ СТАТИСТИКА</div>
                </div>
                <div class="feature-card" onclick="showFeatures()">
                    <div class="feature-icon">⚡</div>
                    <div>СВЕРХСВЕТОВАЯ СВЯЗЬ</div>
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
            <div class="logo">СОЗДАНИЕ ЛЕГЕНДЫ</div>
            <div class="subtitle">СТАНЬТЕ ЧАСТЬЮ ЦИФРОВОЙ ЭПОХИ С ВАШИМ УНИКАЛЬНЫМ ЦИФРОВЫМ ИДЕНТИТЕТОМ</div>
            
            <div class="credential-box">
                <div class="credential-field">
                    <span>👤 ВАШЕ КОСМИЧЕСКОЕ ИМЯ:</span>
                    <span class="credential-value" id="generatedName">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 КВАНТОВЫЙ КЛЮЧ ДОСТУПА:</span>
                    <span class="credential-value" id="generatedPassword">...</span>
                    <button class="copy-btn" onclick="copyToClipboard('generatedPassword')">📋</button>
                </div>
                <div class="credential-field">
                    <span>🆔 ЦИФРОВАЯ СИГНАТУРА:</span>
                    <span class="credential-value" id="generatedUsername">...</span>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="registerProgress" style="width: 0%"></div>
            </div>
            
            <button class="btn btn-primary" onclick="quickRegister()">
                💫 АКТИВИРОВАТЬ ЦИФРОВОЕ СУЩЕСТВОВАНИЕ
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewCredentials()">
                🔄 ГЕНЕРИРОВАТЬ НОВУЮ РЕАЛЬНОСТЬ
            </button>
            
            <button class="btn btn-secondary" onclick="showScreen('welcomeScreen')">
                ← ВЕРНУТЬСЯ В ПОРТАЛ
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
                    <h3 id="userName">Космический Странник</h3>
                    <p id="userRank" style="color: var(--accent-cyan); margin-bottom: 1rem;">Уровень: 1</p>
                    
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
                    <input type="text" class="search-input" placeholder="🔍 СКАНИРОВАТЬ ГАЛАКТИКУ ЧАТОВ..." oninput="searchChats(this.value)">
                </div>
                
                <div class="chats-list" id="chatsList">
                    <!-- Список чатов будет здесь -->
                </div>
            </div>
            
            <!-- Область чата -->
            <div class="chat-area">
                <div class="chat-header">
                    <div style="display: flex; align-items: center; gap: 1.5rem;">
                        <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                        <div class="chat-avatar" id="currentChatAvatar">👤</div>
                        <div>
                            <h3 id="currentChatName">ВЫБЕРИТЕ ГАЛАКТИКУ ОБЩЕНИЯ</h3>
                            <p id="currentChatStatus" style="color: var(--text-secondary);">ДЛЯ ЗАПУСКА МЕЖЗВЕЗДНОЙ СВЯЗИ</p>
                        </div>
                    </div>
                    <div class="chat-actions">
                        <button class="action-btn" onclick="showChatInfo()" title="Информация о чате">ℹ️</button>
                        <button class="action-btn" onclick="showSettings()" title="Настройки">⚙️</button>
                        <button class="action-btn" onclick="logout()" title="Выйти">🚪</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 4rem; color: var(--text-secondary);">
                        <div style="font-size: 5rem; margin-bottom: 2rem; animation: float 4s ease-in-out infinite;">🌌</div>
                        <h3 style="margin-bottom: 1rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ДОБРО ПОЖАЛОВАТЬ В DL-TROLLEDX!</h3>
                        <p>ВЫБЕРИТЕ ЧАТ ИЛИ СОЗДАЙТЕ НОВЫЙ ДЛЯ ЗАПУСКА ЭПИЧЕСКОГО ОБЩЕНИЯ</p>
                        <div class="trust-message" style="margin-top: 2rem;">
                            Спасибо, что доверяете нам! 🌟
                        </div>
                    </div>
                </div>
                
                <div class="typing-indicator hidden" id="typingIndicator">
                    <span id="typingUser">КОСМИЧЕСКИЙ СОБЕСЕДНИК</span> АКТИВИРУЕТ НЕЙРО-СВЯЗЬ
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="ВВЕДИТЕ ВАШЕ МЕЖГАЛАКТИЧЕСКОЕ СООБЩЕНИЕ..." id="messageInput" 
                           onkeypress="handleKeyPress(event)" oninput="handleTyping()">
                    <button class="send-btn" onclick="sendMessage()">ЗАПУСТИТЬ В КОСМОС</button>
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
            }, 2500);
        });

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function initializeSampleData() {
            // Создаем тестовых пользователей с улучшенными данными
            allUsers = [
                {
                    id: 'user1',
                    name: 'Нейро-Алексей',
                    username: '@neuro_alex',
                    avatar: '🤖',
                    isOnline: true,
                    bio: 'AI разработчик | Квантовые вычисления',
                    level: 42,
                    xp: 12500,
                    premium: true,
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user2', 
                    name: 'Цифровая София',
                    username: '@digital_queen',
                    avatar: '👑',
                    isOnline: true,
                    bio: 'Дизайнер интерфейсов | UX/UI Гуру',
                    level: 38,
                    xp: 9800,
                    premium: true,
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user3',
                    name: 'Кибер-Максим',
                    username: '@code_master',
                    avatar: '💻',
                    isOnline: false,
                    bio: 'Full-stack разработчик | Крипто энтузиаст',
                    level: 56,
                    xp: 21000,
                    premium: false,
                    lastSeen: new Date(Date.now() - 3600000).toISOString()
                },
                {
                    id: 'user4',
                    name: 'Виртуальная Анна',
                    username: '@vr_queen',
                    avatar: '👓',
                    isOnline: true,
                    bio: 'VR/AR разработчик | Метавселенные',
                    level: 31,
                    xp: 7600,
                    premium: true,
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user5',
                    name: 'Квантовый Дмитрий',
                    username: '@quantum_d',
                    avatar: '⚛️',
                    isOnline: false,
                    bio: 'Физик | Квантовая механика',
                    level: 67,
                    xp: 28500,
                    premium: false,
                    lastSeen: new Date(Date.now() - 7200000).toISOString()
                }
            ];

            // Загружаем сохраненные данные
            const savedChats = localStorage.getItem('dl_trolledx_chats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            } else {
                // Создаем тестовые чаты если их нет
                createSampleChats();
            }
            
            const savedStats = localStorage.getItem('dl_trolledx_stats');
            if (savedStats) {
                userStats = JSON.parse(savedStats);
            }
        }

        function createSampleChats() {
            const sampleMessages = [
                "Привет! Как твои квантовые вычисления? 🚀",
                "Отлично! Только что запустил новый алгоритм! 💫",
                "Круто! Поделишься результатами? 🔬",
                "Конечно! Смотри что получилось... 📊",
                "Вау! Это революционно! 🌟",
                "Спасибо! Работаем над улучшениями! ⚡",
                "Жду следующих обновлений! 🎯",
                "Скоро будет что-то эпическое! 💎"
            ];

            allUsers.forEach((user, index) => {
                if (index < 3) { // Создаем чаты только с первыми тремя пользователями
                    const chatMessages = [];
                    const messageCount = Math.floor(Math.random() * 4) + 3;
                    
                    for (let i = 0; i < messageCount; i++) {
                        const isUser = i % 2 === 0;
                        chatMessages.push({
                            id: `msg_${Date.now()}_${i}`,
                            text: sampleMessages[i] || "Интересная тема для обсуждения! 💭",
                            senderId: isUser ? 'current_user' : user.id,
                            timestamp: new Date(Date.now() - (messageCount - i) * 600000).toISOString()
                        });
                    }

                    const newChat = {
                        id: `chat_${user.id}`,
                        participants: ['current_user', user.id],
                        lastMessage: chatMessages[chatMessages.length - 1],
                        messages: chatMessages,
                        unread: Math.floor(Math.random() * 5),
                        created_at: new Date().toISOString(),
                        theme: ['purple', 'blue', 'pink', 'matrix', 'cyber'][index]
                    };
                    chats.push(newChat);
                }
            });
            
            localStorage.setItem('dl_trolledx_chats', JSON.stringify(chats));
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dl_trolledx_currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                userStats.logins++;
                saveUserStats();
                
                // Показываем загрузку перед переходом в чат
                showScreen('loadingScreen');
                document.querySelector('.loading-text').textContent = 'Возвращаемся в космос...';
                document.querySelector('.loading-subtext').textContent = 'Спасибо за возвращение! 🌟';
                
                setTimeout(() => {
                    showMainApp();
                    showNotification(`С возвращением, ${currentUser.name}! 🚀 Ваш уровень: ${userStats.level}`, 'success');
                }, 1500);
            } else {
                showScreen('welcomeScreen');
            }
        }

        function saveUserStats() {
            localStorage.setItem('dl_trolledx_stats', JSON.stringify(userStats));
        }

        function showScreen(screenId) {
            console.log('Переход на экран:', screenId);
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
            console.log('Запуск регистрации');
            showScreen('registerScreen');
            generateNewCredentials();
        }

        function showManualLogin() {
            showNotification('Ручной вход будет доступен в следующем обновлении! 🔄', 'info');
        }

        function showFeatures() {
            showNotification(`
                🚀 ВОЗМОЖНОСТИ DL-TROLLEDX:
                • AI-ассистент с контекстным анализом
                • Сквозное квантовое шифрование
                • Голосовые и видео сообщения
                • 3D голографические вызовы
                • Кастомизация тем и интерфейса
                • Система уровней и достижений
                • Премиум функции
                • Cloud синхронизация
            `, 'info');
        }

        function showThemeSelector() {
            showNotification('Галактические темы будут доступны в следующем обновлении! 🎨', 'info');
        }

        function showStats() {
            showNotification('Детальная статистика доступна в вашем профиле! 📊', 'info');
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
            const adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный'];
            const nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр'];
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
            
            const avatars = ['😎', '🤖', '👽', '🐲', '🦄', '⚡', '🌟', '💫'];
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
            
            // Показываем загрузку перед переходом
            showScreen('loadingScreen');
            document.querySelector('.loading-text').textContent = 'Создаем ваше космическое пространство...';
            document.querySelector('.loading-subtext').textContent = 'Спасибо за доверие! 💫';
            
            setTimeout(() => {
                showMainApp();
                const rank = get_user_rank(level);
                showNotification(`Добро пожаловать в DL-TrolledX, ${name}! 🚀 Ваш ранг: ${rank}`, 'success');
            }, 2000);
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
                    <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                        <p>Космос чатов пуст...</p>
                        <button class="btn-secondary" onclick="createSampleChats(); renderChatsList();" style="margin-top: 1rem;">
                            Создать тестовые галактики
                        </button>
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
                    <div class="chat-item" onclick="openChat('${chat.id}')">
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
                '● онлайн в цифровом пространстве' : 
                `● был(а) ${formatLastSeen(otherUser.lastSeen)}`;
            
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

        function formatLastSeen(timestamp) {
            const now = new Date();
            const lastSeen = new Date(timestamp);
            const diffMinutes = Math.floor((now - lastSeen) / 60000);
            
            if (diffMinutes < 1) return 'только что';
            if (diffMinutes < 60) return `${diffMinutes} мин назад`;
            if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)} ч назад`;
            return `${Math.floor(diffMinutes / 1440)} дн назад`;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function handleTyping() {
            if (currentChat) {
                showTypingIndicator();
            }
        }

        function showTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            const typingUser = document.getElementById('typingUser');
            
            if (currentChat) {
                const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== 'current_user'));
                if (otherUser) {
                    typingUser.textContent = otherUser.name;
                    indicator.classList.remove('hidden');
                    
                    setTimeout(() => {
                        indicator.classList.add('hidden');
                    }, 3000);
                }
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
                        💬 ИНФОРМАЦИЯ О ГАЛАКТИКЕ:
                        👤 Имя: ${otherUser.name}
                        🆔 ID: ${otherUser.username}
                        📝 Статус: ${otherUser.bio}
                        ⚡ Уровень: ${otherUser.level}
                        💎 XP: ${otherUser.xp}
                        ${otherUser.premium ? '🌟 Статус: PREMIUM' : '🔹 Статус: Базовый'}
                        🔐 Безопасность: Квантовое шифрование
                    `, 'info');
                }
            } else {
                showNotification('Выберите галактику для просмотра информации 🌌', 'error');
            }
        }

        function showSettings() {
            showNotification(`
                ⚙️ НАСТРОЙКИ РЕАЛЬНОСТИ:
                • Тема: Космическая фиолетовая
                • Уведомления: Включены
                • Звуки: Активны
                • Авто-сохранение: Каждые 30 сек
                • Безопасность: Максимальная
                • Синхронизация: Cloud активна
                
                🎮 ВАША СТАТИСТИКА:
                • Уровень: ${userStats.level}
                • Опыт: ${userStats.xp} XP
                • Сообщений: ${userStats.messagesSent}
                • В сети: ${Math.floor(userStats.timeSpent / 60)} мин
            `, 'info');
        }

        function logout() {
            if (confirm('Покинуть космическое пространство?')) {
                currentUser = null;
                localStorage.removeItem('dl_trolledx_currentUser');
                showScreen('welcomeScreen');
                showNotification('До скорых встреч в цифровом космосе! 👋', 'info');
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
            }, 5000);
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

        // Авто-сохранение каждые 30 секунд
        setInterval(() => {
            if (currentUser) {
                localStorage.setItem('dl_trolledx_chats', JSON.stringify(chats));
                localStorage.setItem('dl_trolledx_stats', JSON.stringify(userStats));
                console.log('💾 Космическое авто-сохранение выполнено');
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
        'status': 'cosmic_online',
        'users_online': random.randint(1000, 5000),
        'version': '1.0_celestial',
        'timestamp': datetime.datetime.now().isoformat(),
        'quantum_entanglement': 'active'
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'quantum_healthy', 
        'service': 'DL-TrolledX Celestial',
        'reality_stability': '98.7%'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌌 DL-TrolledX Celestial Edition активирован!")
    print("🚀 Запуск межгалактического протокола связи...")
    print("💫 Квантовые процессоры инициализированы")
    print("🎮 Система уровней и достижений активна")
    print("🔮 Рабочие чаты с реальными пользователями")
    print(f"🔗 Порталы открыты: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
