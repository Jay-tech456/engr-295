from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Message(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/chat")
def chat_endpoint(msg: Message):
    
    reply = f"You said: {msg.message}"
    return {"reply": reply}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
