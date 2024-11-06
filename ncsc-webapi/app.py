from flask import *
import random
import base64
import time

class Sessions:
    session_dict = {}
    def __init__( self, max_size = 500 ):
        self.max_size = max_size

    def create_session( self, expiration = 14400 ):
        self.del_expired_session()
        session_id = base64.urlsafe_b64encode( random.randbytes( 32 ) ).decode().strip( "=" )
        expiration_date = int( time.time() ) + expiration
        new_session = { "session_id": session_id, "expiration_date": expiration_date }
        self.session_dict[session_id] = new_session
        if len( self.session_dict ) >= self.max_size:
            most_past_session = new_session
            for session in self.session_dict.values():
                if most_past_session["expiration_date"] > session["expiration_date"]:
                    most_past_session = session
            if most_past_session == new_session:
                del self.session_dict[most_past_session["session_id"]]
                raise Exception
            del self.session_dict[most_past_session["session_id"]]
        return new_session

    def get_session( self, session_id ):
        self.del_expired_session()
        if not session_id in self.session_dict:
            raise Exception
        session = self.session_dict[session_id]
        return session

    def del_expired_session( self ):
        for session_id in list( self.session_dict ):
            now = int( time.time() )
            if now > self.session_dict[session_id]["expiration_date"]:
                del self.session_dict[session_id]

    def del_session( self, session_id ):
        self.del_expired_session()
        del self.session_dict[session_id]

class Stocks:
    def __init__( self ):
        self.last_update_time = int( time.time() )
        self.bought_motive_velocity = 0.5
        self.bought_motive_range = 0.2
        self.price_range = 5000
        self.cataclysm_shreshold = 0.05
        self.crash_control = 4;
        self.stock_dict = {}
        self.add_stock( "AAA", 100.00 )
        self.add_stock( "BBB", 300.00 )
        self.add_stock( "CCC", 500.00 )
        self.add_stock( "DDD", 1000.00 )
        self.add_stock( "EEE", 2000.00 )
        self.add_stock( "FFF", 5000.00 )
        self.add_stock( "FLAG", 100000 )

    def exist_stock( self, stock_name ):
        return stock_name in self.stock_dict

    def add_stock( self, stock_name, price ):
        self.stock_dict[stock_name] = { "stock_name": stock_name, "price": price, "trend": pow( -1, random.randrange( 0, 2 ) ) * pow( random.random(), 2 ) }

    def update_stocks( self ):
        now = int( time.time() )
        duration = now - self.last_update_time
        self.last_update_time = now
        for _ in range( 0, duration + 1 ):
            for stock in self.stock_dict.values():
                if stock["stock_name"] == "FLAG":
                    continue
                if stock["price"] > self.price_range or stock["trend"] > self.bought_motive_velocity:
                    bought_motive = 0
                else:
                    bought_motive = self.price_range - int( stock["price"] * ( 1 - pow( self.bought_motive_velocity, self.crash_control ) + stock["trend"] ) )

                if random.random() < self.cataclysm_shreshold:
                    stock["trend"] = pow( -1, random.randrange( 0, 2 ) ) * random.random() * self.bought_motive_range * 5
                else:
                    stock["trend"] += pow( -1, 1 - int( random.randrange( bought_motive, bought_motive + self.price_range ) // self.price_range ) ) * pow( random.random() * self.bought_motive_velocity, self.crash_control )
                volatility = random.random() * self.bought_motive_range * 2 - self.bought_motive_range + stock["trend"]
                stock["price"] = round( stock["price"] * ( 1 + volatility / 100 ), 2 )

    def get_stocks_price( self ):
        self.update_stocks()
        stocks_price = []
        for stock in self.stock_dict.values():
            stocks_price += [ { "stock_name": stock["stock_name"], "price": stock["price"] } ]
        return stocks_price

    def get_stock_price( self, stock_name ):
        self.update_stocks()
        if not stock_name in self.stock_dict:
            raise Exception
        return self.stock_dict[stock_name]["price"]

app = Flask(__name__)
sessions = Sessions()
stocks = Stocks()

def spend_session_credit( session ):
    if "access_credit" in session:
        session["access_credit"] -= 1
        if session["access_credit"] == 0:
            sessions.del_session( session["session_id"] )

@app.route('/api/create_account', methods = ["GET"])
def create_account():
    try:
        session = sessions.create_session( expiration = 1800 )
        session["wallet"] = { "JPY": 2000 }
        session["access_credit"] = 5000
    except Exception as e:
        return jsonify( { "session_id": None } )
    return jsonify( { "session_id": session["session_id"] } )

@app.route('/api/get_wallet', methods = ["POST"])
def get_wallet():
    try:
        session_info = request.get_json()
        if not "session_id" in session_info:
            raise Exception
        session = sessions.get_session( session_info["session_id"] )
        spend_session_credit( session )
    except Exception as e:
        return jsonify( { "wallet": None } )
    appraised_price = session["wallet"]["JPY"]
    for stock_name in session["wallet"]:
        if stocks.exist_stock( stock_name ):
            appraised_price += stocks.get_stock_price( stock_name ) * session["wallet"][stock_name]
    return jsonify( { "wallet": session["wallet"], "appraised_price": round( appraised_price ) } )

@app.route('/api/get_stocks_price', methods = ["GET"])
def get_stocks_price():
    stocks_price = stocks.get_stocks_price()
    return jsonify( { "stocks_price": stocks_price } )

@app.route('/api/get_stock_price', methods = ["POST"])
def get_stock_price():
    try:
        stock_info = request.get_json()
        if not "stock_name" in stock_info:
            raise Exception
        price = stocks.get_stock_price( stock_info["stock_name"] )
    except Exception as e:
        return jsonify( { "price": None } )
    return jsonify( { "price": price } )

@app.route('/api/get_sample_contract_price', methods = ["POST"])
def get_sample_contract_price():
    try:
        contract_info = request.get_json()
        if not "stock_name" in contract_info or not "quantity" in contract_info:
            raise Exception
        stock_name = contract_info["stock_name"]
        price = stocks.get_stock_price( stock_name )
        quantity = int( contract_info["quantity"] )
        sample_contract_price = int( quantity * price )
    except Exception as e:
        return jsonify( { "sample_contract_price": None } )
    return jsonify( { "stock_name": stock_name, "quantity": quantity, "price": price, "sample_contract_price": sample_contract_price } )

@app.route('/api/purchase_stock', methods = ["POST"])
def purchase_stock():
    try:
        purchase_info = request.get_json()
        if not "session_id" in purchase_info or not "stock_name" in purchase_info or not "quantity" in purchase_info:
            raise Exception
        session = sessions.get_session( purchase_info["session_id"] )
        stock_name = purchase_info["stock_name"]
        quantity = int( purchase_info["quantity"] )
        price = stocks.get_stock_price( stock_name )
        if quantity <= 0:
            spend_session_credit( session )
            info = "Invalid quantity."
            return jsonify( { "info": info, "stock_name": stock_name, "quantity": None, "price": price, "contracted_price": None } )

        contract_price = int( quantity * price )
        if contract_price > session["wallet"]["JPY"]:
            spend_session_credit( session )
            info = "Insufficient balance."
            return jsonify( { "info": info, "stock_name": stock_name, "quantity": quantity, "price": price, "contracted_price": None } )
    except Exception as e:
        info = "Contract could not execute for some reason."
        return jsonify( { "info": info, "stock_name": None, "quantity": None, "price": None, "contracted_price": None } )

    session["wallet"]["JPY"] -= contract_price
    if stock_name in session["wallet"]:
        session["wallet"][stock_name] += quantity
    else:
        session["wallet"][stock_name] = quantity
    spend_session_credit( session )
    info = "Contract was successfully executed."
    if stock_name == "FLAG":
        info += " flag{earn_and_earn_by_day_trading}"
    return jsonify( { "info": info, "stock_name": stock_name, "quantity": quantity, "price": price, "contracted_price": contract_price } )

@app.route('/api/sell_stock', methods = ["POST"])
def sell_stock():
    try:
        sell_info = request.get_json()
        if not "session_id" in sell_info or not "stock_name" in sell_info or not "quantity" in sell_info:
            raise Exception
        session = sessions.get_session( sell_info["session_id"] )
        stock_name = sell_info["stock_name"]
        price = stocks.get_stock_price( stock_name )
        quantity = int( sell_info["quantity"] )
        if quantity <= 0:
            spend_session_credit( session )
            info = "Invalid quantity."
            return jsonify( { "info": info, "stock_name": stock_name, "quantity": None, "price": price, "contracted_price": None } )

        contract_price = int( quantity * price )
        if not stock_name in session["wallet"] or quantity > session["wallet"][stock_name]:
            spend_session_credit( session )
            info = "Insufficient stock."
            return jsonify( { "info": info, "stock_name": stock_name, "quantity": quantity, "price": price, "contracted_price": None } )
    except Exception as e:
        info = "Contract could not execute for some reason."
        return jsonify( { "info": info, "stock_name": None, "quantity": None, "price": None, "contracted_price": None } )

    session["wallet"]["JPY"] += contract_price
    session["wallet"][stock_name] -= quantity
    spend_session_credit( session )
    info = "Contract was successfully executed."
    return jsonify( { "info": info, "stock_name": stock_name, "quantity": quantity, "price": price, "contracted_price": contract_price } )

if __name__ == "__main__":
    app.run( debug = True, host = "0.0.0.0", port = 10000 )
