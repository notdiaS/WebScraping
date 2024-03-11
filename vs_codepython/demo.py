server_url = "https://teknolojivehavacilik.com.tr/imgphub"

import logging
import sys
sys.path.append("./")
from signalrcore.hub_connection_builder import HubConnectionBuilder


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


# server_url = input_with_default('Enter your server url(default: {0}): ', "https://teknolojivehavacilik.com.tr/imgphub")
# username = input_with_default('Enter your username (default: {0}): ', "said")
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
    .with_automatic_reconnect({
            "type": "interval",
            "keep_alive_interval": 10,
            "intervals": [1, 3, 5, 6, 7, 87, 3]
        }).build()

hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
hub_connection.on_close(lambda: print("connection closed"))

hub_connection.on("GetInfo", print)
hub_connection.start()
message = None


while message != "exit()":
    message = input(">> ")
    if message is not None and message != "" and message != "exit()":
        hub_connection.send("SendInfo", [message])


hub_connection.stop()

sys.exit(0)