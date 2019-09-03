# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

from waveshare.epd2in9 import epd2in9
# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

try:
    logging.info("raspberry clock")
    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_partial_update)
    epd.Clear(0xFF)
    font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
    time_image = Image.new('1', (epd2in9.EPD_HEIGHT, epd2in9.EPD_WIDTH), 255)
    time_draw = ImageDraw.Draw(time_image)


    while (True):
        time_draw.rectangle((0, 0, 120, 50), fill = 255)
        time_draw.text((0, 0), time.strftime('%H:%M'), font = font48, fill = 0)
        newimage = time_image.crop([0, 0, 120, 50])
        time_image.paste(newimage, (0,0))
        epd.display(epd.getbuffer(time_image))
#        time_draw.rectangle((48, 50, 12, 50), fill = 255)
#        newimage = time_image.crop([48, 50, 12, 50])
#        time_image.paste(newimage, (0,0))
#        epd.display(epd.getbuffer(time_image))

    epd.sleep()

except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()
