"""
    ----------RUNNING FLASK DEV SERVER----------
    1. Environment Variable:
                    export FLASK_APP=app.py  (for Linux/Mac)
                    set FLASK_APP=app.py  (for Windows)
                    flask run
    2. Programmatically:
                    create a "if __name__ == '__main__'" section within app.py
                    python app.py
    
    ----------DEBUGGING IN FLASK----------
    export/set FLASK_DEBUG=1 (OR) app.run(debug=True)
    1. Reloader:
            - Watches all file changes
            - Sever automatically restarts and reflects the change when a modified file is saved
    2. Debugger:
            - Web based tool
            - Interactive stacktrace

    ----------FLASK COMMAND LINE OPTIONS----------
    1. flask --help: general utility
    2. flask run --help: can set runtime parameters
"""

from flask import Flask, request, send_from_directory
from speech_to_text_speaker_diarization import start
import json
import os

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'


@app.route('/')
def index():
    txt = "List of APIs:\n1. Help\n\troute: /\n\tparameters: none\n2. Transcription\n\troute: /transcribe\n\tparameters: .wav file"
    return txt

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio_file = request.files["audio_file"]
    audio_file.save(os.path.join(app.config['DOWNLOAD_FOLDER'], audio_file.filename))
    audio_file = os.path.dirname(os.path.abspath(__file__)) + '/downloads/recording.wav'
    j = start(audio_file)
    return json.loads(j)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/<str>')
def test(str):
    return f"Hi {str}"


if __name__ == '__main__':
    app.run(debug=True)