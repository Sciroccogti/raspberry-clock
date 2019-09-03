import requests
import json
def GetWeatherInfo():
    urlfore = "https://restapi.amap.com/v3/weather/weatherInfo?city=320115&key=2f84cf79e4e4e7b7b055fdb65bdb7d2c&extensions=all"
    urlnow = "https://restapi.amap.com/v3/weather/weatherInfo?city=320115&key=2f84cf79e4e4e7b7b055fdb65bdb7d2c&extensions=base"
    # 昆山：320583
    try:
        respond = requests.get(urlfore)
        data = json.loads(respond.text)
        # #将JSON编码的字符串转换回Python数据结构
        # output result of json
        # print(data)
        return data
    except:
        return None

if __name__ == "__main__":
    data = GetWeatherInfo()
    a = data['forecasts'][0]['casts']
    print(a[0])