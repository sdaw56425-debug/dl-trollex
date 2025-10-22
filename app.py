# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ИСПРАВЛЕННЫЕ КНОПКИ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

# База данных в памяти
users_db = {}
messages_db = {}
news_messages = [
    {
        'id': '1',
        'text': 'Добро пожаловать в DLtrollex! 🎉',
        'sender_name': 'Администратор',
        'timestamp': datetime.datetime.now().isoformat(),
    },
    {
        'id': '2', 
        'text': 'Это фиолетовый мессенджер с максимальной кастомизацией! 💜',
        'sender_name': 'Администратор', 
        'timestamp': datetime.datetime.now().isoformat(),
    }
]

# Админ
ADMIN_PASSWORD = "dltrollex123"

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
    <title>DLtrollex</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💜</text></svg>">
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
        }
        
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px var(--accent-color), 0 0 20px var(--accent-color); }
            50% { text-shadow: 0 0 20px var(--accent-color), 0 0 30px var(--accent-color), 0 0 40px var(--accent-color); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
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
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }
        
        .btn-admin {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        
        .btn-admin:hover {
            box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4);
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
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: var(--bg-color);
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            z-index: 3000;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .chat-container {
            display: flex;
            height: 100vh;
        }
        
        .sidebar {
            width: 300px;
            background: var(--card-color);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        
        .message {
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
            max-width: 70%;
        }
        
        .message.own {
            background: var(--accent-color);
            margin-left: auto;
        }
    </style>
</head>
<body>
    <!-- Главный экран выбора -->
    <div id="mainScreen" class="screen">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Фиолетовый чат с максимальной кастомизацией</div>
            
            <button class="btn pulse" onclick="showRegisterScreen()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn btn-admin pulse" onclick="showAdminScreen()">
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
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" onclick="showMainScreen()">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
        </div>
    </div>

    <!-- Экран входа админа -->
    <div id="adminScreen" class="screen hidden">
        <div class="auth-box floating">
            <div class="logo glowing-logo">💜 DLtrollex</div>
            <div class="subtitle">Панель администратора</div>
            
            <input type="password" id="adminPass" class="input-field" placeholder="🔒 Введите пароль администратора">
            
            <button class="btn btn-admin pulse" onclick="adminLogin()">⚡ Войти</button>
            
            <button class="btn" onclick="showMainScreen()">
                <span>← Назад</span>
            </button>
            
            <div id="adminError" class="error"></div>
        </div>
    </div>

    <!-- Основной интерфейс мессенджера -->
    <div id="mainApp" class="app">
        <!-- Интерфейс будет генерироваться JavaScript -->
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let messages = [];

        // Проверка автоматического входа при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            checkAutoLogin();
        });

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    console.log("🔑 Автоматический вход:", currentUser);
                    showMainApp();
                } catch (e) {
                    console.log("❌ Ошибка автоматического входа:", e);
                    localStorage.removeItem('dlcurrentUser');
                }
            }
        }

        // Функции навигации
        function showMainScreen() {
            console.log("📱 Показываем главный экран");
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showRegisterScreen() {
            console.log("📝 Показываем экран регистрации");
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
            
            // Фокус на поле ввода имени
            document.getElementById('regName').focus();
        }

        function showAdminScreen() {
            console.log("👑 Показываем экран админа");
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
            document.getElementById('mainApp').style.display = 'none';
            
            // Фокус на поле пароля
            document.getElementById('adminPass').focus();
        }

        function showMainApp() {
            console.log("💬 Показываем основное приложение");
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            renderChatInterface();
            showNotification('Добро пожаловать в DLtrollex! 🎉');
        }

        // Регистрация пользователя
        function registerUser() {
            console.log("🔄 Начало регистрации...");
            
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            const errorDiv = document.getElementById('registerError');
            
            // Проверка имени
            if (!name) {
                errorDiv.textContent = '❌ Введите ваше имя';
                return;
            }
            
            // Очистка ошибок
            errorDiv.textContent = '';
            
            // Создание пользователя
            const user_id = Date.now().toString();
            const finalUsername = username || `user${Math.floor(Math.random() * 10000)}`;
            
            currentUser = {
                id: user_id,
                name: name,
                username: finalUsername,
                avatar: '👤',
                registered_at: new Date().toISOString(),
            };
            
            // Сохранение в localStorage
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            
            console.log("✅ Пользователь создан:", currentUser);
            
            // Мгновенный переход в чат
            showMainApp();
        }

        // Вход администратора
        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            const errorDiv = document.getElementById('adminError');
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    is_admin: true
                };
                
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
                showNotification('✅ Вход как администратор выполнен');
            } else {
                errorDiv.textContent = '❌ Неверный пароль администратора';
            }
        }

        // Рендер интерфейса чата
        function renderChatInterface() {
            const isAdmin = currentUser && currentUser.is_admin;
            
            document.getElementById('mainApp').innerHTML = `
                <div class="chat-container">
                    <!-- Боковая панель -->
                    <div class="sidebar">
                        <div style="padding: 20px; border-bottom: 1px solid var(--border-color);">
                            <div class="logo" style="font-size: 24px; margin-bottom: 10px;">💜 DLtrollex</div>
                            <div style="color: #888; font-size: 12px;">Добро пожаловать, ${currentUser.name}!</div>
                            ${isAdmin ? '<div style="color: #dc2626; font-size: 10px; margin-top: 5px;">👑 Администратор</div>' : ''}
                        </div>
                        
                        <div style="padding: 15px; border-bottom: 1px solid var(--border-color);">
                            <div style="font-weight: bold; margin-bottom: 10px;">👥 Онлайн</div>
                            <div style="background: var(--secondary-color); padding: 10px; border-radius: 8px; margin: 5px 0;">
                                <strong>${currentUser.name}</strong>
                                <div style="color: #888; font-size: 12px;">${currentUser.username}</div>
                            </div>
                            <div style="background: var(--secondary-color); padding: 10px; border-radius: 8px; margin: 5px 0;">
                                <strong>Бот DLtrollex</strong>
                                <div style="color: #888; font-size: 12px;">@bot</div>
                            </div>
                        </div>
                        
                        <div style="flex: 1; padding: 15px;">
                            <button class="btn" onclick="showChat()" style="margin-bottom: 10px;">💬 Чат</button>
                            <button class="btn" onclick="showSettings()" style="margin-bottom: 10px;">⚙️ Настройки</button>
                            ${isAdmin ? '<button class="btn btn-admin" onclick="showAdminPanel()">👑 Админ-панель</button>' : ''}
                        </div>
                        
                        <div style="padding: 15px;">
                            <button class="btn" onclick="logout()">🚪 Выйти</button>
                        </div>
                    </div>
                    
                    <!-- Основная область -->
                    <div class="chat-area">
                        <div id="chatContent" style="flex: 1; padding: 20px;">
                            <div style="text-align: center; padding: 50px;">
                                <div class="logo glowing-logo" style="font-size: 80px;">💜</div>
                                <h1>Добро пожаловать в DLtrollex!</h1>
                                <p style="margin: 20px 0;">Вы успешно вошли как <strong>${currentUser.name}</strong></p>
                                <p style="color: #888; margin-bottom: 30px;">@${currentUser.username}</p>
                                
                                <div style="background: var(--card-color); padding: 30px; border-radius: 15px; max-width: 500px; margin: 0 auto;">
                                    <h3 style="color: var(--accent-color); margin-bottom: 20px;">📢 Новости DLtrollex</h3>
                                    <div style="text-align: left;">
                                        <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                                            <p><strong>Администратор:</strong> Добро пожаловать в DLtrollex! 🎉</p>
                                            <small style="color: #888;">Только что</small>
                                        </div>
                                        <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px;">
                                            <p><strong>Администратор:</strong> Это фиолетовый мессенджер с максимальной кастомизацией! 💜</p>
                                            <small style="color: #888;">Только что</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Функции чата
        function showChat() {
            document.getElementById('chatContent').innerHTML = `
                <div class="messages-container" id="messagesContainer">
                    <div class="message">
                        <strong>Администратор:</strong> Добро пожаловать в DLtrollex! 🎉
                        <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                    </div>
                    <div class="message">
                        <strong>Администратор:</strong> Это фиолетовый мессенджер с максимальной кастомизацией! 💜
                        <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                    </div>
                    <div class="message own">
                        <strong>Вы:</strong> Привет всем! 👋
                        <div style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 5px;">Только что</div>
                    </div>
                </div>
                <div style="padding: 20px; background: var(--card-color); border-top: 1px solid var(--border-color);">
                    <input type="text" id="messageInput" class="input-field" placeholder="💬 Напишите сообщение..." style="margin-bottom: 10px;">
                    <button class="btn" onclick="sendMessage()">📤 Отправить</button>
                </div>
            `;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message) {
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = 'message own';
                messageElement.innerHTML = `
                    <strong>Вы:</strong> ${message}
                    <div style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 5px;">Только что</div>
                `;
                messagesContainer.appendChild(messageElement);
                input.value = '';
                
                // Прокрутка вниз
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Имитация ответа
                setTimeout(() => {
                    const responses = [
                        'Привет! Как дела? 😊',
                        'Классное сообщение! 👍',
                        'Я бот DLtrollex! 🤖',
                        'Отличный мессенджер, правда? 💜'
                    ];
                    const response = responses[Math.floor(Math.random() * responses.length)];
                    
                    const responseElement = document.createElement('div');
                    responseElement.className = 'message';
                    responseElement.innerHTML = `
                        <strong>Бот DLtrollex:</strong> ${response}
                        <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                    `;
                    messagesContainer.appendChild(responseElement);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }, 1000);
            }
        }

        function showSettings() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 30px; max-width: 600px; margin: 0 auto;">
                    <h2>⚙️ Настройки</h2>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin: 20px 0;">
                        <h3 style="color: var(--accent-color); margin-bottom: 15px;">👤 Профиль</h3>
                        <input type="text" class="input-field" value="${currentUser.name}" placeholder="Ваше имя">
                        <input type="text" class="input-field" value="${currentUser.username}" placeholder="Юзернейм">
                        <button class="btn" style="margin-top: 10px;">💾 Сохранить</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin: 20px 0;">
                        <h3 style="color: var(--accent-color); margin-bottom: 15px;">🎨 Внешний вид</h3>
                        <button class="btn" style="margin: 5px;">💜 Фиолетовая тема</button>
                        <button class="btn" style="margin: 5px;">🔵 Синяя тема</button>
                        <button class="btn" style="margin: 5px;">🟢 Зеленая тема</button>
                    </div>
                </div>
            `;
        }

        function showAdminPanel() {
            document.getElementById('chatContent').innerHTML = `
                <div style="padding: 30px; max-width: 600px; margin: 0 auto;">
                    <h2>👑 Панель администратора</h2>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin: 20px 0;">
                        <h3 style="color: var(--accent-color); margin-bottom: 15px;">📊 Статистика</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px; text-align: center;">
                                <div style="font-size: 24px; font-weight: bold; color: var(--accent-color);">${Object.keys(users_db).length}</div>
                                <div style="color: #888;">Пользователей</div>
                            </div>
                            <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px; text-align: center;">
                                <div style="font-size: 24px; font-weight: bold; color: var(--accent-color);">${messages.length}</div>
                                <div style="color: #888;">Сообщений</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px; margin: 20px 0;">
                        <h3 style="color: var(--accent-color); margin-bottom: 15px;">🛠️ Управление</h3>
                        <button class="btn btn-admin" style="margin: 5px;">📢 Отправить уведомление</button>
                        <button class="btn btn-admin" style="margin: 5px;">🔄 Перезапустить сервер</button>
                        <button class="btn" style="margin: 5px; background: #dc2626;">🗑️ Очистить данные</button>
                    </div>
                </div>
            `;
        }

        function logout() {
            currentUser = null;
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 20px;">💡</div>
                    <div>${message}</div>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 3000);
        }

        // Обработка клавиши Enter в формах
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                // Регистрация
                if (!document.getElementById('registerScreen').classList.contains('hidden')) {
                    registerUser();
                }
                // Вход админа
                if (!document.getElementById('adminScreen').classList.contains('hidden')) {
                    adminLogin();
                }
                // Отправка сообщения
                if (document.getElementById('messageInput')) {
                    sendMessage();
                }
            }
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
    print("🚀 Запуск DLtrollex с исправленными кнопками...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("✅ Все кнопки работают мгновенно!")
    print("🎯 Регистрация занимает 0 секунд!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
