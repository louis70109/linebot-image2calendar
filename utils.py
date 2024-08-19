import os
import re
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai


def is_url_valid(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def check_image(url="https://github.com/louis70109/ideas-tree/blob/master/images/%E5%8F%B0%E5%8C%97_%E5%A4%A7%E7%9B%B4%E7%BE%8E%E5%A0%A4%E6%A5%B5%E9%99%90%E5%85%AC%E5%9C%92/default.png"):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            '''
            請幫我把圖片中的時間、地點、活動標題 以及活動內容提取出來，其中時間區間的格式必須符合 Google Calendar 的格式，像是 20240409T070000Z81/20240409T080000Z。
            如果是中華民國年，請轉換成西元年，例如 110 年要轉換成 2021 年。
            title & content 請用 urlencode 編碼，並且輸出成 JSON 格式，絕對不能有其他多餘的格式，例如：
            {
                "time": "20240409T070000Z",
                "location": "台北市",
                "title": "大直美術館極限公園",
                "content": "這是一個很棒的地方，歡迎大家來參加！"
            }

            ''',
            image
        ])
        return response.text
    return 'None'