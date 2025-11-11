# app.py
from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import os
import uuid
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trollexdl-premium-2024'

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
            --vip: #ffd700;
            --premium: #c0c0c0;
            --ultra: #ff6b35;
            --moder: #4CAF50;
            --chromek: #2196F3;
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        .cosmic-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(107, 43, 217, 0.4) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(0, 255, 136, 0.2) 0%, transparent 50%);
            animation: cosmicShift 15s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes cosmicShift {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.02); }
        }

        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes glow {
            0%, 100% { 
                box-shadow: 0 0 20px var(--accent-glow),
                           0 0 40px rgba(139, 92, 246, 0.3);
            }
            50% { 
                box-shadow: 0 0 30px var(--accent-glow),
                           0 0 60px rgba(139, 92, 246, 0.5),
                           0 0 80px rgba(0, 255, 136, 0.2);
            }
        }

        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blinkCursor {
            0%, 100% { border-color: transparent; }
            50% { border-color: var(--neon); }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
        }

        @keyframes ripple {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(4); opacity: 0; }
        }

        @keyframes shine {
            0% { background-position: -100px; }
            100% { background-position: 200px; }
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
            padding: 15px;
            z-index: 1000;
            overflow-y: auto;
        }

        .hidden {
            display: none !important;
        }

        .cosmic-card {
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(20px);
            border: 2px solid var(--accent);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            max-width: 450px;
            animation: slideUp 0.6s ease-out, glow 4s infinite;
            position: relative;
            overflow: hidden;
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--neon), var(--accent-glow), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .typewriter-text {
            overflow: hidden;
            border-right: 2px solid var(--neon);
            white-space: nowrap;
            margin: 0 auto;
            animation: typewriter 2s steps(20, end), blinkCursor 0.75s step-end infinite;
            text-align: center;
            color: var(--text-secondary);
        }

        .btn {
            width: 100%;
            padding: 16px 20px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(107, 43, 217, 0.4);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--text);
            border: 2px solid var(--accent);
        }

        .btn-vip {
            background: linear-gradient(135deg, var(--vip), #ffed4e);
            color: #000;
            font-weight: bold;
        }

        .btn-premium {
            background: linear-gradient(135deg, var(--premium), #e0e0e0);
            color: #000;
        }

        .btn-ultra {
            background: linear-gradient(135deg, var(--ultra), #ff8c5a);
            color: white;
        }

        .btn-moder {
            background: linear-gradient(135deg, var(--moder), #66bb6a);
            color: white;
        }

        .btn-chromek {
            background: linear-gradient(135deg, var(--chromek), #64b5f6);
            color: white;
        }

        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        }

        .user-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            border: 1px solid var(--accent);
            text-align: center;
            animation: float 3s ease-in-out infinite;
        }

        .user-avatar {
            width: 70px;
            height: 70px;
            border-radius: 15px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            margin: 0 auto 12px;
            animation: pulse 2s ease-in-out infinite;
        }

        .premium-badge {
            background: linear-gradient(45deg, var(--vip), var(--premium), var(--ultra));
            color: black;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-top: 8px;
            display: inline-block;
            animation: shine 2s infinite linear;
            background-size: 200% 100%;
        }

        .app {
            width: 100%;
            height: 100vh;
            background: var(--primary);
            display: flex;
        }

        .sidebar {
            width: 100%;
            max-width: 350px;
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(10px);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
        }

        .user-header {
            padding: 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
            position: relative;
        }

        .new-year-countdown {
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            margin: 10px 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid var(--neon);
            animation: glow 3s infinite;
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 4px;
            margin: 12px;
            flex-wrap: wrap;
        }

        .nav-tab {
            flex: 1;
            padding: 10px 8px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 0.9rem;
            min-width: 60px;
            user-select: none;
        }

        .nav-tab.active {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
        }

        .search-box {
            padding: 12px;
        }

        .search-input {
            width: 100%;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 12px;
            color: var(--text);
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            box-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            animation: slideUp 0.5s ease-out;
        }

        .chat-item:hover, .chat-item.active {
            background: rgba(107, 43, 217, 0.2);
            border-color: var(--accent);
            transform: translateX(3px);
        }

        .item-avatar {
            width: 45px;
            height: 45px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 1.2rem;
        }

        .online-dot {
            width: 10px;
            height: 10px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
            margin-left: auto;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
        }

        .chat-header {
            padding: 15px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .messages-container {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .message {
            max-width: 85%;
            padding: 12px 15px;
            border-radius: 15px;
            position: relative;
            animation: slideUp 0.3s ease-out;
        }

        .message.received {
            background: rgba(107, 43, 217, 0.3);
            align-self: flex-start;
            border-bottom-left-radius: 5px;
            border: 1px solid var(--accent);
        }

        .message.sent {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            align-self: flex-end;
            border-bottom-right-radius: 5px;
            color: white;
        }

        .message-premium {
            border: 2px solid var(--vip);
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(139, 92, 246, 0.3));
        }

        .message-actions {
            position: absolute;
            top: -25px;
            right: 0;
            background: rgba(26, 26, 74, 0.9);
            border: 1px solid var(--accent);
            border-radius: 8px;
            display: none;
            gap: 5px;
            padding: 5px;
        }

        .message:hover .message-actions {
            display: flex;
        }

        .message-action {
            background: none;
            border: none;
            color: var(--text);
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .message-action:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 4px;
            text-align: right;
        }

        .message-input-container {
            padding: 15px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--accent);
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .message-input {
            flex: 1;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 20px;
            color: var(--text);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .message-input:focus {
            box-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
        }

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .send-btn:active {
            transform: scale(0.95);
        }

        .settings-panel {
            position: fixed;
            top: 0;
            right: -100%;
            width: 100%;
            max-width: 400px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            backdrop-filter: blur(20px);
            border-left: 2px solid var(--accent);
            z-index: 500;
            transition: right 0.3s ease;
            padding: 25px;
            overflow-y: auto;
        }

        .settings-panel.active {
            right: 0;
        }

        .donate-panel {
            position: fixed;
            top: 0;
            left: -100%;
            width: 100%;
            max-width: 400px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            backdrop-filter: blur(20px);
            border-right: 2px solid var(--accent);
            z-index: 500;
            transition: left 0.3s ease;
            padding: 25px;
            overflow-y: auto;
        }

        .donate-panel.active {
            left: 0;
        }

        .donate-tier {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            border: 2px solid;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .donate-tier:hover {
            transform: translateY(-5px);
        }

        .tier-vip { border-color: var(--vip); }
        .tier-premium { border-color: var(--premium); }
        .tier-ultra { border-color: var(--ultra); }
        .tier-moder { border-color: var(--moder); }
        .tier-chromek { border-color: var(--chromek); }

        .tier-price {
            font-size: 1.5rem;
            font-weight: bold;
            margin: 10px 0;
        }

        .tier-features {
            text-align: left;
            margin: 15px 0;
            font-size: 0.9rem;
        }

        .tier-features li {
            margin: 5px 0;
            padding-left: 10px;
        }

        .setting-item {
            margin-bottom: 18px;
        }

        .setting-label {
            display: block;
            margin-bottom: 6px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.95rem;
        }

        .setting-input {
            width: 100%;
            padding: 10px 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 8px;
            color: var(--text);
            font-size: 0.95rem;
        }

        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 24px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.2);
            transition: .4s;
            border-radius: 24px;
        }

        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }

        input:checked + .toggle-slider {
            background-color: var(--accent);
        }

        input:checked + .toggle-slider:before {
            transform: translateX(26px);
        }

        .notification {
            position: fixed;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 12px 20px;
            border-radius: 12px;
            z-index: 4000;
            animation: slideUp 0.3s ease, glow 2s infinite;
            border: 1px solid var(--accent);
            max-width: 300px;
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.3rem;
            cursor: pointer;
            padding: 8px;
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            background: rgba(107, 43, 217, 0.2);
            border-radius: 12px;
            margin: 5px 15px;
            align-self: flex-start;
            animation: pulse 1.5s infinite;
        }

        .typing-dots {
            display: flex;
            margin-left: 8px;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--neon);
            border-radius: 50%;
            margin: 0 2px;
            animation: typingBounce 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }

        .context-menu {
            position: fixed;
            background: rgba(26, 26, 74, 0.95);
            border: 1px solid var(--accent);
            border-radius: 8px;
            padding: 8px;
            z-index: 10000;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .context-menu-item {
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 4px;
            transition: background 0.2s;
        }

        .context-menu-item:hover {
            background: rgba(107, 43, 217, 0.3);
        }

        .emoji-picker {
            position: absolute;
            bottom: 70px;
            right: 15px;
            background: rgba(26, 26, 74, 0.95);
            border: 1px solid var(--accent);
            border-radius: 12px;
            padding: 15px;
            display: none;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            max-width: 300px;
            backdrop-filter: blur(10px);
        }

        .emoji {
            font-size: 1.2rem;
            cursor: pointer;
            padding: 5px;
            border-radius: 5px;
            text-align: center;
            transition: background 0.2s;
        }

        .emoji:hover {
            background: rgba(107, 43, 217, 0.3);
        }

        .emoji-btn {
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.2rem;
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: background 0.2s;
        }

        .emoji-btn:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .message-reactions {
            display: flex;
            gap: 5px;
            margin-top: 5px;
            flex-wrap: wrap;
        }

        .reaction {
            background: rgba(255, 255, 255, 0.1);
            padding: 2px 6px;
            border-radius: 10px;
            font-size: 0.8rem;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s;
        }

        .reaction:hover, .reaction.active {
            background: rgba(107, 43, 217, 0.3);
            border-color: var(--accent);
        }

        .message-edited {
            font-size: 0.7rem;
            opacity: 0.6;
            margin-left: 5px;
        }

        .online-users {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 10px;
            margin: 10px 15px;
        }

        .online-user {
            display: flex;
            align-items: center;
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
            transition: background 0.2s;
        }

        .online-user:hover {
            background: rgba(107, 43, 217, 0.2);
        }

        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                height: 100%;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 200;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .settings-panel, .donate-panel {
                width: 100%;
                max-width: none;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .cosmic-card {
                padding: 20px;
                margin: 10px;
            }
            
            .nav-tabs {
                flex-wrap: nowrap;
                overflow-x: auto;
            }
            
            .nav-tab {
                min-width: 70px;
                font-size: 0.85rem;
            }
            
            .message {
                max-width: 90%;
            }

            .emoji-picker {
                grid-template-columns: repeat(5, 1fr);
                max-width: 250px;
            }
        }

        @media (max-width: 480px) {
            .cosmic-card {
                padding: 15px;
            }
            
            .btn {
                padding: 14px 16px;
                font-size: 0.9rem;
            }
            
            .user-avatar {
                width: 60px;
                height: 60px;
                font-size: 1.5rem;
            }
            
            .message-input {
                padding: 10px 12px;
                font-size: 0.9rem;
            }
            
            .send-btn {
                padding: 10px 16px;
            }

            .emoji-picker {
                grid-template-columns: repeat(4, 1fr);
                max-width: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="cosmic-bg"></div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card" style="text-align: center;">
            <div class="logo">TrollexDL</div>
            <div class="typewriter-text">Initializing Quantum Protocol...</div>
            <div style="margin-top: 30px; font-size: 2rem; animation: float 2s ease-in-out infinite;">🚀</div>
            <div style="color: var(--text-secondary); margin-top: 20px; animation: slideUp 1s ease-out;">
                Secure • Fast • Cosmic
            </div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="text-align: center; color: var(--text-secondary); margin-bottom: 25px; line-height: 1.5;">
                Ultimate messaging with quantum encryption<br>
                and cosmic design
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 START JOURNEY
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ QUICK START
            </button>

            <div class="new-year-countdown">
                🎄 <span id="newYearCountdown">...</span> until New Year!
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">Registration</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">🚀</div>
                <h3 id="registerName">Quantum_User</h3>
                <p style="color: var(--text-secondary);">ID: <span id="registerId">...</span></p>
                <p style="color: var(--text-secondary); margin-top: 5px;">📧 <span id="registerEmail">...</span></p>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ CREATE PROFILE
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewUser()">
                🔄 GENERATE NEW
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← BACK
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="user-avatar" id="userAvatar">🚀</div>
                <h3 id="userName">User</h3>
                <p style="opacity: 0.8;">ID: <span id="userId">...</span></p>
                <div id="userPremiumBadge" class="premium-badge hidden">PREMIUM</div>
            </div>

            <div class="new-year-countdown">
                🎄 <span id="sidebarCountdown">...</span> until New Year!
            </div>

            <div class="online-users">
                <div style="font-weight: bold; margin-bottom: 8px;">🟢 Online Now</div>
                <div id="onlineUsersList">
                    <!-- Динамически заполняется -->
                </div>
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('users')">👥</div>
                <div class="nav-tab" onclick="switchTab('groups')">👨‍👩‍👧‍👦</div>
                <div class="nav-tab" onclick="showDonatePanel()">💎</div>
                <div class="nav-tab" onclick="showSettings()">⚙️</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Search users..." id="searchInput" oninput="searchUsers()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Динамически заполняется -->
            </div>

            <div style="padding: 15px;">
                <button class="btn btn-secondary" onclick="showLogoutConfirm()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger);">
                    🚪 Logout
                </button>
            </div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Select chat to start messaging</p>
                </div>
                <button class="mobile-menu-btn" onclick="showChatOptions()">⋮</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 40px 15px; color: var(--text-secondary);">
                    <div style="font-size: 3.5rem; margin-bottom: 15px; animation: float 3s ease-in-out infinite;">🌌</div>
                    <h3 style="margin-bottom: 12px;">Welcome to TrollexDL!</h3>
                    <p>Start messaging with quantum encryption</p>
                </div>
            </div>

            <div class="typing-indicator hidden" id="typingIndicator">
                <span id="typingUser">User</span> is typing
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>

            <div class="message-input-container">
                <button class="emoji-btn" onclick="toggleEmojiPicker()">😊</button>
                <input type="text" class="message-input" placeholder="Type your message..." id="messageInput" oninput="handleTyping()">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>

            <div class="emoji-picker" id="emojiPicker">
                <!-- Emojis will be populated by JavaScript -->
            </div>
        </div>
    </div>

    <!-- Панель доната -->
    <div class="donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h3 style="margin: 0;">💎 Premium Tiers</h3>
            <button class="mobile-menu-btn" onclick="hideDonatePanel()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div class="donate-tier tier-vip" onclick="selectTier('vip')">
            <h4>🌟 VIP</h4>
            <div class="tier-price">299 ₽</div>
            <ul class="tier-features">
                <li>🌈 Цветные сообщения</li>
                <li>👑 Специальный значок VIP</li>
                <li>💬 Уникальные стикеры</li>
                <li>⚡ Приоритетная поддержка</li>
            </ul>
            <button class="btn btn-vip">Выбрать VIP</button>
        </div>

        <div class="donate-tier tier-premium" onclick="selectTier('premium')">
            <h4>💫 Premium</h4>
            <div class="tier-price">599 ₽</div>
            <ul class="tier-features">
                <li>✅ Все функции VIP</li>
                <li>🎨 Расширенные темы</li>
                <li>📊 Статистика профиля</li>
                <li>🔒 Приватные чаты</li>
                <li>🎮 Игровые режимы</li>
            </ul>
            <button class="btn btn-premium">Выбрать Premium</button>
        </div>

        <div class="donate-tier tier-ultra" onclick="selectTier('ultra')">
            <h4>🚀 Ultra</h4>
            <div class="tier-price">999 ₽</div>
            <ul class="tier-features">
                <li>✅ Все функции Premium</li>
                <li>🤖 AI-ассистент</li>
                <li>🌐 Неограниченное облако</li>
                <li>🎯 Кастомные команды</li>
                <li>⚡ Максимальная скорость</li>
            </ul>
            <button class="btn btn-ultra">Выбрать Ultra</button>
        </div>

        <div class="donate-tier tier-moder" onclick="selectTier('moder')">
            <h4>🛡️ Moder</h4>
            <div class="tier-price">1499 ₽</div>
            <ul class="tier-features">
                <li>✅ Все функции Ultra</li>
                <li>🔧 Модераторские права</li>
                <li>📢 Анонсы сообществу</li>
                <li>👀 Скрытый онлайн-статус</li>
                <li>💾 Резервные копии</li>
            </ul>
            <button class="btn btn-moder">Выбрать Moder</button>
        </div>

        <div class="donate-tier tier-chromek" onclick="selectTier('chromek')">
            <h4>🌈 Chromek</h4>
            <div class="tier-price">2499 ₽</div>
            <ul class="tier-features">
                <li>✅ Все функции Moder</li>
                <li>🌈 Радужные сообщения</li>
                <li>🎪 Анимации премиум-класса</li>
                <li>🔮 Эксклюзивные функции</li>
                <li>⭐ Пожизненный доступ</li>
            </ul>
            <button class="btn btn-chromek">Выбрать Chromek</button>
        </div>

        <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <h4>📞 Для покупки</h4>
            <p style="margin: 10px 0; color: var(--text-secondary);">
                Напишите в Telegram канал:<br>
                <strong style="color: var(--neon);">@trollex_official</strong>
            </p>
            <p style="font-size: 0.9rem; color: var(--text-secondary);">
                Укажите ваш ID и выбранный тариф
            </p>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h3 style="margin: 0;">⚙️ Settings</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="font-size: 1.5rem;">✕</button>
        </div>
        
        <div class="setting-item">
            <label class="setting-label">👤 Display Name</label>
            <input type="text" class="setting-input" id="settingsName" placeholder="Enter new name">
        </div>

        <div class="setting-item">
            <label class="setting-label">📧 Email</label>
            <input type="email" class="setting-input" id="settingsEmail" placeholder="Enter email">
        </div>

        <div class="setting-item">
            <label class="setting-label">🔔 Notifications</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsNotifications">
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">🌙 Dark Mode</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsDarkMode" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">💾 Auto-save</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsAutoSave" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div style="margin-bottom: 25px;">
            <h4 style="margin-bottom: 12px; color: var(--text-secondary);">Profile Info</h4>
            <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                <div>🆔 ID: <span id="settingsUserId">-</span></div>
                <div>📅 Registered: <span id="settingsUserRegDate">-</span></div>
                <div>💎 Premium: <span id="settingsUserPremium">None</span></div>
                <div>💾 Storage: <span id="settingsStorage">0</span> messages</div>
            </div>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()" style="margin-bottom: 12px;">💾 Save Settings</button>
        <button class="btn btn-secondary" onclick="exportData()">📤 Export Data</button>
        <button class="btn btn-secondary" onclick="clearAllData()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 8px;">
            🗑️ Clear All Data
        </button>
    </div>

    <!-- Подтверждение выхода -->
    <div id="logoutConfirm" class="screen hidden" style="background: rgba(10, 10, 42, 0.95); z-index: 4000;">
        <div class="cosmic-card">
            <h3 style="margin-bottom: 20px; text-align: center;">🚪 Confirm Logout</h3>
            <p style="text-align: center; margin-bottom: 25px; color: var(--text-secondary);">
                Your data will be saved securely.<br>
                You can return anytime!
            </p>
            <button class="btn btn-primary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger);">
                ✅ Logout
            </button>
            <button class="btn btn-secondary" onclick="hideLogoutConfirm()">
                ❌ Cancel
            </button>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let currentUser = null;
        let currentTab = 'chats';
        let currentChat = null;
        let messages = {};
        let allUsers = [];
        let friends = [];
        let groups = [];
        let editingMessageId = null;
        let typingTimer = null;
        let emojiPickerVisible = false;

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            updateNewYearCountdown();
            setInterval(updateNewYearCountdown, 60000);
            
            // Инициализация emoji picker
            initEmojiPicker();
            
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 3000);
        });

        function updateNewYearCountdown() {
            const now = new Date();
            const newYear = new Date(now.getFullYear() + 1, 0, 1);
            const diff = newYear - now;
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            
            document.getElementById('newYearCountdown').textContent = `${days} days`;
            document.getElementById('sidebarCountdown').textContent = `${days} days`;
        }

        function hideLoadingScreen() {
            document.getElementById('loadingScreen').classList.add('hidden');
        }

        function showWelcomeScreen() {
            showScreen('welcomeScreen');
        }

        function showRegisterScreen() {
            showScreen('registerScreen');
            generateNewUser();
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.add('hidden');
            });
            document.getElementById('mainApp').classList.add('hidden');
            const targetScreen = document.getElementById(screenId);
            if (targetScreen) {
                targetScreen.classList.remove('hidden');
            }
        }

        function generateNewUser() {
            const name = generateUsername();
            const email = generateEmail(name);
            const userId = generateUserId();
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌', '🌟', '⭐', '☄️', '🌠', '🪐'];
            
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
            document.getElementById('registerEmail').textContent = email;
        }

        function generateUsername() {
            const adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha'];
            const nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther'];
            const numbers = Math.floor(Math.random() * 9000) + 1000;
            return `${adjectives[Math.floor(Math.random() * adjectives.length)]}_${nouns[Math.floor(Math.random() * nouns.length)]}${numbers}`;
        }

        function generateEmail(username) {
            const domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net'];
            return `${username.toLowerCase()}@${domains[Math.floor(Math.random() * domains.length)]}`;
        }

        function generateUserId() {
            return 'user_' + Math.random().toString(36).substr(2, 9).toUpperCase();
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
                premium: 'none',
                settings: {
                    notifications: true,
                    darkMode: true,
                    autoSave: true,
                    theme: 'cosmic'
                },
                created_at: new Date().toISOString()
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            localStorage.setItem('userMessages', JSON.stringify(messages));
            
            // Создаем тестовых пользователей
            initializeSampleUsers();
            
            showMainApp();
            showNotification('Profile created successfully! 🎉', 'success');
        }

        function initializeSampleUsers() {
            // Создаем разнообразных тестовых пользователей
            allUsers = [
                {id: 'user1', name: 'Alex_Quantum', avatar: '👨‍💻', online: true, username: 'alex_quantum', premium: 'vip'},
                {id: 'user2', name: 'Sarah_Cyber', avatar: '👩‍🎨', online: true, username: 'sarah_cyber', premium: 'premium'},
                {id: 'user3', name: 'Mike_Neon', avatar: '👨‍🚀', online: false, username: 'mike_neon', premium: 'none'},
                {id: 'user4', name: 'Emma_Digital', avatar: '👩‍💼', online: true, username: 'emma_digital', premium: 'ultra'},
                {id: 'user5', name: 'Tom_Hyper', avatar: '🧑‍🔬', online: false, username: 'tom_hyper', premium: 'none'},
                {id: 'user6', name: 'Lisa_Virtual', avatar: '👩‍🔧', online: true, username: 'lisa_virtual', premium: 'moder'},
                {id: 'user7', name: 'John_Alpha', avatar: '👨‍🎓', online: true, username: 'john_alpha', premium: 'chromek'},
                {id: 'user8', name: 'Anna_Mega', avatar: '👩‍🍳', online: false, username: 'anna_mega', premium: 'none'}
            ];
            
            // Добавляем текущего пользователя в список
            allUsers.push({
                id: currentUser.id,
                name: currentUser.name,
                avatar: currentUser.avatar,
                online: true,
                username: currentUser.name.toLowerCase().replace(' ', '_'),
                premium: currentUser.premium
            });
            
            localStorage.setItem('allUsers', JSON.stringify(allUsers));
            
            // Создаем тестовые группы
            groups = [
                {id: 'group1', name: 'Quantum_Coders', avatar: '👨‍💻', members: 12, online: 8},
                {id: 'group2', name: 'Cosmic_Designers', avatar: '🎨', members: 7, online: 3},
                {id: 'group3', name: 'AI_Researchers', avatar: '🧠', members: 15, online: 5}
            ];
            
            localStorage.setItem('userGroups', JSON.stringify(groups));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedMessages = localStorage.getItem('userMessages');
                const savedAllUsers = localStorage.getItem('allUsers');
                const savedGroups = localStorage.getItem('userGroups');
                
                if (savedMessages) messages = JSON.parse(savedMessages);
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                if (savedGroups) groups = JSON.parse(savedGroups);
                
                showMainApp();
                showNotification('Welcome back to TrollexDL! 🚀', 'success');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedMessages = localStorage.getItem('userMessages');
                const savedAllUsers = localStorage.getItem('allUsers');
                const savedGroups = localStorage.getItem('userGroups');
                
                if (savedMessages) messages = JSON.parse(savedMessages);
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                if (savedGroups) groups = JSON.parse(savedGroups);
                
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
            document.getElementById('userId').textContent = currentUser.id;
            
            // Показываем бейдж премиума если есть
            updatePremiumBadge();
            
            // Заполняем настройки
            loadSettings();
            
            loadContent();
            updateOnlineUsers();
        }

        function updatePremiumBadge() {
            const badge = document.getElementById('userPremiumBadge');
            if (currentUser.premium && currentUser.premium !== 'none') {
                badge.textContent = currentUser.premium.toUpperCase();
                badge.classList.remove('hidden');
                
                // Добавляем специальный класс для премиум пользователей
                if (currentUser.premium === 'chromek') {
                    badge.style.background = 'linear-gradient(45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #8000ff, #ff00ff)';
                }
            } else {
                badge.classList.add('hidden');
            }
        }

        function loadSettings() {
            if (currentUser.settings) {
                document.getElementById('settingsName').value = currentUser.name;
                document.getElementById('settingsEmail').value = currentUser.email;
                document.getElementById('settingsNotifications').checked = currentUser.settings.notifications;
                document.getElementById('settingsDarkMode').checked = currentUser.settings.darkMode;
                document.getElementById('settingsAutoSave').checked = currentUser.settings.autoSave;
            }
            document.getElementById('settingsUserId').textContent = currentUser.id;
            document.getElementById('settingsUserRegDate').textContent = new Date(currentUser.created_at).toLocaleDateString();
            document.getElementById('settingsUserPremium').textContent = currentUser.premium.charAt(0).toUpperCase() + currentUser.premium.slice(1);
            updateStorageInfo();
        }

        function updateStorageInfo() {
            const totalMessages = Object.values(messages).reduce((acc, msgs) => acc + msgs.length, 0);
            document.getElementById('settingsStorage').textContent = totalMessages;
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Меняем placeholder поиска в зависимости от вкладки
            const searchInput = document.getElementById('searchInput');
            if (tabName === 'users') {
                searchInput.placeholder = '🔍 Search users by name or username...';
            } else if (tabName === 'groups') {
                searchInput.placeholder = '🔍 Search groups...';
            } else {
                searchInput.placeholder = '🔍 Search chats...';
            }
            
            loadContent();
        }

        function loadContent() {
            const contentList = document.getElementById('contentList');
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            let contentHTML = '';
            
            if (currentTab === 'chats') {
                contentHTML = getChatsContent(searchTerm);
            } else if (currentTab === 'users') {
                contentHTML = getUsersContent(searchTerm);
            } else if (currentTab === 'groups') {
                contentHTML = getGroupsContent(searchTerm);
            }
            
            contentList.innerHTML = contentHTML;
        }

        function searchUsers() {
            loadContent();
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 'support', name: 'Trollex Support', avatar: '🛰️', lastMessage: 'How can we help?', online: true},
                {id: 'updates', name: 'System Updates', avatar: '🔧', lastMessage: 'Latest features available', online: true},
                {id: 'community', name: 'Community Chat', avatar: '👥', lastMessage: 'Welcome to TrollexDL!', online: true}
            ];
            
            const filteredChats = chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">💬 No chats found</div>';
            }
            
            return filteredChats.map(chat => `
                <div class="chat-item ${currentChat?.id === chat.id ? 'active' : ''}" onclick="openChat('${chat.id}')">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.85rem;">${chat.lastMessage}</div>
                    </div>
                    ${chat.online ? '<div class="online-dot"></div>' : ''}
                </div>
            `).join('');
        }

        function getUsersContent(searchTerm) {
            // Фильтруем пользователей по имени и username, исключая текущего пользователя
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && 
                (user.name.toLowerCase().includes(searchTerm) || 
                 (user.username && user.username.toLowerCase().includes(searchTerm)))
            );
            
            if (filteredUsers.length === 0) {
                return '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">👥 No users found</div>';
            }
            
            return filteredUsers.map(user => {
                const isFriend = friends.some(f => f.id === user.id);
                return `
                    <div class="chat-item">
                        <div class="item-avatar">${user.avatar}</div>
                        <div style="flex: 1;">
                            <div style="font-weight: bold;">${user.name}</div>
                            <div style="color: ${user.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.85rem;">
                                @${user.username} • ${user.online ? '● Online' : '○ Offline'}
                                ${user.premium !== 'none' ? `<span style="color: var(--${user.premium}); margin-left: 5px;">⭐</span>` : ''}
                            </div>
                        </div>
                        <div style="display: flex; gap: 5px;">
                            <button onclick="startChatWithUser('${user.id}')" style="background: var(--accent); color: white; border: none; border-radius: 6px; padding: 6px 10px; cursor: pointer; font-size: 0.8rem;">💬</button>
                            <button onclick="${isFriend ? `removeFriend('${user.id}')` : `addFriend('${user.id}')`}" 
                                    style="background: ${isFriend ? 'var(--danger)' : 'var(--success)'}; color: white; border: none; border-radius: 6px; padding: 6px 10px; cursor: pointer; font-size: 0.8rem;">
                                ${isFriend ? '❌' : '➕'}
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function getGroupsContent(searchTerm) {
            const filteredGroups = groups.filter(group => 
                group.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredGroups.length === 0) {
                return '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">👨‍👩‍👧‍👦 No groups found</div>';
            }
            
            return filteredGroups.map(group => `
                <div class="chat-item" onclick="openGroup('${group.id}')">
                    <div class="item-avatar">${group.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${group.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.85rem;">
                            ${group.members} members • ${group.online} online
                        </div>
                    </div>
                </div>
            `).join('') + `
                <div class="chat-item" onclick="showCreateGroupDialog()" style="justify-content: center; background: rgba(107, 43, 217, 0.2); border-color: var(--accent);">
                    <div style="font-weight: bold; color: var(--accent);">+ Create Group</div>
                </div>
            `;
        }

        function updateOnlineUsers() {
            const onlineUsers = allUsers.filter(user => user.online && user.id !== currentUser.id);
            const onlineUsersList = document.getElementById('onlineUsersList');
            
            if (onlineUsers.length === 0) {
                onlineUsersList.innerHTML = '<div style="color: var(--text-secondary); font-size: 0.9rem; text-align: center;">No users online</div>';
                return;
            }
            
            onlineUsersList.innerHTML = onlineUsers.slice(0, 5).map(user => `
                <div class="online-user" onclick="startChatWithUser('${user.id}')">
                    <div style="width: 8px; height: 8px; background: var(--success); border-radius: 50%; margin-right: 8px;"></div>
                    <div style="font-size: 0.9rem;">${user.name}</div>
                </div>
            `).join('');
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Trollex Support', avatar: '🛰️', status: 'online'},
                'updates': {name: 'System Updates', avatar: '🔧', status: 'online'},
                'community': {name: 'Community Chat', avatar: '👥', status: 'online'}
            };
            
            const chat = chats[chatId];
            if (chat) {
                currentChat = {...chat, id: chatId};
                
                document.getElementById('currentChatName').textContent = chat.name;
                document.getElementById('currentChatAvatar').textContent = chat.avatar;
                document.getElementById('currentChatStatus').textContent = chat.status;
                
                loadContent();
                showChatMessages(chatId);
            }
        }

        function startChatWithUser(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user) {
                const chatId = `user_${userId}`;
                currentChat = {
                    id: chatId,
                    name: user.name,
                    avatar: user.avatar,
                    status: user.online ? 'online' : 'offline',
                    type: 'user'
                };
                
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? 'online' : 'offline';
                
                showChatMessages(chatId);
                showNotification(`Started chat with ${user.name} 💬`, 'success');
            }
        }

        function addFriend(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user && !friends.some(f => f.id === userId)) {
                friends.push(user);
                localStorage.setItem('userFriends', JSON.stringify(friends));
                loadContent();
                showNotification(`Added ${user.name} as friend! 👥`, 'success');
                
                // Анимация добавления
                createRippleEffect(event);
            }
        }

        function removeFriend(userId) {
            if (confirm('Remove this friend?')) {
                friends = friends.filter(f => f.id !== userId);
                localStorage.setItem('userFriends', JSON.stringify(friends));
                loadContent();
                showNotification('Friend removed 👋', 'info');
            }
        }

        function openGroup(groupId) {
            const group = groups.find(g => g.id === groupId);
            if (group) {
                currentChat = {
                    id: groupId,
                    name: group.name,
                    avatar: group.avatar,
                    status: `${group.online}/${group.members} online`,
                    type: 'group'
                };
                
                document.getElementById('currentChatName').textContent = group.name;
                document.getElementById('currentChatAvatar').textContent = group.avatar;
                document.getElementById('currentChatStatus').textContent = `${group.online}/${group.members} online`;
                
                showChatMessages(groupId);
            }
        }

        function showCreateGroupDialog() {
            const groupName = prompt('Enter group name:');
            if (groupName && groupName.trim()) {
                const newGroup = {
                    id: 'group_' + Date.now(),
                    name: groupName.trim(),
                    avatar: '👨‍👩‍👧‍👦',
                    members: 1,
                    online: 1
                };
                groups.push(newGroup);
                localStorage.setItem('userGroups', JSON.stringify(groups));
                loadContent();
                showNotification('Group created! 🎉', 'success');
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const chatMessages = messages[chatId] || getDefaultMessages(chatId);
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = getWelcomeMessage(chatId);
            } else {
                messagesContainer.innerHTML = chatMessages.map(msg => {
                    const isPremium = msg.premium && msg.premium !== 'none';
                    const reactionsHTML = msg.reactions ? Object.entries(msg.reactions).map(([emoji, count]) => 
                        `<span class="reaction" onclick="addReaction('${msg.id}', '${emoji}')">${emoji} ${count}</span>`
                    ).join('') : '';
                    
                    return `
                        <div class="message ${msg.sender} ${isPremium ? 'message-premium' : ''}" data-message-id="${msg.id}" oncontextmenu="showMessageContextMenu(event, '${msg.id}')">
                            ${isPremium ? `⭐ ${msg.text}` : msg.text}
                            ${msg.edited ? '<span class="message-edited">(edited)</span>' : ''}
                            <div class="message-actions">
                                ${msg.sender === 'sent' ? `
                                    <button class="message-action" onclick="editMessage('${msg.id}')">✏️</button>
                                    <button class="message-action" onclick="deleteMessage('${msg.id}')">🗑️</button>
                                ` : ''}
                                <button class="message-action" onclick="showReactionPicker('${msg.id}')">😊</button>
                                ${msg.views ? `<button class="message-action">👁️ ${msg.views}</button>` : ''}
                            </div>
                            ${reactionsHTML ? `<div class="message-reactions">${reactionsHTML}</div>` : ''}
                            <div class="message-time">${msg.time}</div>
                        </div>
                    `;
                }).join('');
            }
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function getDefaultMessages(chatId) {
            const defaults = {
                'support': [
                    {id: '1', text: 'Welcome to TrollexDL Support! 🚀', sender: 'received', time: '12:00', views: 1},
                    {id: '2', text: 'How can we assist you today?', sender: 'received', time: '12:01', views: 1}
                ],
                'community': [
                    {id: '1', text: 'Welcome to Community Chat! 👋', sender: 'received', time: '10:00', views: 15},
                    {id: '2', text: 'Anyone online? 🚀', sender: 'received', time: '10:05', views: 8, premium: 'vip'},
                    {id: '3', text: 'Testing new features! ⚡', sender: 'received', time: '10:10', views: 12, premium: 'premium'},
                    {id: '4', text: 'This app is amazing! 🌟', sender: 'received', time: '10:15', views: 20},
                    {id: '5', text: 'Join our premium program! 💎', sender: 'received', time: '10:20', views: 25, premium: 'ultra'}
                ]
            };
            return defaults[chatId] || [];
        }

        function getWelcomeMessage(chatId) {
            return `
                <div style="text-align: center; padding: 40px 15px; color: var(--text-secondary);">
                    <div style="font-size: 3rem; margin-bottom: 15px; animation: float 3s ease-in-out infinite;">💬</div>
                    <h3 style="margin-bottom: 12px;">${currentChat.name}</h3>
                    <p>Start conversation with quantum encryption</p>
                </div>
            `;
        }

        function handleTyping() {
            if (currentChat) {
                showTypingIndicator();
                
                clearTimeout(typingTimer);
                typingTimer = setTimeout(() => {
                    hideTypingIndicator();
                }, 1000);
            }
        }

        function showTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            const typingUser = document.getElementById('typingUser');
            
            if (currentChat.type === 'user') {
                typingUser.textContent = currentChat.name;
            } else {
                typingUser.textContent = 'Someone';
            }
            
            indicator.classList.remove('hidden');
        }

        function hideTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            indicator.classList.add('hidden');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && currentChat) {
                if (editingMessageId) {
                    editExistingMessage(editingMessageId, message);
                } else {
                    createNewMessage(message);
                }
                
                input.value = '';
                editingMessageId = null;
                hideTypingIndicator();
                hideEmojiPicker();
            }
        }

        function createNewMessage(message) {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const messageId = 'msg_' + Date.now();
            const isPremium = currentUser.premium && currentUser.premium !== 'none';
            
            const messageElement = document.createElement('div');
            messageElement.className = `message sent ${isPremium ? 'message-premium' : ''}`;
            messageElement.setAttribute('data-message-id', messageId);
            messageElement.setAttribute('oncontextmenu', `showMessageContextMenu(event, '${messageId}')`);
            messageElement.innerHTML = `
                ${isPremium ? `⭐ ${message}` : message}
                <div class="message-actions">
                    <button class="message-action" onclick="editMessage('${messageId}')">✏️</button>
                    <button class="message-action" onclick="deleteMessage('${messageId}')">🗑️</button>
                    <button class="message-action" onclick="showReactionPicker('${messageId}')">😊</button>
                    <button class="message-action">👁️ 1</button>
                </div>
                <div class="message-time">${time}</div>
            `;
            
            if (!messages[currentChat.id] || messages[currentChat.id].length === 0) {
                messagesContainer.innerHTML = '';
            }
            
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Сохраняем сообщение
            if (!messages[currentChat.id]) {
                messages[currentChat.id] = [];
            }
            messages[currentChat.id].push({
                id: messageId,
                text: message,
                sender: 'sent',
                time: time,
                views: 1,
                premium: currentUser.premium,
                timestamp: new Date().toISOString()
            });
            
            saveData();
            showNotification('Message sent! ✨', 'success');
            
            // Имитация ответа
            if (currentChat.type === 'user' || currentChat.id === 'support' || currentChat.id === 'community') {
                setTimeout(() => {
                    if (currentChat) {
                        simulateReply();
                    }
                }, 1000 + Math.random() * 2000);
            }
        }

        function editMessage(messageId) {
            const message = messages[currentChat.id]?.find(m => m.id === messageId);
            if (message && message.sender === 'sent') {
                document.getElementById('messageInput').value = message.text;
                document.getElementById('messageInput').focus();
                editingMessageId = messageId;
                showNotification('Editing message... ✏️', 'info');
            }
        }

        function editExistingMessage(messageId, newText) {
            const messageIndex = messages[currentChat.id]?.findIndex(m => m.id === messageId);
            if (messageIndex > -1) {
                messages[currentChat.id][messageIndex].text = newText;
                messages[currentChat.id][messageIndex].edited = true;
                
                const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
                if (messageElement) {
                    const textElement = messageElement.querySelector('div:first-child');
                    const isPremium = messages[currentChat.id][messageIndex].premium && messages[currentChat.id][messageIndex].premium !== 'none';
                    textElement.innerHTML = (isPremium ? '⭐ ' : '') + newText + ' <span class="message-edited">(edited)</span>';
                }
                
                saveData();
                showNotification('Message updated! ✅', 'success');
            }
        }

        function deleteMessage(messageId) {
            if (confirm('Delete this message?')) {
                messages[currentChat.id] = messages[currentChat.id]?.filter(m => m.id !== messageId) || [];
                const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
                if (messageElement) {
                    messageElement.remove();
                }
                saveData();
                showNotification('Message deleted 🗑️', 'info');
            }
        }

        function showMessageContextMenu(event, messageId) {
            event.preventDefault();
            
            const message = messages[currentChat.id]?.find(m => m.id === messageId);
            if (!message) return;
            
            // Удаляем существующее контекстное меню
            const existingMenu = document.querySelector('.context-menu');
            if (existingMenu) existingMenu.remove();
            
            const menu = document.createElement('div');
            menu.className = 'context-menu';
            menu.style.left = event.pageX + 'px';
            menu.style.top = event.pageY + 'px';
            
            const menuItems = [
                {text: 'Copy Text', action: () => copyMessageText(messageId)},
                {text: 'Add Reaction', action: () => showReactionPicker(messageId)},
            ];
            
            if (message.sender === 'sent') {
                menuItems.push(
                    {text: 'Edit Message', action: () => editMessage(messageId)},
                    {text: 'Delete Message', action: () => deleteMessage(messageId)}
                );
            }
            
            menuItems.push({text: 'Reply', action: () => replyToMessage(messageId)});
            
            menu.innerHTML = menuItems.map(item => 
                `<div class="context-menu-item" onclick="${item.action.toString().replace(/"/g, '&quot;')}">${item.text}</div>`
            ).join('');
            
            document.body.appendChild(menu);
            
            // Закрываем меню при клике вне его
            setTimeout(() => {
                document.addEventListener('click', function closeMenu() {
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                });
            }, 100);
        }

        function copyMessageText(messageId) {
            const message = messages[currentChat.id]?.find(m => m.id === messageId);
            if (message) {
                navigator.clipboard.writeText(message.text);
                showNotification('Message copied! 📋', 'success');
            }
        }

        function replyToMessage(messageId) {
            const message = messages[currentChat.id]?.find(m => m.id === messageId);
            if (message) {
                document.getElementById('messageInput').value = `Replying to: ${message.text}`;
                document.getElementById('messageInput').focus();
                showNotification('Replying to message... ↩️', 'info');
            }
        }

        function showReactionPicker(messageId) {
            const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
            if (!messageElement) return;
            
            const rect = messageElement.getBoundingClientRect();
            
            // Удаляем существующий пикер реакций
            const existingPicker = document.querySelector('.reaction-picker');
            if (existingPicker) existingPicker.remove();
            
            const picker = document.createElement('div');
            picker.className = 'context-menu reaction-picker';
            picker.style.left = (rect.right - 150) + 'px';
            picker.style.top = (rect.top - 50) + 'px';
            
            const reactions = ['👍', '❤️', '😂', '😮', '😢', '😡', '🎉', '👏'];
            picker.innerHTML = reactions.map(emoji => 
                `<div class="context-menu-item" onclick="addReaction('${messageId}', '${emoji}')" style="font-size: 1.2rem;">${emoji}</div>`
            ).join('');
            
            document.body.appendChild(picker);
            
            // Закрываем пикер при клике вне его
            setTimeout(() => {
                document.addEventListener('click', function closePicker() {
                    picker.remove();
                    document.removeEventListener('click', closePicker);
                });
            }, 100);
        }

        function addReaction(messageId, emoji) {
            const messageIndex = messages[currentChat.id]?.findIndex(m => m.id === messageId);
            if (messageIndex > -1) {
                if (!messages[currentChat.id][messageIndex].reactions) {
                    messages[currentChat.id][messageIndex].reactions = {};
                }
                
                if (!messages[currentChat.id][messageIndex].reactions[emoji]) {
                    messages[currentChat.id][messageIndex].reactions[emoji] = 0;
                }
                
                messages[currentChat.id][messageIndex].reactions[emoji]++;
                saveData();
                showChatMessages(currentChat.id);
                showNotification(`Reacted with ${emoji}`, 'success');
            }
        }

        function initEmojiPicker() {
            const emojiPicker = document.getElementById('emojiPicker');
            const emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾'];
            
            emojiPicker.innerHTML = emojis.map(emoji => 
                `<div class="emoji" onclick="addEmojiToMessage('${emoji}')">${emoji}</div>`
            ).join('');
        }

        function toggleEmojiPicker() {
            const emojiPicker = document.getElementById('emojiPicker');
            emojiPickerVisible = !emojiPickerVisible;
            
            if (emojiPickerVisible) {
                emojiPicker.style.display = 'grid';
            } else {
                emojiPicker.style.display = 'none';
            }
        }

        function hideEmojiPicker() {
            const emojiPicker = document.getElementById('emojiPicker');
            emojiPicker.style.display = 'none';
            emojiPickerVisible = false;
        }

        function addEmojiToMessage(emoji) {
            const input = document.getElementById('messageInput');
            input.value += emoji;
            input.focus();
        }

        function showChatOptions() {
            if (!currentChat) return;
            
            const options = [
                {text: 'Clear Chat', action: () => clearChat()},
                {text: 'Export Chat', action: () => exportChat()},
                {text: 'Mute Notifications', action: () => muteChat()},
            ];
            
            // Удаляем существующее меню
            const existingMenu = document.querySelector('.context-menu');
            if (existingMenu) existingMenu.remove();
            
            const menu = document.createElement('div');
            menu.className = 'context-menu';
            menu.style.left = 'auto';
            menu.style.right = '15px';
            menu.style.top = '60px';
            
            menu.innerHTML = options.map(option => 
                `<div class="context-menu-item" onclick="${option.action.toString().replace(/"/g, '&quot;')}">${option.text}</div>`
            ).join('');
            
            document.body.appendChild(menu);
            
            // Закрываем меню при клике вне его
            setTimeout(() => {
                document.addEventListener('click', function closeMenu() {
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                });
            }, 100);
        }

        function clearChat() {
            if (confirm('Clear all messages in this chat?')) {
                messages[currentChat.id] = [];
                saveData();
                showChatMessages(currentChat.id);
                showNotification('Chat cleared 🗑️', 'info');
            }
        }

        function exportChat() {
            const chatMessages = messages[currentChat.id] || [];
            const chatData = {
                chat: currentChat,
                messages: chatMessages,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(chatData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `trollexdl_chat_${currentChat.name}_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            showNotification('Chat exported! 📤', 'success');
        }

        function muteChat() {
            showNotification('Chat notifications muted 🔕', 'info');
        }

        function simulateReply() {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const replyId = 'msg_' + Date.now();
            
            const replies = {
                'support': [
                    'Thanks for your message! How can we help? 🚀',
                    'We appreciate your feedback!',
                    'Our team will review your message shortly. 👨‍🚀'
                ],
                'user': [
                    'Hey! Thanks for reaching out! 👋',
                    'That sounds interesting! Tell me more...',
                    'I will get back to you soon! ⏰'
                ],
                'community': [
                    'Great message! 👍',
                    'Thanks for sharing! 💫',
                    'Welcome to the community! 🎉',
                    'Awesome! 🚀',
                    'Keep them coming! ⚡'
                ]
            };
            
            const chatReplies = replies[currentChat.type] || ['Thank you for your message!'];
            const replyText = chatReplies[Math.floor(Math.random() * chatReplies.length)];
            const randomUser = allUsers[Math.floor(Math.random() * (allUsers.length - 1))];
            const isPremium = randomUser.premium && randomUser.premium !== 'none';
            
            const replyElement = document.createElement('div');
            replyElement.className = `message received ${isPremium ? 'message-premium' : ''}`;
            replyElement.setAttribute('data-message-id', replyId);
            replyElement.setAttribute('oncontextmenu', `showMessageContextMenu(event, '${replyId}')`);
            replyElement.innerHTML = `
                ${isPremium ? `⭐ ${replyText}` : replyText}
                <div class="message-actions">
                    <button class="message-action" onclick="showReactionPicker('${replyId}')">😊</button>
                    <button class="message-action">👁️ 1</button>
                </div>
                <div class="message-time">${time}</div>
            `;
            
            messagesContainer.appendChild(replyElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            if (!messages[currentChat.id]) {
                messages[currentChat.id] = [];
            }
            messages[currentChat.id].push({
                id: replyId,
                text: replyText,
                sender: 'received',
                time: time,
                views: 1,
                premium: randomUser.premium,
                timestamp: new Date().toISOString()
            });
            
            saveData();
        }

        function createRippleEffect(event) {
            const btn = event.currentTarget;
            const circle = document.createElement('span');
            const diameter = Math.max(btn.clientWidth, btn.clientHeight);
            const radius = diameter / 2;
            
            circle.style.width = circle.style.height = `${diameter}px`;
            circle.style.left = `${event.clientX - btn.getBoundingClientRect().left - radius}px`;
            circle.style.top = `${event.clientY - btn.getBoundingClientRect().top - radius}px`;
            circle.classList.add('ripple');
            
            btn.appendChild(circle);
            
            setTimeout(() => {
                circle.remove();
            }, 600);
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function showDonatePanel() {
            document.getElementById('donatePanel').classList.add('active');
        }

        function hideDonatePanel() {
            document.getElementById('donatePanel').classList.remove('active');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
        }

        function selectTier(tier) {
            showNotification(`Selected ${tier.toUpperCase()} tier! Contact @trollex_official on Telegram for purchase. 💎`, 'success');
            // Здесь можно добавить логику обработки выбора тарифа
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            const newEmail = document.getElementById('settingsEmail').value.trim();
            
            if (newName && newName !== currentUser.name) {
                currentUser.name = newName;
                document.getElementById('userName').textContent = newName;
                
                // Обновляем имя в allUsers
                const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
                if (userIndex > -1) {
                    allUsers[userIndex].name = newName;
                    localStorage.setItem('allUsers', JSON.stringify(allUsers));
                }
                
                showNotification('Name updated! ✅', 'success');
            }
            
            if (newEmail && newEmail !== currentUser.email) {
                currentUser.email = newEmail;
                showNotification('Email updated! 📧', 'success');
            }
            
            currentUser.settings.notifications = document.getElementById('settingsNotifications').checked;
            currentUser.settings.darkMode = document.getElementById('settingsDarkMode').checked;
            currentUser.settings.autoSave = document.getElementById('settingsAutoSave').checked;
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            hideSettings();
            showNotification('Settings saved! ⚙️', 'success');
        }

        function exportData() {
            const data = {
                user: currentUser,
                messages: messages,
                friends: friends,
                groups: groups,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `trollexdl_backup_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            showNotification('Data exported! 📤', 'success');
        }

        function clearAllData() {
            if (confirm('Are you sure you want to clear ALL data? This cannot be undone!')) {
                localStorage.clear();
                showNotification('All data cleared 🗑️', 'info');
                setTimeout(() => {
                    location.reload();
                }, 1000);
            }
        }

        function saveData() {
            if (currentUser.settings.autoSave) {
                localStorage.setItem('userMessages', JSON.stringify(messages));
                updateStorageInfo();
            }
        }

        function showLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.remove('hidden');
        }

        function hideLogoutConfirm() {
            document.getElementById('logoutConfirm').classList.add('hidden');
        }

        function logout() {
            localStorage.removeItem('trollexUser');
            showWelcomeScreen();
            showNotification('See you soon in TrollexDL! 👋', 'info');
        }

        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            
            if (type === 'error') {
                notification.style.background = 'linear-gradient(135deg, var(--danger), #cc0000)';
            } else if (type === 'warning') {
                notification.style.background = 'linear-gradient(135deg, var(--warning), #ff8800)';
            }
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Добавляем ripple эффект ко всем кнопкам
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn') || e.target.closest('.btn')) {
                const btn = e.target.classList.contains('btn') ? e.target : e.target.closest('.btn');
                createRippleEffect({...e, currentTarget: btn});
            }
        });

        // Обработка Enter для отправки сообщений
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Закрытие сайдбара и настроек при клике вне их
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                sidebar.classList.remove('active');
            }
            
            const settingsPanel = document.getElementById('settingsPanel');
            if (settingsPanel.classList.contains('active') && 
                !settingsPanel.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                settingsPanel.classList.remove('active');
            }
            
            const donatePanel = document.getElementById('donatePanel');
            if (donatePanel.classList.contains('active') && 
                !donatePanel.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                donatePanel.classList.remove('active');
            }
            
            // Закрываем emoji picker при клике вне его
            const emojiPicker = document.getElementById('emojiPicker');
            if (emojiPickerVisible && !emojiPicker.contains(event.target) && !event.target.classList.contains('emoji-btn')) {
                hideEmojiPicker();
            }
        });

        // Адаптация для мобильных устройств
        function handleResize() {
            if (window.innerWidth > 768) {
                document.getElementById('sidebar').classList.remove('active');
            }
        }

        window.addEventListener('resize', handleResize);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    days_until_new_year = get_days_until_new_year()
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    data = request.json
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running', 
        'service': 'TrollexDL',
        'days_until_new_year': get_days_until_new_year()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL Premium запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
