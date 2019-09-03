import requests
import json

def GetWeatherInfo():
    '''返回fore和now'''
    urlfore = "https://restapi.amap.com/v3/weather/weatherInfo?city=320115&key=2f84cf79e4e4e7b7b055fdb65bdb7d2c&extensions=all"
    urlnow = "https://restapi.amap.com/v3/weather/weatherInfo?city=320115&key=2f84cf79e4e4e7b7b055fdb65bdb7d2c&extensions=base"
    # 昆山：320583
    try:
        respond = requests.get(urlfore)
        fore = json.loads(respond.text)
        # print(fore)
        respond = requests.get(urlnow)
        now = json.loads(respond.text)
        # print(now)
        # #将JSON编码的字符串转换回Python数据结构
        # output result of json
        # print(data)
        return fore, now
    except:
        return None, None

if __name__ == "__main__":
    fore, now = GetWeatherInfo()
    #a = fore['forecasts'][0]['casts']
    print(fore)
    #b = now['lives'][0]
    print(now)
