import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send("{\"type\":\"heartbeat\",\"args\":[]}")
    ws.send("{\"type\":\"login\",\"args\":{\"client_key\":\"\"}}")
    ws.send("{\"type\":\"room\",\"args\":{\"room_id\":184766222994}}")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://webcast.amemv.com", on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()