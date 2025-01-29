import os

from flask import Flask, render_template, jsonify, g
from flask_caching import Cache

from dotenv import load_dotenv
import requests

from dto.CurrentAccountInfoDTO import CurrentAccountInfoDTO
from MQTTClient import MQTTClient

load_dotenv()
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # Cache timeout in seconds

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
                             headers= {"Authorization":f"Bearer {token}"})
    if(response.status_code == 200):
        app.logger.info("Get current account ID succesfully")
        data = response.json()
        g.Id = data["default"]["id"]
        return g.Id
    else:
        app.logger.error("Failed to get account ID with error "+ response.status_code)
        return g.Id

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

client = MQTTClient(get_current_account_id(),get_token())


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
        app.logger.error(f"Failed to get account ID with error {response.status_code}")
        account_data["error"] = "failed to get data"

    return render_template("account.html", account_data = CurrentAccountInfoDTO.from_api(account_data).to_dict())






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
