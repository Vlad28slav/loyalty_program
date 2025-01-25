"""application module """
import os
import logging
from datetime import datetime

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from models import SessionLocal, engine

import models
import schemas






# Set up logging
logging.basicConfig(level=logging.INFO)


load_dotenv(override=True)
TOKEN = os.getenv("TOKEN")
WEB_HOOK = os.getenv("WEB_HOOK")
WEBHOOK_PATH = "/webhook"

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    user_name = update.message.chat.first_name
    id_user= update.message.chat.id
    currentDateTime = datetime.now()
    db_user_check = db.query(models.User).filter(models.User.id == id_user).first()
    if db_user_check is None:
        db_user = models.User(id=id_user, program= '10!1', started_at= currentDateTime)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        answer = (
            f'Hello, {user_name}, print /add_customer to add your first cutomers, or /set_program \n'
            f' to create your custom loyalty program, by default it is buy 10, get 1 for free!'
            )
    else:
        time = db.query(models.User).filter(models.User.id == id_user).first().started_at
        time_str=str(time)[:-10]
        answer= (
            f'You are alredy using this service, since {time_str}'
        )

    await update.message.reply_text(answer)

async def addCustomer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    customer = update.message.text[13::]
    answer= (
            f'You added a new customer {customer}'
        )
    await update.message.reply_text(answer)

@asynccontextmanager
async def lifespan(app: FastAPI):
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_customer", addCustomer))
    db = SessionLocal()
    application.bot_data["db"] = db
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
