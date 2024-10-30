import aiohttp
import asyncio


api_key = 'OrNjAU3uLSxVmqGqU2k9OzK7nUigdz5G'
api_key2= '3AHyoLC7I8em4N9xAPsTYEKR3zS2SBgz'
file_path = 'json_response/response_weather.json '
req_pos = 'json_response/position.json'
API_URL = 'https://dataservice.accuweather.com/'

try:
    async def get_pos(longitude, latitude):
        async with aiohttp.ClientSession() as session:
            headers = {'Accept-Encoding': 'gzip'}
            async with session.get(f'{API_URL}'
                                f'locations/v1/cities/geoposition/search?apikey={api_key2}&q={latitude}%2C{longitude}&language=ru&details=true',
                                headers=headers) as response:  # подставляем динамические значения в запрос
                data = await response.json()
        return data
    
except KeyError:
    async def get_pos(longitude, latitude):
        async with aiohttp.ClientSession() as session:
            headers = {'Accept-Encoding': 'gzip'}
            async with session.get(f'{API_URL}'
                                f'locations/v1/cities/geoposition/search?apikey={api_key2}&q={latitude}%2C{longitude}&language=ru&details=true',
                                headers=headers) as response:  # подставляем динамические значения в запрос
                data = await response.json()
        # print(data)
        return data
    
    








    #         print(data)
    # with open(req_pos, 'w') as file:
    #     json.dump(data, fp=file, indent=3)
if __name__=='__main__':
    asyncio.run(get_pos(37.529, 55.891))
