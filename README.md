# Site Notebook
## API для хранения ссылок пользователей на веб-сайты

### Swagger

Swagger доступен по адресу

```
/doc/swagger/
```

### Инструкция для запуска

1. Склонировать проект
    ```
    git clone https://github.com/NerdSmith/SiteNotebook.git
    ```

2. Перейти в папку "SiteNotebook"
    ```
    cd SiteNotebook
    ```
3. Установить конфигурационные данные в шаблонных файлах .env и .env.db
4. Переименовать шаблонные .env* файлы, убрав .tmpl  
   
   Windows:
   ```
   ren ".env.tmpl" ".env"
   ren ".env.db.tmpl" ".env.db"
   ```
   Linux:
   ```
   mv .env.tmpl .env
   mv .env.db.tmpl .env.db
   ```
5. Запустить docker-compose.yml
   ```
   docker compose up -d
   ```
6. Готово, сервис должен работать на порту :4000

### Авторизация и аутентификация
В сервисе предусмотрена аутентификация JWT  
- Для получения access и refresh токенов (входа) используется /api/v1/jwt/create/  
- Для блокировки refresh токена (выхода) используется /api/v1/jwt/blacklist/  