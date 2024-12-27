"""application module """
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


load_dotenv(override=True)
TOKEN = os.getenv("TOKEN")
WEB_HOOK = os.getenv("WEB_HOOK")
WEBHOOK_PATH = "/webhook"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    app.state.bot_app = application
    await application.bot.set_webhook(url =f"{WEB_HOOK}{WEBHOOK_PATH}", allowed_updates=Update.ALL_TYPES)

    async with application:
        try:
            await application.start()
            yield
        finally:
            await application.bot.delete_webhook()
            await application.stop()

app = FastAPI(lifespan=lifespan)



@app.post(WEBHOOK_PATH)
async def tg_webhook(request: Request):
    """Handle incoming updates from Telegram."""
    application = request.app.state.bot_app
    await application.update_queue.put(Update.de_json(data=await request.json(), bot=application.bot))



@app.post("/")
async def root():
    return {"message": "Webhook bot is running"}
