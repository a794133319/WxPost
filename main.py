from time import time, localtime
import pytz as pytz
import cityinfo
import config
from requests import get, post
from datetime import datetime, date
from bs4 import BeautifulSoup
from zhdate import ZhDate


def get_access_token():
    # appId
    app_id = config.app_id
    # appSecret
    app_secret = config.app_secret
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    print(get(post_url).json())
    access_token = get(post_url).json()['access_token']
    # print(access_token)
    return access_token



# 早安心语
def getzaoan():
    url = 'http://api.tianapi.com/zaoan/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['content']
    else:
        print('请求失败')


# 晚安心语
def getwanan():
    url = 'http://api.tianapi.com/wanan/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['content']
    else:
        print('请求失败')


# 励志古言
def getlzmy():
    url = 'http://api.tianapi.com/lzmy/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['saying']
    else:
        print('请求失败')


# 彩虹屁
def getcaihongpi():
    url = 'http://api.tianapi.com/caihongpi/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['content']
    else:
        print('请求失败')
        
# 网易云
def getwangyiyun():
    url = 'http://api.tianapi.com/hotreview/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['content']
    else:
        print('请求失败')

# 情诗
def getqingshi():
    url = 'http://api.tianapi.com/qingshi/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['content']
    else:
        print('请求失败')        
        
# 英语
def getyingyu():
    url = 'http://api.tianapi.com/everyday/index?key='
    resp = get(url + config.tianxing_key)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]
    else:
        print('请求失败')   

# 空气
def getaqi():
    url = 'http://api.tianapi.com/aqi/index?key='
    resp = get(url + config.tianxing_key + '&area=' + config.city)
    if resp.status_code == 200:
        data = resp.json()
        return data['newslist'][0]['quality']
    else:
        print('请求失败')           
        
        
#获取天气信息
def get_weather(province, city):
    # 城市id
    city_id = cityinfo.cityInfo[province][city]["AREAID"]
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn

# # 犯错记录
# def getError():
    


def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature):
    tz = pytz.timezone('Asia/Shanghai')  # 东八区
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.fromtimestamp(int(time()), tz)
    print(year)
    print(month)
    print(day)
    print(today)
    caihong = getcaihongpi()
   # lizhi = getlzmy()
    wanan = getwanan()
    zaoan = getzaoan()
    wangyiyun = getwangyiyun()
    qingshi = getqingshi()
    yingyu = getyingyu()
    print(yingyu['content'])
    print(yingyu['note'])
    aqi = getaqi()
    if  '污染' in aqi:
        aqi = aqi + ',记得戴口罩哦!'
    week = week_list[today.weekday()]

    # 获取在一起的日子的日期格式
    love_year = int(config.love_date.split("-")[0])
    love_month = int(config.love_date.split("-")[1])
    love_day = int(config.love_date.split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.date().__sub__(love_date)).split(" ")[0]
    # 获取生日的月和日
    birthday_month = int(config.birthday.split("-")[1])
    birthday_day = int(config.birthday.split("-")[2])
    
    #计算生日
    current_year = datetime.date(ZhDate(year,birthday_month,birthday_day).to_datetime())
    today = datetime.date(datetime(year=year, month=month, day=day))
    difference = int(str(current_year.__sub__(today)).split(" ")[0])
    if difference > 0:
        birthday = difference
    else:
        birthday = datetime.date(ZhDate(year+1,birthday_month,birthday_day).to_datetime())
        birthday = int(str(birthday.__sub__(today)).split(" ")[0])

    for i in range(len(to_user)):
        theuser=to_user[i]
        data = {
            "touser": theuser,
            "template_id": config.template_id,
            "url": "https://a794133319.github.io/WxPost/",
            "topcolor": "#FF0000",
            "data": {
                "date": {
                    "value": "{} {}".format(today.strftime('%Y-%m-%d'), week),
                    "color": "#00FFFF"
                },
                "city": {
                    "value": city_name,
                    "color": "#1874CD"
                },
                "weather": {
                    "value": weather,
                    "color": "#ED9121"
                },
                "min_temperature": {
                    "value": min_temperature,
                    "color": "#00FF00"
                },
                "max_temperature": {
                    "value": max_temperature,
                    "color": "#FF6100"
                },
                "love_day": {
                    "value": love_days,
                    "color": "#87CEEB"
                },
                "birthday": {
                    "value": birthday,
                    "color": "#FF8000"
                },
                "zaoan": {
                    "value": zaoan,
                    "color": "#9834eb"
                },
                "caihong": {
                    "value": caihong,
                    "color": "#FF83FA"
                },
                "wangyiyun": {
                    "value": wangyiyun,
                    "color": "#FF83FA"
                },
                "qingshi": {
                    "value": qingshi,
                    "color": "#ed1a80"
                },
                "english_content": {
                    "value": yingyu['content'],
                    "color": "#FF83FA"
                },
                "english_note": {
                    "value": yingyu['note'],
                    "color": "#FF83FA"
                },
                "aqi": {
                    "value": aqi,
                    "color": "#1aaeed"
                }
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        response = post(url, headers=headers, json=data)
        print(response.text)


if __name__ == '__main__':
    # 获取accessToken
    accessToken = get_access_token()
    print('token', accessToken)
    # 接收的用户
    user = config.user
    print('user:',user)
    # 传入省份和市获取天气信息
    province, city = config.province, config.city
    weather, max_temperature, min_temperature = get_weather(province, city)
    # 公众号推送消息
    send_message(user, accessToken, city, weather, max_temperature, min_temperature)
