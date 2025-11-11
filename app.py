from flask import Flask, render_template, request, jsonify, session
import random
import datetime
import uuid
import os
import json
from typing import Dict, List, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ultramodern2024')

class AdvancedChatManager:
    def __init__(self):
        self.users: List[Dict] = []
        self.chats: List[Dict] = []
        self.messages: List[Dict] = []
        self.user_stats: Dict = {}
    
    def add_user(self, user_data: Dict) -> Dict:
        """Добавляет нового пользователя с расширенными данными"""
        user_data['premium'] = random.choice([True, False, False])
        user_data['join_date'] = datetime.datetime.now().isoformat()
        user_data['level'] = random.randint(1, 100)
        user_data['xp'] = random.randint(100, 5000)
        user_data['online'] = True
        user_data['last_seen'] = datetime.datetime.now().isoformat()
        
        self.users.append(user_data)
        
        # Инициализируем статистику пользователя
        self.user_stats[user_data['id']] = {
            'messages_sent': 0,
            'chats_created': 0,
            'login_count': 0,
            'total_time_online': 0,
            'achievements': []
        }
        
        return user_data
    
    def create_chat(self, chat_data: Dict) -> Dict:
        """Создает новый чат с настройками"""
        chat_data['created_at'] = datetime.datetime.now().isoformat()
        chat_data['theme'] = random.choice(['purple', 'blue', 'pink', 'matrix', 'cyber', 'galaxy'])
        chat_data['unread'] = random.randint(0, 5)
        chat_data['active'] = True
        chat_data['participants_count'] = len(chat_data.get('participants', []))
        
        self.chats.append(chat_data)
        return chat_data
    
    def add_message(self, message_data: Dict) -> Dict:
        """Добавляет сообщение в чат"""
        message_data['id'] = str(uuid.uuid4())
        message_data['timestamp'] = datetime.datetime.now().isoformat()
        message_data['edited'] = False
        message_data['read'] = False
        
        self.messages.append(message_data)
        
        # Обновляем статистику пользователя
        if message_data['sender'] in self.user_stats:
            self.user_stats[message_data['sender']]['messages_sent'] += 1
        
        return message_data
    
    def get_user_chats(self, user_id: str) -> List[Dict]:
        """Возвращает чаты пользователя"""
        return [chat for chat in self.chats if user_id in chat.get('participants', [])]
    
    def get_chat_messages(self, chat_id: str, limit: int = 50) -> List[Dict]:
        """Возвращает сообщения чата"""
        chat_messages = [msg for msg in self.messages if msg.get('chat_id') == chat_id]
        return sorted(chat_messages, key=lambda x: x['timestamp'])[-limit:]
    
    def mark_messages_as_read(self, chat_id: str, user_id: str):
        """Помечает сообщения как прочитанные"""
        for message in self.messages:
            if (message.get('chat_id') == chat_id and 
                message.get('sender') != user_id and 
                not message.get('read')):
                message['read'] = True
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Находит пользователя по ID"""
        return next((user for user in self.users if user['id'] == user_id), None)
    
    def update_user_online_status(self, user_id: str, online: bool = True):
        """Обновляет статус онлайн пользователя"""
        user = self.get_user_by_id(user_id)
        if user:
            user['online'] = online
            user['last_seen'] = datetime.datetime.now().isoformat()
    
    def get_system_stats(self) -> Dict:
        """Возвращает статистику системы"""
        return {
            'total_users': len(self.users),
            'total_chats': len(self.chats),
            'total_messages': len(self.messages),
            'online_users': len([u for u in self.users if u.get('online', False)]),
            'premium_users': len([u for u in self.users if u.get('premium', False)]),
            'active_chats': len([c for c in self.chats if c.get('active', True)])
        }

# Инициализация менеджера чатов
chat_manager = AdvancedChatManager()

def generate_username() -> str:
    """Генерирует случайное имя пользователя"""
    adjectives = ['Космический', 'Фиолетовый', 'Неоновый', 'Цифровой', 'Виртуальный', 
                  'Тайный', 'Бесконечный', 'Сверхновый', 'Квантовый', 'Галактический']
    nouns = ['Феникс', 'Единорог', 'Дракон', 'Волк', 'Тигр', 
             'Самурай', 'Ниндзя', 'Маг', 'Рыцарь', 'Пират']
    numbers = random.randint(100, 999)
    
    return f"{random.choice(adjectives)}_{random.choice(nouns)}_{numbers}"

def get_user_rank(level: int) -> str:
    """Определяет ранг пользователя по уровню"""
    if level < 5:
        return "🟢 Новичок"
    elif level < 15:
        return "🔵 Ученик"
    elif level < 30:
        return "🟣 Адепт"
    elif level < 50:
        return "🟡 Мастер"
    elif level < 75:
        return "🟠 Эксперт"
    elif level < 100:
        return "🔴 Легенда"
    else:
        return "👑 Император"

def generate_sample_chats(user_id: str) -> List[Dict]:
    """Генерирует примеры чатов для нового пользователя"""
    chat_names = [
        "Общий чат", "Техподдержка", "Игроки", "Разработчики",
        "Новости", "Музыка", "Игры", "Флудильня",
        "Помощь", "Предложения", "Баги", "Оффтоп"
    ]
    
    sample_messages = [
        "Привет! Как дела?",
        "Кто онлайн?",
        "Есть новости?",
        "Помогите с настройкой",
        "Отличная тема чата!",
        "Что думаете о новом обновлении?",
        "Играем сегодня?",
        "Нашел интересный баг",
        "Предлагаю новые фичи",
        "Всем хорошего дня! 🚀"
    ]
    
    chats = []
    for i in range(6):  # Создаем 6 чатов
        other_user_id = str(uuid.uuid4())
        chat_data = {
            'id': str(uuid.uuid4()),
            'name': random.choice(chat_names),
            'participants': [user_id, other_user_id],
            'last_message': random.choice(sample_messages),
            'last_message_time': datetime.datetime.now().isoformat(),
            'unread': random.randint(0, 3),
            'type': 'group' if i > 2 else 'private',
            'icon': random.choice(['💬', '👥', '🎮', '🎵', '📱', '💻']),
            'pinned': random.choice([True, False, False])
        }
        chats.append(chat_manager.create_chat(chat_data))
        
        # Добавляем несколько сообщений в каждый чат
        for j in range(random.randint(3, 8)):
            message_data = {
                'chat_id': chat_data['id'],
                'sender': other_user_id if j % 2 == 0 else user_id,
                'text': random.choice(sample_messages),
                'is_user': j % 2 == 1
            }
            chat_manager.add_message(message_data)
    
    return chats

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    try:
        user_data = {
            'id': str(uuid.uuid4()),
            'name': generate_username(),
            'avatar': f'https://api.dicebear.com/7.x/avataaars/svg?seed={random.randint(1, 10000)}',
            'color': f'#{random.randint(0, 0xFFFFFF):06x}'
        }
        
        # Добавляем пользователя
        user_data = chat_manager.add_user(user_data)
        session['user_id'] = user_data['id']
        session['user_name'] = user_data['name']
        
        # Создаем примеры чатов
        generate_sample_chats(user_data['id'])
        
        # Обновляем статистику
        chat_manager.user_stats[user_data['id']]['login_count'] += 1
        
        response_data = {
            'success': True, 
            'user': user_data,
            'message': 'Добро пожаловать в UltraMsg! 🚀',
            'stats': chat_manager.get_system_stats()
        }
        
        print(f"👤 Новый пользователь: {user_data['name']} (ID: {user_data['id']})")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Ошибка регистрации: {str(e)}")
        return jsonify({'success': False, 'error': f'Ошибка регистрации: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Вход существующего пользователя"""
    try:
        user_id = request.json.get('user_id')
        user = chat_manager.get_user_by_id(user_id)
        
        if user:
            session['user_id'] = user_id
            session['user_name'] = user['name']
            
            # Обновляем статус онлайн
            chat_manager.update_user_online_status(user_id, True)
            chat_manager.user_stats[user_id]['login_count'] += 1
            
            response_data = {
                'success': True, 
                'user': user,
                'message': f'С возвращением, {user["name"]}! 👋',
                'stats': chat_manager.get_system_stats()
            }
            
            print(f"🔑 Пользователь вошел: {user['name']}")
            return jsonify(response_data)
        
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
        
    except Exception as e:
        print(f"❌ Ошибка входа: {str(e)}")
        return jsonify({'success': False, 'error': f'Ошибка входа: {str(e)}'}), 500

@app.route('/api/chats')
def get_chats():
    """Получить список чатов пользователя"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Не авторизован'}), 401
        
        user_chats = chat_manager.get_user_chats(user_id)
        
        # Сортируем чаты по времени последнего сообщения
        user_chats.sort(key=lambda x: x.get('last_message_time', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'chats': user_chats,
            'total': len(user_chats)
        })
        
    except Exception as e:
        print(f"❌ Ошибка получения чатов: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/messages/<chat_id>')
def get_messages(chat_id):
    """Получить сообщения чата"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Не авторизован'}), 401
        
        # Проверяем доступ пользователя к чату
        chat = next((c for c in chat_manager.chats if c['id'] == chat_id and user_id in c.get('participants', [])), None)
        if not chat:
            return jsonify({'error': 'Чат не найден или доступ запрещен'}), 404
        
        messages = chat_manager.get_chat_messages(chat_id)
        
        # Помечаем сообщения как прочитанные
        chat_manager.mark_messages_as_read(chat_id, user_id)
        
        # Обновляем непрочитанные
        chat['unread'] = 0
        
        return jsonify({
            'success': True,
            'messages': messages,
            'chat_info': chat
        })
        
    except Exception as e:
        print(f"❌ Ошибка получения сообщений: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Отправить сообщение"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Не авторизован'}), 401
        
        data = request.json
        chat_id = data.get('chat_id')
        text = data.get('text', '').strip()
        
        if not chat_id:
            return jsonify({'error': 'ID чата обязателен'}), 400
        
        if not text:
            return jsonify({'error': 'Текст сообщения не может быть пустым'}), 400
        
        # Проверяем доступ пользователя к чату
        chat = next((c for c in chat_manager.chats if c['id'] == chat_id and user_id in c.get('participants', [])), None)
        if not chat:
            return jsonify({'error': 'Чат не найден или доступ запрещен'}), 404
        
        # Создаем сообщение
        message_data = {
            'chat_id': chat_id,
            'sender': user_id,
            'text': text,
            'is_user': True
        }
        
        message = chat_manager.add_message(message_data)
        
        # Обновляем информацию о чате
        chat['last_message'] = text
        chat['last_message_time'] = message['timestamp']
        
        # Увеличиваем непрочитанные для других участников
        for participant in chat['participants']:
            if participant != user_id:
                chat['unread'] = chat.get('unread', 0) + 1
                break
        
        response_data = {
            'success': True, 
            'message': message,
            'chat_updated': chat
        }
        
        print(f"💬 Сообщение отправлено в чат {chat_id}: {text[:50]}...")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user/profile')
def get_user_profile():
    """Получить профиль пользователя"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Не авторизован'}), 401
        
        user = chat_manager.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        stats = chat_manager.user_stats.get(user_id, {})
        rank = get_user_rank(user['level'])
        
        profile_data = {
            'user': user,
            'stats': stats,
            'rank': rank,
            'join_date': user.get('join_date', ''),
            'premium': user.get('premium', False)
        }
        
        return jsonify({'success': True, 'profile': profile_data})
        
    except Exception as e:
        print(f"❌ Ошибка получения профиля: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/system/stats')
def get_system_stats():
    """Получить статистику системы"""
    try:
        stats = chat_manager.get_system_stats()
        
        # Добавляем информацию о сервере
        stats.update({
            'server_time': datetime.datetime.now().isoformat(),
            'version': '1.0.0',
            'status': 'operational'
        })
        
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        print(f"❌ Ошибка получения статистики: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Проверка здоровья приложения"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'users_count': len(chat_manager.users),
        'chats_count': len(chat_manager.chats),
        'messages_count': len(chat_manager.messages)
    })

@app.route('/api/user/online', methods=['POST'])
def update_online_status():
    """Обновить статус онлайн"""
    try:
        user_id = session.get('user_id')
        online = request.json.get('online', True)
        
        if user_id:
            chat_manager.update_user_online_status(user_id, online)
            
        return jsonify({'success': True, 'online': online})
        
    except Exception as e:
        print(f"❌ Ошибка обновления статуса: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search/chats')
def search_chats():
    """Поиск чатов"""
    try:
        user_id = session.get('user_id')
        query = request.args.get('q', '').lower().strip()
        
        if not user_id:
            return jsonify({'error': 'Не авторизован'}), 401
        
        if not query:
            return jsonify({'success': True, 'results': []})
        
        user_chats = chat_manager.get_user_chats(user_id)
        results = [
            chat for chat in user_chats 
            if query in chat.get('name', '').lower() or 
               query in chat.get('last_message', '').lower()
        ]
        
        return jsonify({
            'success': True,
            'results': results,
            'query': query,
            'count': len(results)
        })
        
    except Exception as e:
        print(f"❌ Ошибка поиска: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat/create', methods=['POST'])
def create_chat():
    """Создать новый чат"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Не авторизован'}), 401
        
        data = request.json
        chat_name = data.get('name', 'Новый чат')
        chat_type = data.get('type', 'private')
        
        chat_data = {
            'id': str(uuid.uuid4()),
            'name': chat_name,
            'type': chat_type,
            'participants': [user_id],
            'last_message': 'Чат создан',
            'last_message_time': datetime.datetime.now().isoformat(),
            'unread': 0,
            'created_by': user_id
        }
        
        # Добавляем второго участника для приватного чата
        if chat_type == 'private':
            bot_user_id = str(uuid.uuid4())
            chat_data['participants'].append(bot_user_id)
            
            # Создаем бота-пользователя
            bot_user = {
                'id': bot_user_id,
                'name': 'Ассистент',
                'avatar': f'https://api.dicebear.com/7.x/bottts/svg?seed={random.randint(1, 1000)}',
                'premium': False,
                'level': 99,
                'online': True
            }
            chat_manager.users.append(bot_user)
        
        chat = chat_manager.create_chat(chat_data)
        
        # Добавляем приветственное сообщение
        welcome_message = {
            'chat_id': chat['id'],
            'sender': 'system',
            'text': f'Добро пожаловать в чат "{chat_name}"! 🎉',
            'is_user': False
        }
        chat_manager.add_message(welcome_message)
        
        # Обновляем статистику
        if user_id in chat_manager.user_stats:
            chat_manager.user_stats[user_id]['chats_created'] += 1
        
        return jsonify({
            'success': True,
            'chat': chat,
            'message': 'Чат успешно создан'
        })
        
    except Exception as e:
        print(f"❌ Ошибка создания чата: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Ресурс не найден'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Внутренняя ошибка сервера'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("🚀 UltraModern Messenger запущен!")
    print("=" * 50)
    print("💫 Ультра-современный дизайн")
    print("📱 Оптимизирован для мобильных")
    print("🎯 Рабочие чаты сразу после регистрации")
    print("🔧 Расширенная система пользователей")
    print("📊 Подробная статистика")
    print("🔍 Поиск по чатам")
    print("👥 Групповые и приватные чаты")
    print("=" * 50)
    print(f"🔗 Порт: {port}")
    print(f"🐛 Режим отладки: {debug}")
    print(f"🕒 Время запуска: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Создаем тестового пользователя для демонстрации
    if debug:
        test_user = {
            'id': 'demo-user-123',
            'name': 'Демо Пользователь',
            'avatar': 'https://api.dicebear.com/7.x/avataaars/svg?seed=demo',
            'premium': True,
            'level': 42,
            'xp': 2500,
            'online': True
        }
        chat_manager.add_user(test_user)
        generate_sample_chats('demo-user-123')
        print("👤 Создан демо-пользователь для тестирования")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
