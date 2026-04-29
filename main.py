import anthropic
from kiteconnect import KiteConnect

# ---- Zerodha Kite Setup ----
api_key = "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"
api_secret = "your_kite_api_secret"
request_token = "your_request_token"  # Get this after login

kite = KiteConnect(api_key=api_key)

# Generate access token
data = kite.generate_session(request_token, api_secret=api_secret)
kite.set_access_token(data["access_token"])

# ---- Claude AI Setup ----
claude = anthropic.Anthropic(api_key="your_claude_api_key")

# ---- Fetch Market Data from Zerodha ----
def get_market_data(symbol="NSE:RELIANCE"):
    quote = kite.quote([symbol])
    price = quote[symbol]["last_price"]
    ohlc = quote[symbol]["ohlc"]
    return {
        "symbol": symbol,
        "last_price": price,
        "open": ohlc["open"],
        "high": ohlc["high"],
        "low": ohlc["low"],
        "close": ohlc["close"]
    }

# ---- Ask Claude to Analyze the Data ----
def analyze_with_claude(market_data):
    prompt = f"""
    You are a stock market analyst. Analyze this market data and give a 
    BUY, SELL, or HOLD recommendation with a brief reason.
    
    Stock: {market_data['symbol']}
    Last Price: ₹{market_data['last_price']}
    Open: ₹{market_data['open']}
    High: ₹{market_data['high']}
    Low: ₹{market_data['low']}
    Previous Close: ₹{market_data['close']}
    
    Respond in this format:
    Decision: BUY/SELL/HOLD
    Reason: (2-3 lines)
    """
    
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# ---- Place Order Based on Claude's Decision ----
def place_order(symbol, decision):
    if decision == "BUY":
        order_id = kite.place_order(
            tradingsymbol="RELIANCE",
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=1,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS  # Intraday
        )
        print(f"✅ BUY Order placed! Order ID: {order_id}")
    
    elif decision == "SELL":
        order_id = kite.place_order(
            tradingsymbol="RELIANCE",
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=1,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS
        )
        print(f"✅ SELL Order placed! Order ID: {order_id}")
    
    else:
        print("⏸ HOLD - No order placed.")

# ---- Main Flow ----
if __name__ == "__main__":
    # 1. Get market data
    data = get_market_data("NSE:RELIANCE")
    print(f"📊 Market Data: {data}")
    
    # 2. Claude analyzes
    analysis = analyze_with_claude(data)
    print(f"\n🤖 Claude's Analysis:\n{analysis}")
    
    # 3. Extract decision
    decision_line = [l for l in analysis.split('\n') if 'Decision:' in l]
    if decision_line:
        decision = decision_line[0].split(':')[1].strip()
        
        # 4. Place order (optional - uncomment to enable auto trading)
        # place_order("RELIANCE", decision)
