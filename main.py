# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import threading
import RPi.GPIO as GPIO

from waveshare import epd2in9
from weather.service import GetWeatherInfo
# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)
path = os.path.dirname(os.path.realpath(__file__))

print("raspberrypi clock")

WEATHER = {u"小雨": "WXYU.BMP", u"中雨": "WZYU.BMP", u"大雨": "WDYU.BMP", u"暴雨": "WWET.BMP",
           u"晴": "WQING.BMP", u"多云": "WDYZQ.BMP", u"阴": "WYIN.BMP",
           u"雷阵雨": "WLZYU.BMP", u"阵雨": "WYGTQ.BMP",
           u"霾": "WFOG.BMP", u"雾": "WWU.BMP",
           u"雪": "WXUE.BMP", u"雨夹雪": "WYJX.BMP", u"冰雹": "WBBAO.BMP",
           u"月亮": "WMOON.BMP", u"深夜": "WSLEEP.BMP", u"日落": "SUMSET.BMP", u"日出": "SUNRISE.BMP"}

font12 = ImageFont.truetype(path + '/Font.ttc', 12)
font18 = ImageFont.truetype(path + '/Font.ttc', 18)
font24 = ImageFont.truetype(path + '/Font.ttc', 24)
font36 = ImageFont.truetype(path + '/Font.ttc', 36)
font48 = ImageFont.truetype(path + '/Font.ttc', 48)
font60 = ImageFont.truetype(path + '/Font.ttc', 60)
font72 = ImageFont.truetype(path + '/Font.ttc', 72)

try:
    epd = epd2in9.EPD()
    print("init and Clear")
    epd.init(epd.lut_partial_update)
    epd.Clear(0xFF)
    # font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48) # 数字宽度25，半角宽度12
    # font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    # font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)

    # timer = threading.Timer(1, fun_timer)
    # timer.start()
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    firstweather = True
    lastmin = -1
    while (True):
        sec = int(time.strftime('%S'))
        min = int(time.strftime('%M'))
        hour = int(time.strftime('%H'))
        if min != lastmin:
            print("Display Time...")
            draw.rectangle((0, 0, 71, 128), fill = 0)
            draw.text((4, 4), '%02d' % hour, font = font60, fill = 255)
            draw.text((4, 64), '%02d' % min, font = font60, fill = 255)
            newimage = image.crop((0, 0, 71, 128))
            image.paste(newimage, (0, 0))
            lastmin = min
        
        # if hour > 20:
        #     GPIO.output(4, GPIO.HIGH)#BCM
        if hour % 6 == 0 and min <= 0 and sec <= 1:  # 每六小时刷新屏幕
            print("Clear...")
            epd.init(epd.lut_full_update)
            epd.Clear(0xFF)
            epd.init(epd.lut_partial_update)

        if ((sec <= 1 and min <= 0) or firstweather): # 整点
            print("Fetch weather...")
            firstweather = False
            fore, now = GetWeatherInfo()
            weather = now['lives'][0]['weather']
            print(weather)
            if abs(hour - 12) < 6:  # 白天
                cast1 = fore['forecasts'][0]['casts'][0]['nightweather']
                name1 = '今晚'
                cast2 = fore['forecasts'][0]['casts'][1]['dayweather']
                name2 = '明天'
            else:  # 晚上
                cast1 = fore['forecasts'][0]['casts'][1]['dayweather']
                name1 = '明天'
                cast2 = fore['forecasts'][0]['casts'][2]['dayweather']
                name2 = '后天'
            print("Display weather...")
            bmp = Image.open(os.path.join(path + '/bmp', WEATHER[weather]))
            bmp.thumbnail((80, 80))
            image.paste(bmp, (72, 0))
            bmp = Image.open(os.path.join(path + '/bmp', WEATHER[cast1]))
            bmp.thumbnail((36, 36))
            image.paste(bmp, (74, 80))
            draw.text((80, 116), name1, font = font12, fill = 0)
            bmp = Image.open(os.path.join(path + '/bmp', WEATHER[cast2]))
            bmp.thumbnail((36, 36))
            image.paste(bmp, (114, 80))
            draw.text((120, 116), name2, font = font12, fill = 0)
        epd.display(epd.getbuffer(image))
        
        time.sleep(1)
        # Twinkle()
        # time.sleep(0.5)
        

    print("Clear...")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    print("Goto Sleep...")
    epd.sleep()

except IOError as e:
    print(e)

except KeyboardInterrupt:    
    print("ctrl + c:")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)    
    print("Goto Sleep...")
    epd.sleep()
    exit()
