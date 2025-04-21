
import yt_dlp
import asyncio
import websockets
from flask import Flask, request, jsonify

app = Flask(__name__)

clients = []

async def register(websocket):
    clients.append(websocket)

async def unregister(websocket):
    clients.remove(websocket)

async def send_to_clients(message):
    for client in clients:
        await client.send(message)

@app.route('/api/request', methods=['POST'])
def get_audio_url():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
        'extract_flat': 'in_playlist',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            return jsonify({
                'title': info['title'],
                'url': info['url'],
                'webpage_url': info['webpage_url']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/trigger', methods=['POST'])
async def trigger_request():
    data = request.json
    song = data.get('song')
    if not song:
        return jsonify({'error': 'No song provided'}), 400
    
    await send_to_clients(f"New song request: {song}")
    return jsonify({'status': 'success'}), 200

async def handler(websocket, path):
    await register(websocket)
    try:
        while True:
            message = await websocket.recv()
            # Process incoming messages here
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)

def run_server():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(handler, 'localhost', 8080))
    loop.run_forever()

if __name__ == '__main__':
    import threading
    threading.Thread(target=run_server).start()
    app.run(host='0.0.0.0', port=5000)
