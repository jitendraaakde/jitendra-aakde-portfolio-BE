from fastapi import HTTPException, APIRouter
from schemas import ContactMessage
from utils.email import send_email
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

router = APIRouter()

@router.post("/contact")
async def submit_contact(contact: ContactMessage):
    """
    Handle contact form submissions and send email
    """
    try:
        await send_email(contact)
        logger.info(f"Contact form submitted by {contact.email}")
        return {
            "success": True,
            "message": "Thank you for your message! We'll get back to you soon."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"An error occurred while submitting contact form: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )
