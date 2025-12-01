import sqlite3
import os
from schemas import HeaderSchema
from fastapi import UploadFile

DB = "mockchat.db"


def initDB():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT DEFAULT 'whatsapp',
            name TEXT,
            status TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chatID INTEGER,
            sender TEXT,
            text TEXT,
            time TEXT,
            direction TEXT
        );
    """)

    conn.commit()
    conn.close()


def createChat(platform):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chats(platform, name, status) VALUES(?, ?, ?)",
        (platform, "Contact Name", "online")
    )
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def setHeader(chatID, header: HeaderSchema):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "UPDATE chats SET name=?, status=? WHERE id=?",
        (header.name, header.status, chatID)
    )
    conn.commit()
    conn.close()


def saveDP(chatID: int, file: UploadFile):
    folder = "static/uploads"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/chat_{chatID}_dp.png"

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path


def getHeader(chatID):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT name, status FROM chats WHERE id=?", (chatID,))
    row = cur.fetchone()
    conn.close()
    return row


def getDP(chatID):
    path = f"static/uploads/chat_{chatID}_dp.png"
    return path if os.path.exists(path) else None


def addMessage(chatID, msg):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO messages(chatID, sender, text, time, direction)
        VALUES (?, ?, ?, ?, ?)
    """, (chatID, msg.sender, msg.text, msg.time, msg.direction))
    conn.commit()
    conn.close()


def addBulkMessages(chatID, messages):
    for msg in messages:
        addMessage(chatID, msg)


def getMessages(chatID):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT sender, text, time, direction
        FROM messages WHERE chatID=?
    """, (chatID,))
    rows = cur.fetchall()
    conn.close()
    return rows
