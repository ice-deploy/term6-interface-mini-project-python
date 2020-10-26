# Get Started
```bash
# update GPIO-lib to latest-version

# download code
mkdir -p /home/pi/Desktop/dev-path--Pi3/tru-ice/mini-project-bed-motor/ && cd "$_"

git clone https://github.com/ice-deploy/term6-interface-mini-project-python.git v2

# next(Config raspberry Pi)
```

# App Tips
```
- หากติดตั้ง App ไม่ได้(ปัญหา android-auto ใน flutter) ### https://support.google.com/androidauto/thread/8458247?hl=en
    - ให้ clear-cache ของ App [android auto, google play store] ในมือถือ
    - หลังจากนั้น uninstall, reInstall ไฟล์ APK ใหม่
```

# Config raspberry Pi
## linux service(single-process)

<br>

sudo nano /etc/systemd/system/bedmotorApi.service
```bash
/*
[Unit]
Description=mini project ICE06 (ต่อยอด)Bed Motor
After=network.target

[Service]
WorkingDirectory=/home/pi/Desktop/dev-path--Pi3/tru-ice/mini-project-bed-motor/v2/
ExecStart=python3 api.py
Type=simple

Restart=always
RestartSec=2

[Install]
WantedBy=default.target

*/
```

<br>

//sudo systemctl daemon-reload

sudo systemctl enable bedmotorApi

//sudo systemctl disable bedmotorApi

sudo systemctl start bedmotorApi

//sudo systemctl stop bedmotorApi

//sudo systemctl restart bedmotorApi

systemctl status bedmotorApi.service

<br>

# Changelog
API:v2.1.6 

```
- lockThread both(drive_linear_motor.py, api.py)
    
- move API-path: 
    from 
        '/debug/<command>' 
    to 
        '/api/<command>'
```
<br>
fluttApp: 2.1.2

```
- support API-v2.1.6
- add logo [tru.itech]
- fix ip-address Function:
    - move 'show-currentIP' to buttom.
    - save lastSettingIP to SharedPreferences.
    - hidden [port,protocol].
```
