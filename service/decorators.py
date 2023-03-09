from functools import wraps

from service.config import config

# TODO Find a proper way to read value from env variable and default it to something if it's not set
# Like ${ENV_VAR:default_value} in java spring-boot
allowed_users = config.get('telegram', 'allowed-users').split(',')
if len(allowed_users) == 1 and allowed_users[0] == "$ALLOWED_USERS":
    allowed_users = []


def restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""

    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        print("User " + str(user_id))
        if len(allowed_users) != 0 and str(user_id) not in allowed_users:
            await update.message.reply_text("You're not authorized. Shoo!")
            return  # quit function
        return await func(update, context, *args, **kwargs)

    return wrapped
