from aiohttp import ClientSession

import config
import functools

MEASUREMENT_ID = config.MEASUREMENT_ID
API_SECRET = config.API_SECRET


class KeyParams:
    LANG = "language"
    USER_ID = "id"


def analytic_wrapper_with_id(action, request_bool: bool = False):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(user_id):
            answer = await func(user_id)
            if (request_bool and answer) or not request_bool:
                params = {KeyParams.USER_ID: str(user_id)}
                await send_analytics(user_id, action, params)
            return answer
        return wrapped
    return wrapper


def analytic_wrapper_with_message(action: str = "", request_bool: bool = False):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **partial_data):
            answer = await func(*args, **partial_data)
            if (request_bool and answer) or not request_bool:
                message = args[0]
                user_id = message.from_user.id
                params = {KeyParams.USER_ID: str(user_id)}
                action_name = message.text if len(action) == 0 else action
                await send_analytics(user_id, action_name, params)
            return answer
        return wrapped
    return wrapper


async def send_analytics(user_id: int, action: str, params_event: dict = dict()):
    """

    :param user_id: Айди пользователя телеграмм
    :param action: описание события без пробелов!
    :param params_event: доп параметры
    :return:
    """
    params_event['language'] = 'ru'
    params_event['engagement_time_msec'] = '1'
    params = {
        'client_id': str(user_id),
        'user_id': str(user_id),
        'events': [{
            'name': action,
            'params': params_event
        }],
    }
    async with ClientSession() as session:
        await session.post(
            f'https://www.google-analytics.com/'
            f'mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}',
            json=params)
