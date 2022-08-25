from datetime import date, datetime
from zhdate import ZhDate as lunar_date
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random

today = datetime.now()
start_date = '2014-10-23'
city = '北京'
birthday = '04-16'

app_id = 'wx4ae406e43a509399'
app_secret = 'c5a27f0ac787b86d00b8e95a90623282'

user_id = 'oN8p-6XF9LPmHNSMbAVtuIrSU-ls'
# user_id = 'oN8p-6eKgr2ORDzUAV1L4J3M5S6E'
template_id = 'brXJ2SQ91WvwE3G9ihVpNE58OTVHO_YjEt2QGr5htmw'


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  # next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  # print(lunar_date(str(date.today().year), 4, 16))
  next = lunar_date(date.today().year, 4, 16).to_datetime()
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
