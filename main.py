import asyncio
import logging
import sys
import json
import os
from dotenv import load_dotenv
import geo_request

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties


default=DefaultBotProperties(parse_mode='HTML')


load_dotenv()
print(os.getenv("BOT_TOKEN"))

bot = Bot(token=(os.getenv('BOT_TOKEN')), default=default)

# все хэндлеры должны быть присоединены к диспетчеру
dp = Dispatcher()


current_dir = os.path.dirname(os.path.abspath(__file__))

def _save(obj, fp):
    with open(fp, 'r+') as f:
        json.dump(obj, f, indent=2)

endings = {1:"", 2 :"а", 3:"а", 4:"а", 5:"ов",
           6:"ов", 7:"ов", 8:"ов", 9:"ов", 10:"ов", 11:"ов", 12:"ов", 13:"ов", 14:"ов", 15:"ов", 16:"ов", 17:"ов", 18:"ов", 19:"ов", 0:"ов"}
def get_ending(value):
    if 9 < abs(value) < 20:
        return endings[abs(value)] 
    else: 
        return endings[abs(value) % 10] 
    

@dp.message(Command('start'))
async def start(message: types.Message):
    button_loc = types.KeyboardButton(text='Отправить локацию', request_location=True)
    buttons = [button_loc]
    # db.create_user(message.chat.id)
    user_path = f"{current_dir}/json_files/private_jsons/user_{message.chat.id}.json"
    if os.path.exists(user_path):
        pass
    else:
        os.mkdir(f'{current_dir}/json_files')
        os.mkdir(f'{current_dir}/json_files/private_jsons')
        data = {"num":0, "UserForecast":{}}
        with open(user_path, 'w') as f:
            json.dump(data, f, indent=2)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[buttons])
    await bot.send_message(message.chat.id, f'Здравствуйте! Этот бот скажет вам погоду на сегодня.'
                                            f' Отправьте мне свою геопозицию, чтобы узнать точный прогноз.'
                                            f' Не забудьте включить геопозицию', reply_markup=keyboard)


@dp.message()  # хандлер на локацию dav
async def location(message: types.Location):
    response = await geo_request.get_meteo(message.location.longitude, message.location.latitude)
    user_path = f"{current_dir}/json_files/private_jsons/user_{message.chat.id}.json"
    with open(user_path, 'r') as path:
        info = json.load(path)
        # print(info)
        info["UserForecast"] = response
    _save(info, user_path)
    # db.save_json(user_path, message.chat.id)
    # print(response)
    min_temp = round((response[3]['DailyForecasts'][0]['Temperature']['Minimum']['Value'] - 32) * 5 / 9)
    max_temp = round((response[3]['DailyForecasts'][0]['Temperature']['Maximum']['Value'] - 32) * 5 / 9)
    av_feel_temp = (round((response[3]['DailyForecasts'][0]['RealFeelTemperature']['Minimum']['Value'] - 32) * 5 / 9) +
    round((response[3]['DailyForecasts'][0]['RealFeelTemperature']['Maximum']['Value'] - 32) * 5 / 9)) // 2

    ending_min = get_ending(min_temp)
    ending_max = get_ending(max_temp)
    ending_av = get_ending(av_feel_temp)

    forward_button = types.InlineKeyboardButton(text="->", callback_data="forward" )
    back_button = types.InlineKeyboardButton(text="<-", callback_data="back")
    buttons = [back_button, forward_button]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

    await bot.send_message(message.chat.id,
                           text=f"Погода в {response[4]} на {response[2]}.{response[1]} {response[0]} года\n"
                                f"<b>Минимальная температура</b>: {min_temp} градус{ending_min}\n"
                                f"<b>Максимальная температура</b>: {max_temp} градус{ending_max}\n"
                                f"<b>Средняя ощущаемая температура</b>: {av_feel_temp} градус{ending_av}", reply_markup=keyboard)
    await bot.delete_message(message.chat.id, message.message_id)

    


@dp.callback_query()  # диспетчер dp с объектом класса call_backquery
async def callback_query_handler(callback_query: types.CallbackQuery):
    # колбэк аннотированный типом класса CallbackQuery, т.к. в класс передается callback_data
    try:
        if callback_query.data == 'forward':
            fp = f'{current_dir}/json_files/private_jsons/user_{callback_query.message.chat.id}.json'
            with open(fp, 'r') as f:
                response = json.load(f)
                if response["num"] < 5:
                    response["num"]+=1
                else:
                    raise IndexError
            _save(response, fp)
            min_temp = round((response["UserForecast"][3]['DailyForecasts'][response['num']]['Temperature']['Minimum']['Value'] - 32) * 5 / 9)
            max_temp = round((response["UserForecast"][3]['DailyForecasts'][response['num']]['Temperature']['Maximum']['Value'] - 32) * 5 / 9)
            av_feel_temp = (round((response["UserForecast"][3]['DailyForecasts'][response['num']]['RealFeelTemperature']['Minimum']['Value'] - 32) * 5 / 9) +
            round((response["UserForecast"][3]['DailyForecasts'][response['num']]['RealFeelTemperature']['Maximum']['Value'] - 32) * 5 / 9)) // 2

            ending_min = get_ending(min_temp)
            ending_max = get_ending(max_temp)
            ending_av = get_ending(av_feel_temp)

            forward_button = types.InlineKeyboardButton(text="->", callback_data="forward" )
            back_button = types.InlineKeyboardButton(text="<-", callback_data="back")
            buttons = [back_button, forward_button]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

            year = response["UserForecast"][3]['DailyForecasts'][response['num']]['Date'][:4]
            month = response["UserForecast"][3]['DailyForecasts'][response['num']]['Date'][5:7]
            day = response["UserForecast"][3]['DailyForecasts'][response['num']]['Date'][8:10]
                
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=f"Погода в {response["UserForecast"][4]} на {day}.{month} {year} года\n<b>Минимальная температура</b>: {min_temp} градус{ending_min}\n<b>Максимальная температура</b>: {max_temp} градус{ending_max}\n<b>Средняя ощущаемая температура</b>: {av_feel_temp} градус{ending_av}",
                                reply_markup=keyboard)

        if callback_query.data == 'back':
            fp = f'{current_dir}/json_files/private_jsons/user_{callback_query.message.chat.id}.json'
            with open(fp, 'r') as f:
                response = json.load(f)
                if response["num"] > -1:
                    response["num"]-=1
                else:
                    raise IndexError
            _save(response, fp)
            min_temp = round((response["UserForecast"][3]['DailyForecasts'][response['num']]['Temperature']['Minimum']['Value'] - 32) * 5 / 9)
            max_temp = round((response["UserForecast"][3]['DailyForecasts'][response['num']]['Temperature']['Maximum']['Value'] - 32) * 5 / 9)
            av_feel_temp = (round((response["UserForecast"][3]['DailyForecasts'][response['num']]['RealFeelTemperature']['Minimum']['Value'] - 32) * 5 / 9) +
            round((response["UserForecast"][3]['DailyForecasts'][response['num']]['RealFeelTemperature']['Maximum']['Value'] - 32) * 5 / 9)) // 2

            ending_min = get_ending(min_temp)
            ending_max = get_ending(max_temp)
            ending_av = get_ending(av_feel_temp)

            forward_button = types.InlineKeyboardButton(text="->", callback_data="forward" )
            back_button = types.InlineKeyboardButton(text="<-", callback_data="back")
            buttons = [back_button, forward_button]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

            year = response["UserForecast"][3]['DailyForecasts'][response['num']]['Date'][:4]
            month = response["UserForecast"][3]['DailyForecasts'][response['num']]['Date'][5:7]
            day = response["UserForecast"][3]['DailyForecasts'][response['num']]['Date'][8:10]
                
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=f"Погода в {response["UserForecast"][4]} на {day}.{month} {year} года\n"
                                f"<b>Минимальная температура</b>: {min_temp} градус{ending_min}\n"
                                f"<b>Максимальная температура</b>: {max_temp} градус{ending_max}\n"
                                f"<b>Средняя ощущаемая температура</b>: {av_feel_temp} градус{ending_av}",
                                reply_markup=keyboard)
            
    except IndexError:
            forward_button = types.InlineKeyboardButton(text="->", callback_data="forward" )
            back_button = types.InlineKeyboardButton(text="<-", callback_data="back")
            buttons = [back_button, forward_button]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                         text='На этот день погода недоступна', reply_markup=keyboard)    


async def main() -> None:  # запуск бота(поллинг)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
