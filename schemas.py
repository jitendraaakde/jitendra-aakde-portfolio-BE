from pydantic import BaseModel, EmailStr
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = "New Contact Form Submission"
    message: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = []

class ChatResponse(BaseModel):
    reply: str