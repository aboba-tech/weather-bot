import json
import asyncio

file_path = 'json_files/private_jsons/user_1089193715.json'
file_path_output = 'json_files/response.json'


async def getter_func():
# await geo_request.get_meteo()
        with open(file_path, 'r') as file:
                data = json.load(file)
                print(type(data['UserForecast'][3]['DailyForecasts'][0]['Day']['RainProbability']))


if __name__=='__main__':
        asyncio.run(getter_func())




# f"Погода в Москве на {day}.{month} {year} года",
# f"Минимальная температура: {round((data['DailyForecasts'][0]['Temperature']['Minimum']['Value'] - 32) * 5 / 9)} градуса",
# f"Максимальная температура: {round((data['DailyForecasts'][0]['Temperature']['Maximum']['Value'] - 32) * 5 / 9)} градуса",
# f"Минимальная ощущаемая температура: {round((data['DailyForecasts'][0]['RealFeelTemperature']['Minimum']['Value'] - 32) * 5 / 9)} градуса",
# f"Максимальная ощущаемая температура: {round((data['DailyForecasts'][0]['RealFeelTemperature']['Maximum']['Value'] - 32) * 5 / 9)} градуса",

#         year = data['DailyForecasts'][0]['Date'][:4]
#         month = data['DailyForecasts'][0]['Date'][5:7]
#         day = data['DailyForecasts'][0]['Date'][8:10]