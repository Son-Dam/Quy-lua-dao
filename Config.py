# python 3.11

import random


class Config:
    """
    Application Configuration Class
    """
    BROKER = 'datafeed-lts.dnse.com.vn'
    PORT = 443
    TOPICS = ("plaintext/quotes/derivative/OHLC/1/VN30F1M", #Thông tin nến của VN30
              "plaintext/quotes/stock/tick/+" #Thông tin 
              )
    CLIENT_ID = f'python-json-mqtt-ws-sub-{random.randint(0, 1000)}'
    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60
    lastest_data = {}