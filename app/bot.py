from app import app
from telegram import *
from telegram.ext import *
from helpers.helper_functions import generate_login_password
from helpers.db_helper import (create_user, create_statistics,
                               get_user, get_choice_id,
                               get_all_choices, get_new_task,
                               get_picture_by_task_id)
from werkzeug.security import check_password_hash
from config import API_KEY, REGISTER_BUTTON, TASK_BUTTON, EXIT_BUTTON, SIGN_IN_COMMAND

app.logger.info("Telegram ZERO_BOT running . . .")
data = {"task_count": 10,
        "choises_list": [],
        "task_list": [],
        "welcome_message": "Please register for sign in.",
        "task_message": "Are you ready to start Zerobot task?"}

updater = Updater(token=API_KEY)
dispacher = updater.dispatcher

bot = Bot(token=API_KEY)


def create_markup_task(update, context, new_task, user_id):
    with app.app_context():
        choises = get_all_choices(new_task.picture_id)
        new_picture = get_picture_by_task_id(new_task.picture_id)
        data["choises_list"].clear()
        for choice in choises:
            data["choises_list"].append(choice[0])
        data["choises_list"].append("other")
        buttonsCommand(data["choises_list"], update=update, context=context)
    if new_picture:
        picture = bytes.fromhex(new_picture.picture[2:])
        bot.send_photo(update.message.chat_id, picture)
        data["task_list"].clear()
        data["task_list"].append(new_task)
        data["task_list"].append(user_id)


def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(REGISTER_BUTTON)], [KeyboardButton(EXIT_BUTTON)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text=data["welcome_message"],
    reply_markup=ReplyKeyboardMarkup(buttons))


def taskCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(TASK_BUTTON)], [KeyboardButton(EXIT_BUTTON)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text=data["task_message"],
    reply_markup=ReplyKeyboardMarkup(buttons))


def buttonsCommand(choises, update: Update, context: CallbackContext):
    buttons = []
    for choise in choises:
        buttons.append([KeyboardButton(choise)])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please choose appropriate option.",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def messageHandler(update: Update, context: CallbackContext):
    if update.message:
        telegram_user = update.message.chat.username
        # Registration
        if REGISTER_BUTTON in update.message.text:
            with app.app_context():
                telegram_account = get_user(telegram_user)
            if telegram_account:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Telegram user {telegram_user} already redgistered.")
                app.logger.info(f"Telegram user {telegram_user} already redgistered.")
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please sign in using below form.")
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"/sign_in login password")
            else:
                login, password = generate_login_password()
                if not telegram_user:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please set your telegram username before registartion.")
                    app.logger.error(f"Telegram user with chat id {update.message.chat_id} has not set username.")
                else:
                    with app.app_context():
                        create_user(login, password, telegram_user)
                    text_info = f"You have sucessfully resgisterd \nYour login is {login} \nYour password is {password}"
                    app.logger.info(f"Telegram user {telegram_user} sucessfully redgistered.")
                    app.logger.info(f"Username is '{login}' password is '{password}'")
                    context.bot.send_message(chat_id=update.effective_chat.id, text=text_info)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please remember your credentials for next sign in!")

                    # Start markup task
                    data["task_message"] = "Are you ready to start new markup tasks?"
                    taskCommand(update=update, context=context)

        # Sign In
        if update.message.text[0:8] == SIGN_IN_COMMAND:
            credentials = update.message.text[8:].split()
            if len(credentials) != 2:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Login or password wrote form was wrong.")
                context.bot.send_message(chat_id=update.effective_chat.id, text="Please try again")
                app.logger.warning(f"Telegram user {telegram_user} login or password wrote form was wrong.")
            else:
                login_in, password_in = credentials
                with app.app_context():
                    user_credentials = get_user(telegram_user)
                if user_credentials:
                    username = user_credentials.username
                    password = user_credentials.password
                    if login_in == username and check_password_hash(password, password_in):
                        context.bot.send_message(chat_id=update.effective_chat.id, text="You have successfully logged in.")
                        app.logger.info(f"Telegram user {telegram_user} sucessfully logged in.")
                        # Start markup task
                        data["task_message"] = "Are you ready to start new markup tasks again?"
                        taskCommand(update=update, context=context)
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Login or password was incorrect.")
                        app.logger.warning(f"Telegram user {telegram_user} login or password was incorrect.")
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Please try again.")

                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Telegram user was not found.")
                    app.logger.warning(f"Telegram user {telegram_user} was not found.")
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Please try again.")

        # Exit
        if EXIT_BUTTON in update.message.text:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You are successfully logged off!")
            app.logger.info(f"Telegram user {telegram_user} successfully logged off.")
            data["welcome_message"] = "Please register for sign in!"
            startCommand(update=update, context=context)

        # Start the task
        if TASK_BUTTON in update.message.text:
            with app.app_context():
                user = get_user(telegram_user)
                user_id = None
                if user:
                    user_id = user.id
            data['task_count'] = 0
            if user_id:
                with app.app_context():
                    new_task = get_new_task(user_id)
                    if not new_task:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You have no any task yet!")
                        app.logger.info(f"Telegram user {telegram_user} completed all markup tasks.")
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thank you for completion for all markup tasks.")
                        data["welcome_message"] = "See you later."
                        startCommand(update=update, context=context)
                    
                if new_task:
                    app.logger.info(f"Teegram user {telegram_user} starts markup task.")
                    create_markup_task(update, context, new_task, user_id)

        if (TASK_BUTTON not in update.message.text) and (update.message.text in data["choises_list"]):
            data['task_count'] += 1
            if data["task_list"]:
                with app.app_context():
                    choice_id = get_choice_id(data["task_list"][0].picture_id, update.message.text)
                    if choice_id:
                        with app.app_context():
                            create_statistics(data["task_list"][1], data["task_list"][0].id, choice_id[0])
                        app.logger.info('User choice accepted.')
                    elif choice_id is None and update.message.text == "other":
                            create_statistics(data["task_list"][1], data["task_list"][0].id, 0) 

            with app.app_context():
                user = get_user(telegram_user)
                user_id = None
                if user:
                    user_id = user.id
            if user_id:
                with app.app_context():
                    new_task = get_new_task(user_id)
                    if not new_task or data['task_count'] == 10:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You have completed your markup tasks!")
                        app.logger.info(f"Telegram user {telegram_user} completed ongoing markup tasks.")
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thank you for participating markup program.")
                        if data['task_count'] < 10:
                            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thank you for completion for all markup tasks.")
                            data["welcome_message"] = "See you later."
                            app.logger.info(f"Telegram user {telegram_user} completed all markup tasks.")
                            startCommand(update=update, context=context)
                        else:
                            data["task_message"] = "Are you ready to start new markup tasks again?"
                            taskCommand(update=update, context=context)
                    else:
                        create_markup_task(update, context, new_task, user_id)

dispacher.add_handler(CommandHandler("start", startCommand))
dispacher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()
