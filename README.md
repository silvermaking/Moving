# **6기 2학기 특화PJT(22/02/21 ~ 22/04/8)**

## **광주 2반 6팀 워라벨없는 워라벨팀(C206)**

## Contents

[프로젝트 주제](## 프로젝트-주제) 

[빌드 및 배포](##빌드-및-배포)

## 프로젝트 주제

사용자 평점 기반 빅데이터 영화 추천 서비스

![moving_main](https://user-images.githubusercontent.com/68841702/170449675-e944dc91-22d1-45db-8119-66bf5fdb80c1.png)

![image](https://user-images.githubusercontent.com/68841702/170447435-a1b3cdf0-eb09-4681-b94a-d6c6859d7933.png)

## 기획

![image](https://user-images.githubusercontent.com/68841702/170447574-fbc4ed70-b538-4c7e-85f2-bd5bdf1c36eb.png)

### 기술스택

### Front-End

![image](https://user-images.githubusercontent.com/68841702/170447887-d8f44bb4-6ec3-44c0-af15-2fce97c0061a.png)

### Back-End

![image](https://user-images.githubusercontent.com/68841702/170447932-127111da-4300-4fec-afcd-ac83b159960c.png)



### E-R Diagram

![image](https://user-images.githubusercontent.com/68841702/170448829-3f92ef6a-d540-4a4d-8e81-8942e9d9a431.png)



## 빌드 및 배포

### 프론트엔드

front 빌드 및 배포 순서

1. npm run build
2. sudo npx pm2 start npm -- start (무중단 배포)
3. sudo npx pm2 kill (중단)



### 백엔드

1. 사용한 JVM, 웹서버

   - python 3.7.9 version , Django 3.2.3 version
   - 웹서버 : Amazon EC2

2. WAS 제품 등의 종류와 설정값

   - uWSGI

     ```ini
     // server.ini
     
     [uwsgi]
     chdir = /home/ubuntu/S06P22C206/back/
     module = server.wsgi:application
     home = /home/ubuntu/S06P22C206/back/venv/
     
     uid = ubuntu
     gid = ubuntu
     
     socket = /tmp/server.sock
     chmod-socket = 666
     chown-socket = ubuntu:ubuntu
     
     enable-threads = true
     master = true
     vacuum = true
     pidfile = /tmp/project_name.pid
     logto = /var/log/uwsgi/server/@(exec://date +%%Y-%%m-%%d).log
     log-reopen = true
     ```

     ```plaintext
     // uwsgi.service
     
     [Unit]
     Description=uWSGI service
     After=syslog.target
     
     [Service]
     ExecStart=/home/ubuntu/S06P22C206/back/venv/bin/uwsgi -i /home/ubuntu/S06P22C206/back/.config/uwsgi/server.ini
     
     Restart=always
     KillSignal=SIGQUIT
     Type=notify
     StandardError=syslog
     NotifyAccess=all
     
     [Install]
     WantedBy=multi-user.target
     ```

   - Nginx

     ```conf
     // server.conf
     
     server {
         listen 8000;
         server_name *.compute.amazonaws.com;
         charset utf-8;
         client_max_body_size 128M;
     
         location / {
             uwsgi_pass  unix:///tmp/server.sock;
             include     uwsgi_params;
         }
     
         location /static/ {
             alias /home/ubuntu/S06P22C206/back/static/;
         }
     }
     ```

1. 배포 시 특이사항 기재

   - 코드가 수정되어 변동사항이 생길 때 다음과 같이 입력해주면 적용됩니다.

   ```shell
   $ sudo systemctl daemon-reload
   $ sudo systemctl restart uwsgi nginx
   ```