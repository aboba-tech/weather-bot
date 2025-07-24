
import aiohttp
import asyncio
from geo_pos import get_pos


api_key = 'OrNjAU3uLSxVmqGqU2k9OzK7nUigdz5G'
api_key2= '3AHyoLC7I8em4N9xAPsTYEKR3zS2SBgz'
file_path = 'json_files/response_weather.json '
req_pos = 'json_files/position.json'
API_URL = 'https://dataservice.accuweather.com/'

try:
    async def get_meteo(longitude, latitude):
        location = await get_pos(longitude, latitude)
        region_key = location['Key'] 
        town = location['LocalizedName']
        async with aiohttp.ClientSession() as session:
            headers = {'Accept-Encoding': 'gzip'}
            async with session.get(f'{API_URL}'
                                f'forecasts/v1/daily/5day/{region_key}?apikey={api_key2}&language=ru&details=true',
                                headers=headers) as response:  # подставляем динамические значения в запрос
                data = await response.json()

                year = data['DailyForecasts'][0]['Date'][:4]
                month = data['DailyForecasts'][0]['Date'][5:7]
                day = data['DailyForecasts'][0]['Date'][8:10]

        return year, month, day, data, town
    
except KeyError:
    async def get_meteo(longitude, latitude):
        location = await get_pos(longitude, latitude)
        region_key = location['Key'] 
        town = location['LocalizedName']
        async with aiohttp.ClientSession() as session:
            headers = {'Accept-Encoding': 'gzip'}   
            async with session.get(f'{API_URL}'
                                f'forecasts/v1/daily/5day/{region_key}?apikey={api_key2}&language=ru&details=true',
                                headers=headers) as response:  # подставляем динамические значения в запрос
                data = await response.json()
                year = data['DailyForecasts'][0]['Date'][:4]
                month = data['DailyForecasts'][0]['Date'][5:7]
                day = data['DailyForecasts'][0]['Date'][8:10]

        return year, month, day, data, town
    


if __name__=='__main__':
    asyncio.run(get_meteo(37.529, 55.891, 1089193715))

# locations/v1/cities/geoposition/search?apikey={api_key}={longitude}%2C{latitude}&language=ru&details=true
# mini_temp = round((data['DailyForecasts'][0]['Temperature']['Minimum']['Value'] - 32) * 5 / 9)
# maxi_temp = round((data['DailyForecasts'][0]['Temperature']['Maximum']['Value'] - 32) * 5 / 9)
# av_feel_temp = (round((data['DailyForecasts'][0]['RealFeelTemperature']['Minimum']['Value'] - 32) * 5 / 9) + round((data['DailyForecasts'][0]['RealFeelTemperature']['Maximum']['Value'] - 32) * 5 / 9)) // 2
# windspeed= round(data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'] * 0.44704)
# humid = data['DailyForecasts'][0]['Day']["RelativeHumidity"]['Average']
# rain = data['DailyForecasts'][0]['Day']["RainProbability"]
