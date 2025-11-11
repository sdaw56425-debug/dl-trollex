# app.py
from flask import Flask, render_template_string
import datetime
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultramodern2024'

def generate_username():
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(1000, 9999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(12))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DL-TrolledX ✨ Мессенджер</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        :root {
            --bg-primary: #0a0a0a; --bg-secondary: #111111; --bg-card: #1a1a1a;
            --text-primary: #ffffff; --text-secondary: #b0b0b0; --accent-purple: #8b5cf6;
            --gradient-primary: linear-gradient(135deg, #8b5cf6, #ec4899, #3b82f6);
        }
        body { background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; }
        
        .screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .hidden { display: none !important; }
        
        .auth-container { background: var(--bg-card); border-radius: 20px; padding: 30px; width: 100%; max-width: 450px; border: 1px solid rgba(139, 92, 246, 0.3); }
        .logo { font-size: 2.5rem; font-weight: 800; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 1rem; }
        
        .btn { width: 100%; padding: 14px 20px; border: none; border-radius: 12px; font-size: 0.95rem; font-weight: 600; cursor: pointer; margin-bottom: 0.8rem; }
        .btn-primary { background: var(--gradient-primary); color: white; }
        .btn-secondary { background: var(--bg-secondary); color: var(--text-primary); border: 1px solid rgba(139, 92, 246, 0.3); }
        
        .app { display: none; height: 100vh; background: var(--bg-primary); width: 100%; }
        .chat-container { display: flex; height: 100vh; width: 100%; background: var(--bg-secondary); }
        
        .sidebar { width: 320px; background: var(--bg-card); border-right: 1px solid rgba(139, 92, 246, 0.3); display: flex; flex-direction: column; }
        .user-header { padding: 1.5rem; background: var(--bg-secondary); border-bottom: 1px solid rgba(139, 92, 246, 0.3); }
        .user-avatar { width: 50px; height: 50px; border-radius: 50%; background: var(--gradient-primary); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.8rem; }
        
        .chats-list { flex: 1; overflow-y: auto; padding: 1rem; }
        .chat-item { display: flex; align-items: center; padding: 1rem; border-radius: 12px; cursor: pointer; margin-bottom: 0.5rem; background: rgba(255,255,255,0.02); }
        .chat-item:hover { background: rgba(139, 92, 246, 0.1); }
        .chat-avatar { width: 45px; height: 45px; border-radius: 50%; background: var(--gradient-primary); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-right: 1rem; }
        
        .chat-area { flex: 1; display: flex; flex-direction: column; background: var(--bg-secondary); }
        .chat-header { padding: 1.2rem 1.5rem; background: var(--bg-card); border-bottom: 1px solid rgba(139, 92, 246, 0.3); }
        
        .messages-container { flex: 1; padding: 1.5rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem; }
        .message { max-width: 80%; padding: 1rem 1.2rem; border-radius: 18px; }
        .message.received { background: var(--bg-card); align-self: flex-start; }
        .message.sent { background: var(--gradient-primary); align-self: flex-end; color: white; }
        
        .message-input-container { padding: 1.2rem 1.5rem; background: var(--bg-card); border-top: 1px solid rgba(139, 92, 246, 0.3); display: flex; gap: 0.8rem; }
        .message-input { flex: 1; padding: 12px 16px; background: var(--bg-secondary); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 20px; color: var(--text-primary); }
        .send-btn { padding: 12px 20px; background: var(--gradient-primary); border: none; border-radius: 15px; color: white; cursor: pointer; }
    </style>
</head>
<body>
    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen">
        <div class="auth-container">
            <div class="logo">DL-TrolledX</div>
            <div style="color: var(--text-secondary); text-align: center; margin-bottom: 1.5rem;">
                Ультра-современный мессенджер
            </div>
            <button class="btn btn-primary" onclick="startQuickRegistration()">
                🚀 Начать
            </button>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">Регистрация</div>
            <div style="color: var(--text-secondary); text-align: center; margin-bottom: 1.5rem;">
                Создайте аккаунт
            </div>
            
            <div style="background: var(--bg-secondary); padding: 1.2rem; border-radius: 12px; margin: 1.2rem 0;">
                <div style="display: flex; justify-content: space-between; margin: 0.4rem 0; padding: 0.6rem; background: var(--bg-primary); border-radius: 8px;">
                    <span>👤 Имя:</span>
                    <span style="font-family: monospace; color: var(--accent-purple); font-weight: 600;" id="generatedName">...</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 0.4rem 0; padding: 0.6rem; background: var(--bg-primary); border-radius: 8px;">
                    <span>🔐 Пароль:</span>
                    <span style="font-family: monospace; color: var(--accent-purple); font-weight: 600;" id="generatedPassword">...</span>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="quickRegister()">
                💫 Войти
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewCredentials()">
                🔄 Новые данные
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
            <div class="sidebar">
                <div class="user-header">
                    <div class="user-avatar" id="userAvatar">😊</div>
                    <h3 id="userName" style="font-size: 1.1rem;">Пользователь</h3>
                    <p style="color: var(--accent-purple);">● онлайн</p>
                </div>
                
                <div class="chats-list" id="chatsList">
                    <!-- Чаты появятся здесь -->
                </div>
            </div>
            
            <!-- Область чата -->
            <div class="chat-area">
                <div class="chat-header">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div class="chat-avatar" id="currentChatAvatar">👤</div>
                        <div>
                            <h3 id="currentChatName" style="font-size: 1.1rem;">Выберите чат</h3>
                            <p style="color: var(--text-secondary); font-size: 0.8rem;">для начала общения</p>
                        </div>
                    </div>
                </div>
                
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                        <h3 style="margin-bottom: 0.5rem;">Добро пожаловать!</h3>
                        <p>Выберите чат для начала общения</p>
                    </div>
                </div>
                
                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="Напишите сообщение..." id="messageInput">
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

        // ТЕСТОВЫЕ ПОЛЬЗОВАТЕЛИ - создаем сразу
        allUsers = [
            { id: 'user1', name: 'Алексей', avatar: '🤖', isOnline: true },
            { id: 'user2', name: 'София', avatar: '👑', isOnline: true },
            { id: 'user3', name: 'Максим', avatar: '💻', isOnline: false }
        ];

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DL-TrolledX запущен");
            checkAutoLogin();
        });

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                console.log("🔑 Авто-вход:", currentUser.name);
                
                // ВАЖНО: Всегда создаем чаты при входе
                createSampleChats();
                showMainApp();
                
            } else {
                showScreen('welcomeScreen');
            }
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            document.getElementById(screenId).classList.remove('hidden');
        }

        function startQuickRegistration() {
            showScreen('registerScreen');
            generateNewCredentials();
        }

        function generateNewCredentials() {
            const name = generateUsername();
            const password = generatePassword();
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
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

        function quickRegister() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            
            if (!name || name === '...') {
                alert('Сначала сгенерируйте данные!');
                return;
            }
            
            const avatars = ['😎', '🤖', '👽', '🐲', '🦄'];
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                avatar: randomChoice(avatars),
                isOnline: true
            };
            
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
            // СОЗДАЕМ ЧАТЫ СРАЗУ
            createSampleChats();
            showMainApp();
        }

        // ВАЖНАЯ ФУНКЦИЯ: СОЗДАНИЕ ЧАТОВ
        function createSampleChats() {
            console.log("🔄 СОЗДАЕМ ЧАТЫ...");
            
            // Очищаем старые чаты
            chats = [];
            
            // Создаем чаты для каждого тестового пользователя
            allUsers.forEach(user => {
                const chatMessages = [
                    {
                        id: 'msg1',
                        text: `Привет! Я ${user.name}. Рад познакомиться! 👋`,
                        senderId: user.id,
                        timestamp: new Date().toISOString()
                    },
                    {
                        id: 'msg2', 
                        text: "Как твои дела? Что нового? 🚀",
                        senderId: 'current_user',
                        timestamp: new Date().toISOString()
                    },
                    {
                        id: 'msg3',
                        text: "Отлично! Работаю над интересными проектами! 💫",
                        senderId: user.id,
                        timestamp: new Date().toISOString()
                    }
                ];

                const newChat = {
                    id: `chat_${user.id}`,
                    participants: ['current_user', user.id],
                    lastMessage: chatMessages[chatMessages.length - 1],
                    messages: chatMessages,
                    unread: Math.floor(Math.random() * 3)
                };
                
                chats.push(newChat);
                console.log("✅ Создан чат с:", user.name);
            });
            
            // Сохраняем чаты
            localStorage.setItem('chats', JSON.stringify(chats));
            console.log("🎉 Все чаты созданы! Всего:", chats.length);
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.remove('hidden');
            
            // Обновляем интерфейс
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            
            // Загружаем чаты если есть сохраненные
            const savedChats = localStorage.getItem('chats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            }
            
            renderChatsList();
        }

        function renderChatsList() {
            const chatsList = document.getElementById('chatsList');
            
            console.log("📋 Рендерим чаты:", chats.length);
            
            if (chats.length === 0) {
                chatsList.innerHTML = `
                    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
                        <p>Чатов пока нет</p>
                        <button class="btn-secondary" onclick="createSampleChats(); renderChatsList();" style="margin-top: 1rem;">
                            Создать чаты
                        </button>
                    </div>
                `;
                return;
            }
            
            chatsList.innerHTML = chats.map(chat => {
                const otherUser = allUsers.find(u => u.id === chat.participants.find(p => p !== 'current_user'));
                if (!otherUser) return '';
                
                return `
                    <div class="chat-item" onclick="openChat('${chat.id}')">
                        <div class="chat-avatar">${otherUser.avatar}</div>
                        <div>
                            <div style="font-weight: 600;">${otherUser.name}</div>
                            <div style="color: var(--text-secondary); font-size: 0.8rem;">
                                ${chat.lastMessage?.text || 'Нет сообщений'}
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function openChat(chatId) {
            console.log("🔓 Открываем чат:", chatId);
            
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            const otherUser = allUsers.find(u => u.id === currentChat.participants.find(p => p !== 'current_user'));
            if (!otherUser) return;
            
            document.getElementById('currentChatName').textContent = otherUser.name;
            document.getElementById('currentChatAvatar').textContent = otherUser.avatar;
            
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = currentChat.messages.map(msg => {
                const isOwn = msg.senderId === 'current_user';
                return `
                    <div class="message ${isOwn ? 'sent' : 'received'}">
                        ${msg.text}
                    </div>
                `;
            }).join('');
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
                
                localStorage.setItem('chats', JSON.stringify(chats));
                
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.textContent = message;
                messagesContainer.appendChild(messageElement);
                
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                renderChatsList();
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 DL-TrolledX запущен!")
    print("💫 Теперь точно будут чаты!")
    print(f"🔗 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
