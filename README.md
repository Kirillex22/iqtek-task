# Описание
Это приложение использует FastAPI для реализации REST API. В качестве хранилища данных можно настроить как PostgreSQL,  
так и Redis. В этой инструкции предполагается, что используется Redis для хранения данных.

## Требования
- Python 3.8+
- Установленный Redis или Postgresql

## Шаги для запуска  

### Установка зависимостей  

Клонируйте репозиторий и установите необходимые зависимости:  
git clone <URL_репозитория>  
cd <папка_проекта>  
pip install -r requirements.txt  

### Конфигурация базы данных

В каталоге проекта (./api) лежит конфигурации config.yml. Пример содержимого для использования Redis:  

db_type: redis  
postgres_data:  
  username: postgres  
  password: postgres  
  host: localhost  
  db_name: test  
redis_data:  
  host: localhost  
  port: 6379  
  db_idx: 0  
  password: null  

### Запуск  
Когда все зависимости установлены и Redis (Postgresql) запущен, можно запустить приложение:  

uvicorn main:app --reload  

Приложение доступно по адресу http://127.0.0.1:8000.

Тестирование

Приложение доступно по адресу http://127.0.0.1:8000. Вы можете протестировать доступные эндпоинты через Swagger UI,  
который будет доступен по адресу http://127.0.0.1:8000/docs.  

Если вы хотите использовать PostgreSQL вместо Redis, измените конфиг следующим образом:  
 
db_type: postgres  
postgres_data:  
  username: postgres  
  password: postgres  
  host: localhost  
  db_name: test  
redis_data:  
  host: localhost  
  port: 6379  
  db_idx: 0  
  password: null  
