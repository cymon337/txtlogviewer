# txt 로그 뷰어

## 개요
- txt 파일로 저장되는 로그를 실시간으로 웹페이지에서 보여준다.

## 기능
- 개발언어: python
- ubuntu22.04 서버의 /tmp/test 폴더에 txt 파일로 저장되는 로그를 웹페이지에서 보여준다.
- 웹브라우저 에서 server-ip 에 10000번 포트로 접속하면 /tmp/test 폴더내의 텍스트 파일 리스트를 보여준다.
- 리스트의 텍스트 파일을 클릭하면 파일의 내용을 채팅창 처럼 socket stream으로 실시간 업데이트 하여 로그가 업데이트되는것을 확인할 수 있도록 한다.
- 파일 리스트는 변화를 감지하여 실시간으로 업데이트해준다.
- 파일 내용은 변화를 감지하여 실시간으로 업데이트해준다.
- 서버에 서비스로 등록하고 venv 가상환경에서 실행된다.

##
```bash
pip freeze > requirements.txt

pip install -r requirements.txt
```

## 서비스파일
```bash
sudo vi /etc/systemd/system/txtlogviewer.service
```

```txtlogviewer.service
[Unit]
Description=Text Log Viewer
After=network.target

[Service]
ExecStart=/home/tkmtlab/apps/txtlogviewer/venv/bin/python /home/tkmtlab/apps/txtlogviewer/app.py
WorkingDirectory=/home/tkmtlab/apps/txtlogviewer
User=tkmtlab
Group=tkmtlab
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start txtlogviewer
sudo systemctl enable txtlogviewer

sudo journalctl -u txtlogviewer #  로그확인
```

