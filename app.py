# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import json
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-2024'

# Глобальные переменные для хранения данных
users_db = {}
chats_db = {}
messages_db = {}

def generate_username():
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{random.randint(1000, 9999)}"

def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(10))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureChat - Безопасный мессенджер</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            overflow-x: hidden;
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
        }

        .hidden {
            display: none !important;
        }

        .auth-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 400px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .logo {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 30px;
        }

        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }

        .btn-primary {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .credential-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .credential-field {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }

        .app {
            width: 100%;
            height: 100vh;
            background: white;
            color: #333;
        }

        .chat-container {
            display: flex;
            height: 100vh;
        }

        .sidebar {
            width: 300px;
            background: #2c3e50;
            color: white;
            display: flex;
            flex-direction: column;
        }

        .user-header {
            padding: 20px;
            background: #34495e;
            text-align: center;
        }

        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin: 0 auto 10px;
        }

        .nav-tabs {
            display: flex;
            padding: 10px;
            gap: 5px;
        }

        .nav-tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .nav-tab.active {
            background: #3498db;
        }

        .search-box {
            padding: 15px;
        }

        .search-input {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }

        .search-input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .chat-item, .user-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .chat-item:hover, .user-item:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateX(5px);
        }

        .item-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 1.2rem;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #ecf0f1;
        }

        .chat-header {
            padding: 20px;
            background: white;
            border-bottom: 1px solid #bdc3c7;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 70%;
            padding: 15px;
            border-radius: 15px;
            position: relative;
        }

        .message.received {
            background: white;
            align-self: flex-start;
            border-bottom-left-radius: 5px;
        }

        .message.sent {
            background: #3498db;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 5px;
        }

        .message-input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #bdc3c7;
            display: flex;
            gap: 10px;
        }

        .message-input {
            flex: 1;
            padding: 15px;
            border: 1px solid #bdc3c7;
            border-radius: 25px;
            outline: none;
        }

        .send-btn {
            padding: 15px 25px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }

        .call-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            z-index: 1000;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .call-avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            margin-bottom: 20px;
        }

        .call-controls {
            display: flex;
            gap: 20px;
            margin-top: 40px;
        }

        .control-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .call-end {
            background: #e74c3c;
            color: white;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2ecc71;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 2000;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }

        .logout-btn {
            background: #e74c3c;
            color: white;
            margin-top: 20px;
        }

        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                height: 100%;
                z-index: 100;
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
            font-size: 1.5rem;
            cursor: pointer;
            padding: 10px;
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 20px;">🚀</div>
            <h1>SecureChat</h1>
            <p>Загрузка...</p>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">SecureChat</div>
            <div class="subtitle">Безопасный мессенджер с VoIP звонками</div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 Начать использование
            </button>
            
            <button class="btn btn-secondary" onclick="autoLogin()">
                🔄 Быстрый вход
            </button>

            <div style="text-align: center; margin-top: 20px; color: rgba(255,255,255,0.7)">
                Работает в обход блокировок 🔓
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="auth-container">
            <div class="logo">Регистрация</div>
            
            <div class="credential-box">
                <div class="credential-field">
                    <span>👤 Имя:</span>
                    <span id="generatedName" style="font-weight: bold;">...</span>
                </div>
                <div class="credential-field">
                    <span>🔐 Пароль:</span>
                    <span id="generatedPassword" style="font-weight: bold;">...</span>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ Создать аккаунт
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewCredentials()">
                🔄 Новые данные
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← Назад
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="chat-container">
            <!-- Сайдбар -->
            <div class="sidebar" id="sidebar">
                <div class="user-header">
                    <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                    <div class="user-avatar" id="userAvatar">😊</div>
                    <h3 id="userName">Пользователь</h3>
                    <p>Уровень: <span id="userLevel">1</span></p>
                </div>

                <div class="nav-tabs">
                    <div class="nav-tab active" onclick="switchTab('chats')">💬 Чаты</div>
                    <div class="nav-tab" onclick="switchTab('calls')">📞 Звонки</div>
                    <div class="nav-tab" onclick="switchTab('contacts')">👥 Контакты</div>
                </div>

                <div class="search-box">
                    <input type="text" class="search-input" placeholder="Поиск..." id="searchInput" oninput="searchItems()">
                </div>

                <div class="content-list" id="contentList">
                    <!-- Список будет заполнен JavaScript -->
                </div>

                <div style="padding: 20px;">
                    <button class="btn logout-btn" onclick="showLogoutConfirm()">
                        🚪 Выйти
                    </button>
                </div>
            </div>

            <!-- Область чата -->
            <div class="chat-area">
                <div class="chat-header">
                    <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                    <div class="item-avatar" id="currentChatAvatar">💬</div>
                    <div>
                        <h3 id="currentChatName">Выберите чат</h3>
                        <p style="color: #7f8c8d;" id="currentChatStatus">для начала общения</p>
                    </div>
                </div>

                <div class="messages-container" id="messagesContainer">
                    <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                        <div style="font-size: 4rem; margin-bottom: 20px;">👋</div>
                        <h3>Добро пожаловать в SecureChat!</h3>
                        <p>Выберите чат или начните звонок</p>
                    </div>
                </div>

                <div class="message-input-container">
                    <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput">
                    <button class="send-btn" onclick="sendMessage()">Отправить</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Экран звонка -->
    <div id="callScreen" class="call-screen hidden">
        <div class="call-avatar" id="callAvatar">👤</div>
        <h2 id="callUserName">Абонент</h2>
        <p id="callStatus">Звонок...</p>
        <p id="callTimer" style="font-size: 2rem; margin: 20px 0;">00:00</p>
        
        <div class="call-controls">
            <button class="control-btn" onclick="toggleMute()">🎤</button>
            <button class="control-btn call-end" onclick="endCall()">📞</button>
            <button class="control-btn" onclick="toggleVideo()">📹</button>
        </div>
    </div>

    <!-- Подтверждение выхода -->
    <div id="logoutConfirm" class="screen hidden" style="background: rgba(0,0,0,0.8); z-index: 2000;">
        <div class="auth-container">
            <h3 style="margin-bottom: 20px; text-align: center;">Подтверждение выхода</h3>
            <p style="text-align: center; margin-bottom: 30px; color: rgba(255,255,255,0.8);">
                Ваши данные будут сохранены. Вернуться можно в любой момент.
            </p>
            <button class="btn btn-primary" onclick="logout()">✅ Выйти</button>
            <button class="btn btn-secondary" onclick="hideLogoutConfirm()">❌ Отмена</button>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let callTimer = null;
        let callStartTime = null;

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 2000);
        });

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function showWelcomeScreen() {
            showScreen('welcomeScreen');
        }

        function showRegisterScreen() {
            showScreen('registerScreen');
            generateNewCredentials();
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            document.getElementById(screenId).classList.remove('hidden');
        }

        function generateNewCredentials() {
            const name = "User_" + Math.floor(Math.random() * 10000);
            const password = Math.random().toString(36).slice(-8);
            
            document.getElementById('generatedName').textContent = name;
            document.getElementById('generatedPassword').textContent = password;
        }

        function registerUser() {
            const name = document.getElementById('generatedName').textContent;
            const password = document.getElementById('generatedPassword').textContent;
            
            currentUser = {
                id: 'user_' + Date.now(),
                name: name,
                avatar: '😊',
                level: 1,
                online: true
            };
            
            // Сохраняем пользователя
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            localStorage.setItem('userPassword', password);
            
            showMainApp();
            showNotification('Аккаунт успешно создан! 🎉');
        }

        function autoLogin() {
            const savedUser = localStorage.getItem('currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
                showNotification('Автоматический вход выполнен! 🔄');
            } else {
                showNotification('Нет сохраненного аккаунта!', 'error');
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('currentUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                showMainApp();
            } else {
                showWelcomeScreen();
            }
        }

        function showMainApp() {
            showScreen('mainApp');
            
            // Заполняем данные пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userLevel').textContent = currentUser.level;
            
            // Загружаем контент
            loadContent();
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            // Обновляем активные табы
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Загружаем контент
            loadContent();
        }

        function loadContent() {
            const contentList = document.getElementById('contentList');
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            let contentHTML = '';
            
            if (currentTab === 'chats') {
                contentHTML = getChatsContent(searchTerm);
            } else if (currentTab === 'calls') {
                contentHTML = getCallsContent(searchTerm);
            } else if (currentTab === 'contacts') {
                contentHTML = getContactsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 1, name: 'Техподдержка', avatar: '🔧', lastMessage: 'Чем можем помочь?', unread: 2, online: true},
                {id: 2, name: 'Общий чат', avatar: '👥', lastMessage: 'Добро пожаловать!', unread: 0, online: true},
                {id: 3, name: 'Новости', avatar: '📰', lastMessage: 'Новые обновления', unread: 5, online: true},
                {id: 4, name: 'Помощь', avatar: '❓', lastMessage: 'Задайте вопрос', unread: 0, online: true}
            ];
            
            return chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            ).map(chat => `
                <div class="chat-item" onclick="openChat(${chat.id})">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${chat.name}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">${chat.lastMessage}</div>
                    </div>
                    ${chat.unread > 0 ? `<div style="background: #e74c3c; color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 0.8em;">${chat.unread}</div>` : ''}
                </div>
            `).join('');
        }

        function getCallsContent(searchTerm) {
            const users = [
                {id: 1, name: 'Алексей', avatar: '👨‍💻', online: true, lastCall: '2 мин назад'},
                {id: 2, name: 'Мария', avatar: '👩‍🎨', online: true, lastCall: '5 мин назад'},
                {id: 3, name: 'Дмитрий', avatar: '👨‍🔬', online: false, lastCall: '1 час назад'},
                {id: 4, name: 'Анна', avatar: '👩‍💼', online: true, lastCall: '10 мин назад'},
                {id: 5, name: 'Сергей', avatar: '👨‍🚀', online: false, lastCall: '2 часа назад'}
            ];
            
            return users.filter(user => 
                user.name.toLowerCase().includes(searchTerm)
            ).map(user => `
                <div class="user-item">
                    <div class="item-avatar">${user.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${user.name}</div>
                        <div style="font-size: 0.9em; opacity: 0.8; color: ${user.online ? '#2ecc71' : '#95a5a6'}">
                            ${user.online ? '● онлайн' : '○ офлайн'} • ${user.lastCall}
                        </div>
                    </div>
                    <div style="display: flex; gap: 5px;">
                        <button onclick="startVoiceCall(${user.id})" style="background: #2ecc71; color: white; border: none; border-radius: 5px; padding: 5px 10px; cursor: pointer;">📞</button>
                        <button onclick="startVideoCall(${user.id})" style="background: #3498db; color: white; border: none; border-radius: 5px; padding: 5px 10px; cursor: pointer;">📹</button>
                    </div>
                </div>
            `).join('');
        }

        function getContactsContent(searchTerm) {
            const contacts = [
                {name: 'Техподдержка', avatar: '🔧', role: 'Помощь и поддержка'},
                {name: 'Администратор', avatar: '👑', role: 'Управление системой'},
                {name: 'Модератор', avatar: '🛡️', role: 'Контроль качества'},
                {name: 'Разработчик', avatar: '👨‍💻', role: 'Техническая поддержка'}
            ];
            
            return contacts.filter(contact => 
                contact.name.toLowerCase().includes(searchTerm)
            ).map(contact => `
                <div class="chat-item">
                    <div class="item-avatar">${contact.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${contact.name}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">${contact.role}</div>
                    </div>
                </div>
            `).join('');
        }

        function searchItems() {
            loadContent();
        }

        function openChat(chatId) {
            const chats = [
                {id: 1, name: 'Техподдержка', avatar: '🔧', status: 'онлайн'},
                {id: 2, name: 'Общий чат', avatar: '👥', status: 'активен'},
                {id: 3, name: 'Новости', avatar: '📰', status: 'рассылка'},
                {id: 4, name: 'Помощь', avatar: '❓', status: 'онлайн'}
            ];
            
            const chat = chats.find(c => c.id === chatId);
            if (chat) {
                currentChat = chat;
                
                document.getElementById('currentChatName').textContent = chat.name;
                document.getElementById('currentChatAvatar').textContent = chat.avatar;
                document.getElementById('currentChatStatus').textContent = chat.status;
                
                // Показываем тестовые сообщения
                showChatMessages(chatId);
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const messages = [
                {text: 'Добро пожаловать в чат! 👋', sender: 'received', time: '12:00'},
                {text: 'Чем могу помочь?', sender: 'received', time: '12:01'},
                {text: 'Привет! Как работает приложение?', sender: 'sent', time: '12:02'},
                {text: 'Всё отлично! Доступны чаты и звонки 📞', sender: 'received', time: '12:03'}
            ];
            
            messagesContainer.innerHTML = messages.map(msg => `
                <div class="message ${msg.sender}">
                    ${msg.text}
                    <div style="font-size: 0.8em; opacity: 0.7; text-align: right; margin-top: 5px;">${msg.time}</div>
                </div>
            `).join('');
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                const messagesContainer = document.getElementById('messagesContainer');
                const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.innerHTML = `
                    ${message}
                    <div style="font-size: 0.8em; opacity: 0.7; text-align: right; margin-top: 5px;">${time}</div>
                `;
                
                messagesContainer.appendChild(messageElement);
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                showNotification('Сообщение отправлено ✉️');
            }
        }

        function startVoiceCall(userId) {
            const users = [
                {id: 1, name: 'Алексей', avatar: '👨‍💻'},
                {id: 2, name: 'Мария', avatar: '👩‍🎨'},
                {id: 3, name: 'Дмитрий', avatar: '👨‍🔬'},
                {id: 4, name: 'Анна', avatar: '👩‍💼'},
                {id: 5, name: 'Сергей', avatar: '👨‍🚀'}
            ];
            
            const user = users.find(u => u.id === userId);
            if (user) {
                showCallScreen(user, 'voice');
            }
        }

        function startVideoCall(userId) {
            const users = [
                {id: 1, name: 'Алексей', avatar: '👨‍💻'},
                {id: 2, name: 'Мария', avatar: '👩‍🎨'},
                {id: 3, name: 'Дмитрий', avatar: '👨‍🔬'},
                {id: 4, name: 'Анна', avatar: '👩‍💼'},
                {id: 5, name: 'Сергей', avatar: '👨‍🚀'}
            ];
            
            const user = users.find(u => u.id === userId);
            if (user) {
                showCallScreen(user, 'video');
            }
        }

        function showCallScreen(user, type) {
            document.getElementById('callScreen').classList.remove('hidden');
            document.getElementById('callAvatar').textContent = user.avatar;
            document.getElementById('callUserName').textContent = user.name;
            document.getElementById('callStatus').textContent = type === 'voice' ? 'Голосовой звонок...' : 'Видеозвонок...';
            
            startCallTimer();
            showNotification(`Звонок ${user.name}...`);
        }

        function startCallTimer() {
            callStartTime = new Date();
            callTimer = setInterval(() => {
                const now = new Date();
                const diff = Math.floor((now - callStartTime) / 1000);
                const minutes = Math.floor(diff / 60);
                const seconds = diff % 60;
                document.getElementById('callTimer').textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }, 1000);
        }

        function endCall() {
            clearInterval(callTimer);
            document.getElementById('callScreen').classList.add('hidden');
            showNotification('Звонок завершён 📞');
        }

        function toggleMute() {
            showNotification('Микрофон переключен 🎤');
        }

        function toggleVideo() {
            showNotification('Камера переключена 📹');
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.remove('hidden');
        }

        function hideLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.add('hidden');
        }

        function logout() {
            localStorage.removeItem('currentUser');
            showWelcomeScreen();
            showNotification('Вы вышли из системы 👋');
        }

        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            notification.style.background = type === 'error' ? '#e74c3c' : '#2ecc71';
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Обработка Enter для отправки сообщений
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Закрытие сайдбара при клике вне его на мобильных
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                sidebar.classList.remove('active');
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
def register():
    data = request.json
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        'id': user_id,
        'name': data.get('name'),
        'avatar': data.get('avatar', '😊'),
        'level': 1,
        'online': True,
        'created_at': datetime.datetime.now().isoformat()
    }
    return jsonify({'success': True, 'user': users_db[user_id]})

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    message_id = str(uuid.uuid4())
    messages_db[message_id] = {
        'id': message_id,
        'chat_id': data.get('chat_id'),
        'user_id': data.get('user_id'),
        'text': data.get('text'),
        'timestamp': datetime.datetime.now().isoformat()
    }
    return jsonify({'success': True, 'message': messages_db[message_id]})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running',
        'users_count': len(users_db),
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 SecureChat запущен на порту {port}")
    print("📱 Доступен по адресу: http://localhost:" + str(port))
    app.run(host='0.0.0.0', port=port, debug=False)
