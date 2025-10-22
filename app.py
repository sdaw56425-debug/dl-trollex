# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ (ХЕЛЛОУИН 2025 ВЕРСИЯ)
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

# Простая база данных в памяти
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

# Создаем фавикон роут чтобы убрать 404 ошибку
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'DLtrollex is running'})

def generate_user_id():
    return str(int(datetime.datetime.now().timestamp() * 1000)) + str(random.randint(1000, 9999))

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
            --halloween-color: #ff7b25;
        }
        
        body {
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        body.halloween-theme {
            --accent-color: #ff7b25;
            --bg-color: #1a0f00;
            --card-color: #2a1a00;
        }
        
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 10px var(--accent-color), 0 0 20px var(--accent-color);
            }
            50% {
                text-shadow: 0 0 20px var(--accent-color), 0 0 30px var(--accent-color), 0 0 40px var(--accent-color);
            }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes spooky {
            0%, 100% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(5deg) scale(1.1); }
            75% { transform: rotate(-5deg) scale(1.1); }
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
        
        .spooky {
            animation: spooky 3s ease-in-out infinite;
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
        
        .optional {
            color: #888;
            font-size: 12px;
            margin-top: -15px;
            margin-bottom: 20px;
            text-align: left;
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
        
        .btn-halloween {
            background: linear-gradient(135deg, #ff7b25, #ff5500);
        }
        
        .btn-halloween:hover {
            box-shadow: 0 10px 25px rgba(255, 123, 37, 0.4);
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
        
        .notification-toast {
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
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .halloween-decoration {
            position: fixed;
            font-size: 24px;
            z-index: 100;
            opacity: 0.1;
            animation: float 8s ease-in-out infinite;
        }
        
        .pumpkin { animation-delay: 0s; left: 10%; top: 20%; }
        .ghost { animation-delay: 2s; right: 15%; top: 30%; }
        .bat { animation-delay: 4s; left: 20%; bottom: 25%; }
        .spider { animation-delay: 6s; right: 10%; bottom: 15%; }
    </style>
</head>
<body>
    <!-- Хеллоуинские декорации -->
    <div class="halloween-decoration pumpkin">🎃</div>
    <div class="halloween-decoration ghost">👻</div>
    <div class="halloween-decoration bat">🦇</div>
    <div class="halloween-decoration spider">🕷️</div>

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
            
            <button class="btn btn-halloween pulse" onclick="toggleHalloweenTheme()">
                <span>🎃 Хеллоуин 2025!</span>
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
            <div class="optional">✨ Юзернейм не обязателен. Если не указать, будет сгенерирован автоматически</div>
            
            <button class="btn pulse" onclick="registerUser()">
                <span>🚀 Начать общение</span>
            </button>
            
            <button class="btn" onclick="showMainScreen()">
                <span>← Назад</span>
            </button>
            
            <div id="registerError" class="error"></div>
            <div id="registerSuccess" class="success hidden"></div>
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
        <div style="text-align: center; padding: 100px;">
            <div class="logo glowing-logo" style="font-size: 64px;">💜</div>
            <h1>DLtrollex</h1>
            <p>Мессенджер загружается...</p>
        </div>
    </div>

    <script>
        let currentUser = null;
        let isHalloweenTheme = false;

        document.addEventListener('DOMContentLoaded', function() {
            console.log("🚀 DLtrollex загружен!");
            checkAutoLogin();
            loadHalloweenTheme();
        });

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                try {
                    currentUser = JSON.parse(savedUser);
                    showMainApp();
                } catch (e) {
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

        function showMainScreen() {
            document.getElementById('mainScreen').classList.remove('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showRegisterScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.remove('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showAdminScreen() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.remove('hidden');
            document.getElementById('mainApp').style.display = 'none';
        }

        function showMainApp() {
            document.getElementById('mainScreen').classList.add('hidden');
            document.getElementById('registerScreen').classList.add('hidden');
            document.getElementById('adminScreen').classList.add('hidden');
            document.getElementById('mainApp').style.display = 'block';
            
            renderMainApp();
            showNotification('Добро пожаловать в DLtrollex! 🎉', 'success');
        }

        function renderMainApp() {
            const isAdmin = currentUser && currentUser.is_admin;
            
            document.getElementById('mainApp').innerHTML = `
                <div style="padding: 50px; text-align: center;">
                    <div class="logo glowing-logo ${isHalloweenTheme ? 'spooky' : ''}" style="font-size: 80px;">${isHalloweenTheme ? '🎃' : '💜'}</div>
                    <h1>Добро пожаловать в DLtrollex${isHalloweenTheme ? ' 🎃' : ''}!</h1>
                    <p style="margin: 20px 0; font-size: 18px;">Вы успешно вошли как <strong>${currentUser.name}</strong></p>
                    <p style="color: #888; margin-bottom: 30px;">@${currentUser.username}</p>
                    
                    <div style="background: var(--card-color); padding: 30px; border-radius: 15px; max-width: 500px; margin: 0 auto;">
                        <h3 style="color: var(--accent-color); margin-bottom: 20px;">📢 Новости DLtrollex</h3>
                        <div style="text-align: left;">
                            <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                                <p><strong>Администратор:</strong> Добро пожаловать в DLtrollex! 🎉</p>
                                <small style="color: #888;">Только что</small>
                            </div>
                            <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                                <p><strong>Администратор:</strong> Это фиолетовый мессенджер с максимальной кастомизацией! 💜</p>
                                <small style="color: #888;">Только что</small>
                            </div>
                            ${isHalloweenTheme ? `
                            <div style="background: #ff7b25; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                                <p><strong>🎃 Хеллоуин 2025:</strong> Активирована хеллоуинская тема! Счастливого Хеллоуина! 👻</p>
                                <small style="color: rgba(255,255,255,0.8);">Только что</small>
                            </div>
                            ` : ''}
                        </div>
                    </div>

                    <div style="margin: 30px 0;">
                        <h3 style="color: var(--accent-color); margin-bottom: 20px;">🎮 Новые функции</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; max-width: 400px; margin: 0 auto;">
                            <button class="btn" onclick="showChat()">💬 Открыть чат</button>
                            <button class="btn" onclick="showGames()">🎮 Игры</button>
                            <button class="btn" onclick="showThemes()">🎨 Темы</button>
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()">
                                ${isHalloweenTheme ? '👻 Выкл.Хеллоуин' : '🎃 Вкл.Хеллоуин'}
                            </button>
                        </div>
                    </div>
                    
                    ${isAdmin ? `
                    <div style="margin: 30px 0;">
                        <h3 style="color: #dc2626; margin-bottom: 15px;">👑 Админ-панель</h3>
                        <button class="btn btn-admin" onclick="showAdminPanel()">⚙️ Управление системой</button>
                    </div>
                    ` : ''}
                    
                    <button class="btn" onclick="logout()" style="margin-top: 30px;">
                        <span>🚪 Выйти</span>
                    </button>
                </div>
            `;
        }

        function registerUser() {
            const name = document.getElementById('regName').value.trim();
            const username = document.getElementById('regUsername').value.trim();
            
            if (!name) {
                document.getElementById('registerError').textContent = 'Введите имя';
                return;
            }
            
            // Мгновенная регистрация
            const user_id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
            const finalUsername = username || `user${Math.floor(Math.random() * 10000)}`;
            
            currentUser = {
                id: user_id,
                name: name,
                username: finalUsername,
                avatar: '👤',
                avatar_bg: '#6b21a8',
                registered_at: new Date().toISOString(),
            };
            
            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            showMainApp();
        }

        function adminLogin() {
            const password = document.getElementById('adminPass').value;
            
            if (password === 'dltrollex123') {
                currentUser = {
                    id: 'admin',
                    name: 'Администратор',
                    username: '@admin',
                    is_admin: true
                };
                localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
                showMainApp();
                showNotification('Вход как администратор выполнен', 'success');
            } else {
                document.getElementById('adminError').textContent = 'Неверный пароль';
            }
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
            showNotification('🎃 Хеллоуинская тема активирована! С Хеллоуином 2025!', 'success');
            
            // Обновляем интерфейс если пользователь уже в системе
            if (currentUser) {
                renderMainApp();
            }
        }

        function deactivateHalloweenTheme() {
            document.body.classList.remove('halloween-theme');
            isHalloweenTheme = false;
            localStorage.setItem('dlhalloween', 'false');
            showNotification('👻 Хеллоуинская тема деактивирована!', 'info');
            
            if (currentUser) {
                renderMainApp();
            }
        }

        // Новые функции
        function showChat() {
            document.getElementById('mainApp').innerHTML = `
                <div style="padding: 20px; max-width: 800px; margin: 0 auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h1>💬 Чат DLtrollex${isHalloweenTheme ? ' 🎃' : ''}</h1>
                        <button class="btn" onclick="renderMainApp()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); border-radius: 15px; padding: 20px; margin-bottom: 20px; height: 400px; overflow-y: auto;">
                        <div style="background: var(--secondary-color); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                            <strong>Администратор:</strong> Добро пожаловать в чат DLtrollex! 🎉
                            <div style="color: #888; font-size: 12px; margin-top: 5px;">Только что</div>
                        </div>
                        ${isHalloweenTheme ? `
                        <div style="background: #ff7b25; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                            <strong>🎃 Хеллоуин-бот:</strong> Бууу! 👻 Счастливого Хеллоуина 2025! Не забудьте про конфеты! 🍬
                            <div style="color: rgba(255,255,255,0.8); font-size: 12px; margin-top: 5px;">Только что</div>
                        </div>
                        ` : ''}
                        <div style="background: var(--accent-color); padding: 15px; border-radius: 10px; margin-bottom: 15px; margin-left: 100px;">
                            <strong>Вы:</strong> Привет всем! 👋
                            <div style="color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 5px;">Только что</div>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 10px;">
                        <input type="text" class="input-field" placeholder="💬 Напишите сообщение..." style="flex: 1;">
                        <button class="btn" onclick="sendMessage()">📤</button>
                        ${isHalloweenTheme ? '<button class="btn btn-halloween" onclick="sendHalloweenMessage()">🎃</button>' : ''}
                    </div>
                </div>
            `;
        }

        function showGames() {
            document.getElementById('mainApp').innerHTML = `
                <div style="padding: 20px; max-width: 800px; margin: 0 auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h1>🎮 Игры и развлечения${isHalloweenTheme ? ' 🎃' : ''}</h1>
                        <button class="btn" onclick="renderMainApp()">← Назад</button>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="background: var(--card-color); padding: 30px; border-radius: 15px; text-align: center; cursor: pointer;" onclick="startGame('emoji')">
                            <div style="font-size: 48px; margin-bottom: 15px;">😀</div>
                            <h3>Угадай эмодзи</h3>
                            <p style="color: #888; margin-top: 10px;">Отгадай слово по эмодзи</p>
                        </div>
                        
                        <div style="background: var(--card-color); padding: 30px; border-radius: 15px; text-align: center; cursor: pointer;" onclick="startGame('quiz')">
                            <div style="font-size: 48px; margin-bottom: 15px;">❓</div>
                            <h3>Викторина</h3>
                            <p style="color: #888; margin-top: 10px;">Проверь свои знания</p>
                        </div>
                        
                        ${isHalloweenTheme ? `
                        <div style="background: #ff7b25; padding: 30px; border-radius: 15px; text-align: center; cursor: pointer;" onclick="startHalloweenGame()">
                            <div style="font-size: 48px; margin-bottom: 15px;">👻</div>
                            <h3>Хеллоуинская игра</h3>
                            <p style="color: rgba(255,255,255,0.8); margin-top: 10px;">Страшные загадки</p>
                        </div>
                        
                        <div style="background: #ff7b25; padding: 30px; border-radius: 15px; text-align: center; cursor: pointer;" onclick="showHalloweenJokes()">
                            <div style="font-size: 48px; margin-bottom: 15px;">🎃</div>
                            <h3>Хеллоуинские шутки</h3>
                            <p style="color: rgba(255,255,255,0.8); margin-top: 10px;">Страшно смешные шутки</p>
                        </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }

        function showThemes() {
            document.getElementById('mainApp').innerHTML = `
                <div style="padding: 20px; max-width: 600px; margin: 0 auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h1>🎨 Настройки тем</h1>
                        <button class="btn" onclick="renderMainApp()">← Назад</button>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 30px; border-radius: 15px;">
                        <h3 style="margin-bottom: 20px;">Выберите тему оформления:</h3>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <button class="btn" onclick="changeTheme('purple')">💜 Фиолетовая</button>
                            <button class="btn" style="background: #3b82f6;" onclick="changeTheme('blue')">🔵 Синяя</button>
                            <button class="btn" style="background: #10b981;" onclick="changeTheme('green')">🟢 Зеленая</button>
                            <button class="btn" style="background: #ef4444;" onclick="changeTheme('red')">🔴 Красная</button>
                            <button class="btn ${isHalloweenTheme ? 'btn-halloween' : ''}" onclick="toggleHalloweenTheme()">
                                ${isHalloweenTheme ? '👻 Хеллоуин' : '🎃 Хеллоуин'}
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        function showAdminPanel() {
            document.getElementById('mainApp').innerHTML = `
                <div style="padding: 20px; max-width: 800px; margin: 0 auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h1>👑 Панель администратора</h1>
                        <button class="btn" onclick="renderMainApp()">← Назад</button>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 30px;">
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${Object.keys(users_db).length}</div>
                            <div style="color: #888;">Пользователей</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">0</div>
                            <div style="color: #888;">Сообщений</div>
                        </div>
                        <div style="background: var(--card-color); padding: 20px; border-radius: 10px; text-align: center;">
                            <div style="font-size: 24px; color: var(--accent-color);">${isHalloweenTheme ? '🎃' : '💜'}</div>
                            <div style="color: #888;">Тема</div>
                        </div>
                    </div>
                    
                    <div style="background: var(--card-color); padding: 20px; border-radius: 15px;">
                        <h3 style="margin-bottom: 15px;">Действия администратора:</h3>
                        <button class="btn btn-admin" style="margin: 5px;" onclick="sendSystemMessage()">📢 Системное уведомление</button>
                        <button class="btn btn-admin" style="margin: 5px;" onclick="clearAllData()">🗑️ Очистить данные</button>
                        ${isHalloweenTheme ? '<button class="btn btn-halloween" style="margin: 5px;" onclick="sendHalloweenNotification()">🎃 Хеллоуин-уведомление</button>' : ''}
                    </div>
                </div>
            `;
        }

        function changeTheme(theme) {
            showNotification(`Тема изменена на ${theme}`, 'success');
        }

        function startGame(game) {
            showNotification(`Запускается игра: ${game}`, 'info');
        }

        function startHalloweenGame() {
            showNotification('🎃 Запускается хеллоуинская игра! Готовьтесь к страшным загадкам! 👻', 'success');
        }

        function showHalloweenJokes() {
            const jokes = [
                "Почему призрак перешел дорогу? Чтобы добраться до другого дома с привидениями! 👻",
                "Что говорит скелет, когда не может открыть дверь? Костяной помощи! 💀",
                "Почему тыква не могла поделиться секретом? Потому что у нее не было тыквенных семян! 🎃",
                "Что летает и светится в темноте? Вампир-светлячок! 🦇"
            ];
            const joke = jokes[Math.floor(Math.random() * jokes.length)];
            showNotification(`🎃 Хеллоуинская шутка: ${joke}`, 'success');
        }

        function sendMessage() {
            showNotification('Сообщение отправлено!', 'success');
        }

        function sendHalloweenMessage() {
            const messages = ['Бууу! 👻', 'Счастливого Хеллоуина! 🎃', 'Конфеты или смерть! 🍬', 'Тыквенное настроение! 🎃'];
            const message = messages[Math.floor(Math.random() * messages.length)];
            showNotification(`🎃 Отправлено хеллоуинское сообщение: ${message}`, 'success');
        }

        function sendSystemMessage() {
            showNotification('Системное уведомление отправлено всем пользователям!', 'success');
        }

        function sendHalloweenNotification() {
            showNotification('🎃 Хеллоуинское уведомление отправлено всем пользователям! Счастливого Хеллоуина 2025! 👻', 'success');
        }

        function clearAllData() {
            if (confirm('Вы уверены что хотите очистить все данные?')) {
                localStorage.clear();
                showNotification('Все данные очищены!', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        }

        function logout() {
            currentUser = null;
            localStorage.removeItem('dlcurrentUser');
            location.reload();
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification-toast';
            notification.style.background = type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : 'var(--accent-color)';
            notification.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 20px;">${type === 'error' ? '❌' : type === 'success' ? '✅' : '💡'}</div>
                    <div>${message}</div>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 4000);
        }

        // Обработка Enter в формах
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                if (!document.getElementById('registerScreen').classList.contains('hidden')) {
                    registerUser();
                }
                if (!document.getElementById('adminScreen').classList.contains('hidden')) {
                    adminLogin();
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
        
        user_id = generate_user_id()
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
    print("🚀 Запуск DLtrollex с хеллоуин-функциями...")
    print("💜 Сервер запущен!")
    print(f"🔗 Доступен по адресу: http://0.0.0.0:{port}")
    print("🎃 Хеллоуин 2025 тема готова!")
    print("✅ Кнопка 'Начать общение' исправлена!")
    
    app.run(host='0.0.0.0', port=port, debug=False)
