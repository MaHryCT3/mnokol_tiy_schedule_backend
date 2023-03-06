# Deploy

OS: Ubuntu/Debian

Обновляемямся
```bash
sudo apt-get update
```

Устанавливаем докер [инструкция](https://docs.docker.com/engine/install/ubuntu/)

# Запуск бэка

```bash
mkdir code
cd code
```

Клонируем репозиторий и *переходим в него*
```bash
git clone https://github.com/MaHryCT3/tiy_vizor_backend.git
```

Создаем образ
```bash
sudo docker build -f 'docker/fastapi/Dockerfile' -t "tiy-back" .
```

Запускаем!
```bash
sudo docker run -d -p 4430:4430 --name vizor-back tiy-back
```


# Настройка nginx

```bash
sudo apt-get install nginx
```

Отрывем конфиг файл, а именно
```bash
sudo vim /etc/nginx/sites-enabled/default
```

Вставляем конфиг
```nginx
server {
        listen 443 default_server;
        listen [::]:443 default_server;


        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                proxy_pass http://127.0.0.1:4430;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                add_header Access-Control-Allow-Origin *;
        }

}
```

Перезапускаем nginx и проверяем чтобы все работало 

```bash
sudo service nginx restart
```
