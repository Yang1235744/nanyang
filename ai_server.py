from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import sqlite3
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DOWNLOAD_URL = "请到南洋数码工作室官网下载库获取所有资源"

knowledge_base = {
    "装机": [
        "装机注意CPU与主板兼容，内存插紧，散热器涂硅脂，电源线插满。",
        f"系统镜像、PE工具、驱动请到官网下载库：{DOWNLOAD_URL}"
    ],
    "装系统": [
        "用8G以上U盘做启动盘，新电脑用UEFI+GPT，装纯净版系统。",
        f"纯净系统镜像下载：{DOWNLOAD_URL}"
    ],
    "驱动": [
        "驱动异常会导致没声音、没网、蓝屏、花屏，优先装官方驱动。",
        f"万能网卡驱动、驱动合集：{DOWNLOAD_URL}"
    ],
    "蓝屏": [
        "蓝屏常见原因：驱动冲突、内存不稳、硬盘坏道、温度高。",
        f"纯净系统可减少蓝屏：{DOWNLOAD_URL}"
    ],
    "卡顿": [
        "卡顿优先换固态、清C盘、关自启、装纯净系统。",
        f"纯净系统下载：{DOWNLOAD_URL}"
    ],
    "网络": [
        "上不了网先查驱动、网线、路由器，DNS可设223.5.5.5。",
        f"万能网卡驱动：{DOWNLOAD_URL}"
    ],
    "黑屏": [
        "黑屏先重插内存，独显要接显卡，别接主板。",
        f"系统修复工具：{DOWNLOAD_URL}"
    ],
    "没声音": [
        "没声音先查音量和驱动，台式机前面板需禁用检测。",
        f"声卡驱动：{DOWNLOAD_URL}"
    ],
    "密码": [
        "忘记密码用PE清除，不删文件。",
        f"PE工具箱：{DOWNLOAD_URL}"
    ]
}

greetings = [
    "你好", "您好", "嗨", "哈喽", "在吗", "在不在", "在",
    "喂", "哎", "你好啊", "您好啊", "有人吗", "在呢"
]

greet_replies = [
    "你好呀！有什么电脑问题可以问我～",
    "您好！我是南洋数码助手，随时为您服务。",
    "哈喽！我在呢，你说～",
    "你好！需要修电脑、装系统都可以告诉我。",
    "嗨！有什么可以帮你的吗？"
]

default_replies = [
    "我没太明白你的意思，可以说具体一点哦。",
    "你可以问我电脑相关的问题，比如蓝屏、卡顿、装系统～",
    "这个我暂时不太清楚，换个问题试试吧。",
    "你说的我没听懂，再说清楚一点呗。"
]

keywords = {
    "装机": ["装机", "组装", "装电脑"],
    "装系统": ["装系统", "重装", "镜像"],
    "驱动": ["驱动", "显卡驱动", "声卡驱动", "网卡驱动"],
    "蓝屏": ["蓝屏", "崩溃"],
    "卡顿": ["卡", "卡顿", "慢"],
    "网络": ["网", "上网", "wifi", "网线"],
    "黑屏": ["黑屏", "没信号"],
    "没声音": ["声音", "没声音"],
    "密码": ["密码", "忘记密码"]
}

# ===================== 数据库功能（只加这段）=====================
def init_db():
    conn = sqlite3.connect("ai_chat.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS chat_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_msg TEXT,
        ai_reply TEXT,
        create_time TEXT
    )''')
    conn.commit()
    conn.close()

def save_chat(user_msg, ai_reply):
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("ai_chat.db")
        c = conn.cursor()
        c.execute("INSERT INTO chat_log (user_msg, ai_reply, create_time) VALUES (?,?,?)",
                  (user_msg, ai_reply, now))
        conn.commit()
        conn.close()
    except:
        pass
# ================================================================

def get_reply(msg):
    msg = str(msg).strip()
    
    for g in greetings:
        if g in msg:
            return random.choice(greet_replies)
    
    for key, kw_list in keywords.items():
        for kw in kw_list:
            if kw in msg:
                return random.choice(knowledge_base[key])
    
    return random.choice(default_replies)

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    data = request.get_json(silent=True) or {}
    msg = data.get("message", "")
    reply = get_reply(msg)
    
    # 自动保存聊天记录到数据库
    save_chat(msg, reply)
    
    return {"reply": reply}

if __name__ == "__main__":
    init_db()  # 启动自动创建数据库
    app.run(host='0.0.0.0', port=5000)