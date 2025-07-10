import psycopg2
import asyncio
import json



def connection():  # соединение с базой данных
    conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    database='WeatherDB',
    password='admin')
    conn.autocommit = True

    return conn


def create_user(id):  # создание пользователя
    try:
        conn = connection()
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO users (user_id) VALUES ({id})")
            print('Data added...')

    finally:
        if conn:
            conn.close()
            print("Connection closed...")


# async def add_info(min_temp, max_temp, av_temp,  wind_speed, humidity, rain_probability, user_id):  # добавление информации о пользователе
#     try:
#         conn = connection()
#         with conn.cursor() as cur:
#             await cur.execute(
#                 f"""
#                 UPDATE users
#                 SET MinTemp = {min_temp}
#                 WHERE user_id = {user_id};
#                 """
#             )

#     except Exception as ex:
#         print('Exception occured....', ex)

#     finally:
#         if conn:
#             conn.close()
#             print("Connection closed...")





async def selector(condition, id):
    try:
        conn = connection()
        with conn.cursor() as cur:
            data = await cur.execute(
                            f"""
                            SELECT {condition} FROM users
                            WHERE user_id = {id}
                            """)
            return data
        
    except Exception as ex:
        print('Exception occured....', ex)

    finally:
        if conn:
            conn.close()
            print("Connection closed...")


def save_json():
    try:
        with open('json_files/private_jsons/user_1089193715.json') as f:
            data = json.load(f)
        json_string = json.dumps(data)
        print(json_string)
        # conn = connection()
        # with conn.cursor() as cur:
        #     cur.execute(
        #                         f"""
        #                         INSERT INTO users (Forecast) VALUES ({json_string})
        #                         """)
        # print(f'')
    except Exception as ex:
        print('Exception occured....', ex)

    # finally:
    #     if conn:
    #         conn.close()
    #         print("Connection closed...")



