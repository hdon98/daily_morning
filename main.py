from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
dayOfWeek = datetime.now().isoweekday()

start_date = os.environ['START_DATE']
city = os.environ['CITY']
city_code = os.environ['CITY_CODE']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
weather_template = os.environ["WEATHER_TEMPLATE"]
weather_user = os.environ["WEATHER_USER"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), weather['low'], weather['high'], weather['wind'], weather[
        'airQuality']


def get_lifestyle():
    url = "https://free-api.heweather.net/s6/weather?key=04cd3530b6454d78899e2af9a01d3039&location=" + city_code
    res = requests.get(url).json()
    lifestyle = res['HeWeather6'][0]['lifestyle']
    # 舒适指数，穿衣指数，流感指数，运动指数，出行指数，辐射指数，洗车指数，空气指数
    return lifestyle[0], lifestyle[1], lifestyle[2], lifestyle[3], lifestyle[4], lifestyle[5], lifestyle[7]


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    else:
        return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_day_of_week():
    if dayOfWeek == 1:
        return "一"
    elif dayOfWeek == 2:
        return "二"
    elif dayOfWeek == 3:
        return "三"
    elif dayOfWeek == 4:
        return "四"
    elif dayOfWeek == 5:
        return "五"
    elif dayOfWeek == 6:
        return "六"
    elif dayOfWeek == 7:
        return "七"


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, low, high, wind, airQuality = get_weather()
# 舒适指数，穿衣指数，流感指数，运动指数，出行指数，辐射指数，洗车指数，空气指数
comf, drsg, flu, sport, trav, uv, air = get_lifestyle()
happyWord = "要记住，每天都是快乐的一天！٩(๑^o^๑)۶"
data = {"today": {"value": today.strftime("%Y-%m-%d")},
        "dayOfWeek": {"value": get_day_of_week()},
        "happyWord": {"value": happyWord, "color": "#ffb6b6"},
        "city": {"value": city, "color": "#4dc6f5"},
        "weather": {"value": wea, "color": "#a7dc46"},
        "temperature": {"value": str(int(temperature)) + "℃", "color": "#ef8751"},
        "low": {"value": str(int(low)) + "℃", "color": "#015bb2"},
        "high": {"value": str(int(high)) + "℃", "color": "#ff2518"},
        "wind": {"value": wind}, "airQuality": {"value": airQuality},
        "love_days": {"value": get_count()},
        "birthday_left": {"value": "距离你的生日还有 " + str(get_birthday()) + " 天   (๑♡ω♡๑)", "color": "#002FA7"},

        "words": {"value": get_words(), "color": get_random_color()},
        "comf": {"value": "舒适指数：『" + comf['brf'] + "』 " + comf['txt']},
        "drsg": {"value": "穿衣指数：『" + drsg['brf'] + "』 " + drsg['txt']},
        "flu": {"value": "流感指数：『" + flu['brf'] + "』 " + flu['txt']},
        "sport": {"value": "运动指数：『" + sport['brf'] + "』 " + sport['txt']},
        "trav": {"value": "出行指数：『" + trav['brf'] + "』 " + trav['txt']},
        "uv": {"value": "辐射指数：『" + uv['brf'] + "』 " + uv['txt']},
        "air": {"value": "空气指数：『" + air['brf'] + "』 " + air['txt']},
        }

user_ids = user_id.split(",")
for i in user_ids:
    res = wm.send_template(i, template_id, data)
    print(res)
    
weather_users = weather_user.split(",")
for j in user_ids:
    resp = wm.send_template(j, weather_template, data)
    print(resp)
