# app.py
from flask import Flask, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DL-TrolledX</title>
    <style>
        body { margin: 0; padding: 0; background: #0a0a0a; color: white; font-family: Arial; }
        .screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
        .hidden { display: none; }
        .auth-container { background: #1a1a1a; padding: 40px; border-radius: 20px; border: 1px solid #8b5cf6; max-width: 400px; width: 90%; }
        .btn { width: 100%; padding: 15px; margin: 10px 0; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; }
        .btn-primary { background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; }
        .btn-secondary { background: #222; color: white; border: 1px solid #8b5cf6; }
        
        .app { display: none; height: 100vh; background: #111; }
        .chat-container { display: flex; height: 100vh; }
        .sidebar { width: 300px; background: #1a1a1a; border-right: 1px solid #8b5cf6; }
        .user-header { padding: 20px; background: #222; border-bottom: 1px solid #8b5cf6; }
        .chats-list { padding: 20px; }
        .chat-item { padding: 15px; margin: 10px 0; background: #222; border-radius: 10px; cursor: pointer; }
        .chat-item:hover { background: #2a2a2a; }
        
        .chat-area { flex: 1; display: flex; flex-direction: column; }
        .chat-header { padding: 20px; background: #1a1a1a; border-bottom: 1px solid #8b5cf6; }
        .messages-container { flex: 1; padding: 20px; overflow-y: auto; }
        .message { padding: 10px 15px; margin: 5px 0; border-radius: 15px; max-width: 70%; }
        .received { background: #222; align-self: flex-start; }
        .sent { background: linear-gradient(135deg, #8b5cf6, #ec4899); align-self: flex-end; }
        .message-input-container { padding: 20px; background: #1a1a1a; border-top: 1px solid #8b5cf6; display: flex; gap: 10px; }
        .message-input { flex: 1; padding: 12px; background: #222; border: 1px solid #8b5cf6; border-radius: 20px; color: white; }
        .send-btn { padding: 12px 20px; background: #8b5cf6; border: none; border-radius: 20px; color: white; cursor: pointer; }
    </style>
</head>
<body>
    <!-- Экран приветствия -->
    <div id="welcomeScreen" class="screen">
        <div class="auth-container">
            <h1 style="text-align: center; background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px;">DL-TrolledX</h1>
            <p style="text-align: center; color: #b0b0b0; margin-bottom: 30px;">Ультра-современный мессенджер</p>
            <button class="btn btn-primary" onclick="startRegistration()">🚀 Начать</button>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-container">
            <h1 style="text-align: center; margin-bottom: 20px;">Регистрация</h1>
            <div style="background: #222; padding: 15px; border-radius: 10px; margin: 20px 0;">
                <div style="margin: 10px 0;">Имя: <span id="generatedName" style="color: #8b5cf6; font-weight: bold;">...</span></div>
                <div style="margin: 10px 0;">Пароль: <span id="generatedPassword" style="color: #8b5cf6; font-weight: bold;">...</span></div>
            </div>
            <button class="btn btn-primary" onclick="register()">💫 Войти</button>
            <button class="btn btn-secondary" onclick="generateCredentials()">🔄 Новые данные</button>
            <button class="btn btn-secondary" onclick="showScreen('welcomeScreen')">← Назад</button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="chat-container">
            <div class="sidebar">
                <div class="user-header">
                    <h3 id="userName">Пользователь</h3>
                    <p style="color: #8b5cf6;">● онлайн</p>
                </div>
                <div class="chats-list" id="chatsList">
                    <!-- Чаты появятся здесь -->
                </div>
            </div>
            <div class="chat-area">
                <div class="chat-header">
                    <h3 id="currentChatName">Выберите чат</h3>
                </div>
                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 50px; color: #b0b0b0;">
                        <div style="font-size: 48px; margin-bottom: 20px;">💬</div>
                        <h3>Добро пожаловать!</h3>
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
        
        // Тестовые пользователи
        const testUsers = [
            { id: 'user1', name: 'Алексей 🤖', avatar: '🤖' },
            { id: 'user2', name: 'София 👑', avatar: '👑' },
            { id: 'user3', name: 'Максим 💻', avatar: '💻' }
        ];

        // Проверяем авто-вход при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            const savedUser = localStorage.getItem('currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                loadChats();
                showMainApp();
            }
        });

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            document.getElementById(screenId).classList.remove('hidden');
        }

        function startRegistration() {
            showScreen('registerScreen');
            generateCredentials();
        }

        function generateCredentials() {
            const names = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой'];
            const nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк'];
            const name = names[Math.floor(Math.random() * names.length)] + nouns[Math.floor(Math.random() * nouns.length)] + Math.floor(Math.random() * 1000);
            const password = Math.random().toString(36).slice(-12);
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
        }

        function register() {
            const name = document.getElementById('generatedName').textContent;
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                avatar: '😎'
            };
            
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            createSampleChats();
            showMainApp();
        }

        function createSampleChats() {
            chats = [];
            
            testUsers.forEach(user => {
                const messages = [
                    { id: '1', text: `Привет! Я ${user.name}. Рад познакомиться! 👋`, senderId: user.id },
                    { id: '2', text: "Привет! Как дела? 🚀", senderId: 'current_user' },
                    { id: '3', text: "Отлично! Работаю над крутыми проектами! 💫", senderId: user.id }
                ];
                
                chats.push({
                    id: 'chat_' + user.id,
                    name: user.name,
                    avatar: user.avatar,
                    messages: messages,
                    lastMessage: messages[messages.length - 1]
                });
            });
            
            localStorage.setItem('chats', JSON.stringify(chats));
        }

        function loadChats() {
            const savedChats = localStorage.getItem('chats');
            if (savedChats) {
                chats = JSON.parse(savedChats);
            } else {
                createSampleChats();
            }
        }

        function showMainApp() {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.remove('hidden');
            
            document.getElementById('userName').textContent = currentUser.name;
            renderChatsList();
        }

        function renderChatsList() {
            const chatsList = document.getElementById('chatsList');
            
            if (chats.length === 0) {
                chatsList.innerHTML = '<p style="text-align: center; color: #b0b0b0;">Чатов пока нет</p>';
                return;
            }
            
            chatsList.innerHTML = chats.map(chat => `
                <div class="chat-item" onclick="openChat('${chat.id}')">
                    <strong>${chat.name}</strong><br>
                    <small style="color: #b0b0b0;">${chat.lastMessage.text}</small>
                </div>
            `).join('');
        }

        function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;
            
            document.getElementById('currentChatName').textContent = currentChat.name;
            
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = currentChat.messages.map(msg => `
                <div class="message ${msg.senderId === 'current_user' ? 'sent' : 'received'}">
                    ${msg.text}
                </div>
            `).join('');
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (text && currentChat) {
                const newMessage = {
                    id: 'msg_' + Date.now(),
                    text: text,
                    senderId: 'current_user'
                };
                
                currentChat.messages.push(newMessage);
                currentChat.lastMessage = newMessage;
                
                localStorage.setItem('chats', JSON.stringify(chats));
                
                const messagesContainer = document.getElementById('messagesContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message sent';
                messageDiv.textContent = text;
                messagesContainer.appendChild(messageDiv);
                
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
    print("💫 Теперь ВСЕ РАБОТАЕТ!")
    print(f"🔗 http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)
