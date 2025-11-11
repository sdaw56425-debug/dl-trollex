<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UltraModern Messenger</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
            padding: 20px;
        }

        .screen {
            display: none;
        }

        #authScreen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            min-height: 100vh;
        }

        .logo {
            font-size: 3em;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            color: white;
            font-size: 1.1em;
            cursor: pointer;
            margin: 10px;
            transition: transform 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        #mainApp {
            display: none;
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }

        .chat-list {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
            max-height: 300px;
            overflow-y: auto;
        }

        .chat-item {
            padding: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            cursor: pointer;
            transition: background 0.3s ease;
            border-radius: 10px;
            margin-bottom: 10px;
        }

        .chat-item:hover {
            background: rgba(255,255,255,0.2);
        }

        .chat-item.active {
            background: rgba(255,255,255,0.3);
        }

        .chat-window {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }

        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }

        .user-message {
            background: linear-gradient(45deg, #48dbfb, #0abde3);
            margin-left: auto;
            text-align: right;
        }

        .other-message {
            background: rgba(255,255,255,0.2);
        }

        .message-time {
            font-size: 0.8em;
            opacity: 0.7;
            margin-top: 5px;
        }

        .message-input {
            display: flex;
            gap: 10px;
        }

        .message-input input {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 1em;
        }

        .message-input input::placeholder {
            color: rgba(255,255,255,0.7);
        }

        .loading {
            text-align: center;
            padding: 20px;
        }

        .error {
            background: rgba(255,0,0,0.2);
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
        }

        .success {
            background: rgba(0,255,0,0.2);
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <!-- Экран авторизации -->
    <div id="authScreen" class="screen">
        <div class="logo">💫 UltraMsg</div>
        <p>Современный мессенджер нового поколения</p>
        <button class="btn" onclick="register()" id="registerBtn">Начать общение</button>
        <div id="authMessage"></div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="screen">
        <div class="header">
            <h2>💫 UltraMsg</h2>
            <div id="userInfo">Загрузка...</div>
        </div>
        
        <div class="chat-list" id="chatList">
            <div class="loading">Загрузка чатов...</div>
        </div>

        <div class="chat-window" id="chatWindow">
            <div id="messagesContainer" class="loading">
                Выберите чат для начала общения
            </div>
        </div>

        <div class="message-input">
            <input type="text" id="messageInput" placeholder="Введите сообщение..." onkeypress="handleKeyPress(event)" disabled>
            <button class="btn" onclick="sendMessage()" id="sendBtn" disabled>Отправить</button>
        </div>
    </div>

    <script>
        let currentUser = null;
        let chats = [];
        let currentChat = null;

        // Показ экрана
        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.style.display = 'none';
            });
            document.getElementById(screenId).style.display = screenId === 'mainApp' ? 'block' : 'flex';
        }

        // Показать сообщение
        function showMessage(text, type = 'info') {
            const messageDiv = document.getElementById('authMessage');
            messageDiv.innerHTML = `<div class="${type}">${text}</div>`;
            setTimeout(() => messageDiv.innerHTML = '', 3000);
        }

        // Регистрация
        async function register() {
            const btn = document.getElementById('registerBtn');
            btn.disabled = true;
            btn.textContent = 'Регистрация...';

            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (data.success) {
                    currentUser = data.user;
                    localStorage.setItem('messenger_user', JSON.stringify(currentUser));
                    showMessage('Регистрация успешна!', 'success');
                    await loadApp();
                } else {
                    showMessage(data.error || 'Ошибка регистрации', 'error');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                showMessage('Ошибка соединения', 'error');
            } finally {
                btn.disabled = false;
                btn.textContent = 'Начать общение';
            }
        }

        // Загрузка приложения
        async function loadApp() {
            showScreen('mainApp');
            await loadUserInfo();
            await loadChats();
        }

        // Загрузка информации пользователя
        async function loadUserInfo() {
            if (!currentUser) return;

            document.getElementById('userInfo').innerHTML = `
                <div>👤 ${currentUser.name}</div>
                <div>⭐ Уровень ${currentUser.level}</div>
            `;
        }

        // Загрузка чатов
        async function loadChats() {
            try {
                const response = await fetch('/api/chats');
                const data = await response.json();

                if (data.success) {
                    chats = data.chats || [];
                    renderChatList();
                } else {
                    document.getElementById('chatList').innerHTML = '<div class="error">Ошибка загрузки чатов</div>';
                }
            } catch (error) {
                console.error('Ошибка загрузки чатов:', error);
                document.getElementById('chatList').innerHTML = '<div class="error">Ошибка соединения</div>';
            }
        }

        // Отрисовка списка чатов
        function renderChatList() {
            const chatList = document.getElementById('chatList');
            
            if (chats.length === 0) {
                chatList.innerHTML = '<div class="loading">Нет чатов</div>';
                return;
            }

            chatList.innerHTML = chats.map(chat => `
                <div class="chat-item ${currentChat?.id === chat.id ? 'active' : ''}" onclick="openChat('${chat.id}')">
                    <strong>${chat.name}</strong>
                    ${chat.unread > 0 ? `<span style="background: red; border-radius: 50%; padding: 2px 6px; font-size: 0.8em;">${chat.unread}</span>` : ''}
                    <p>${chat.last_message}</p>
                    <small>${new Date(chat.last_message_time).toLocaleTimeString()}</small>
                </div>
            `).join('');
        }

        // Открытие чата
        async function openChat(chatId) {
            currentChat = chats.find(chat => chat.id === chatId);
            if (!currentChat) return;

            // Активируем поле ввода
            document.getElementById('messageInput').disabled = false;
            document.getElementById('sendBtn').disabled = false;

            // Показываем загрузку
            document.getElementById('messagesContainer').innerHTML = '<div class="loading">Загрузка сообщений...</div>';
            renderChatList();

            try {
                const response = await fetch(`/api/messages/${chatId}`);
                const data = await response.json();

                if (data.success && data.messages) {
                    const messagesContainer = document.getElementById('messagesContainer');
                    messagesContainer.innerHTML = data.messages.map(message => `
                        <div class="message ${message.is_user ? 'user-message' : 'other-message'}">
                            ${message.text}
                            <div class="message-time">
                                ${new Date(message.timestamp).toLocaleTimeString()}
                            </div>
                        </div>
                    `).join('');

                    // Прокрутка вниз
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                } else {
                    document.getElementById('messagesContainer').innerHTML = '<div class="error">Ошибка загрузки сообщений</div>';
                }
            } catch (error) {
                console.error('Ошибка загрузки сообщений:', error);
                document.getElementById('messagesContainer').innerHTML = '<div class="error">Ошибка соединения</div>';
            }
        }

        // Отправка сообщения
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (!text || !currentChat) return;

            try {
                const response = await fetch('/api/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        chat_id: currentChat.id,
                        text: text
                    })
                });

                const data = await response.json();

                if (data.success) {
                    input.value = '';
                    // Обновляем сообщения
                    await openChat(currentChat.id);
                    // Обновляем список чатов
                    await loadChats();
                } else {
                    showMessage(data.error || 'Ошибка отправки', 'error');
                }
            } catch (error) {
                console.error('Ошибка отправки:', error);
                showMessage('Ошибка соединения', 'error');
            }
        }

        // Обработка клавиши Enter
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Инициализация при загрузке
        window.addEventListener('load', async function() {
            const savedUser = localStorage.getItem('messenger_user');
            
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    await loadApp();
                } catch (error) {
                    console.error('Ошибка загрузки пользователя:', error);
                    showScreen('authScreen');
                }
            } else {
                showScreen('authScreen');
            }
        });
    </script>
</body>
</html>
