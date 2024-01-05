from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import subprocess
import sys

app = Flask(__name__)
socketio = SocketIO(app)

LOG_FOLDER = 'c:/tmp/test'

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

        file_path = event.src_path

        # '.swp' 파일은 처리하지 않음
        if file_path.endswith('.swp'):
            return

        for _ in range(5):  # 최대 5번 시도, 짧은 지연 포함
            try:
                socketio.emit('update_log', {'content': get_log_content(file_path)})
                socketio.emit('update_file_list', {'files': get_file_list()})
                break  # 성공하면 루프를 종료
            except PermissionError:
                print(f"PermissionError: 파일을 읽을 수 없습니다. {file_path}. 다시 시도 중...")
                time.sleep(0.1)  # 잠시 대기한 후 다시 시도
            except FileNotFoundError:
                print(f"FileNotFoundError: 파일이 존재하지 않습니다. {file_path}")
                break  # 파일이 존재하지 않으면 루프 종료
            except Exception as e:
                print(f"Unknown Error: {e}")
                restart_application()

def restart_application():
    print("Restarting the application...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def get_log_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"FileNotFoundError: 파일이 존재하지 않습니다. {file_path}")
        return ""

def get_file_list():
    return os.listdir(LOG_FOLDER)

if __name__ == '__main__':
    observer = Observer()
    observer.schedule(LogFileEventHandler(), path=LOG_FOLDER)
    observer.start()

    try:
        socketio.run(app, host='0.0.0.0', port=10000)
    except Exception as e:
        print(f"Unknown Error: {e}")
