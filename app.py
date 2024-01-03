from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

app = Flask(__name__)
socketio = SocketIO(app)

LOG_FOLDER = 'C:/tmp/test'

@app.route('/')
def index():
    files = get_file_list()
    return render_template('index.html', files=files)

@app.route('/logs/<filename>')
def show_log(filename):
    return render_template('log_detail.html', filename=filename)

@socketio.on('get_log')
def get_log(data):
    file_path = os.path.join(LOG_FOLDER, data['file'])
    with open(file_path, 'r') as file:
        log_content = file.read()
        socketio.emit('update_log', {'content': log_content})

@socketio.on('get_file_list')
def get_file_list():
    files = os.listdir(LOG_FOLDER)
    socketio.emit('update_file_list', {'files': files})

class LogFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        socketio.emit('update_log', {'content': get_log_content(event.src_path)})
        socketio.emit('update_file_list', {'files': get_file_list()})

def get_file_list():
    return os.listdir(LOG_FOLDER)

def get_log_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == '__main__':
    observer = Observer()
    observer.schedule(LogFileEventHandler(), path=LOG_FOLDER)
    observer.start()

    socketio.run(app, host='0.0.0.0', port=10000)
