import irc.bot
import websockets
import asyncio
import json

class SongRequestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, botnick, server):
        self.channel = channel
        self.botnick = botnick
        self.server = server
        self.websocket = None

        # Setup WebSocket connection
        self.ws_url = "ws://localhost:8080"
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.connect_ws())

        irc.bot.SingleServerIRCBot.__init__(self, [(server, 6667)], botnick, botnick)

    async def connect_ws(self):
        self.websocket = await websockets.connect(self.ws_url)
        print("Connected to WebSocket server.")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        if msg.startswith('!request'):
            song_request = msg[9:].strip()  # Ambil lagu setelah !request
            if song_request:
                self.send_song_request(song_request)

    def send_song_request(self, song):
        if self.websocket:
            message = json.dumps({"song": song})
            asyncio.run(self.websocket.send(message))
            print(f"Requesting song: {song}")
    
    def on_privmsg(self, c, e):
        if e.arguments[0].startswith('!request'):
            song_request = e.arguments[0][9:].strip()  # Ambil lagu setelah !request
            if song_request:
                self.send_song_request(song_request)

if __name__ == "__main__":
    bot = SongRequestBot("#yourchannel", "YourBotNick", "irc.server.com")
    bot.start()
