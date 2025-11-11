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
    adjectives = ['Quantum', 'Neon', 'Cyber', 'Digital', 'Virtual', 'Hyper', 'Mega', 'Ultra', 'Super', 'Alpha', 'Cosmic', 'Galactic']
    nouns = ['Phoenix', 'Dragon', 'Wolf', 'Tiger', 'Eagle', 'Falcon', 'Shark', 'Lion', 'Hawk', 'Panther', 'Unicorn', 'Pegasus']
    numbers = random.randint(1000, 9999)
    return f"{random.choice(adjectives)}_{random.choice(nouns)}{numbers}"

def generate_email(username):
    domains = ['quantum.io', 'nebula.org', 'cosmic.com', 'trollex.ai', 'universe.net', 'galaxy.tech']
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
            --legend: #ff00ff;
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
            animation: cosmicShift 20s ease-in-out infinite;
            z-index: -1;
        }

        /* Анимации */
        @keyframes cosmicShift {
            0%, 100% { opacity: 0.6; transform: scale(1) rotate(0deg); }
            50% { opacity: 0.8; transform: scale(1.02) rotate(1deg); }
        }

        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes slideDown {
            from { transform: translateY(-30px); opacity: 0; }
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

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-10px) rotate(1deg); }
            66% { transform: translateY(-5px) rotate(-1deg); }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
        }

        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { transform: scale(1.05); opacity: 0.8; }
            70% { transform: scale(0.9); }
            100% { transform: scale(1); opacity: 1; }
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blinkCursor {
            0%, 100% { border-color: transparent; }
            50% { border-color: var(--neon); }
        }

        @keyframes ripple {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(4); opacity: 0; }
        }

        @keyframes shine {
            0% { background-position: -100px; }
            100% { background-position: 200px; }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes slideInLeft {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.1); }
            50% { transform: scale(1); }
            75% { transform: scale(1.05); }
        }

        /* Базовые стили */
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
            overflow-y: auto;
        }

        .hidden {
            display: none !important;
        }

        .cosmic-card {
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(20px);
            border: 2px solid var(--accent);
            border-radius: 25px;
            padding: 30px;
            width: 100%;
            max-width: 450px;
            animation: slideUp 0.6s ease-out, glow 4s infinite;
            position: relative;
            overflow: hidden;
        }

        .logo {
            font-size: 2.8rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(45deg, var(--neon), var(--accent-glow), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 3s infinite;
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
            border-radius: 15px;
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
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(107, 43, 217, 0.4);
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

        .btn-legend {
            background: linear-gradient(135deg, var(--legend), #ff66ff);
            color: white;
            animation: pulse 2s infinite;
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
            border-radius: 20px;
            margin: 15px 0;
            border: 1px solid var(--accent);
            text-align: center;
            animation: float 6s ease-in-out infinite;
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
            margin: 0 auto 12px;
            animation: pulse 3s ease-in-out infinite;
        }

        .premium-badge {
            background: linear-gradient(45deg, var(--vip), var(--premium), var(--ultra));
            color: black;
            padding: 6px 15px;
            border-radius: 25px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-top: 8px;
            display: inline-block;
            animation: shine 2s infinite linear;
            background-size: 200% 100%;
        }

        .legend-badge {
            background: linear-gradient(45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #8000ff, #ff00ff);
            color: white;
            padding: 6px 15px;
            border-radius: 25px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-top: 8px;
            display: inline-block;
            animation: shine 1s infinite linear;
            background-size: 400% 100%;
        }

        .app {
            width: 100%;
            height: 100vh;
            background: var(--primary);
            display: flex;
        }

        .sidebar {
            width: 100%;
            max-width: 380px;
            background: rgba(26, 26, 74, 0.95);
            backdrop-filter: blur(15px);
            border-right: 2px solid var(--accent);
            display: flex;
            flex-direction: column;
            animation: slideInLeft 0.4s ease-out;
        }

        .user-header {
            padding: 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            text-align: center;
            position: relative;
            animation: slideDown 0.5s ease-out;
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            background: var(--success);
            border-radius: 50%;
            position: absolute;
            top: 20px;
            right: 20px;
            border: 2px solid white;
            animation: pulse 2s infinite;
        }

        .new-year-countdown {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            margin: 15px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid var(--neon);
            animation: glow 4s infinite;
        }

        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 6px;
            margin: 15px;
            flex-wrap: wrap;
            gap: 4px;
        }

        .nav-tab {
            flex: 1;
            padding: 12px 8px;
            text-align: center;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 0.9rem;
            min-width: 60px;
            user-select: none;
            animation: fadeIn 0.5s ease-out;
        }

        .nav-tab.active {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            transform: scale(1.05);
        }

        .search-box {
            padding: 15px;
        }

        .search-input {
            width: 100%;
            padding: 14px 18px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 15px;
            color: var(--text);
            font-size: 0.95rem;
            transition: all 0.3s ease;
            animation: slideUp 0.6s ease-out;
        }

        .search-input:focus {
            box-shadow: 0 0 25px rgba(107, 43, 217, 0.5);
            transform: scale(1.02);
        }

        .content-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .chat-item {
            display: flex;
            align-items: center;
            padding: 16px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            animation: slideUp 0.5s ease-out;
            position: relative;
        }

        .chat-item:hover, .chat-item.active {
            background: rgba(107, 43, 217, 0.25);
            border-color: var(--accent);
            transform: translateX(5px) scale(1.02);
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
            font-size: 1.3rem;
            animation: bounceIn 0.5s ease-out;
        }

        .online-dot {
            width: 12px;
            height: 12px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--success);
            margin-left: auto;
            animation: pulse 2s infinite;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--primary);
            animation: slideInRight 0.4s ease-out;
        }

        .chat-header {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 15px;
            animation: slideDown 0.4s ease-out;
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
            max-width: 80%;
            padding: 15px 18px;
            border-radius: 20px;
            position: relative;
            animation: slideUp 0.4s ease-out;
            transition: all 0.3s ease;
        }

        .message:hover {
            transform: scale(1.02);
        }

        .message.received {
            background: rgba(107, 43, 217, 0.25);
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
            animation: glow 3s infinite, bounceIn 0.5s ease-out;
        }

        .message-legend {
            border: 2px solid var(--legend);
            background: linear-gradient(135deg, rgba(255, 0, 255, 0.3), rgba(139, 92, 246, 0.4));
            animation: glow 2s infinite, heartbeat 2s ease-in-out infinite;
        }

        .message-actions {
            position: absolute;
            top: -30px;
            right: 0;
            background: rgba(26, 26, 74, 0.95);
            border: 1px solid var(--accent);
            border-radius: 10px;
            display: none;
            gap: 5px;
            padding: 8px;
            backdrop-filter: blur(10px);
            animation: slideDown 0.2s ease-out;
        }

        .message:hover .message-actions {
            display: flex;
        }

        .message-action {
            background: none;
            border: none;
            color: var(--text);
            padding: 6px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s ease;
        }

        .message-action:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: scale(1.1);
        }

        .message-time {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-top: 6px;
            text-align: right;
        }

        .message-input-container {
            padding: 20px;
            background: rgba(26, 26, 74, 0.9);
            border-top: 2px solid var(--accent);
            display: flex;
            gap: 12px;
            align-items: center;
            animation: slideUp 0.5s ease-out;
        }

        .message-input {
            flex: 1;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 25px;
            color: var(--text);
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .message-input:focus {
            box-shadow: 0 0 30px rgba(107, 43, 217, 0.6);
            transform: scale(1.02);
        }

        .send-btn {
            padding: 15px 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            animation: pulse 2s infinite;
        }

        .send-btn:active {
            transform: scale(0.95);
            animation: none;
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 10px 15px;
            background: rgba(107, 43, 217, 0.25);
            border-radius: 15px;
            margin: 10px 20px;
            align-self: flex-start;
            animation: pulse 1.5s infinite, slideUp 0.3s ease-out;
        }

        .typing-dots {
            display: flex;
            margin-left: 10px;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: var(--neon);
            border-radius: 50%;
            margin: 0 3px;
            animation: typingBounce 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }

        /* Панели */
        .panel {
            position: fixed;
            top: 0;
            width: 100%;
            max-width: 450px;
            height: 100%;
            background: rgba(26, 26, 74, 0.98);
            backdrop-filter: blur(25px);
            z-index: 500;
            transition: transform 0.4s ease;
            padding: 25px;
            overflow-y: auto;
        }

        .settings-panel {
            right: -100%;
            border-left: 3px solid var(--accent);
            animation: slideInRight 0.4s ease-out;
        }

        .settings-panel.active {
            right: 0;
        }

        .donate-panel {
            left: -100%;
            border-right: 3px solid var(--accent);
            animation: slideInLeft 0.4s ease-out;
        }

        .donate-panel.active {
            left: 0;
        }

        .donate-tier {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 20px;
            border: 2px solid;
            text-align: center;
            transition: all 0.4s ease;
            cursor: pointer;
            animation: slideUp 0.6s ease-out;
        }

        .donate-tier:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        }

        .tier-vip { border-color: var(--vip); }
        .tier-premium { border-color: var(--premium); }
        .tier-ultra { border-color: var(--ultra); }
        .tier-moder { border-color: var(--moder); }
        .tier-chromek { border-color: var(--chromek); }
        .tier-legend { 
            border-color: var(--legend);
            animation: glow 3s infinite, pulse 2s ease-in-out infinite;
        }

        .tier-price {
            font-size: 1.8rem;
            font-weight: bold;
            margin: 15px 0;
            animation: pulse 3s infinite;
        }

        .tier-features {
            text-align: left;
            margin: 20px 0;
            font-size: 0.95rem;
        }

        .tier-features li {
            margin: 8px 0;
            padding-left: 15px;
            animation: fadeIn 0.5s ease-out;
        }

        .setting-item {
            margin-bottom: 25px;
            animation: slideUp 0.5s ease-out;
        }

        .setting-label {
            display: block;
            margin-bottom: 8px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 1rem;
        }

        .setting-input, .setting-select {
            width: 100%;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--accent);
            border-radius: 12px;
            color: var(--text);
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        .setting-input:focus, .setting-select:focus {
            box-shadow: 0 0 20px rgba(107, 43, 217, 0.5);
        }

        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 30px;
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
            border-radius: 30px;
        }

        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 22px;
            width: 22px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
            animation: bounceIn 0.3s ease-out;
        }

        input:checked + .toggle-slider {
            background-color: var(--accent);
        }

        input:checked + .toggle-slider:before {
            transform: translateX(30px);
        }

        .notification {
            position: fixed;
            top: 25px;
            right: 25px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: white;
            padding: 15px 25px;
            border-radius: 15px;
            z-index: 4000;
            animation: slideInRight 0.3s ease, glow 2s infinite;
            border: 1px solid var(--accent);
            max-width: 350px;
            backdrop-filter: blur(10px);
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.4rem;
            cursor: pointer;
            padding: 10px;
            transition: all 0.3s ease;
            animation: pulse 3s infinite;
        }

        .mobile-menu-btn:active {
            transform: scale(0.9);
        }

        /* Адаптация для мобильных */
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                height: 100%;
                transform: translateX(-100%);
                transition: transform 0.4s ease;
                z-index: 300;
                max-width: 85%;
            }
            
            .sidebar.active {
                transform: translateX(0);
            }
            
            .panel {
                max-width: 100%;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .cosmic-card {
                padding: 25px;
                margin: 15px;
            }
            
            .nav-tabs {
                flex-wrap: nowrap;
                overflow-x: auto;
            }
            
            .nav-tab {
                min-width: 70px;
                font-size: 0.85rem;
                padding: 10px 6px;
            }
            
            .message {
                max-width: 90%;
            }

            .user-avatar {
                width: 70px;
                height: 70px;
                font-size: 1.8rem;
            }

            .btn {
                padding: 14px 18px;
                font-size: 0.95rem;
            }
        }

        @media (max-width: 480px) {
            .cosmic-card {
                padding: 20px;
            }
            
            .logo {
                font-size: 2.2rem;
            }
            
            .user-avatar {
                width: 60px;
                height: 60px;
                font-size: 1.6rem;
            }
            
            .message-input {
                padding: 12px 16px;
                font-size: 0.95rem;
            }
            
            .send-btn {
                padding: 12px 20px;
            }

            .donate-tier {
                padding: 20px;
            }

            .tier-price {
                font-size: 1.5rem;
            }
        }

        /* Дополнительные элементы */
        .theme-selector {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
        }

        .theme-option {
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .theme-option.active {
            border-color: var(--neon);
            transform: scale(1.05);
        }

        .theme-cosmic { background: linear-gradient(135deg, #0a0a2a, #1a1a4a); }
        .theme-dark { background: linear-gradient(135deg, #1a1a1a, #2d2d2d); }
        .theme-purple { background: linear-gradient(135deg, #2d1b69, #4a2c92); }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            animation: slideUp 0.6s ease-out;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: var(--neon);
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="cosmic-bg"></div>

    <!-- Экран загрузки -->
    <div id="loadingScreen" class="screen">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div class="typewriter-text">Quantum Connection Established...</div>
            <div style="margin-top: 30px; font-size: 2.5rem; animation: float 3s ease-in-out infinite, spin 4s linear infinite;">🌌</div>
            <div style="color: var(--text-secondary); margin-top: 25px; animation: slideUp 1s ease-out;">
                Secure • Fast • Cosmic • Premium
            </div>
        </div>
    </div>

    <!-- Главный экран -->
    <div id="welcomeScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">TrollexDL</div>
            <div style="text-align: center; color: var(--text-secondary); margin-bottom: 30px; line-height: 1.6;">
                Ultimate messaging experience with<br>
                quantum encryption and cosmic design
            </div>
            
            <button class="btn btn-primary" onclick="showRegisterScreen()">
                🚀 START QUANTUM JOURNEY
            </button>
            
            <button class="btn btn-secondary" onclick="quickStart()">
                ⚡ INSTANT QUANTUM LOGIN
            </button>

            <div class="new-year-countdown">
                🎄 Quantum Countdown: <span id="newYearCountdown">...</span> until New Year!
            </div>
        </div>
    </div>

    <!-- Регистрация -->
    <div id="registerScreen" class="screen hidden">
        <div class="cosmic-card">
            <div class="logo">Quantum Registration</div>
            
            <div class="user-card">
                <div class="user-avatar" id="registerAvatar">🚀</div>
                <h3 id="registerName">Quantum_User</h3>
                <p style="color: var(--text-secondary);">ID: <span id="registerId">...</span></p>
                <p style="color: var(--text-secondary); margin-top: 8px;">📧 <span id="registerEmail">...</span></p>
            </div>
            
            <button class="btn btn-primary" onclick="registerUser()">
                ✅ ACTIVATE QUANTUM PROFILE
            </button>
            
            <button class="btn btn-secondary" onclick="generateNewUser()">
                🔄 GENERATE QUANTUM IDENTITY
            </button>
            
            <button class="btn btn-secondary" onclick="showWelcomeScreen()">
                ← QUANTUM RETURN
            </button>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="mainApp" class="app hidden">
        <!-- Сайдбар -->
        <div class="sidebar" id="sidebar">
            <div class="user-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="user-avatar" id="userAvatar">🚀</div>
                <h3 id="userName">User</h3>
                <p style="opacity: 0.9;">ID: <span id="userId">...</span></p>
                <div class="status-indicator"></div>
                <div id="userPremiumBadge" class="premium-badge hidden">PREMIUM</div>
            </div>

            <div class="new-year-countdown">
                🎄 <span id="sidebarCountdown">...</span> until Quantum New Year!
            </div>

            <div class="nav-tabs">
                <div class="nav-tab active" onclick="switchTab('chats')">💬</div>
                <div class="nav-tab" onclick="switchTab('users')">👥</div>
                <div class="nav-tab" onclick="switchTab('groups')">👨‍👩‍👧‍👦</div>
                <div class="nav-tab" onclick="switchTab('donate')">💎</div>
                <div class="nav-tab" onclick="switchTab('settings')">⚙️</div>
            </div>

            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Quantum Search..." id="searchInput" oninput="searchContent()">
            </div>

            <div class="content-list" id="contentList">
                <!-- Контент загружается динамически -->
            </div>
        </div>

        <!-- Область чата -->
        <div class="chat-area">
            <div class="chat-header">
                <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
                <div class="item-avatar" id="currentChatAvatar">💬</div>
                <div style="flex: 1;">
                    <h3 id="currentChatName">TrollexDL Quantum</h3>
                    <p style="color: var(--text-secondary);" id="currentChatStatus">Select quantum channel</p>
                </div>
                <button class="mobile-menu-btn" onclick="showChatMenu()">⋮</button>
            </div>

            <div class="messages-container" id="messagesContainer">
                <div style="text-align: center; padding: 50px 20px; color: var(--text-secondary);">
                    <div style="font-size: 4rem; margin-bottom: 20px; animation: float 4s ease-in-out infinite;">🌌</div>
                    <h3 style="margin-bottom: 15px;">Welcome to Quantum TrollexDL!</h3>
                    <p>Begin your cosmic messaging journey</p>
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
                <input type="text" class="message-input" placeholder="Type your quantum message..." id="messageInput" oninput="handleTyping()">
                <button class="send-btn" onclick="sendMessage()">🚀</button>
            </div>
        </div>
    </div>

    <!-- Панель доната -->
    <div class="panel donate-panel" id="donatePanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
            <h3 style="margin: 0; background: linear-gradient(45deg, var(--vip), var(--premium)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">💎 Quantum Premium Tiers</h3>
            <button class="mobile-menu-btn" onclick="hideDonatePanel()" style="font-size: 1.6rem;">✕</button>
        </div>
        
        <div class="donate-tier tier-vip" onclick="selectTier('vip')">
            <h4>🌟 VIP ACCESS</h4>
            <div class="tier-price">299 ₽</div>
            <ul class="tier-features">
                <li>🌈 Quantum Color Messages</li>
                <li>👑 Exclusive VIP Badge</li>
                <li>💬 Premium Stickers</li>
                <li>⚡ Priority Support</li>
                <li>🎨 Custom Themes</li>
            </ul>
            <button class="btn btn-vip">ACTIVATE VIP</button>
        </div>

        <div class="donate-tier tier-premium" onclick="selectTier('premium')">
            <h4>💫 PREMIUM QUANTUM</h4>
            <div class="tier-price">599 ₽</div>
            <ul class="tier-features">
                <li>✅ All VIP Features</li>
                <li>🎨 Advanced Themes</li>
                <li>📊 Quantum Statistics</li>
                <li>🔒 Private Chats</li>
                <li>🎮 Game Modes</li>
                <li>🌙 Dark Mode Plus</li>
            </ul>
            <button class="btn btn-premium">UPGRADE TO PREMIUM</button>
        </div>

        <div class="donate-tier tier-ultra" onclick="selectTier('ultra')">
            <h4>🚀 ULTRA QUANTUM</h4>
            <div class="tier-price">999 ₽</div>
            <ul class="tier-features">
                <li>✅ All Premium Features</li>
                <li>🤖 AI Assistant</li>
                <li>🌐 Unlimited Cloud</li>
                <li>🎯 Custom Commands</li>
                <li>⚡ Maximum Speed</li>
                <li>🔮 Future Features Access</li>
            </ul>
            <button class="btn btn-ultra">GO ULTRA</button>
        </div>

        <div class="donate-tier tier-moder" onclick="selectTier('moder')">
            <h4>🛡️ MODER QUANTUM</h4>
            <div class="tier-price">1499 ₽</div>
            <ul class="tier-features">
                <li>✅ All Ultra Features</li>
                <li>🔧 Moderator Rights</li>
                <li>📢 Community Announcements</li>
                <li>👀 Stealth Mode</li>
                <li>💾 Backup Systems</li>
                <li>🎪 Special Effects</li>
            </ul>
            <button class="btn btn-moder">BECOME MODER</button>
        </div>

        <div class="donate-tier tier-chromek" onclick="selectTier('chromek')">
            <h4>🌈 CHROMEK QUANTUM</h4>
            <div class="tier-price">2499 ₽</div>
            <ul class="tier-features">
                <li>✅ All Moder Features</li>
                <li>🌈 Rainbow Messages</li>
                <li>🎪 Premium Animations</li>
                <li>🔮 Exclusive Functions</li>
                <li>⭐ Lifetime Access</li>
                <li>👑 Founder Status</li>
            </ul>
            <button class="btn btn-chromek">UNLOCK CHROMEK</button>
        </div>

        <div class="donate-tier tier-legend" onclick="selectTier('legend')">
            <h4>⚡ LEGEND QUANTUM</h4>
            <div class="tier-price">4999 ₽</div>
            <ul class="tier-features">
                <li>✅ All Chromek Features</li>
                <li>⚡ Legendary Status</li>
                <li>🎨 Ultimate Customization</li>
                <li>🤖 Advanced AI</li>
                <li>🌌 Cosmic Effects</li>
                <li>💫 Eternal Premium</li>
                <li>👑 Legend Badge</li>
            </ul>
            <button class="btn btn-legend">BECOME LEGEND</button>
        </div>

        <div style="text-align: center; margin-top: 25px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px;">
            <h4>📞 Quantum Purchase</h4>
            <p style="margin: 12px 0; color: var(--text-secondary);">
                Contact Quantum Support:<br>
                <strong style="color: var(--neon);">@trollex_official</strong>
            </p>
            <p style="font-size: 0.9rem; color: var(--text-secondary);">
                Provide your Quantum ID and selected tier
            </p>
        </div>
    </div>

    <!-- Панель настроек -->
    <div class="panel settings-panel" id="settingsPanel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
            <h3 style="margin: 0; background: linear-gradient(45deg, var(--accent), var(--neon)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚙️ Quantum Settings</h3>
            <button class="mobile-menu-btn" onclick="hideSettings()" style="font-size: 1.6rem;">✕</button>
        </div>
        
        <div class="setting-item">
            <label class="setting-label">👤 Quantum Name</label>
            <input type="text" class="setting-input" id="settingsName" placeholder="Enter quantum name">
        </div>

        <div class="setting-item">
            <label class="setting-label">📧 Quantum Email</label>
            <input type="email" class="setting-input" id="settingsEmail" placeholder="Enter quantum email">
        </div>

        <div class="setting-item">
            <label class="setting-label">🎨 Quantum Theme</label>
            <div class="theme-selector">
                <div class="theme-option theme-cosmic active" onclick="changeTheme('cosmic')">Cosmic</div>
                <div class="theme-option theme-dark" onclick="changeTheme('dark')">Dark</div>
                <div class="theme-option theme-purple" onclick="changeTheme('purple')">Purple</div>
            </div>
        </div>

        <div class="setting-item">
            <label class="setting-label">🔔 Quantum Notifications</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsNotifications" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">🌙 Quantum Dark Mode</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsDarkMode" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">💾 Quantum Auto-save</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsAutoSave" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="setting-item">
            <label class="setting-label">⚡ Quantum Animations</label>
            <label class="toggle-switch">
                <input type="checkbox" id="settingsAnimations" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="statMessages">0</div>
                <div>Quantum Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="statFriends">0</div>
                <div>Quantum Friends</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="statGroups">0</div>
                <div>Quantum Groups</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="statOnline">0</div>
                <div>Online Now</div>
            </div>
        </div>

        <button class="btn btn-primary" onclick="saveSettings()" style="margin-bottom: 12px;">💾 Save Quantum Settings</button>
        <button class="btn btn-secondary" onclick="exportData()">📤 Export Quantum Data</button>
        <button class="btn btn-secondary" onclick="clearCache()" style="margin-top: 8px;">🧹 Clear Quantum Cache</button>
        <button class="btn btn-secondary" onclick="logout()" style="background: rgba(255,68,68,0.2); color: var(--danger); border-color: var(--danger); margin-top: 8px;">
            🚪 Quantum Logout
        </button>
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
        let typingTimer = null;

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            updateNewYearCountdown();
            setInterval(updateNewYearCountdown, 60000);
            
            setTimeout(() => {
                hideLoadingScreen();
                checkAutoLogin();
            }, 2500);
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
            const avatars = ['🚀', '👨‍🚀', '👩‍🚀', '🛸', '🌌', '🌟', '⭐', '☄️', '🌠', '🪐'];
            
            document.getElementById('registerAvatar').textContent = avatars[Math.floor(Math.random() * avatars.length)];
            document.getElementById('registerName').textContent = name;
            document.getElementById('registerId').textContent = userId;
            document.getElementById('registerEmail').textContent = email;
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
                    animations: true,
                    theme: 'cosmic'
                },
                created_at: new Date().toISOString()
            };
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            initializeSampleUsers();
            
            showMainApp();
            showNotification('Quantum Profile Activated! 🎉', 'success');
        }

        function initializeSampleUsers() {
            allUsers = [
                {id: 'user1', name: 'Alex_Quantum', avatar: '👨‍💻', online: true, username: 'alex_quantum', premium: 'vip'},
                {id: 'user2', name: 'Sarah_Cyber', avatar: '👩‍🎨', online: true, username: 'sarah_cyber', premium: 'premium'},
                {id: 'user3', name: 'Mike_Neon', avatar: '👨‍🚀', online: false, username: 'mike_neon', premium: 'none'},
                {id: 'user4', name: 'Emma_Digital', avatar: '👩‍💼', online: true, username: 'emma_digital', premium: 'ultra'},
                {id: 'user5', name: 'Tom_Hyper', avatar: '🧑‍🔬', online: false, username: 'tom_hyper', premium: 'none'},
                {id: 'user6', name: 'Lisa_Virtual', avatar: '👩‍🔧', online: true, username: 'lisa_virtual', premium: 'moder'},
                {id: 'user7', name: 'John_Alpha', avatar: '👨‍🎓', online: true, username: 'john_alpha', premium: 'chromek'},
                {id: 'user8', name: 'Anna_Mega', avatar: '👩‍🍳', online: false, username: 'anna_mega', premium: 'none'},
                {id: 'user9', name: 'Max_Legend', avatar: '🦸', online: true, username: 'max_legend', premium: 'legend'}
            ];
            
            allUsers.push({
                id: currentUser.id,
                name: currentUser.name,
                avatar: currentUser.avatar,
                online: true,
                username: currentUser.name.toLowerCase().replace(' ', '_'),
                premium: currentUser.premium
            });
            
            localStorage.setItem('allUsers', JSON.stringify(allUsers));
            
            groups = [
                {id: 'group1', name: 'Quantum_Coders', avatar: '👨‍💻', members: 15, online: 8},
                {id: 'group2', name: 'Cosmic_Designers', avatar: '🎨', members: 12, online: 5},
                {id: 'group3', name: 'AI_Researchers', avatar: '🧠', members: 20, online: 12}
            ];
            
            localStorage.setItem('userGroups', JSON.stringify(groups));
        }

        function quickStart() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                const savedGroups = localStorage.getItem('userGroups');
                
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                if (savedGroups) groups = JSON.parse(savedGroups);
                
                showMainApp();
                showNotification('Quantum Reconnection Successful! 🚀', 'success');
            } else {
                showRegisterScreen();
            }
        }

        function checkAutoLogin() {
            const savedUser = localStorage.getItem('trollexUser');
            if (savedUser) {
                currentUser = JSON.parse(savedUser);
                const savedAllUsers = localStorage.getItem('allUsers');
                const savedGroups = localStorage.getItem('userGroups');
                
                if (savedAllUsers) allUsers = JSON.parse(savedAllUsers);
                if (savedGroups) groups = JSON.parse(savedGroups);
                
                showMainApp();
            } else {
                showWelcomeScreen();
            }
        }

        function showMainApp() {
            hideAllScreens();
            document.getElementById('mainApp').classList.remove('hidden');
            
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userAvatar').textContent = currentUser.avatar;
            document.getElementById('userId').textContent = currentUser.id;
            
            updatePremiumBadge();
            loadSettings();
            loadContent();
            updateStats();
        }

        function updatePremiumBadge() {
            const badge = document.getElementById('userPremiumBadge');
            if (currentUser.premium && currentUser.premium !== 'none') {
                badge.textContent = currentUser.premium.toUpperCase();
                badge.classList.remove('hidden');
                
                if (currentUser.premium === 'legend') {
                    badge.className = 'legend-badge';
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
                document.getElementById('settingsAnimations').checked = currentUser.settings.animations;
                
                // Активируем текущую тему
                document.querySelectorAll('.theme-option').forEach(option => {
                    option.classList.remove('active');
                });
                document.querySelector(`.theme-${currentUser.settings.theme}`).classList.add('active');
            }
        }

        function updateStats() {
            const totalMessages = Object.values(messages).reduce((acc, msgs) => acc + msgs.length, 0);
            const onlineUsers = allUsers.filter(user => user.online).length;
            
            document.getElementById('statMessages').textContent = totalMessages;
            document.getElementById('statFriends').textContent = friends.length;
            document.getElementById('statGroups').textContent = groups.length;
            document.getElementById('statOnline').textContent = onlineUsers;
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            if (tabName === 'donate') {
                showDonatePanel();
                return;
            } else if (tabName === 'settings') {
                showSettings();
                return;
            }
            
            const searchInput = document.getElementById('searchInput');
            if (tabName === 'users') {
                searchInput.placeholder = '🔍 Search quantum users...';
            } else if (tabName === 'groups') {
                searchInput.placeholder = '🔍 Search quantum groups...';
            } else {
                searchInput.placeholder = '🔍 Search quantum chats...';
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

        function searchContent() {
            loadContent();
        }

        function getChatsContent(searchTerm) {
            const chats = [
                {id: 'support', name: 'Quantum Support', avatar: '🛰️', lastMessage: 'How can we help?', online: true},
                {id: 'updates', name: 'System Updates', avatar: '🔧', lastMessage: 'New features available', online: true},
                {id: 'community', name: 'Quantum Community', avatar: '👥', lastMessage: 'Welcome to TrollexDL!', online: true}
            ];
            
            const filteredChats = chats.filter(chat => 
                chat.name.toLowerCase().includes(searchTerm)
            );
            
            if (filteredChats.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--text-secondary);">💬 No quantum chats found</div>';
            }
            
            return filteredChats.map(chat => `
                <div class="chat-item ${currentChat?.id === chat.id ? 'active' : ''}" onclick="openChat('${chat.id}')">
                    <div class="item-avatar">${chat.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${chat.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">${chat.lastMessage}</div>
                    </div>
                    ${chat.online ? '<div class="online-dot"></div>' : ''}
                </div>
            `).join('');
        }

        function getUsersContent(searchTerm) {
            const filteredUsers = allUsers.filter(user => 
                user.id !== currentUser.id && 
                (user.name.toLowerCase().includes(searchTerm) || 
                 user.username.toLowerCase().includes(searchTerm))
            );
            
            if (filteredUsers.length === 0) {
                return '<div style="text-align: center; padding: 40px; color: var(--text-secondary);">👥 No quantum users found</div>';
            }
            
            return filteredUsers.map(user => {
                const isFriend = friends.some(f => f.id === user.id);
                const badge = user.premium !== 'none' ? 
                    `<span style="color: var(--${user.premium}); margin-left: 5px;">${user.premium === 'legend' ? '⚡' : '⭐'}</span>` : '';
                
                return `
                    <div class="chat-item" onclick="startChatWithUser('${user.id}')">
                        <div class="item-avatar">${user.avatar}</div>
                        <div style="flex: 1;">
                            <div style="font-weight: bold;">${user.name} ${badge}</div>
                            <div style="color: ${user.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.9rem;">
                                @${user.username} • ${user.online ? '● Quantum Online' : '○ Quantum Offline'}
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button onclick="event.stopPropagation(); startChatWithUser('${user.id}')" 
                                    style="background: var(--accent); color: white; border: none; border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 0.85rem;">
                                💬
                            </button>
                            <button onclick="event.stopPropagation(); ${isFriend ? `removeFriend('${user.id}')` : `addFriend('${user.id}')`}" 
                                    style="background: ${isFriend ? 'var(--danger)' : 'var(--success)'}; color: white; border: none; border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 0.85rem;">
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
                return '<div style="text-align: center; padding: 40px; color: var(--text-secondary);">👨‍👩‍👧‍👦 No quantum groups found</div>';
            }
            
            return filteredGroups.map(group => `
                <div class="chat-item" onclick="openGroup('${group.id}')">
                    <div class="item-avatar">${group.avatar}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: bold;">${group.name}</div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">
                            ${group.members} quantum members • ${group.online} online
                        </div>
                    </div>
                </div>
            `).join('') + `
                <div class="chat-item" onclick="showCreateGroupDialog()" style="justify-content: center; background: rgba(107, 43, 217, 0.25); border-color: var(--accent);">
                    <div style="font-weight: bold; color: var(--accent);">+ Create Quantum Group</div>
                </div>
            `;
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Quantum Support', avatar: '🛰️', status: 'Quantum Online', type: 'support'},
                'updates': {name: 'System Updates', avatar: '🔧', status: 'Always Active', type: 'updates'},
                'community': {name: 'Quantum Community', avatar: '👥', status: '25 quantum users online', type: 'community'}
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
                    status: user.online ? 'Quantum Online' : 'Quantum Offline',
                    type: 'user'
                };
                
                document.getElementById('currentChatName').textContent = user.name;
                document.getElementById('currentChatAvatar').textContent = user.avatar;
                document.getElementById('currentChatStatus').textContent = user.online ? 'Quantum Online' : 'Quantum Offline';
                
                showChatMessages(chatId);
                showNotification(`Quantum connection established with ${user.name} 💬`, 'success');
            }
        }

        function addFriend(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (user && !friends.some(f => f.id === userId)) {
                friends.push(user);
                localStorage.setItem('userFriends', JSON.stringify(friends));
                loadContent();
                updateStats();
                showNotification(`Quantum friendship formed with ${user.name}! 👥`, 'success');
                createRippleEffect(event);
            }
        }

        function removeFriend(userId) {
            if (confirm('Remove this quantum friend?')) {
                friends = friends.filter(f => f.id !== userId);
                localStorage.setItem('userFriends', JSON.stringify(friends));
                loadContent();
                updateStats();
                showNotification('Quantum friend removed 👋', 'info');
            }
        }

        function openGroup(groupId) {
            const group = groups.find(g => g.id === groupId);
            if (group) {
                currentChat = {
                    id: groupId,
                    name: group.name,
                    avatar: group.avatar,
                    status: `${group.online}/${group.members} quantum users online`,
                    type: 'group'
                };
                
                document.getElementById('currentChatName').textContent = group.name;
                document.getElementById('currentChatAvatar').textContent = group.avatar;
                document.getElementById('currentChatStatus').textContent = `${group.online}/${group.members} quantum users online`;
                
                showChatMessages(groupId);
            }
        }

        function showCreateGroupDialog() {
            const groupName = prompt('Enter quantum group name:');
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
                updateStats();
                showNotification('Quantum group created! 🎉', 'success');
            }
        }

        function showChatMessages(chatId) {
            const messagesContainer = document.getElementById('messagesContainer');
            const defaultMessages = {
                'support': [
                    {id: '1', text: 'Welcome to Quantum TrollexDL Support! 🚀', sender: 'received', time: '12:00', views: 1},
                    {id: '2', text: 'How can we assist your quantum journey?', sender: 'received', time: '12:01', views: 1}
                ],
                'community': [
                    {id: '1', text: 'Welcome to Quantum Community! 👋', sender: 'received', time: '10:00', views: 25, senderName: 'Alex_Quantum', premium: 'vip'},
                    {id: '2', text: 'Anyone testing quantum features? 🚀', sender: 'received', time: '10:05', views: 18, senderName: 'Sarah_Cyber', premium: 'premium'},
                    {id: '3', text: 'This app is quantum amazing! ⚡', sender: 'received', time: '10:10', views: 32, senderName: 'Emma_Digital', premium: 'ultra'},
                    {id: '4', text: 'Join our quantum premium program! 💎', sender: 'received', time: '10:15', views: 45, senderName: 'Max_Legend', premium: 'legend'}
                ]
            };
            
            const chatMessages = messages[chatId] || defaultMessages[chatId] || [];
            
            if (chatMessages.length === 0) {
                messagesContainer.innerHTML = `
                    <div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">
                        <div style="font-size: 4rem; margin-bottom: 20px; animation: float 4s ease-in-out infinite;">💬</div>
                        <h3 style="margin-bottom: 15px;">${currentChat.name}</h3>
                        <p>Begin your quantum conversation</p>
                    </div>
                `;
            } else {
                messagesContainer.innerHTML = chatMessages.map(msg => {
                    const isPremium = msg.premium && msg.premium !== 'none';
                    const messageClass = `message ${msg.sender} ${isPremium ? (msg.premium === 'legend' ? 'message-legend' : 'message-premium') : ''}`;
                    
                    return `
                        <div class="${messageClass}" data-message-id="${msg.id}">
                            ${msg.senderName ? `<strong>${msg.senderName}:</strong> ` : ''}
                            ${msg.text}
                            <div class="message-actions">
                                ${msg.sender === 'sent' ? `
                                    <button class="message-action" onclick="editMessage('${msg.id}')">✏️</button>
                                    <button class="message-action" onclick="deleteMessage('${msg.id}')">🗑️</button>
                                ` : ''}
                                <button class="message-action" onclick="reactToMessage('${msg.id}')">😊</button>
                                ${msg.views ? `<button class="message-action">👁️ ${msg.views}</button>` : ''}
                            </div>
                            <div class="message-time">${msg.time}</div>
                        </div>
                    `;
                }).join('');
            }
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
                typingUser.textContent = 'Quantum User';
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
                const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                const messageId = 'msg_' + Date.now();
                const isPremium = currentUser.premium && currentUser.premium !== 'none';
                
                const messagesContainer = document.getElementById('messagesContainer');
                const messageElement = document.createElement('div');
                messageElement.className = `message sent ${isPremium ? (currentUser.premium === 'legend' ? 'message-legend' : 'message-premium') : ''}`;
                messageElement.setAttribute('data-message-id', messageId);
                messageElement.innerHTML = `
                    ${message}
                    <div class="message-actions">
                        <button class="message-action" onclick="editMessage('${messageId}')">✏️</button>
                        <button class="message-action" onclick="deleteMessage('${messageId}')">🗑️</button>
                        <button class="message-action" onclick="reactToMessage('${messageId}')">😊</button>
                        <button class="message-action">👁️ 1</button>
                    </div>
                    <div class="message-time">${time}</div>
                `;
                
                if (!messages[currentChat.id]) {
                    messagesContainer.innerHTML = '';
                }
                
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
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
                
                localStorage.setItem('userMessages', JSON.stringify(messages));
                input.value = '';
                hideTypingIndicator();
                updateStats();
                showNotification('Quantum message transmitted! ✨', 'success');
                
                if (currentChat.type === 'user' || currentChat.id === 'support' || currentChat.id === 'community') {
                    setTimeout(() => {
                        if (currentChat) {
                            simulateReply();
                        }
                    }, 1500 + Math.random() * 2000);
                }
            }
        }

        function simulateReply() {
            const messagesContainer = document.getElementById('messagesContainer');
            const time = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
            const replyId = 'msg_' + Date.now();
            
            const replies = {
                'support': [
                    'Quantum thanks for your message! How can we assist? 🚀',
                    'We appreciate your quantum feedback!',
                    'Our quantum team will review your message shortly. 👨‍🚀'
                ],
                'user': [
                    'Quantum hello! Thanks for reaching out! 👋',
                    'That sounds quantum interesting! Tell me more...',
                    'I will quantum respond soon! ⏰'
                ],
                'community': [
                    'Quantum great message! 👍',
                    'Thanks for quantum sharing! 💫',
                    'Welcome to the quantum community! 🎉',
                    'Quantum awesome! 🚀',
                    'Keep the quantum messages coming! ⚡'
                ]
            };
            
            const chatReplies = replies[currentChat.type] || ['Quantum thank you for your message!'];
            const replyText = chatReplies[Math.floor(Math.random() * chatReplies.length)];
            const randomUser = allUsers[Math.floor(Math.random() * (allUsers.length - 1))];
            const isPremium = randomUser.premium && randomUser.premium !== 'none';
            
            const replyElement = document.createElement('div');
            replyElement.className = `message received ${isPremium ? (randomUser.premium === 'legend' ? 'message-legend' : 'message-premium') : ''}`;
            replyElement.setAttribute('data-message-id', replyId);
            replyElement.innerHTML = `
                ${replyText}
                <div class="message-actions">
                    <button class="message-action" onclick="reactToMessage('${replyId}')">😊</button>
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
            
            localStorage.setItem('userMessages', JSON.stringify(messages));
            updateStats();
        }

        function editMessage(messageId) {
            const message = messages[currentChat.id]?.find(m => m.id === messageId);
            if (message && message.sender === 'sent') {
                const newText = prompt('Edit your quantum message:', message.text);
                if (newText !== null) {
                    message.text = newText;
                    message.edited = true;
                    localStorage.setItem('userMessages', JSON.stringify(messages));
                    showChatMessages(currentChat.id);
                    showNotification('Quantum message updated! ✅', 'success');
                }
            }
        }

        function deleteMessage(messageId) {
            if (confirm('Delete this quantum message?')) {
                messages[currentChat.id] = messages[currentChat.id]?.filter(m => m.id !== messageId) || [];
                localStorage.setItem('userMessages', JSON.stringify(messages));
                showChatMessages(currentChat.id);
                updateStats();
                showNotification('Quantum message deleted 🗑️', 'info');
            }
        }

        function reactToMessage(messageId) {
            const reactions = ['👍', '❤️', '😂', '😮', '😢', '🎉'];
            const reaction = reactions[Math.floor(Math.random() * reactions.length)];
            showNotification(`Reacted with ${reaction} to quantum message`, 'success');
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

        function showChatMenu() {
            if (!currentChat) return;
            
            const options = [
                {text: 'Clear Quantum Chat', action: () => clearChat()},
                {text: 'Export Quantum History', action: () => exportChat()},
                {text: 'Mute Quantum Notifications', action: () => muteChat()},
            ];
            
            let menuHTML = options.map(option => 
                `<div style="padding: 12px; cursor: pointer; border-radius: 8px; transition: background 0.2s;" 
                      onclick="${option.action.toString().replace(/"/g, '&quot;')}">${option.text}</div>`
            ).join('');
            
            alert('Quantum Chat Options:\n\n' + options.map(o => o.text).join('\n'));
        }

        function clearChat() {
            if (confirm('Clear all quantum messages in this chat?')) {
                messages[currentChat.id] = [];
                localStorage.setItem('userMessages', JSON.stringify(messages));
                showChatMessages(currentChat.id);
                updateStats();
                showNotification('Quantum chat cleared 🗑️', 'info');
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
            link.download = `quantum_chat_${currentChat.name}_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            showNotification('Quantum chat exported! 📤', 'success');
        }

        function muteChat() {
            showNotification('Quantum notifications muted 🔕', 'info');
        }

        function showDonatePanel() {
            document.getElementById('donatePanel').classList.add('active');
        }

        function hideDonatePanel() {
            document.getElementById('donatePanel').classList.remove('active');
            switchTab('chats');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
            switchTab('chats');
        }

        function selectTier(tier) {
            showNotification(`Quantum ${tier.toUpperCase()} tier selected! Contact @trollex_official for activation. 💎`, 'success');
            createRippleEffect(event);
        }

        function changeTheme(theme) {
            document.querySelectorAll('.theme-option').forEach(option => {
                option.classList.remove('active');
            });
            event.target.classList.add('active');
            
            currentUser.settings.theme = theme;
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            showNotification(`Quantum theme changed to ${theme}! 🎨`, 'success');
        }

        function saveSettings() {
            const newName = document.getElementById('settingsName').value.trim();
            const newEmail = document.getElementById('settingsEmail').value.trim();
            
            if (newName && newName !== currentUser.name) {
                currentUser.name = newName;
                document.getElementById('userName').textContent = newName;
                
                const userIndex = allUsers.findIndex(u => u.id === currentUser.id);
                if (userIndex > -1) {
                    allUsers[userIndex].name = newName;
                    localStorage.setItem('allUsers', JSON.stringify(allUsers));
                }
                
                showNotification('Quantum name updated! ✅', 'success');
            }
            
            if (newEmail && newEmail !== currentUser.email) {
                currentUser.email = newEmail;
                showNotification('Quantum email updated! 📧', 'success');
            }
            
            currentUser.settings.notifications = document.getElementById('settingsNotifications').checked;
            currentUser.settings.darkMode = document.getElementById('settingsDarkMode').checked;
            currentUser.settings.autoSave = document.getElementById('settingsAutoSave').checked;
            currentUser.settings.animations = document.getElementById('settingsAnimations').checked;
            
            localStorage.setItem('trollexUser', JSON.stringify(currentUser));
            hideSettings();
            showNotification('Quantum settings saved! ⚙️', 'success');
        }

        function exportData() {
            const data = {
                user: currentUser,
                messages: messages,
                friends: friends,
                groups: groups,
                allUsers: allUsers,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `quantum_backup_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            showNotification('Quantum data exported! 📤', 'success');
        }

        function clearCache() {
            if (confirm('Clear quantum cache? This will not delete your messages.')) {
                localStorage.removeItem('allUsers');
                localStorage.removeItem('userGroups');
                showNotification('Quantum cache cleared! 🧹', 'info');
            }
        }

        function logout() {
            if (confirm('Quantum logout? Your data will be saved.')) {
                localStorage.removeItem('trollexUser');
                showWelcomeScreen();
                showNotification('Quantum connection closed! 👋', 'info');
            }
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

        // Обработчики событий
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            const donatePanel = document.getElementById('donatePanel');
            const settingsPanel = document.getElementById('settingsPanel');
            
            if (window.innerWidth <= 768 && sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && !event.target.classList.contains('mobile-menu-btn')) {
                sidebar.classList.remove('active');
            }
            
            if (donatePanel.classList.contains('active') && 
                !donatePanel.contains(event.target) && !event.target.closest('.nav-tab')) {
                hideDonatePanel();
            }
            
            if (settingsPanel.classList.contains('active') && 
                !settingsPanel.contains(event.target) && !event.target.closest('.nav-tab')) {
                hideSettings();
            }
        });

        // Добавляем ripple эффект ко всем кнопкам
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn') || e.target.closest('.btn')) {
                const btn = e.target.classList.contains('btn') ? e.target : e.target.closest('.btn');
                createRippleEffect({...e, currentTarget: btn});
            }
        });

        // Адаптация для мобильных
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    data = request.json
    return jsonify({'success': True, 'message': 'Quantum message sent'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'quantum_running', 
        'service': 'TrollexDL Quantum',
        'days_until_new_year': get_days_until_new_year(),
        'version': '2.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 TrollexDL Quantum запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    print(f"⚡ Версия: 2.0.0 | Quantum Edition")
    app.run(host='0.0.0.0', port=port, debug=False)
