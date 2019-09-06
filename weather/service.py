import requests
import json

def GetWeatherInfo():
    '''
    返回fore、now、text
    若text为''，则无报错
    '''
    urlip = "https://restapi.amap.com/v3/ip?key=2f84cf79e4e4e7b7b055fdb65bdb7d2c"
    text = ''
    try:
        respond = requests.get(urlip)
        locate = json.loads(respond.text)
        adcode = locate['adcode']
    except Exception as error:
        adcode = 320115 # 南京
        text += '%s ' % error

    urlfore = "https://restapi.amap.com/v3/weather/weatherInfo?city=%s&key=2f84cf79e4e4e7b7b055fdb65bdb7d2c&extensions=all" % adcode
    urlnow = "https://restapi.amap.com/v3/weather/weatherInfo?city=%s&key=2f84cf79e4e4e7b7b055fdb65bdb7d2c&extensions=base" % adcode
    # 昆山：320583
    try:
        respond = requests.get(urlfore)
        fore = json.loads(respond.text)

        respond = requests.get(urlnow)
        now = json.loads(respond.text)
        # #将JSON编码的字符串转换回Python数据结构
    except Exception as error:
        text += '%s ' % error
        fore = now = None
    return fore, now, text

if __name__ == "__main__":
    fore, now, text = GetWeatherInfo()
    #a = fore['forecasts'][0]['casts']
    print(fore)
    #b = now['lives'][0]
    print(now)
    print(text)
