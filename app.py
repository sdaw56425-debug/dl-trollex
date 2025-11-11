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

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
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
            animation: slideDown 0.2s ease;
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
            animation: slideUp 0.3s ease;
        }

        .emoji {
            font-size: 1.2rem;
            cursor: pointer;
            padding: 5px;
            border-radius: 5px;
            text-align: center;
            transition: all 0.2s;
        }

        .emoji:hover {
            background: rgba(107, 43, 217, 0.3);
            transform: scale(1.2);
        }

        .emoji-btn {
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.2rem;
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: all 0.2s;
        }

        .emoji-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: scale(1.1);
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
            animation: bounceIn 0.3s ease;
        }

        .reaction:hover, .reaction.active {
            background: rgba(107, 43, 217, 0.3);
            border-color: var(--accent);
            transform: scale(1.1);
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
            animation: slideUp 0.5s ease;
        }

        .online-user {
            display: flex;
            align-items: center;
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
            transition: all 0.2s;
            cursor: pointer;
        }

        .online-user:hover {
            background: rgba(107, 43, 217, 0.2);
            transform: translateX(5px);
        }

        .profile-panel {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.7);
            background: rgba(26, 26, 74, 0.98);
            border: 2px solid var(--accent);
            border-radius: 20px;
            padding: 30px;
            z-index: 600;
            max-width: 400px;
            width: 90%;
            opacity: 0;
            transition: all 0.3s ease;
            backdrop-filter: blur(20px);
        }

        .profile-panel.active {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }

        .profile-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 599;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .profile-overlay.active {
            opacity: 1;
        }

        .community-message {
            border-left: 3px solid var(--neon);
            animation: slideUp 0.4s ease;
        }

        .community-message:hover {
            animation: shake 0.5s ease;
        }

        .user-status {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 8px;
        }

        .status-online {
            color: var(--success);
        }

        .status-offline {
            color: var(--text-secondary);
        }

        .floating-animation {
            animation: float 3s ease-in-out infinite;
        }

        .pulse-animation {
            animation: pulse 2s infinite;
        }

        .bounce-animation {
            animation: bounceIn 0.6s ease;
        }

        .shake-animation {
            animation: shake 0.5s ease;
        }

        .spin-animation {
            animation: spin 1s linear infinite;
        }

        .fade-in {
            animation: fadeIn 0.5s ease;
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

            .profile-panel {
                width: 95%;
                padding: 20px;
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
                <div class="nav-tab active" data-tab="chats">💬</div>
                <div class="nav-tab" data-tab="users">👥</div>
                <div class="nav-tab" data-tab="groups">👨‍👩‍👧‍👦</div>
                <div class="nav-tab" data-tab="donate">💎</div>
                <div class="nav-tab" data-tab="settings">⚙️</div>
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
            <button class="btn btn-vip" onclick="event.stopPropagation(); selectTier('vip')">Выбрать VIP</button>
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
            <button class="btn btn-premium" onclick="event.stopPropagation(); selectTier('premium')">Выбрать Premium</button>
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
            <button class="btn btn-ultra" onclick="event.stopPropagation(); selectTier('ultra')">Выбрать Ultra</button>
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
            <button class="btn btn-moder" onclick="event.stopPropagation(); selectTier('moder')">Выбрать Moder</button>
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
            <button class="btn btn-chromek" onclick="event.stopPropagation(); selectTier('chromek')">Выбрать Chromek</button>
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

    <!-- Панель профиля -->
    <div class="profile-overlay" id="profileOverlay" onclick="hideProfile()"></div>
    <div class="profile-panel" id="profilePanel">
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="user-avatar" id="profileAvatar">👤</div>
            <h3 id="profileName">User Name</h3>
            <p style="color: var(--text-secondary);" id="profileUsername">@username</p>
            <div id="profilePremium" class="premium-badge hidden" style="margin: 10px auto;"></div>
        </div>
        
        <div class="user-status">
            <span id="profileStatus">🟢 Online</span>
            <span style="color: var(--text-secondary);">•</span>
            <span id="profileId">ID: user_123</span>
        </div>

        <div style="margin: 20px 0; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;">
            <h4 style="margin-bottom: 10px;">📊 Profile Info</h4>
            <div>📧 Email: <span id="profileEmail">user@example.com</span></div>
            <div>📅 Member since: <span id="profileJoinDate">2024</span></div>
            <div>💬 Messages: <span id="profileMessageCount">0</span></div>
        </div>

        <button class="btn btn-primary" id="profileActionBtn" onclick="profileAction()" style="margin-bottom: 10px;">
            💬 Send Message
        </button>
        <button class="btn btn-secondary" onclick="hideProfile()">
            ✕ Close
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
        let currentProfileUser = null;

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            updateNewYearCountdown();
            setInterval(updateNewYearCountdown, 60000);
            
            // Инициализация emoji picker
            initEmojiPicker();
            
            // Инициализация навигации
            initNavigation();
            
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
                {id: 'user1', name: 'Alex_Quantum', avatar: '👨‍💻', online: true, username: 'alex_quantum', premium: 'vip', email: 'alex@quantum.io', joinDate: '2024-01-15', messageCount: 127},
                {id: 'user2', name: 'Sarah_Cyber', avatar: '👩‍🎨', online: true, username: 'sarah_cyber', premium: 'premium', email: 'sarah@cyber.org', joinDate: '2024-02-20', messageCount: 89},
                {id: 'user3', name: 'Mike_Neon', avatar: '👨‍🚀', online: false, username: 'mike_neon', premium: 'none', email: 'mike@neon.com', joinDate: '2024-03-10', messageCount: 45},
                {id: 'user4', name: 'Emma_Digital', avatar: '👩‍💼', online: true, username: 'emma_digital', premium: 'ultra', email: 'emma@digital.ai', joinDate: '2024-01-05', messageCount: 203},
                {id: 'user5', name: 'Tom_Hyper', avatar: '🧑‍🔬', online: false, username: 'tom_hyper', premium: 'none', email: 'tom@hyper.net', joinDate: '2024-04-15', messageCount: 67},
                {id: 'user6', name: 'Lisa_Virtual', avatar: '👩‍🔧', online: true, username: 'lisa_virtual', premium: 'moder', email: 'lisa@virtual.io', joinDate: '2024-02-28', messageCount: 156},
                {id: 'user7', name: 'John_Alpha', avatar: '👨‍🎓', online: true, username: 'john_alpha', premium: 'chromek', email: 'john@alpha.org', joinDate: '2024-01-01', messageCount: 312},
                {id: 'user8', name: 'Anna_Mega', avatar: '👩‍🍳', online: false, username: 'anna_mega', premium: 'none', email: 'anna@mega.com', joinDate: '2024-03-22', messageCount: 23}
            ];
            
            // Добавляем текущего пользователя в список
            allUsers.push({
                id: currentUser.id,
                name: currentUser.name,
                avatar: currentUser.avatar,
                online: true,
                username: currentUser.name.toLowerCase().replace(' ', '_'),
                premium: currentUser.premium,
                email: currentUser.email,
                joinDate: currentUser.created_at.split('T')[0],
                messageCount: 0
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

        function initNavigation() {
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    const tabName = this.getAttribute('data-tab');
                    switchTab(tabName);
                });
            });
        }

        function switchTab(tabName) {
            currentTab = tabName;
            
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Обработка специальных вкладок
            if (tabName === 'donate') {
                showDonatePanel();
                return;
            } else if (tabName === 'settings') {
                showSettings();
                return;
            }
            
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
                    <div class="chat-item" onclick="showUserProfile('${user.id}')">
                        <div class="item-avatar">${user.avatar}</div>
                        <div style="flex: 1;">
                            <div style="font-weight: bold;">${user.name}</div>
                            <div style="color: ${user.online ? 'var(--success)' : 'var(--text-secondary)'}; font-size: 0.85rem;">
                                @${user.username} • ${user.online ? '● Online' : '○ Offline'}
                                ${user.premium !== 'none' ? `<span style="color: var(--${user.premium}); margin-left: 5px;">⭐</span>` : ''}
                            </div>
                        </div>
                        <div style="display: flex; gap: 5px;">
                            <button onclick="event.stopPropagation(); startChatWithUser('${user.id}')" style="background: var(--accent); color: white; border: none; border-radius: 6px; padding: 6px 10px; cursor: pointer; font-size: 0.8rem;">💬</button>
                            <button onclick="event.stopPropagation(); ${isFriend ? `removeFriend('${user.id}')` : `addFriend('${user.id}')`}" 
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
                <div class="online-user" onclick="showUserProfile('${user.id}')">
                    <div style="width: 8px; height: 8px; background: var(--success); border-radius: 50%; margin-right: 8px;"></div>
                    <div style="font-size: 0.9rem;">${user.name}</div>
                </div>
            `).join('');
        }

        function showUserProfile(userId) {
            const user = allUsers.find(u => u.id === userId);
            if (!user) return;
            
            currentProfileUser = user;
            
            document.getElementById('profileAvatar').textContent = user.avatar;
            document.getElementById('profileName').textContent = user.name;
            document.getElementById('profileUsername').textContent = `@${user.username}`;
            document.getElementById('profileEmail').textContent = user.email;
            document.getElementById('profileId').textContent = `ID: ${user.id}`;
            document.getElementById('profileStatus').textContent = user.online ? '🟢 Online' : '⚫ Offline';
            document.getElementById('profileStatus').className = user.online ? 'status-online' : 'status-offline';
            document.getElementById('profileJoinDate').textContent = new Date(user.joinDate).toLocaleDateString();
            document.getElementById('profileMessageCount').textContent = user.messageCount || 0;
            
            const premiumBadge = document.getElementById('profilePremium');
            if (user.premium && user.premium !== 'none') {
                premiumBadge.textContent = user.premium.toUpperCase();
                premiumBadge.classList.remove('hidden');
            } else {
                premiumBadge.classList.add('hidden');
            }
            
            const actionBtn = document.getElementById('profileActionBtn');
            const isFriend = friends.some(f => f.id === user.id);
            if (isFriend) {
                actionBtn.textContent = '❌ Remove Friend';
                actionBtn.style.background = 'rgba(255,68,68,0.2)';
                actionBtn.style.color = 'var(--danger)';
                actionBtn.style.borderColor = 'var(--danger)';
            } else {
                actionBtn.textContent = '➕ Add Friend';
                actionBtn.style.background = '';
                actionBtn.style.color = '';
                actionBtn.style.borderColor = '';
            }
            
            document.getElementById('profileOverlay').classList.add('active');
            document.getElementById('profilePanel').classList.add('active');
        }

        function hideProfile() {
            document.getElementById('profileOverlay').classList.remove('active');
            document.getElementById('profilePanel').classList.remove('active');
            currentProfileUser = null;
        }

        function profileAction() {
            if (!currentProfileUser) return;
            
            const isFriend = friends.some(f => f.id === currentProfileUser.id);
            if (isFriend) {
                removeFriend(currentProfileUser.id);
            } else {
                addFriend(currentProfileUser.id);
            }
            hideProfile();
        }

        function openChat(chatId) {
            const chats = {
                'support': {name: 'Trollex Support', avatar: '🛰️', status: 'online', type: 'support'},
                'updates': {name: 'System Updates', avatar: '🔧', status: 'online', type: 'updates'},
                'community': {name: 'Community Chat', avatar: '👥', status: 'online', type: 'community'}
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
                updateOnlineUsers();
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
                updateOnlineUsers();
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
                    const isCommunity = currentChat.type === 'community';
                    const reactionsHTML = msg.reactions ? Object.entries(msg.reactions).map(([emoji, count]) => 
                        `<span class="reaction" onclick="addReaction('${msg.id}', '${emoji}')">${emoji} ${count}</span>`
                    ).join('') : '';
                    
                    return `
                        <div class="message ${msg.sender} ${isPremium ? 'message-premium' : ''} ${isCommunity ? 'community-message' : ''}" 
                             data-message-id="${msg.id}" 
                             oncontextmenu="showMessageContextMenu(event, '${msg.id}')"
                             ${isCommunity ? `onclick="showCommunityUserProfile('${msg.senderId || 'unknown'}')"` : ''}>
                            ${isCommunity ? `<strong>${msg.senderName || 'User'}:</strong> ` : ''}
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

        function showCommunityUserProfile(senderId) {
            if (senderId && senderId !== 'unknown') {
                showUserProfile(senderId);
            }
        }

        function getDefaultMessages(chatId) {
            const communityUsers = allUsers.filter(u => u.id !== currentUser.id).slice(0, 5);
            
            const defaults = {
                'support': [
                    {id: '1', text: 'Welcome to TrollexDL Support! 🚀', sender: 'received', time: '12:00', views: 1},
                    {id: '2', text: 'How can we assist you today?', sender: 'received', time: '12:01', views: 1}
                ],
                'community': [
                    {id: '1', text: 'Welcome to Community Chat! 👋', sender: 'received', time: '10:00', views: 15, senderId: communityUsers[0]?.id, senderName: communityUsers[0]?.name},
                    {id: '2', text: 'Anyone online? 🚀', sender: 'received', time: '10:05', views: 8, premium: 'vip', senderId: communityUsers[1]?.id, senderName: communityUsers[1]?.name},
                    {id: '3', text: 'Testing new features! ⚡', sender: 'received', time: '10:10', views: 12, premium: 'premium', senderId: communityUsers[2]?.id, senderName: communityUsers[2]?.name},
                    {id: '4', text: 'This app is amazing! 🌟', sender: 'received', time: '10:15', views: 20, senderId: communityUsers[3]?.id, senderName: communityUsers[3]?.name},
                    {id: '5', text: 'Join our premium program! 💎', sender: 'received', time: '10:20', views: 25, premium: 'ultra', senderId: communityUsers[4]?.id, senderName: communityUsers[4]?.name}
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
                    ${currentChat.type === 'community' ? `
                        <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                            <h4>👥 Community Rules</h4>
                            <p style="font-size: 0.9rem; margin-top: 8px;">
                                • Be respectful to others<br>
                                • No spam or advertising<br>
                                • Keep conversations friendly<br>
                                • Have fun! 🎉
                            </p>
                        </div>
                    ` : ''}
                </div>
            `;
        }

        // ... (остальные функции остаются такими же, как в предыдущей версии)

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
                emojiPicker.classList.add('bounce-animation');
            } else {
                emojiPicker.style.display = 'none';
                emojiPicker.classList.remove('bounce-animation');
            }
        }

        function addEmojiToMessage(emoji) {
            const input = document.getElementById('messageInput');
            input.value += emoji;
            input.focus();
            input.classList.add('shake-animation');
            setTimeout(() => input.classList.remove('shake-animation'), 500);
        }

        function showDonatePanel() {
            document.getElementById('donatePanel').classList.add('active');
            document.querySelector('[data-tab="donate"]').classList.add('active');
        }

        function hideDonatePanel() {
            document.getElementById('donatePanel').classList.remove('active');
            document.querySelector('[data-tab="donate"]').classList.remove('active');
            switchTab('chats');
        }

        function showSettings() {
            document.getElementById('settingsPanel').classList.add('active');
            document.querySelector('[data-tab="settings"]').classList.add('active');
        }

        function hideSettings() {
            document.getElementById('settingsPanel').classList.remove('active');
            document.querySelector('[data-tab="settings"]').classList.remove('active');
            switchTab('chats');
        }

        function selectTier(tier) {
            showNotification(`Selected ${tier.toUpperCase()} tier! Contact @trollex_official on Telegram for purchase. 💎`, 'success');
            // Анимация выбора
            event.target.classList.add('pulse-animation');
            setTimeout(() => event.target.classList.remove('pulse-animation'), 1000);
        }

        // ... (остальной код функций остается таким же)

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
