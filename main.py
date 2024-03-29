# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import threading
import random
import pigpio # BCM

print("raspberrypi clock")

from waveshare import epd2in9
from weather.service import GetWeatherInfo

path = os.path.dirname(os.path.realpath(__file__))
pin = 4
pi = pigpio.pi()
pi.set_PWM_dutycycle(21, 10) # duty = 32/256, duty <=255/256

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11

WEATHER = {u"小雨": "WXYU.BMP", u"中雨": "WZYU.BMP", u"大雨": "WDYU.BMP", u"暴雨": "WWET.BMP",
           u"晴": "WQING.BMP", u"多云": "WDYZQ.BMP", u"阴": "WYIN.BMP", u"雷阵雨": "WLZYU.BMP",
           u"阵雨": "WYGTQ.BMP", u"霾": "WFOG.BMP", u"雾": "WWU.BMP", u"雪": "WXUE.BMP",
           u"雨夹雪": "WYJX.BMP", u"冰雹": "WBBAO.BMP", u"月亮": "WMOON.BMP", u"深夜": "WSLEEP.BMP",
           u"日落": "SUMSET.BMP", u"日出": "SUNRISE.BMP", u"雨": "WZYU.BMP"}
           
WEEK = {'1': u"一", '2': u"二", '3': u"三", '4': u"四", '5': u"五", '6': u"六", '0': u"日"}

HAPPY = ['^_^', '^o^', '!o!']
SAD = ['-_-', '~_~', 'TAT']

text = ''
err_count = 0

if abs(int(time.strftime('%m')) - 7) < 3:
    maxhum = 60
    minhum = 30
    maxtemp = 28
    mintemp = 23
else:
    maxhum = 80
    minhum = 30
    maxtemp = 25
    mintemp = 18

try:
    fon8 = ImageFont.truetype(path + '/4fun.ttf', 8)
    font8 = ImageFont.truetype(path + '/Font.ttc', 8)
    font12 = ImageFont.truetype(path + '/Font.ttc', 12)
    font24 = ImageFont.truetype(path + '/Font.ttc', 24)
    font48 = ImageFont.truetype(path + '/4fun.ttf', 48)
except Exception as error:
    text += '%s' % error

try:
    epd = epd2in9.EPD()
    print("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    epd.init(epd.lut_partial_update)
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    lastsec = -1
    lastmin = -1
    lasthour = -1
    time.sleep(10)
    while (True):
        sec = int(time.strftime('%S'))
        min = int(time.strftime('%M'))
        hour = int(time.strftime('%H'))
        if min != lastmin:
            print("Display Time...")
            newimage = Image.new('1', (108, 48), 255)
            newdraw = ImageDraw.Draw(newimage)
            print("Fetch DHT11...")
            #humidity = temperature = 66
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            print('%02d' % temperature, '%02d' % humidity)
            newdraw.text((96, 4), '%02d' % temperature, font = fon8, fill = 0)
            newdraw.text((96, 20), '%02d' % humidity, font = fon8, fill = 0)
            if (humidity <= maxhum and humidity >= minhum and temperature <= maxtemp and temperature >= mintemp):
                face = HAPPY[random.randint(0, 2)]
            else:
                face = SAD[random.randint(0, 2)]
            newdraw.text((95, 33), face, font = font8, fill = 0)
            newdraw.text((2, 4), '%02d' % hour, font = font48, fill = 0)
            newdraw.text((50, 4), '%02d' % min, font = font48, fill = 0)
            newimage = newimage.resize((216, 96))
            image.paste(newimage, (0, 0))
        
        if sec <= 1 or lasthour == -1:
            print("setting LED")
            t = hour + min / 60
            if hour < 8:
                pi.set_PWM_dutycycle(21, t * t * 2)
            elif hour >= 18:
                pi.set_PWM_dutycycle(21, (24 - t) * (24 - t) * 2)
            else:
                pi.set_PWM_dutycycle(21, 0)

        if hour % 6 == 0 and min <= 0 and sec <= 1:  # 每六小时刷新屏幕
            print("Clear...")
            epd.init(epd.lut_full_update)
            epd.Clear(0xFF)
            epd.init(epd.lut_partial_update)

        if (err_count > 0 and err_count < 10 and lastsec != sec and lastsec != -1) or lasthour != hour: # 整点 or error lasttime
            print("err_count=" , err_count)
            print("Fetch weather...")
            fore, now, weathertext = GetWeatherInfo()
            text += weathertext
            if text == '':  # 输出天气
                weather = now['lives'][0]['weather']
                print(weather)

                if abs(hour - 12) < 6:  # 白天
                    cast1 = fore['forecasts'][0]['casts'][0]['nightweather']
                    name1 = '今晚'
                    cast2 = fore['forecasts'][0]['casts'][1]['dayweather']
                    name2 = '明天'
                elif hour <= 6:
                    cast1 = fore['forecasts'][0]['casts'][0]['dayweather']
                    name1 = '今早'
                    cast2 = fore['forecasts'][0]['casts'][0]['nightweather']
                    name2 = '今晚'
                else:  # 晚上
                    cast1 = fore['forecasts'][0]['casts'][1]['dayweather']
                    name1 = '明天'
                    cast2 = fore['forecasts'][0]['casts'][2]['dayweather']
                    name2 = '后天'

                print("Display weather...")
                draw.rectangle((216, 0, 296, 128), fill = 255)
                try:  # 加载天气图片
                    bmp = Image.open(os.path.join(path + '/bmp', WEATHER[weather]))
                    bmp.thumbnail((80, 80))
                    image.paste(bmp, (216, 0))

                    bmp = Image.open(os.path.join(path + '/bmp', WEATHER[cast1]))
                    bmp.thumbnail((36, 36))
                    image.paste(bmp, (218, 80))
                    draw.text((224, 116), name1, font = font12, fill = 0)

                    bmp = Image.open(os.path.join(path + '/bmp', WEATHER[cast2]))
                    bmp.thumbnail((36, 36))
                    image.paste(bmp, (258, 80))
                    draw.text((264, 116), name2, font = font12, fill = 0)
                except Exception as error:
                    text += '%s ' % error

                if text == '':  # 输出其它天气信息
                    draw.rectangle((0, 96, 214, 127), fill = 255, outline = 0)
                    info = '%2s°C %2s%% ' % (now['lives'][0]['temperature'], now['lives'][0]['humidity'])
                    #info = '%2d°C %2d%% ' % (temperature, humidity)
                    info += time.strftime('%m/%d ')
                    info += '%s' % WEEK[time.strftime('%w')]
                    draw.text((4, 98), info, font = font24, fill = 0)
        
        if text != '':
            text = str(err_count) + text
            draw.rectangle((0, 100, 216, 128), fill = 255)
            draw.text((0, 100), text, font = font24, fill = 0)
            err_count += 1
            text = ''  # 清空报错信息
            if err_count >= 10:
                sys.exit(0)
        else:
            err_count = 0

        epd.display(epd.getbuffer(image))
        time.sleep(1)
        lastsec = sec
        lastmin = min
        lasthour = hour

    print("Clear...")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    print("Goto Sleep...")
    epd.sleep()

except IOError as e:
    print(e)

except KeyboardInterrupt:    
    print("ctrl + c:")
    pi.set_PWM_dutycycle(21, 0)
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)    
    print("Goto Sleep...")
    epd.sleep()
    exit()

except:
    epd.init(epd.lut_full_update)
    pi.set_PWM_dutycycle(21, 0)
    epd.Clear(0xFF)
    print("Goto Sleep...")
    epd.sleep()
    exit()
