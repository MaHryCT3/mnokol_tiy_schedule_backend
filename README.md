# TIY Vizor(@Backend)

# О проекте

Данное приложение является частью проекта по реализации отдельного рассписания занятий многопрофильного колледжа ТИУ. 

# Как запустить?


### Продакшен
* Debian/Ubuntu
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose](https://docs.docker.com/compose/install/)

### Разработка
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose](https://docs.docker.com/compose/install/)
* [Poetry](https://python-poetry.org/)
* [Python](https://www.python.org/downloads/) ^3.10
* Good mood
  

### Клонируем репозиторий

```bash
git clone https://github.com/MaHryCT3/tiy_vizor_backend.git
```
### Запуск приложения

```bash
make run-dev
```

или

```bash
uvicorn app:app --reload --port 443
```


### Deploy

Гайд по [деплою](/deployment.md) 