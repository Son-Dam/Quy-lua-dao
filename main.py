import os
import json
import time

from flask import Flask, render_template, jsonify, g
from flask_caching import Cache
from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5
from paho.mqtt.subscribeoptions import SubscribeOptions

from dotenv import load_dotenv
import requests

from dto.CurrentAccountInfoDTO import CurrentAccountInfoDTO
from dto.DealDTO import DealDTO

from Config import Config

load_dotenv()
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  #Cache timeout in seconds
cache = Cache(app)


USERNAME = os.getenv("DNSE_USERNAME")
PASSWORD = os.getenv("DNSE_PASSWORD")

#thông tin tài khoản
def get_current_account_id():
    """
        Returns account Id
    """
    id = getattr(g,'Id', None)
    if id is not None:
        return id
    token = get_token()
    response = requests.get(url="https://services.entrade.com.vn/dnse-order-service/accounts",
                             headers= {"Authorization":f"Bearer {token}"}, timeout=300)
    if(response.status_code == 200):
        
        data = response.json()
        g.Id = data["default"]["id"]
        app.logger.info("Get current account ID succesfully: %s", g.Id)
        return g.Id
    else:
        app.logger.error("Failed to get account ID with error %s", response.status_code)
        return g.Id


def get_investor_id():
    """
        Returns account Id
    """
    id = getattr(g,'investorId', None)
    if id is not None:
        return id
    token = get_token()
    response = requests.get(url="https://services.entrade.com.vn/dnse-user-service/api/me",
                             headers= {"Authorization":f"Bearer {token}"}, timeout=300)
    if(response.status_code == 200):
        
        data = response.json()
        g.investorId = data["investorId"]
        app.logger.info("Get current investor ID succesfully: %s", g.investorId)
        return g.investorId
    else:
        app.logger.error("Failed to get account ID with error %s", response.status_code)
        return g.investorId


def get_token():
    """
        Return the access token for DNSE API
    """
    if cache.has("token"):
        return cache.get("token")
    else:
        body = {
            "username": USERNAME,
            "password": PASSWORD
        }
        response = requests.post("https://services.entrade.com.vn/dnse-auth-service/login",
                                json= body, timeout=300)
        if(response.status_code == 200):
            data = response.json()
            cache.set("token", data["token"])
            
            return data["token"]
        else:
            app.logger.error("Unable to login")
            raise Exception("Unable to login")


def on_connect(client : mqtt_client.Client, userdata, flags, rc, properties=None):
    """
        Handles new connection
    """
    if rc == 0 and client.is_connected():
        app.logger.info("Connected to MQTT Broker!")
        topic_tuple = [(topic, SubscribeOptions(qos=2)) for topic in Config.TOPICS]
        client.subscribe(topic_tuple)
    else:
        app.logger.error(f'Failed to connect, return code {rc}')


def on_disconnect_forever_loop(client: mqtt_client.Client, userdata, rc, properties=None):
    """
        Handles disconnection for MQTT connection that will loop forever
    """
    app.logger.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, Config.FIRST_RECONNECT_DELAY
    while reconnect_count < Config.MAX_RECONNECT_COUNT:
        app.logger.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.username_pw_set(get_investor_id(),get_token())
            client.reconnect()
            app.logger.info("Reconnected successfully!")
            return
        except Exception as err:
            app.logger.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= Config.RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, Config.MAX_RECONNECT_DELAY)
        reconnect_count += 1
    app.logger.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    
def on_disconnect(client: mqtt_client.Client, userdata, rc, properties=None):
    """
        Handles disconnection for MQTT connection that will loop once. Does nothing except logging
    """
    app.logger.info("Disconnected with result code: %s", rc)


def on_message(client: mqtt_client.Client, userdata, msg):
    """
        Handles incoming message
    """
    app.logger.debug('Topic: %s, msg: %s', msg.topic, msg.payload)
    payload = json.JSONDecoder().decode(msg.payload.decode())
    Config.lastest_data[msg.topic] = payload
    app.logger.debug('payload: %s', payload)
    app.logger.debug('symbol: %s',payload["symbol"])




@app.route("/")
def home():
    """Example Hello World route."""
    return render_template("index.html")

@app.route('/get-info',methods=['GET'])
def get_info():
    """
        Returns the information on the account
    """
    token = get_token()
    id = get_current_account_id()
    response = requests.get(f"https://services.entrade.com.vn/dnse-order-service/account-balances/{id}",
                            headers= {"Authorization":f"Bearer {token}"},timeout=300)

    account_data = {}
    if(response.status_code == 200):
        account_data = response.json()
    else:
        app.logger.error("Failed to get account ID with error %s", response.status_code)
        account_data["error"] = "failed to get data"

    deals = [DealDTO.from_api(deal).to_dict() for deal in get_deals()]

    orderIds = []

    for deal in deals:
        orderIds.append(deal["orders"])
    
    orders = get_orders(orderIds)

    market_data = get_mqtt_data()

    return render_template("account.html", account_data = CurrentAccountInfoDTO.from_api(account_data).to_dict(),
                            deals = deals,
                            orders = orders,
                            market_data = market_data)

@app.route('/get-deals',methods=['GET'])
def get_deals():
    """
        Returns the deals from the account
    """
    token = get_token()
    id = get_current_account_id()
    response = requests.get(f"https://services.entrade.com.vn/dnse-deal-service/deals?accountNo={id}",
                            headers= {"Authorization":f"Bearer {token}"},timeout=300)
    deals = []
    if(response.status_code == 200):
        deals = response.json()["deals"]
        Config.TOPICS = ()
        for deal in deals:
            Config.TOPICS += (f'plaintext/quotes/stock/OHLC/1D/{deal["symbol"]}', # Data nến in 1 day
                         f'plaintext/quotes/stock/tick/{deal["symbol"]}', # Data thông tin khớp lệnh của mã
                         f'plaintext/quotes/stock/SI/{deal["symbol"]}', # Data stock info
                         )
    else:
        app.logger.error("Failed to get account's deals with error %s", response.status_code)
        return None
    return deals

@app.route('/get-orders',methods=['GET'])
def get_orders(orderIds: list[str]):
    """
        Returns the deals from the account
    """
    token = get_token()
    id = get_current_account_id()
    response = requests.get(f"https://services.entrade.com.vn/dnse-order-service/v2/orders?accountNo={id}",
                            headers= {"Authorization":f"Bearer {token}"},timeout=300)
    orders = []
    if(response.status_code == 200):
        orders = response.json()["orders"]
    else:
        app.logger.error("Failed to get account's orders with error %s", response.status_code)
    return orders

@app.route('/get-market-data',methods=['GET'])
def get_mqtt_data():
    """
        Returns the deals from the account
    """
    get_deals()
    Config.lastest_data = {}
    app_client = mqtt_client.Client(Config.CLIENT_ID,
                                         protocol=MQTTv5,
                                         transport='websockets')
    app_client.username_pw_set(get_investor_id(), get_token())
    app_client.tls_set_context()
    app_client.ws_set_options(path="/wss")
    app_client.on_connect = on_connect
    app_client.on_message = on_message
    app_client.on_disconnect = on_disconnect

    app_client.connect(Config.BROKER, Config.PORT, keepalive=120)
    app_client.loop_start()
    time.sleep(2)
    app_client.loop_stop()
    app_client.disconnect()
    app.logger.info(app_client.is_connected())

    return Config.lastest_data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
