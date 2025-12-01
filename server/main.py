from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from database import (
    initDB,
    createChat,
    addMessage,
    addBulkMessages,
    getMessages,
    setHeader,
    saveDP,
    getHeader,
    getDP
)
from schemas import MessageSchema, BulkMessageSchema, HeaderSchema
from utils.renderers.whatsapp import renderWhatsApp

app = FastAPI(title="MockChat Generator")


@app.on_event("startup")
def startupEvent():
    initDB()


@app.post("/chat/create")
def createChatAPI(platform: str = "whatsapp"):
    cid = createChat(platform)
    return {"chatID": cid, "platform": platform}


@app.post("/chat/{chatID}/header")
def setHeaderAPI(chatID: int, header: HeaderSchema):
    setHeader(chatID, header)
    return {"status": "header set"}


@app.post("/chat/{chatID}/dp")
def uploadDP(chatID: int, file: UploadFile = File(...)):
    path = saveDP(chatID, file)
    return {"status": "dp uploaded", "path": path}


@app.post("/chat/{chatID}/message")
def addMessageAPI(chatID: int, msg: MessageSchema):
    addMessage(chatID, msg)
    return {"status": "message added"}


@app.post("/chat/{chatID}/messages/bulk")
def addBulkMessagesAPI(chatID: int, data: BulkMessageSchema):
    addBulkMessages(chatID, data.messages)
    return {"status": "bulk messages added"}


@app.get("/chat/{chatID}/render")
def renderChat(chatID: int):
    msgs = getMessages(chatID)
    header = getHeader(chatID)
    dp = getDP(chatID)

    filepath = renderWhatsApp(chatID, msgs, header, dp)
    return FileResponse(filepath, media_type="image/png")
