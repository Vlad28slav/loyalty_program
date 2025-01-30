"""application module """
import os
import logging
from datetime import datetime

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from models import SessionLocal, engine

import models






# Set up logging
logging.basicConfig(level=logging.INFO)


load_dotenv(override=True)
TOKEN = os.getenv("TOKEN")
WEB_HOOK = os.getenv("WEB_HOOK")
WEBHOOK_PATH = "/webhook"
ADD_CUSTOMER_COMMAND = "add_customer"

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
    current_date_time= datetime.now()
    db_user_check = db.query(models.User).filter(models.User.id == id_user).first()
    if db_user_check is None:
        db_user = models.User(id=id_user, started_at=current_date_time)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        answer = (
            f'Hello, {user_name}, print /add_customer to add your first cutomers, or /set_program '
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
    customer_name = update.message.text.replace(f'/{ADD_CUSTOMER_COMMAND}', '').strip()
    id_user= update.message.chat.id
    current_date_time = datetime.now()
    customer_check = db.query(models.Customer).filter(
        models.Customer.name == customer_name).filter(
            models.Customer.seller_id == id_user).first()
    if customer_check is None:
        new_customer = models.Customer(
            name= customer_name, seller_id= id_user, created_at= current_date_time)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        answer= (
                f'You have added a new customer {customer_name}'
            )
    else:
        answer=(
            f'You already have {customer_name} as a customer, try to change somehow '
            f'name, you can use letters, numbers and other symbols'
        )
    await update.message.reply_text(answer)

async def purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data["db"]
    customer_name=''
    amount=0
    id_user= update.message.chat.id
    customer_name_and_amount = update.message.text
    customer_name_and_amount = customer_name_and_amount.split(' ')
    answer=''
    transaction = False
    if len(customer_name_and_amount) == 2:
        try:
            customer_name= customer_name_and_amount[0]
            amount = int(customer_name_and_amount[1])
            transaction = True
        except ValueError:
            try:
                amount = int(customer_name_and_amount[0])
                customer_name= customer_name_and_amount[1]
                transaction = True
            except ValueError:
                answer ="To create a purchase write your customer's name and amount"

    else:
        answer ="To create a purchase write your customer's name and amount"

    if transaction is True:
        answer = f'It is looks like you do not have {customer_name} as your registrated customer'
        customer = db.query(models.Customer).filter(
            models.Customer.seller_id == id_user).filter(
                models.Customer.name == customer_name).first()
        if customer:
            amount1= amount
            bonus_program= db.query(models.User).filter(models.User.id == id_user).first().program
            parsed_bonuses= bonus_program.split('!')
            nums_bonuses= len(parsed_bonuses)
            bonus_total = 0
            for i in range(1, nums_bonuses +1):
                atempt = parsed_bonuses[-i]
                amount_for_bonus_and_bonus = atempt.split(',')
                if amount > int(amount_for_bonus_and_bonus[0]):
                    bonus_size = (amount/int(amount_for_bonus_and_bonus[0])) // 1 #rounding down to get the bonus size
                    bonus_temp = int(amount_for_bonus_and_bonus[1]) * bonus_size
                    bonus_total= int(bonus_temp + bonus_total)
                    amount= amount -(bonus_size * int(amount_for_bonus_and_bonus[0]))
            old_amount= customer.current_amount
            new_amount = old_amount + amount1
            old_bonus = customer.bonuses
            new_bonus = int(old_bonus + bonus_total)
            customer.current_amount = new_amount
            customer.bonuses = new_bonus
            db.commit()
            db.refresh(customer)
            answer=(
                f'{customer_name} bought {amount1} and deserved for {bonus_total} of reward! In tota'
                f'l {customer_name} spent {new_amount}, and received {new_bonus} at yours bussines'
                )

        
    
    await update.message.reply_text(answer)



@asynccontextmanager
async def lifespan(app: FastAPI):
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler(ADD_CUSTOMER_COMMAND, addCustomer))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, purchase))
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
