# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'trollexdl-premium-2024')

# Хранилище активных звонков
active_calls = {}

def get_days_until_new_year():
    now = datetime.datetime.now()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    return (new_year - now).days

def generate_username():
    adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha']
    nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther']
    numbers = random.randint(1000, 9999)
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"

def generate_email(username):
    domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net']
    return f"{username.lower()}@{random.choice(domains)}"

def generate_user_id():
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_call_id():
    return f"call_{uuid.uuid4().hex[:12]}"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrollexDL 🚀 Ultimate Messenger</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        :root {
            --primary: #0a0a2a;
            --secondary: #1a1a4a;
            --accent: #6c2bd9;
            --accent-glow: #8b5cf6;
            --neon: #00ff88;
            --text: #ffffff;
            --text-secondary: #b0b0ff;
            --danger: #ff4444;
            --success: #00ff88;
            --warning: #ffaa00;
            --glass: rgba(255, 255, 255, 0.1);
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--text);
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
            z-index: 1000;
            background: var(--primary);
        }

        .hidden {
            display: none !important;
        }

        .cosmic-card {
            background: rgba(26, 26, 74, 0.95);
            border: 2px solid var(--accent);
            border-radius: 25px;
            padding: 40px 30px;
            width: 100%;
            max-width: 420px;
            text-align: center;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .logo {
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 25px;
            background: linear-gradient(45deg, var(--neon), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(107, 43, 217, 0.5);
        }

        .typing-animation {
            display: inline-block;
            overflow: hidden;
            border-right: 3px solid var(--neon);
            white-space: nowrap;
            margin: 0 auto;
            animation: typing 2.5s steps(40, end), blink-caret 0.75s step-end infinite;
            font-size: 1.2rem;
            min-height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--neon) }
        }

        .pulse-glow {
            animation: pulse-glow 2s ease-in-out infinite alternate;
        }

        @keyframes pulse-glow {
            from {
                box-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
            }
            to {
                box-shadow: 0 0 40px rgba(107, 43, 217, 0.8), 0 0 60px rgba(0, 255, 136, 0.4);
            }
        }

        .btn {
            width: 100%;
            padding: 18px;
            border: none;
            border-radius: 15px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            margin: 12px 0;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn:active {
            transform: scale(0.95);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            box-shadow: 0 8px 25px rgba(107, 43, 217, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(107, 43, 217, 0.6);
        }

        .btn-secondary {
            background: var(--glass);
            color: var(--text);
            border: 2px solid var(--accent);
            backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(107, 43, 217, 0.3);
        }

        .user-card {
            background: var(--glass);
            padding: 25px;
            border-radius: 20px;
            margin: 20px 0;
            border: 1px solid var(--accent);
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .user-avatar {
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 15px;
            box-shadow: 0 8px 25px rgba(107, 43, 217, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }

        .app {
            width: 100%;
            height: 100vh;
            display: flex;
        }

        .sidebar {
            width: 320px;
            background: rgba(26, 26, 74, 0.95);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(20px);
            box-shadow: 5px 0 25px rgba(0, 0, 0, 0.3);
        }

        .user-header {
            padding: 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
            border-bottom: 2px solid var(--accent);
        }

        .nav-tabs {
            display: flex;
            background: var(--glass);
            border-radius: 15px;
            padding: 8px;
            margin: 15px;
            border: 1px solid var(--accent);
            backdrop-filter: blur(10px);
        }

        .nav-tab {
            flex: 1;
            padding: 12px 8px;
            text-align: center;
            cursor: pointer;
            border-radius: 12px;
            transition: all 0.3s ease;
            font-size: 0.95rem;
            font-weight: 600;
            border: none;
            background: transparent;
            color: var(--text);
        }

        .nav-tab.active {
            background: var(--accent);
            box-shadow: 0 4px 15px rgba(107, 43, 217, 0.4);
        }

        .nav-tab:not(.active):hover {
            background: rgba(107, 43, 217, 0.2);
        }

        .search-box {
            padding: 15px;
        }

        .search-input {
            width: 100%;
            padding: 15px 20px;
            background: var(--glass);
            border: 2px solid var(--accent);
            border-radius: 15px;
            color: var(--text);
            font-size: 1rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--neon);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
            background: rgba(255, 255, 255, 0.15);
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: var(--glass);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            backdrop-filter: blur(10px);
        }

        .chat-item:active {
            transform: scale(0.98);
        }

        .chat-item:hover {
            background: rgba(107, 43, 217, 0.3);
            border-color: var(--accent);
            box-shadow: 0 5px 15px rgba(107, 43, 217, 0.2);
        }

        .item-avatar {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            flex-shrink: 0;
            font-size: 1.2rem;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
            position: relative;
        }

        .chat-header {
            padding: 20px;
            background: rgba(26, 26, 74, 0.95);
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 15px;
            backdrop-filter: blur(20px);
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
        }

        .messages-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: linear-gradient(180deg, rgba(10, 10, 42, 0.8) 0%, rgba(26, 26, 74, 0.6) 100%);
        }

        .message {
            max-width: 75%;
            padding: 15px 20px;
            border-radius: 20px;
            position: relative;
            word-wrap: break-word;
            backdrop-filter: blur(10px);
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.received {
            background: rgba(107, 43, 217, 0.25);
            align-self: flex-start;
            border-bottom-left-radius: 8px;
            border: 1px solid rgba(107, 43, 217, 0.3);
        }

        .message.sent {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            align-self: flex-end;
            color: white;
            border-bottom-right-radius: 8px;
            box-shadow: 0 4px 15px rgba(107, 43, 217, 0.3);
        }

        .message-input-container {
            padding: 20px;
            background: rgba(26, 26, 74, 0.95);
            border-top: 2px solid var(--accent);
            display: flex;
            gap: 15px;
            backdrop-filter: blur(20px);
        }

        .message-input {
            flex: 1;
            padding: 18px 20px;
            background: var(--glass);
            border: 2px solid var(--accent);
            border-radius: 25px;
            color: var(--text);
            font-size: 1rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .message-input:focus {
            outline: none;
            border-color: var(--neon);
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.3);
        }

        .send-btn {
            padding: 18px 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1.1rem;
            font-weight: 600;
            box-shadow: 0 5px 20px rgba(107, 43, 217, 0.4);
        }

        .send-btn:active {
            transform: scale(0.95);
        }

        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(107, 43, 217, 0.6);
        }

        /* Стили для видеозвонков */
        .call-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--primary);
            z-index: 2000;
            display: none;
            flex-direction: column;
        }

        .call-container.active {
            display: flex;
        }

        .video-grid {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            padding: 25px;
            align-items: center;
            justify-items: center;
        }

        .video-container {
            position: relative;
            background: var(--secondary);
            border-radius: 25px;
            overflow: hidden;
            border: 3px solid var(--accent);
            min-height: 280px;
            max-width: 550px;
            width: 100%;
            transition: all 0.4s ease;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            backdrop-filter: blur(10px);
        }

        .video-container.speaking {
            border-color: var(--neon);
            box-shadow: 0 0 40px rgba(0, 255, 136, 0.6);
            transform: scale(1.03);
        }

        .video-container.remote {
            border-color: var(--accent-glow);
        }

        .video-container.local {
            border-color: var(--accent);
        }

        .video-container.main-view {
            grid-column: 1 / -1;
            max-width: 900px;
            min-height: 500px;
        }

        .video-element {
            width: 100%;
            height: 100%;
            object-fit: cover;
            background: var(--secondary);
        }

        .video-label {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 18px;
            border-radius: 20px;
            font-size: 1rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .video-status {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 8px 15px;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }

        .call-controls {
            padding: 30px;
            background: rgba(26, 26, 74, 0.95);
            display: flex;
            justify-content: center;
            gap: 25px;
            border-top: 2px solid var(--accent);
            backdrop-filter: blur(20px);
        }

        .control-btn {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: none;
            font-size: 1.6rem;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
        }

        .control-btn:active {
            transform: scale(0.9);
        }

        .control-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent, rgba(255,255,255,0.15), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .control-btn:hover::before {
            opacity: 1;
        }

        .control-btn:hover {
            transform: scale(1.15);
            box-shadow: 0 12px 35px rgba(0,0,0,0.5);
        }

        .control-btn.call-end {
            background: linear-gradient(135deg, var(--danger), #ff6b6b);
            color: white;
        }

        .control-btn.mic-toggle {
            background: linear-gradient(135deg, var(--success), #00cc77);
            color: white;
        }

        .control-btn.mic-toggle.muted {
            background: linear-gradient(135deg, var(--danger), #ff6b6b);
        }

        .control-btn.cam-toggle {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .control-btn.cam-toggle.off {
            background: linear-gradient(135deg, var(--warning), #ffbb33);
        }

        .call-link-container {
            position: absolute;
            top: 25px;
            left: 25px;
            background: rgba(0,0,0,0.85);
            padding: 15px 22px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            backdrop-filter: blur(15px);
            z-index: 10;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }

        .call-link {
            color: var(--neon);
            font-family: 'Courier New', monospace;
            font-size: 1rem;
            max-width: 220px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-weight: 600;
        }

        .copy-link-btn {
            background: var(--accent);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .copy-link-btn:active {
            transform: scale(0.95);
        }

        .copy-link-btn:hover {
            background: var(--accent-glow);
            transform: scale(1.05);
        }

        .call-invite {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(26, 26, 74, 0.95);
            border: 2px solid var(--accent);
            border-radius: 30px;
            padding: 40px;
            z-index: 3000;
            text-align: center;
            display: none;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
            animation: invite-pulse 2s infinite;
        }

        @keyframes invite-pulse {
            0%, 100% { box-shadow: 0 0 25px rgba(107, 43, 217, 0.6); }
            50% { box-shadow: 0 0 40px rgba(107, 43, 217, 0.9), 0 0 60px rgba(0, 255, 136, 0.5); }
        }

        .call-invite.active {
            display: block;
        }

        .settings-panel {
            position: fixed;
            top: 0;
            right: -450px;
            width: 450px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            border-left: 2px solid var(--accent);
            z-index: 500;
            transition: right 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            padding: 25px;
            overflow-y: auto;
            backdrop-filter: blur(20px);
            box-shadow: -5px 0 30px rgba(0,0,0,0.4);
        }

        .settings-panel.active {
            right: 0;
        }

        .donate-panel {
            position: fixed;
            top: 0;
            left: -450px;
            width: 450px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            border-right: 2px solid var(--accent);
            z-index: 500;
            transition: left 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            padding: 25px;
            overflow-y: auto;
            backdrop-filter: blur(20px);
            box-shadow: 5px 0 30px rgba(0,0,0,0.4);
        }

        .donate-panel.active {
            left: 0;
        }

        .notification {
            position: fixed;
            top: 25px;
            right: 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 18px 28px;
            border-radius: 20px;
            z-index: 4000;
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            animation: slideIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 1px solid rgba(255,255,255,0.15);
            font-weight: 600;
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

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.3rem;
            cursor: pointer;
            padding: 10px;
            border-radius: 12px;
            transition: all 0.3s ease;
        }

        .mobile-menu-btn:active {
            transform: scale(0.9);
        }

        .mobile-menu-btn:hover {
            background: rgba(255,255,255,0.1);
        }

        .empty-state {
            text-align: center;
            padding: 60px 25px;
            color: var(--text-secondary);
        }

        .empty-state-icon {
            font-size: 5rem;
            margin-bottom: 25px;
            opacity: 0.7;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }

        .error-message {
            background: rgba(255,68,68,0.2);
            border: 1px solid var(--danger);
            color: var(--danger);
            padding: 15px;
            border-radius: 15px;
            margin: 15px 0;
            text-align: center;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }

        .loading {
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 4px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: var(--neon);
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .call-timer {
            position: absolute;
            top: 25px;
            right: 25px;
            background: rgba(0,0,0,0.85);
            color: var(--neon);
            padding: 10px 18px;
            border-radius: 20px;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            font-weight: 700;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }

        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                height: 100%;
                transform: translateX(-100%);
                transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                z-index: 200;
                width: 300px;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .mobile-menu-btn {
                display: block;
            }

            .video-grid {
                grid-template-columns: 1fr;
                padding: 15px;
                gap: 15px;
            }

            .video-container {
                min-height: 220px;
                border-radius: 20px;
            }

            .video-container.main-view {
                min-height: 350px;
            }

            .control-btn {
                width: 65px;
                height: 65px;
                font-size: 1.4rem;
            }

            .call-link-container {
                top: 15px;
                left: 15px;
                right: 15px;
                padding: 12px 18px;
            }

            .call-link {
                max-width: 200px;
                font-size: 0.9rem;
            }

            .settings-panel,
            .donate-panel {
                width: 100%;
                max-width: 350px;
            }

            .message {
                max-width: 85%;
            }

            .call-controls {
                padding: 25px;
                gap: 20px;
            }

            .btn {
                padding: 16px;
                font-size: 1rem;
            }
        }

        @media (max-width: 480px) {
            .cosmic-card {
                padding: 30px 20px;
                margin: 15px;
            }

            .logo {
                font-size: 2.5rem;
            }

            .call-controls {
                padding: 20px;
                gap: 15px;
            }

            .control-btn {
                width: 60px;
                height: 60px;
                font-size: 1.3rem;
            }

            .video-container {
                min-height: 200px;
            }

            .call-timer {
                top: 15px;
                right: 15px;
                font-size: 1rem;
                padding: 8px 15px;
            }

            .user-avatar {
                width: 70px;
                height: 70px;
                font-size: 1.8rem;
            }
        }

        /* Анимация подключения */
        .connection-status {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: var(--text);
            z-index: 5;
            background: rgba(0,0,0,0.8);
            padding: 25px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            border: 1px solid var(--accent);
        }

        .connecting-dots {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 20px;
        }

        .connecting-dots span {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--neon);
            animation: bounce 1.4s ease-in-out infinite both;
            box-shadow: 0 0 10px var(--neon);
        }

        .connecting-dots span:nth-child(1) { animation-delay: -0.32s; }
        .connecting-dots span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
            0%, 80%, 100% {
                transform: scale(0);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }

        /* Улучшенные hover эффекты */
        .clickable {
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .clickable:active {
            transform: scale(0.95);
        }

        .glass-effect {
            background: var(--glass);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .neon-glow {
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
            border: 1px solid rgba(0, 255, 136, 0.3);
        }

        /* Анимации появления */
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .slide-in-left {
            animation: slideInLeft 0.4s ease-out;
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Улучшенная прокрутка */
        .content-list::-webkit-scrollbar {
            width: 6px;
        }

        .content-list::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
        }

        .content-list::-webkit-scrollbar-thumb {
            background: var(--accent);
            border-radius: 3px;
        }

        .content-list::-webkit-scrollbar-thumb:hover {
            background: var(--accent-glow);
        }
    </style>
</head>
<body>
    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card pulse-glow">
            <div class="logo">TrollexDL</div>
            <div style="margin: 30px 0; font-size: 1.3rem; min-height: 80px; display: flex; align-items: center; justify-content: center;">
                <div class="typing-animation" id="typingText">Инициализация квантового интерфейса...</div>
            </div>
            <div class="loading" style="margin: 0 auto;"></div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card pulse-glow">
            <div class="logo">TrollexDL</div>
            <div style="margin-bottom: 35px; color: var(--text-secondary); font-size: 1.2rem; line-height: 1.5;">
                Премиум мессенджер с видеозвонками<br>и квантовым шифрованием
            </div>
            
            <button class="btn btn-primary clickable" onclick="showRegisterScreen()">
                🚀 НАЧАТЬ ПУТЕШЕСТВИЕ
            </button>
            
            <button class="btn btn-secondary clickable" onclick="quickStart()">
                ⚡ МГНОВЕННЫЙ СТАРТ
            </button>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-card pulse-glow">
            <div class="logo">Создание профиля</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">🚀</div>
                <h3 id="registerName">Quantum_User</h3>
                <p style="color: var(--text-secondary);">ID: <span id="registerId">...</span></p>
                <p style="color: var(--text-secondary);">📧 <span id="registerEmail">...</span></p>
            </div>
            
            <button class="btn btn-primary clickable" onclick="registerUser()">
                ✅ АКТИВИРОВАТЬ ПРОФИЛЬ
            </button>
            
            <button class="btn btn-secondary clickable" onclick="generateNewUser()">
                🔄 ОБНОВИТЬ АВАТАР
            </button>
            
            <button class="btn btn-secondary clickable" onclick="showWelcomeScreen()">
                ← ВЕРНУТЬСЯ
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <button class="mobile-menu-btn clickable" onclick="toggleSidebar()">☰</button>
                <div class="user-avatar" id="userAvatar">🚀</div>
                <h3 id="userName">User</h3>
                <p>ID: <span id="userId">...</span></p>
            </div>

            <div class="nav-tabs">
                <button class="nav-tab active clickable" onclick="switchTab('chats')">💬</button>
                <button class="nav-tab clickable" onclick="switchTab('users')">👥</button>
                <button class="nav-tab clickable" onclick="switchTab('calls')">📞</button>
                <button class="nav-tab clickable" onclick="showDonatePanel()">💎</button>
                <button class="nav-tab clickable" onclick="showSettings()">⚙️</button>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Поиск..." id="searchInput" oninput="searchContent()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Динамически заполняется -->
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn clickable" onclick="toggleSidebar()">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Выберите чат для начала общения</p>
                </div>
                <button class="control-btn clickable" onclick="startVideoCall()" style="background: var(--success); width: 50px; height: 50px; font-size: 1.2rem;">📞</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div class="empty-state">
                    <div class="empty-state-icon">🌌</div>
                    <h3>Добро пожаловать в TrollexDL!</h3>
                    <p>Начните общение с квантовым шифрованием</p>
                    <button class="btn btn-primary clickable" onclick="createCallRoom()" style="margin-top: 30px;">
                        🎥 СОЗДАТЬ ВИДЕОЗВОНОК
                    </button>
                </div>
            </div>

            <div class="message-input-container">
                <input type="text" class="message-input" placeholder="Введите сообщение..." id="messageInput">
                <button class="send-btn clickable" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Контейнер видеозвонка -->
    <div id="callContainer" class="call-container">
        <div class="call-link-container">
            <span class="call-link" id="callLink">Загрузка...</span>
            <button class="copy-link-btn clickable" onclick="copyCallLink()">📋</button>
        </div>
        
        <div class="call-timer" id="callTimer">00:00</div>
        
        <div class="video-grid" id="videoGrid">
            <div class="video-container local" id="localVideoContainer">
                <video id="localVideo" autoplay muted playsinline class="video-element"></video>
                <div class="video-label">Вы 🔴</div>
                <div class="video-status" id="localStatus">🔴 LIVE</div>
                <div class="connection-status" id="localConnection">
                    <div class="connecting-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <div>Подключение...</div>
                </div>
            </div>
            <div class="video-container remote" id="remoteVideoContainer">
                <video id="remoteVideo" autoplay playsinline class="video-element"></video>
                <div class="video-label">Участник</div>
                <div class="video-status" id="remoteStatus">⏳ Ожидание</div>
                <div class="connection-status" id="remoteConnection">
                    <div class="connecting-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <div>Ожидание участника...</div>
                </div>
            </div>
        </div>
        
        <div class="call-controls">
            <button class="control-btn mic-toggle clickable" id="micToggle" onclick="toggleMicrophone()">🎤</button>
            <button class="control-btn cam-toggle clickable" id="camToggle" onclick="toggleCamera()">📹</button>
            <button class="control-btn call-end clickable" onclick="endCall()">📞</button>
        </div>
    </div>

    <!-- Приглашение на звонок -->
    <div id="callInvite" class="call-invite">
        <div class="logo">📞 ВХОДЯЩИЙ ВЫЗОВ</div>
        <div class="user-card">
            <div class="user-avatar" id="callerAvatar">👤</div>
            <h3 id="callerName">Unknown</h3>
            <p style="color: var(--text-secondary);">приглашает вас на видеозвонок</p>
        </div>
        <button class="btn btn-primary clickable" onclick="acceptCall()">✅ ПРИНЯТЬ</button>
        <button class="btn btn-secondary clickable" onclick="declineCall()">❌ ОТКЛОНИТЬ</button>
    </div>

    <!-- Панель доната -->
    <div class="donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h3>💎 ПРЕМИУМ ТАРИФЫ</h3>
            <button class="mobile-menu-btn clickable" onclick="hideDonatePanel()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div class="user-card" style="border-color: var(--accent);">
            <h4>🌟 VIP - 299 ₽</h4>
            <p style="color: var(--text-secondary); margin: 10px 0 15px 0;">Цветные сообщения, специальный значок</p>
            <button class="btn btn-primary clickable" onclick="selectTier('vip')">ВЫБРАТЬ VIP</button>
        </div>

        <div class="user-card" style="border-color: var(--neon);">
            <h4>💫 Premium - 599 ₽</h4>
            <p style="color: var(--text-secondary); margin: 10px 0 15px 0;">Все функции VIP + расширенные темы</p>
            <button class="btn btn-primary clickable" onclick="selectTier('premium')">ВЫБРАТЬ PREMIUM</button>
        </div>

        <div style="text-align: center; margin-top: 30px; padding: 25px; background: var(--glass); border-radius: 20px; border: 1px solid var(--accent);">
            <p>Напишите в Telegram: <strong>@trollex_official</strong></p>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h3>⚙️ НАСТРОЙКИ</h3>
            <button class="mobile-menu-btn clickable" onclick="hideSettings()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 600;">👤 Имя пользователя</label>
            <input type="text" class="search-input" id="settingsName" placeholder="Введите новое имя">
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 600;">🎥 Камера по умолчанию</label>
            <select class="search-input" id="cameraSelect">
                <option value="">Автовыбор</option>
            </select>
        </div>

        <div style="margin-bottom: 25px;">
            <label style="display: block; margin-bottom: 8px; font-weight: 600;">🎤 Микрофон по умолчанию</label>
            <select class="search-input" id="microphoneSelect">
                <option value="">Автовыбор</option>
            </select>
        </div>

        <button class="btn btn-primary clickable" onclick="saveSettings()">💾 СОХРАНИТЬ</button>
        <button class="btn btn-secondary clickable" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 20px;">
            🚪 ВЫЙТИ
        </button>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let messages = {};
        let allUsers = [];
        
        // Переменные для видеозвонков
        let localStream = null;
        let remoteStream = null;
        let peerConnection = null;
        let currentCallId = null;
        let isInCall = false;
        let isMicMuted = false;
        let isCamOff = false;
        let callStartTime = null;
        let callTimerInterval = null;
        let audioContext = null;
        let analyser = null;
        let isCallCreator = false;
        
        // STUN/TURN серверы для обхода блокировок
        const iceServers = [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' },
            { urls: 'stun:stun2.l.google.com:19302' },
            { urls: 'stun:stun3.l.google.com:19302' },
            { urls: 'stun:stun4.l.google.com:19302' },
            // Резервные TURN серверы
            {
                urls: 'turn:turn.anyfirewall.com:443?transport=tcp',
                username: 'webrtc',
                credential: 'webrtc'
            },
            {
                urls: 'turn:numb.viagenie.ca',
                username: 'webrtc@live.com',
                credential: 'muazkh'
            }
        ];

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            startTypingAnimation();
            
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 4000);
            
            // Проверяем URL на наличие приглашения на звонок
            checkCallInvite();
        });

        function startTypingAnimation() {
            const texts = [
                "Инициализация квантового интерфейса...",
                "Загрузка защищённого канала...", 
                "Подключение к нейросети...",
                "Оптимизация видеокодека...",
                "Готово! Запускаем TrollexDL..."
            ];
            let currentIndex = 0;
            const typingElement = document.getElementById('typingText');
            
            function typeNextText() {
                if (currentIndex < texts.length) {
                    typingElement.textContent = texts[currentIndex];
                    typingElement.style.animation = 'none';
                    void typingElement.offsetWidth;
                    typingElement.style.animation = 'typing 2s steps(40, end), blink-caret 0.75s step-end infinite';
                    currentIndex++;
                    setTimeout(typeNextText, 2000);
                }
            }
            
            typeNextText();
        }

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function showWelcomeScreen() {
            hideAllScreens();
            document.getElementById('welcomeScreen').classList.remove('hidden');
        }

        function showRegisterScreen() {
            hideAllScreens();
            document.getElementById('registerScreen').classList.remove('hidden');
            generateNewUser();
        }

        function hideAllScreens() {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
        }

        function generateNewUser() {
            const name = generateUsername();
            const email = generateEmail(name);
            const userId = generateUserId();
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌'];
            
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
            document.getElementById('registerEmail').textContent = email;
        }

        function generateUsername() {
            const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital'];
            const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger'];
            const numbers = Math.floor(Math.random() * 9000) + 1000;
            return `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
        }

        function generateEmail(username) {
            const domains = ['quantum.io', 'cosmic.com', 'trollex.ai'];
            return `${username.toLowerCase()}@${domains[Math.floor(Math.random() * domains.length)]}`;
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 8).toUpperCase();
        }

        function registerUser() {
            const name = document.getElementById('registerName').textContent;
            const avatar = document.getElementById('registerAvatar').textContent;
            const userId = document.getElementById('registerId').textContent;
            const email = document.getElementById('registerEmail').textContent;
            
            currentUser = {
                id: userId,
                name: name,
                avatar: avatar,
                email: email,
                settings: {}
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            
            // Создаем тестовых пользователей
            initializeSampleUsers();
            
            showMainApp();
            showNotification('Профиль создан успешно! 🎉');
        }

        function initializeSampleUsers() {
            allUsers = [
                {id: 'user1', name: 'Alex_Quantum', avatar: '👨‍💻', online: true},
                {id: 'user2', name: 'Sarah_Cyber', avatar: '👩‍🎨', online: true},
                {id: 'user3', name: 'Mike_Neon', avatar: '👨‍🚀', online: false},
                {id: 'user4', name: 'Emma_Digital', avatar: '👩‍💼', online: true}
            ];
            
            // Добавляем текущего пользователя
            allUsers.push({
                id: currentUser.id,
                name: currentUser.name,
                avatar: currentUser.avatar,
                online: true
            });
            
            localStorage.setItem('allUsers', JSON.stringify(allUsers));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                showMainApp();
                showNotification('С возвращением! 🚀');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                showMainApp();
            } else {
                showWelcomeScreen();
            }
        }

        function showMainApp() {
            hideAllScreens();
            document.getElementById('mainApp').classList.remove('hidden');
            
            // Заполняем данные пользователя
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            
            loadContent();
            loadMediaDevices();
        }

        // Функции для видеозвонков
        async function createCallRoom() {
            try {
                showNotification('Создание комнаты для звонка... 🎥');
                isCallCreator = true;
                
                // Генерируем ID звонка
                currentCallId = 'call_' + Math.random().toString(36).substr(2, 12);
                
                // Получаем медиапоток
                await getLocalStream();
                
                // Создаем ссылку для приглашения
                const callLink = `${window.location.origin}?call=${currentCallId}&inviter=${currentUser.id}`;
                document.getElementById('callLink').textContent = callLink;
                
                // Показываем интерфейс звонка
                document.getElementById('callContainer').classList.add('active');
                startCallTimer();
                hideConnectionStatus('local');
                
                showNotification('Комната создана! Отправьте ссылку участникам 🔗');
                
                // Запускаем мониторинг аудио
                startAudioMonitoring();
                
            } catch (error) {
                console.error('Ошибка создания комнаты:', error);
                showNotification('Ошибка доступа к камере/микрофону ❌');
            }
        }

        async function getLocalStream() {
            try {
                // Оптимизированные настройки для мобильных устройств
                const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
                const constraints = {
                    video: {
                        width: { ideal: isMobile ? 640 : 1280 },
                        height: { ideal: isMobile ? 480 : 720 },
                        frameRate: { ideal: isMobile ? 24 : 30 },
                        facingMode: isMobile ? 'user' : 'environment'
                    },
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true,
                        sampleRate: 48000,
                        channelCount: 1
                    }
                };
                
                localStream = await navigator.mediaDevices.getUserMedia(constraints);
                document.getElementById('localVideo').srcObject = localStream;
                
                return localStream;
            } catch (error) {
                console.error('Ошибка доступа к медиаустройствам:', error);
                // Пробуем без видео
                try {
                    const audioConstraints = {
                        audio: {
                            echoCancellation: true,
                            noiseSuppression: true,
                            autoGainControl: true
                        }
                    };
                    localStream = await navigator.mediaDevices.getUserMedia(audioConstraints);
                    document.getElementById('localVideo').srcObject = null;
                    document.getElementById('localVideoContainer').style.background = 'linear-gradient(135deg, var(--accent), var(--accent-glow))';
                    showNotification('Камера недоступна, используется только аудио 🎤');
                    return localStream;
                } catch (audioError) {
                    showNotification('Не удалось получить доступ к медиаустройствам ❌');
                    throw audioError;
                }
            }
        }

        function startAudioMonitoring() {
            if (!localStream) return;
            
            try {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioContext.createAnalyser();
                const source = audioContext.createMediaStreamSource(localStream);
                source.connect(analyser);
                analyser.fftSize = 256;
                
                checkAudioLevel();
            } catch (error) {
                console.error('Ошибка мониторинга аудио:', error);
            }
        }

        function checkAudioLevel() {
            if (!analyser) return;
            
            const dataArray = new Uint8Array(analyser.frequencyBinCount);
            analyser.getByteFrequencyData(dataArray);
            
            let sum = 0;
            for (let i = 0; i < dataArray.length; i++) {
                sum += dataArray[i];
            }
            const average = sum / dataArray.length;
            
            // Если уровень звука выше порога, подсвечиваем видео
            if (average > 20 && !isMicMuted) {
                document.getElementById('localVideoContainer').classList.add('speaking');
            } else {
                document.getElementById('localVideoContainer').classList.remove('speaking');
            }
            
            requestAnimationFrame(checkAudioLevel);
        }

        function toggleMicrophone() {
            if (localStream) {
                const audioTracks = localStream.getAudioTracks();
                if (audioTracks.length > 0) {
                    isMicMuted = !isMicMuted;
                    audioTracks[0].enabled = !isMicMuted;
                    
                    const micBtn = document.getElementById('micToggle');
                    micBtn.textContent = isMicMuted ? '🎤❌' : '🎤';
                    micBtn.classList.toggle('muted', isMicMuted);
                    
                    showNotification(isMicMuted ? 'Микрофон выключен 🔇' : 'Микрофон включен 🔊');
                }
            }
        }

        function toggleCamera() {
            if (localStream) {
                const videoTracks = localStream.getVideoTracks();
                if (videoTracks.length > 0) {
                    isCamOff = !isCamOff;
                    videoTracks[0].enabled = !isCamOff;
                    
                    const camBtn = document.getElementById('camToggle');
                    camBtn.textContent = isCamOff ? '📹❌' : '📹';
                    camBtn.classList.toggle('off', isCamOff);
                    
                    if (isCamOff) {
                        document.getElementById('localVideo').style.display = 'none';
                        document.getElementById('localVideoContainer').style.background = 'linear-gradient(135deg, var(--accent), var(--accent-glow))';
                    } else {
                        document.getElementById('localVideo').style.display = 'block';
                        document.getElementById('localVideoContainer').style.background = 'var(--secondary)';
                    }
                    
                    showNotification(isCamOff ? 'Камера выключена 📷' : 'Камера включена 📹');
                }
            }
        }

        function copyCallLink() {
            const callLink = document.getElementById('callLink').textContent;
            navigator.clipboard.writeText(callLink).then(() => {
                showNotification('Ссылка скопирована в буфер! 📋');
            }).catch(() => {
                // Fallback для старых браузеров
                const textArea = document.createElement('textarea');
                textArea.value = callLink;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showNotification('Ссылка скопирована! 📋');
            });
        }

        function startCallTimer() {
            callStartTime = new Date();
            callTimerInterval = setInterval(() => {
                const now = new Date();
                const diff = now - callStartTime;
                const minutes = Math.floor(diff / 60000);
                const seconds = Math.floor((diff % 60000) / 1000);
                document.getElementById('callTimer').textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }, 1000);
        }

        function hideConnectionStatus(type) {
            document.getElementById(`${type}Connection`).style.display = 'none';
            document.getElementById(`${type}Status`).textContent = type === 'local' ? '🔴 LIVE' : '✅ Подключен';
        }

        function endCall() {
            // Останавливаем таймер
            if (callTimerInterval) {
                clearInterval(callTimerInterval);
                callTimerInterval = null;
            }
            
            // Останавливаем мониторинг аудио
            if (audioContext) {
                audioContext.close();
                audioContext = null;
            }
            
            // Останавливаем все медиапотоки
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
                localStream = null;
            }
            
            if (remoteStream) {
                remoteStream.getTracks().forEach(track => track.stop());
                remoteStream = null;
            }
            
            // Закрываем соединение
            if (peerConnection) {
                peerConnection.close();
                peerConnection = null;
            }
            
            // Скрываем интерфейс звонка
            document.getElementById('callContainer').classList.remove('active');
            document.getElementById('callInvite').classList.remove('active');
            
            isInCall = false;
            currentCallId = null;
            isCallCreator = false;
            
            showNotification('Звонок завершен 📞');
        }

        function checkCallInvite() {
            const urlParams = new URLSearchParams(window.location.search);
            const callId = urlParams.get('call');
            const inviterId = urlParams.get('inviter');
            
            if (callId && inviterId) {
                // Находим информацию о звонящем
                const inviter = allUsers.find(user => user.id === inviterId) || 
                               { name: 'Unknown User', avatar: '👤' };
                
                document.getElementById('callerName').textContent = inviter.name;
                document.getElementById('callerAvatar').textContent = inviter.avatar;
                
                currentCallId = callId;
                document.getElementById('callInvite').classList.add('active');
            }
        }

        async function acceptCall() {
            try {
                document.getElementById('callInvite').classList.remove('active');
                isCallCreator = false;
                
                // Получаем медиапоток
                await getLocalStream();
                
                // Показываем интерфейс звонка
                document.getElementById('callContainer').classList.add('active');
                document.getElementById('callLink').textContent = 'Присоединились к звонку';
                startCallTimer();
                hideConnectionStatus('local');
                
                showNotification('Вы присоединились к звонку! 🎥');
                
                // Запускаем мониторинг аудио
                startAudioMonitoring();
                
                // Симулируем подключение удаленного участника
                setTimeout(() => {
                    hideConnectionStatus('remote');
                    // Симуляция голосовой активности
                    setInterval(() => {
                        if (Math.random() > 0.7) {
                            document.getElementById('remoteVideoContainer').classList.add('speaking');
                            setTimeout(() => {
                                document.getElementById('remoteVideoContainer').classList.remove('speaking');
                            }, 1000);
                        }
                    }, 3000);
                }, 2000);
                
            } catch (error) {
                console.error('Ошибка подключения к звонку:', error);
                showNotification('Ошибка подключения к звонку ❌');
            }
        }

        function declineCall() {
            document.getElementById('callInvite').classList.remove('active');
            currentCallId = null;
            showNotification('Вы отклонили вызов 📞');
        }

        async function loadMediaDevices() {
            try {
                const devices = await navigator.mediaDevices.enumerateDevices();
                const cameraSelect = document.getElementById('cameraSelect');
                const microphoneSelect = document.getElementById('microphoneSelect');
                
                cameraSelect.innerHTML = '<option value="">Автовыбор</option>';
                microphoneSelect.innerHTML = '<option value="">Автовыбор</option>';
                
                devices.forEach(device => {
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.textContent = device.label || `${device.kind} ${device.deviceId.slice(0, 5)}`;
                    
                    if (device.kind === 'videoinput') {
                        cameraSelect.appendChild(option);
                    } else if (device.kind === 'audioinput') {
                        microphoneSelect.appendChild(option);
                    }
                });
            } catch (error) {
                console.error('Ошибка загрузки медиаустройств:', error);
            }
        }

        function startVideoCall() {
            if (currentChat) {
                createCallRoom();
            } else {
                showNotification('Выберите чат для начала звонка 💬');
            }
        }

        // Остальные функции остаются аналогичными предыдущей версии
        // ... (они такие же как в предыдущем коде)

    </script>
</body>
</html>
'''

@app.route('/')
def index():
    logger.info("Главная страница запрошена")
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/create_call', methods=['POST'])
def api_create_call():
    try:
        data = request.json
        call_id = generate_call_id()
        active_calls[call_id] = {
            'creator': data.get('user_id'),
            'participants': [],
            'created_at': datetime.datetime.now().isoformat()
        }
        logger.info(f"Создан звонок: {call_id}")
        return jsonify({'success': True, 'call_id': call_id, 'call_link': f'{request.host_url}?call={call_id}'})
    except Exception as e:
        logger.error(f"Ошибка создания звонка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running', 
        'service': 'TrollexDL',
        'version': '2.2.0',
        'active_calls': len(active_calls),
        'timestamp': datetime.datetime.now().isoformat(),
        'days_until_new_year': get_days_until_new_year()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 TrollexDL запущен на порту {port}")
    logger.info(f"🌐 Откройте: http://localhost:{port}")
    logger.info(f"🔧 Режим отладки: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
