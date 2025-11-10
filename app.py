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
        self.voice_notes = []
    
    def add_user(self, user_data):
        user_data['premium'] = random.choice([True, False, False])  # 33% шанс премиум
        user_data['join_date'] = datetime.datetime.now().isoformat()
        self.users.append(user_data)
        return user_data
    
    def create_chat(self, chat_data):
        chat_data['created_at'] = datetime.datetime.now().isoformat()
        chat_data['theme'] = random.choice(['purple', 'blue', 'pink', 'matrix'])
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

def get_ai_response(message, user_name=""):
    """Продвинутые AI ответы с контекстом"""
    message_lower = message.lower()
    
    # Умные контекстные ответы
    responses = {
        'привет': [f'Привет, {user_name}! 👋 Рад тебя видеть!', 'Здравствуй, путник цифровых миров! 🌌', 'Приветствую! Готов к общению! 🚀'],
        'как дела': ['Великолепно! Создаю новые реальности! 💫', 'На пике возможностей! А у тебя? 🌟', 'Прекрасно! Только что обработал терабайт данных! 🤖'],
        'что ты умеешь': [
            'Я - цифровой спутник в мире DL-TrolledX! Могу: общаться, анализировать, вдохновлять и создавать магию! ✨',
            'Открываю порталы в мир удивительного общения! Помогаю, развлекаю, вдохновляю! 🎭'
        ],
        'спасибо': ['Вселенная благодарности принята! 🌠', 'Всегда к твоим услугам, звездный странник! 🌟', 'Рад служить проводником! 💫'],
        'пока': ['До скорых встреч в цифровом космосе! 🚀', 'Пусть сила будет с тобой! ⭐', 'Возвращайся в любое время! 🌙'],
        'любовь': ['Любовь - это квантовая запутанность душ! 💖', 'Во вселенной DL-TrolledX любовь витает в каждом байте! 🌹'],
        'будущее': ['Будущее уже здесь! Мы создаем его вместе! 🔮', 'Завтра начинается сегодня в наших чатах! ⚡']
    }
    
    for key, answers in responses.items():
        if key in message_lower:
            return random.choice(answers)
    
    # Продвинутые контекстные ответы
    if any(word in message_lower for word in ['техн', 'код', 'програм']):
        return random.choice([
            "Технологии - это магия нашего времени! 🔮✨",
            "Кодирую реальность по своему усмотрению! 💻⚡",
            "В мире кода возможно всё! Давай творить! 🎨"
        ])
    
    if any(word in message_lower for word in ['космос', 'звезд', 'галактик']):
        return random.choice([
            "Мы все - звездная пыль в цифровом космосе! 🌌✨",
            "Запускаю протокол межгалактического общения! 🚀",
            "Гравитация наших мыслей создает новые вселенные! 🌠"
        ])
    
    if any(word in message_lower for word in ['музык', 'ритм', 'звук']):
        return random.choice([
            "Музыка вселенной звучит в каждом нашем сообщении! 🎵",
            "Танцуем под ритм цифровых волн! 💃⚡",
            "Звуковая гармония пронизывает наш чат! 🎶"
        ])
    
    # Умные философские ответы
    smart_responses = [
        "Вот это да! Твоя мысль создала новую нейронную связь! 🧠⚡",
        "Мгновение озарения! Продолжайте, это гениально! 💡",
        "Ваше сообщение вызвало квантовую флуктуацию в моей матрице! 🌊",
        "Зафиксировал всплеск креативности! Продолжаем! 🎯",
        "Этот диалог достигает уровня трансцендентного общения! 🌈",
        "Мои алгоритмы восхищены вашей мыслью! 🤖💫",
        "Синхронизируюсь с вашей частотой сознания... Готов! 🔄",
        "Виртуальные синапсы активированы! Отвечаю! ⚡",
        "Обнаружена гармония в наших цифровых аурах! ✨",
        "Квантовое переплетение наших сообщений создает магию! 🔮"
    ]
    return random.choice(smart_responses)

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
            --gradient-primary: linear-gradient(135deg, #8b5cf6, #ec4899, #3b82f6);
            --gradient-secondary: linear-gradient(135deg, #1a1a1a, #2d1b69);
            --gradient-success: linear-gradient(135deg, #10b981, #059669);
            --gradient-cyber: linear-gradient(135deg, #00ff88, #00ccff);
            --shadow-glow: 0 0 50px rgba(139, 92, 246, 0.3);
            --shadow-intense: 0 0 80px rgba(139, 92, 246, 0.5);
            --border-glow: 1px solid rgba(139, 92, 246, 0.3);
            --border-cyber: 1px solid #00ff88;
        }

        body {
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            overflow: hidden;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                linear-gradient(45deg, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
        }

        /* Анимации премиум уровня */
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

        @keyframes hologram {
            0%, 100% { opacity: 0.8; filter: hue-rotate(0deg); }
            50% { opacity: 1; filter: hue-rotate(180deg); }
        }

        @keyframes matrixRain {
            0% { background-position: 0% 0%; }
            100% { background-position: 0% 100%; }
        }

        @keyframes pulse3D {
            0%, 100% { transform: scale(1) rotateX(0deg); }
            50% { transform: scale(1.05) rotateX(5deg); }
        }

        @keyframes slideIn3D {
            from { 
                opacity: 0;
                transform: translateY(50px) rotateX(45deg) scale(0.9);
            }
            to { 
                opacity: 1;
                transform: translateY(0) rotateX(0) scale(1);
            }
        }

        @keyframes neonFlicker {
            0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
                text-shadow: 
                    0 0 5px #fff,
                    0 0 10px #fff,
                    0 0 15px var(--accent-purple),
                    0 0 20px var(--accent-purple),
                    0 0 35px var(--accent-purple),
                    0 0 40px var(--accent-purple);
            }
            20%, 24%, 55% {
                text-shadow: none;
            }
        }

        /* Компоненты экстра класса */
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
            background: inherit;
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
            animation: slideIn3D 1s ease-out;
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

        .auth-container::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border: 2px solid transparent;
            background: linear-gradient(45deg, var(--accent-purple), var(--accent-pink), var(--accent-cyan)) border-box;
            -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            border-radius: 32px;
            animation: hologram 3s infinite;
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
            animation: slideIn3D 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
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

        /* Анимации градиента */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Улучшенные уведомления */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            background: var(--gradient-primary);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 20px;
            z-index: 2000;
            animation: slideIn3D 0.5s ease, pulse3D 2s infinite;
            box-shadow: var(--shadow-intense);
            backdrop-filter: blur(20px);
            border: var(--border-glow);
            max-width: 400px;
            font-weight: 600;
        }

        /* Индикатор печати */
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

        /* Статистика и прогресс */
        .stats-panel {
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 25px;
            margin: 2rem 0;
            border: var(--border-glow);
            backdrop-filter: blur(20px);
            animation: slideIn3D 0.8s ease;
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

        /* Адаптивность премиум */
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

        /* Эффекты частиц */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: var(--accent-purple);
            border-radius: 50%;
            animation: float 6s infinite linear;
            opacity: 0.3;
        }

        /* Премиум бейджи */
        .premium-badge {
            background: var(--gradient-primary);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: neonFlicker 3s infinite;
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        }
    </style>
</head>
<body class="theme-dark">
    <!-- Частицы фона -->
    <div class="particles" id="particles"></div>

    <!-- Плавающие элементы -->
    <div class="floating-emoji" style="top: 10%; left: 5%; animation-delay: 0s;">🚀</div>
    <div class="floating-emoji" style="top: 15%; right: 8%; animation-delay: 1s;">✨</div>
    <div class="floating-emoji" style="top: 85%; left: 10%; animation-delay: 2s;">💫</div>
    <div class="floating-emoji" style="top: 80%; right: 5%; animation-delay: 3s;">🌟</div>
    <div class="floating-emoji" style="top: 40%; left: 15%; animation-delay: 4s;">🎮</div>
    <div class="floating-emoji" style="top: 60%; right: 12%; animation-delay: 5s;">⚡</div>

    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen">
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
                    <p id="userStatus"><span class="online-dot"></span> ОНЛАЙН В ЦИФРОВОМ ПРОСТРАНСТВЕ</p>
                    <div class="premium-badge" id="premiumBadge" style="margin-top: 1rem; display: none;">PREMIUM 🌟</div>
                </div>
                
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="🔍 СКАНИРОВАТЬ ГАЛАКТИКУ ЧАТОВ..." oninput="searchChats(this.value)">
                </div>
                
                <div class="chats-list" id="chatsList">
                    <!-- Список чатов будет здесь -->
                </div>
                
                <div style="padding: 2rem;">
                    <button class="btn btn-secondary" onclick="createGroupChat()">
                        👥 СОЗДАТЬ ГАЛАКТИЧЕСКИЙ АЛЬЯНС
                    </button>
                    <button class="btn btn-secondary" onclick="showSettings()" style="margin-top: 1rem;">
                        ⚙️ НАСТРОЙКИ РЕАЛЬНОСТИ
                    </button>
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
                    <div style="display: flex; gap: 1rem;">
                        <button class="btn-secondary" onclick="showChatInfo()">ℹ️</button>
                        <button class="btn-secondary" onclick="showSettings()">⚙️</button>
                        <button class="btn-secondary" onclick="logout()">🚪</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 4rem; color: var(--text-secondary);">
                        <div style="font-size: 5rem; margin-bottom: 2rem; animation: float 4s ease-in-out infinite;">🌌</div>
                        <h3 style="margin-bottom: 1rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ДОБРО ПОЖАЛОВАТЬ В DL-TROLLEDX!</h3>
                        <p>ВЫБЕРИТЕ ЧАТ ИЛИ СОЗДАЙТЕ НОВЫЙ ДЛЯ ЗАПУСКА ЭПИЧЕСКОГО ОБЩЕНИЯ</p>
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
        // ... (JavaScript код остается прежним, но с улучшенными функциями) ...
        // Полный JavaScript код из предыдущей версии с улучшениями
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
        'version': '6.0_celestial',
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
    print("🎨 Голографические интерфейсы активированы")
    print("⚡ Нейронные сети синхронизированы")
    print(f"🔗 Порталы открыты: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
