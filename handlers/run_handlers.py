import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, \
    filters

from dto.Job import Job
from service import jenkins_svc
from service.decorators import restricted

RUN = "RUN"

SELECT_JOB = 1
CONFIGURE_JOB = 2
CONFIGURE_PARAM = 3

JOB = "job"
PARAM = "param"


def run_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(["run", "start"], run_command_handler)],
        states={
            SELECT_JOB: [CallbackQueryHandler(job_selected_handler)],
            CONFIGURE_JOB: [CallbackQueryHandler(configure_job_handler)],
            CONFIGURE_PARAM: [CallbackQueryHandler(configure_choice_param_handler),
                              MessageHandler(filters.TEXT, configure_text_param_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler(["run", "start"], run_command_handler)],
    )
    return conv_handler


@restricted
async def run_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the run job conversation"""
    context.user_data.clear()

    job_names = jenkins_svc.list_jobs()
    keyboard = []
    for job_name in job_names:
        keyboard.append([InlineKeyboardButton(job_name, callback_data=job_name)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Which job to run?", reply_markup=reply_markup)

    return SELECT_JOB


@restricted
async def job_selected_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Job was selected. Gets jobs parameters and creates user context"""
    context.user_data.clear()

    job_name = update.callback_query.data
    query = update.callback_query
    await query.answer()

    await update.effective_message.reply_text("Fetching parameters for " + job_name + ", hang on a sec...")
    job = jenkins_svc.get_job_config(job_name)

    context.user_data[JOB] = job

    await update.effective_message.reply_text("Configuring " + job.name,
                                              reply_markup=build_job_keyboard(context.user_data[JOB]))

    return CONFIGURE_JOB


async def configure_job_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    param_name = query.data
    job = context.user_data[JOB]

    await query.answer()

    if param_name == RUN:
        await update.effective_message.reply_text("Running job " + job.name + ". Will update you soon!")
        asyncio.create_task(run_and_reply(update, job))
        return ConversationHandler.END
    else:
        context.user_data[PARAM] = param_name
        param = next((param for param in job.params if param.name == param_name), None)
        if param.type == "Choice":
            await update.effective_message.edit_text("Select " + param_name + " value:",
                                                     reply_markup=build_param_keyboard(job, param_name))
            return CONFIGURE_PARAM
        else:
            await update.effective_message.reply_text("Enter " + param_name + " value:")
            return CONFIGURE_PARAM


async def configure_choice_param_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    message_data = query.data
    param_name = context.user_data[PARAM]

    job = context.user_data[JOB]

    param = next((param for param in job.params if param.name == param_name), None)
    param.value = message_data

    await query.answer()
    await update.effective_message.edit_text("Configuring " + job.name,
                                             reply_markup=build_job_keyboard(context.user_data[JOB]))

    return CONFIGURE_JOB


async def configure_text_param_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message_data = update.effective_message.text
    param_name = context.user_data[PARAM]

    job = context.user_data[JOB]

    param = next((param for param in job.params if param.name == param_name), None)
    param.value = message_data

    await update.effective_message.reply_text("Configuring " + job.name,
                                              reply_markup=build_job_keyboard(context.user_data[JOB]))

    return CONFIGURE_JOB


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Cya", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def run_and_reply(update: Update, job: Job):
    build_number = await jenkins_svc.run_job_dto(job)
    await update.effective_message.reply_text("Build number is " + str(build_number))


def build_job_keyboard(job: Job):
    keyboard = []
    for param in job.params:
        keyboard.append(
            [InlineKeyboardButton(param.name + ": " + param.value, callback_data=param.name)])

    keyboard.append([InlineKeyboardButton("RUN!", callback_data=RUN)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


def build_param_keyboard(job: Job, param_name: str):
    keyboard = []
    param = next((param for param in job.params if param.name == param_name), None)
    for value in param.availableValues:
        keyboard.append(
            [InlineKeyboardButton(value, callback_data=value)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup
