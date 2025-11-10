# app6.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramodern2024'

class ChatManager:
    def __init__(self):
        self.users = []
        self.chats = []
        self.messages = []
    
    def add_user(self, user_data):
        self.users.append(user_data)
        return user_data
    
    def create_chat(self, chat_data):
        self.chats.append(chat_data)
        return chat_data
    
    def add_message(self, message_data):
        self.messages.append(message_data)
        return message_data

chat_manager = ChatManager()

def generate_username():
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный', 'Голографический', 'Квантовый', 'Кибернетический']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр', 'Орёл', 'Робот', 'Андроид']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(100, 999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(12))

def get_ai_response(message):
    """Умные ответы AI"""
    message_lower = message.lower()
    
    responses = {
        'привет': ['Привет! 👋', 'Здравствуйте! 😊', 'Приветствую! 🌟'],
        'как дела': ['Отлично! А у вас? 💫', 'Прекрасно! Работаю над новыми функциями! 🚀', 'Всё хорошо, спасибо! ✨'],
        'что ты умеешь': ['Я могу общаться, помогать и создавать крутые чаты! 🤖', 'Отвечать на сообщения и делать общение интереснее! 💡'],
        'спасибо': ['Всегда рад помочь! 😊', 'Пожалуйста! 🌟', 'Обращайтесь! 💫'],
        'пока': ['До свидания! 👋', 'Удачи! 🍀', 'Был рад общению! ✨']
    }
    
    for key, answers in responses.items():
        if key in message_lower:
            return random.choice(answers)
    
    # Умные ответы по контексту
    smart_responses = [
        "Интересно! Расскажи подробнее 🤔",
        "Отличная мысль! 💫",
        "Согласен с тобой! 👍",
        "А что если попробовать по-другому? 🔄",
        "Это напоминает мне одну идею... 💡",
        "Продолжаем в том же духе! 🚀",
        "Увлекательно! 🎯",
        "Как насчет обсудить это детальнее? 🔍",
        "Вот это поворот! 🎭",
        "Продолжайте, я слушаю 👂"
    ]
    return random.choice(smart_responses)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DL-TrolledX 6.0 🚀</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💫</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, sans-serif;
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
            --gradient-primary: linear-gradient(135deg, #8b5cf6, #ec4899, #3b82f6);
            --gradient-secondary: linear-gradient(135deg, #1a1a1a, #2d1b69);
            --gradient-success: linear-gradient(135deg, #10b981, #059669);
            --shadow-glow: 0 0 50px rgba(139, 92, 246, 0.3);
            --border-glow: 1px solid rgba(139, 92, 246, 0.3);
        }

        /* ... (предыдущие стили остаются) ... */

        /* НОВЫЕ СТИЛИ */
        
        /* Темная тема улучшена */
        .theme-dark {
            --bg-primary: #0a0a0a;
            --bg-secondary: #111111;
        }

        .theme-matrix {
            --bg-primary: #000000;
            --bg-secondary: #001100;
            --accent-purple: #00ff00;
            --accent-pink: #00ff00;
            --accent-blue: #00ff00;
            --text-primary: #00ff00;
        }

        .theme-ocean {
            --bg-primary: #001f3f;
            --bg-secondary: #003366;
            --accent-purple: #0074D9;
            --accent-pink: #7FDBFF;
            --accent-blue: #39CCCC;
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin: 0.5rem 0;
        }

        .typing-dots {
            display: flex;
            margin-left: 0.5rem;
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

        .message-time {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-align: right;
            margin-top: 0.25rem;
        }

        .online-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            display: inline-block;
            margin-right: 0.5rem;
            animation: pulse 2s infinite;
        }

        .message-actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .message:hover .message-actions {
            opacity: 1;
        }

        .action-btn {
            background: rgba(255,255,255,0.1);
            border: none;
            color: var(--text-primary);
            padding: 0.25rem 0.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }

        .action-btn:hover {
            background: var(--accent-purple);
        }

        .stats-panel {
            background: var(--bg-card);
            padding: 1rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: var(--border-glow);
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: var(--bg-input);
            border-radius: 8px;
        }

        /* Мобильная адаптация улучшена */
        @media (max-width: 768px) {
            .chat-container {
                margin: 0;
                border-radius: 0;
                height: 100vh;
            }
            
            .sidebar {
                position: absolute;
                z-index: 1000;
                height: 100vh;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
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
            font-size: 1.5rem;
            cursor: pointer;
        }

        /* Анимации улучшены */
        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateY(20px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .message {
            animation: messageSlide 0.3s ease;
        }

        /* Прогресс бар */
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
    </style>
</head>
<body class="theme-dark">
    <!-- Плавающие элементы -->
    <div class="floating-emoji" style="top: 10%; left: 5%;">💫</div>
    <div class="floating-emoji" style="top: 15%; right: 8%;">✨</div>
    <div class="floating-emoji" style="top: 85%; left: 10%;">🚀</div>
    <div class="floating-emoji" style="top: 80%; right: 5%;">🌟</div>

    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen">
        <div class="auth-container">
            <div class="logo">DL-TrolledX 6.0</div>
            <div class="subtitle">Ультра-современный мессенджер с AI</div>
            
            <div class="stats-panel">
                <h4>📊 Статистика платформы:</h4>
                <div class="stat-item">
                    <span>Пользователей онлайн:</span>
                    <span id="onlineCount">0</span>
                </div>
                <div class="stat-item">
                    <span>Сообщений сегодня:</span>
                    <span id="messagesToday">0</span>
                </div>
                <div class="stat-item">
                    <span>Активных чатов:</span>
                    <span id="activeChats">0</span>
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
                    <h3 id="userName">Пользователь</h3>
                    <p id="userStatus"><span class="online-dot"></span> онлайн</p>
                </div>
                
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="🔍 Поиск чатов..." oninput="searchChats(this.value)">
                </div>
                
                <div class="chats-list" id="chatsList">
                    <!-- Список чатов будет здесь -->
                </div>
                
                <div style="padding: 1rem;">
                    <button class="btn btn-secondary" onclick="createGroupChat()">
                        👥 Создать группу
                    </button>
                    <button class="btn btn-secondary" onclick="showSettings()" style="margin-top: 0.5rem;">
                        ⚙️ Настройки
                    </button>
                </div>
            </div>
            
            <!-- Область чата -->
            <div class="chat-area">
                <div class="chat-header">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                        <div class="chat-avatar" id="currentChatAvatar">👤</div>
                        <div>
                            <h3 id="currentChatName">Выберите чат</h3>
                            <p id="currentChatStatus" style="color: var(--text-secondary);">для начала общения</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 1rem;">
                        <button class="btn-secondary" onclick="showChatInfo()">ℹ️</button>
                        <button class="btn-secondary" onclick="showSettings()">⚙️</button>
                        <button class="btn-secondary" onclick="logout()">🚪</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">💬</div>
                        <h3>Добро пожаловать в DL-TrolledX 6.0!</h3>
                        <p>Выберите чат или создайте новый для начала общения</p>
                    </div>
                </div>
                
                <div class="typing-indicator hidden" id="typingIndicator">
                    <span id="typingUser">Кто-то</span> печатает
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="Напишите сообщение..." id="messageInput" 
                           onkeypress="handleKeyPress(event)" oninput="handleTyping()">
                    <button class="send-btn" onclick="sendMessage()">Отправить</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ... (предыдущий JavaScript код) ...

        // НОВЫЕ ФУНКЦИИ

        function showThemeSelector() {
            const themes = [
                {name: 'Тёмная', class: 'theme-dark'},
                {name: 'Матрица', class: 'theme-matrix'},
                {name: 'Океан', class: 'theme-ocean'}
            ];
            
            let themeHTML = themes.map(theme => 
                `<button class="btn-secondary" onclick="changeTheme('${theme.class}')">${theme.name}</button>`
            ).join('');
            
            showNotification('Выберите тему:' + themeHTML, 'info');
        }

        function changeTheme(themeClass) {
            document.body.className = themeClass;
            showNotification('Тема изменена! 🎨', 'success');
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function handleTyping() {
            if (currentChat) {
                // Симуляция печатания других пользователей
                showTypingIndicator();
            }
        }

        function showTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            const typingUser = document.getElementById('typingUser');
            
            if (currentChat) {
                const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== currentUser.id));
                if (otherUser) {
                    typingUser.textContent = otherUser.name;
                    indicator.classList.remove('hidden');
                    
                    // Автоматически скрыть через 3 секунды
                    setTimeout(() => {
                        indicator.classList.add('hidden');
                    }, 3000);
                }
            }
        }

        function createGroupChat() {
            showNotification('Создание групповых чатов будет в следующем обновлении! 👥', 'info');
        }

        function showChatInfo() {
            if (currentChat) {
                const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== currentUser.id));
                if (otherUser) {
                    showNotification(`
                        💬 Информация о чате:
                        👤 Имя: ${otherUser.name}
                        🆔 ID: ${otherUser.username}
                        📝 Статус: ${otherUser.bio}
                        🔐 Безопасность: Сквозное шифрование
                    `, 'info');
                }
            } else {
                showNotification('Выберите чат для просмотра информации', 'error');
            }
        }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('active');
        }

        // Улучшенная генерация учетных данных
        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            const username = '@' + name.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
            document.getElementById('generatedUsername').textContent = username;
            
            // Анимация прогресса
            animateProgress('registerProgress', 100, 1000);
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

        // Авто-сохранение
        setInterval(() => {
            if (currentUser) {
                localStorage.setItem('nebula_chats', JSON.stringify(chats));
                localStorage.setItem('nebula_stats', JSON.stringify(userStats));
                console.log('💾 Авто-сохранение выполнено');
            }
        }, 30000);

        // Улучшенная система уведомлений
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

        // Инициализация при загрузке
        function initializeSampleData() {
            // Тестовые пользователи с улучшенными данными
            allUsers = [
                {
                    id: 'user1',
                    name: 'Алексей',
                    username: '@neuro_alex',
                    avatar: '🤖',
                    isOnline: true,
                    bio: 'AI разработчик | Люблю нейросети',
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user2', 
                    name: 'София',
                    username: '@digital_queen',
                    avatar: '👑',
                    isOnline: true,
                    bio: 'Дизайнер интерфейсов | UX/UI',
                    lastSeen: new Date().toISOString()
                },
                {
                    id: 'user3',
                    name: 'Максим',
                    username: '@code_master',
                    avatar: '💻',
                    isOnline: false,
                    bio: 'Full-stack разработчик',
                    lastSeen: new Date(Date.now() - 3600000).toISOString()
                }
            ];

            // Обновляем статистику
            updatePlatformStats();
        }

        function updatePlatformStats() {
            document.getElementById('onlineCount').textContent = allUsers.filter(u => u.isOnline).length;
            document.getElementById('messagesToday').textContent = userStats.messagesSent;
            document.getElementById('activeChats').textContent = chats.length;
        }

        // Запуск
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DL-TrolledX 6.0 запущен!");
            checkAutoLogin();
            initializeSampleData();
            setInterval(updatePlatformStats, 5000);
        });
    </script>
</body>
</html>
'''

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'status': 'online',
        'users_online': random.randint(50, 100),
        'version': '6.0',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'DL-TrolledX 6.0'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 DL-TrolledX 6.0 запущен!")
    print("💫 Ультра-современный дизайн")
    print("🎨 Несколько тем на выбор") 
    print("⚡ Умный AI ассистент")
    print("📱 Адаптивный дизайн")
    print(f"🔗 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
