from flask import Flask, request, send_file
import yt_dlp, uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data['url']
    bitrate = data.get('bitrate', '192')

    file_id = str(uuid.uuid4())

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{file_id}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate,
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(f"{file_id}.mp3", as_attachment=True)

if __name__ == '__main__':
    app.run()