# DLtrollex - УЛЬТРА КАСТОМИЗИРУЕМЫЙ ЧАТ
from flask import Flask, render_template_string
import datetime
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydltrollex2024'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DLtrollex</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        body {
            background: #0f0f0f;
            color: white;
            height: 100vh;
            overflow: hidden;
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
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
            padding: 20px;
        }
        
        .auth-box {
            background: #1a1a1a;
            padding: 40px 30px;
            border-radius: 20px;
            border: 2px solid #8b5cf6;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        
        .logo {
            font-size: 42px;
            font-weight: bold;
            color: #8b5cf6;
            margin-bottom: 15px;
        }
        
        .subtitle {
            color: #888;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .btn {
            width: 100%;
            padding: 16px;
            background: #8b5cf6;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: #7c3aed;
            transform: translateY(-2px);
        }
        
        .hidden {
            display: none !important;
        }
        
        .app {
            display: none;
            height: 100vh;
            background: #0f0f0f;
        }
    </style>
</head>
<body>
    <!-- ПЕРВАЯ СТРАНИЦА -->
    <div id="screen1" class="screen">
        <div class="auth-box">
            <div class="logo">💬 DLtrollex</div>
            <div class="subtitle">Современный мессенджер для общения</div>
            
            <button class="btn" onclick="startQuickRegistration()">
                Начать общение
            </button>
            
            <div style="margin-top: 20px; font-size: 12px; color: #888;">
                Быстро • Просто • Удобно
            </div>
        </div>
    </div>

    <!-- РЕГИСТРАЦИЯ -->
    <div id="quickRegisterScreen" class="screen hidden">
        <div class="auth-box">
            <div class="logo">💬 DLtrollex</div>
            <div class="subtitle">Создайте свой аккаунт</div>
            
            <input type="text" style="width: 100%; padding: 16px; margin-bottom: 15px; background: #2d2d2d; border: 2px solid #3d3d3d; border-radius: 12px; color: white; font-size: 16px;" placeholder="Ваше имя" id="regName">
            
            <button class="btn" onclick="quickRegister()">
                Создать аккаунт
            </button>
            
            <button class="btn" onclick="showScreen('screen1')" style="background: #666;">
                Назад
            </button>
        </div>
    </div>

    <!-- ОСНОВНОЙ ИНТЕРФЕЙС -->
    <div id="mainApp" class="app hidden">
        <div style="padding: 20px; text-align: center;">
            <h1>Добро пожаловать в чат!</h1>
            <p>Здесь будет интерфейс мессенджера</p>
            <button class="btn" onclick="showScreen('screen1')" style="margin-top: 20px;">
                Выйти
            </button>
        </div>
    </div>

    <script>
        let currentUser = null;

        function startQuickRegistration() {
            showScreen('quickRegisterScreen');
        }

        function showScreen(screenId) {
            // Скрываем все экраны
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            
            // Показываем нужный экран
            const targetScreen = document.getElementById(screenId);
            if (targetScreen) {
                targetScreen.classList.remove('hidden');
            }
        }

        function quickRegister() {
            const name = document.getElementById('regName').value.trim();
            if (!name) {
                alert('Введите имя');
                return;
            }

            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                avatar: '😊'
            };

            localStorage.setItem('dlcurrentUser', JSON.stringify(currentUser));
            showMainApp();
        }

        function showMainApp() {
            showScreen('mainApp');
        }

        // Проверяем автологин при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            const savedUser = localStorage.getItem('dlcurrentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
            } else {
                showScreen('screen1');
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("💬 DLtrollex запущен!")
    print(f"🔗 http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
