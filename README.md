# Описание  

## Требования
- Python 3.10+
- Установленный Redis или Postgresql

## Шаги для запуска  

### Установка зависимостей  

Клонируйте репозиторий и установите необходимые зависимости.

### Конфигурация базы данных

В каталоге проекта (./api) лежит конфигурации config.yaml. Пример содержимого для использования Redis:  

<pre lang="markdown">
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
</pre>

### Запуск  
Когда все зависимости установлены и Redis (Postgresql) запущен, можно запустить приложение:  

uvicorn main:app --reload  

Приложение доступно по адресу http://127.0.0.1:8000.

Тестирование

Приложение доступно по адресу http://127.0.0.1:8000. Вы можете протестировать доступные эндпоинты через Swagger UI,  
который будет доступен по адресу http://127.0.0.1:8000/docs.  

Если вы хотите использовать PostgreSQL вместо Redis, измените конфиг следующим образом:  

<pre lang="markdown">
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
</pre>
