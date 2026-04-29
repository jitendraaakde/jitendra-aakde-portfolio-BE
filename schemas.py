from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ContactMessage(BaseModel):
    name: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: EmailStr
    subject: Optional[str] = "New Contact Form Submission"
    message: str

    @model_validator(mode="after")
    def populate_name(self):
        if self.name:
            self.name = self.name.strip()
            return self

        full_name = " ".join(
            part.strip()
            for part in [self.firstName, self.lastName]
            if part and part.strip()
        )

        if not full_name:
            raise ValueError("Either name or firstName is required")

        self.name = full_name
        return self

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = []

class ChatResponse(BaseModel):
    reply: str
