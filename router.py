from controllers import health, contact, chatbot

def register_routers(app):
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(contact.router, prefix="/api/v1", tags=["Contact"])
    app.include_router(chatbot.router, prefix="/api/v1", tags=["Chatbot"])