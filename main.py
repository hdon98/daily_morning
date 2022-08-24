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
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), weather['low'], weather['high'], weather['wind'], weather[
        'airQuality']


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
        "words": {"value": get_words(), "color": get_random_color()}}

user_ids = user_id.split(",")
for i in user_ids:
    res = wm.send_template(i, template_id, data)
    print(res)

