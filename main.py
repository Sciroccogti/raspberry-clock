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

WEATHER = {u"小雨": "WXYU.BMP", u"中雨": "WZYU.BMP", u"大雨": "WDYU.BMP", u"暴雨": "WWET.BMP",
           u"晴": "WQING.BMP", u"多云": "WDYZQ.BMP", u"阴": "WYIN.BMP",
           u"雷阵雨": "WLZYU.BMP", u"阵雨": "WYGTQ.BMP",
           u"霾": "WFOG.BMP", u"雾": "WWU.BMP",
           u"雪": "WXUE.BMP", u"雨夹雪": "WYJX.BMP", u"冰雹": "WBBAO.BMP",
           u"月亮": "WMOON.BMP", u"深夜": "WSLEEP.BMP", u"日落": "SUMSET.BMP", u"日出": "SUNRISE.BMP"}


def DisplayTime():
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    time_draw.rectangle((0, 0, 115, 48), fill = 255)
    time_draw.text((0, 0), time.strftime('%H:%M'), font = font48, fill = 0)
    newimage = time_image.crop([0, 0, 115, 50])
    time_image.paste(newimage, (0,0))
    epd.display(epd.getbuffer(time_image))

    time.sleep(0.2)
    time_draw.rectangle((50, 0, 62, 48), fill = 255)
    epd.display(epd.getbuffer(time_image))


try:
    print("raspberry clock")
    epd = epd2in9.EPD()
    print("init and Clear")
    epd.init(epd.lut_partial_update)
    epd.Clear(0xFF)
    font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48) # 数字宽度25，半角宽度12
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)

    # timer = threading.Timer(1, fun_timer)
    # timer.start()
    print("Display time...")
    while (True):
        DisplayTime()
        # if int(time.strftime('%H')) > 20:
        #     GPIO.output(4, GPIO.HIGH)#BCM
        #if int(time.strftime('%S')) <= 1 and int(time.strftime('%M')) <= 0: # 整点
        if True:
            print("Fetch weather...")
            fore, now = GetWeatherInfo()
            weather = now['lives'][0]['weather']
            if abs(int(time.strftime('%H')) - 12) < 6:  # 白天
                forecast = now['lives'][0]['dayweather']
            else:  # 晚上
                forecast = now['lives'][0]['nightweather']
            print("Display weather...")
            image = Image.new('1', (80, 80), 255)
            bmp = Image.open(os.path.join('bmp', WEATHER[weather]))
            bmp.thumbnail((80, 80))
            image.paste(bmp, (0, 48))
            epd.display(epd.getbuffer(image))
        
        time.sleep(0.2)
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
