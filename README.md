Процесс запуска:
Надеюсь вы будете проверять через Postman(слетела вся статика, к сожалению)
1) Склонировать проект
2) docker-compose build
3) docker-compose up
4) docker ps(взять id контейнера)
5) docker exec -it (сюда id) bash
6) python manage.py migrate
7) python manage.py createsuperuser(для админки)
6) /api/swagger/ - свагер
Скрипт
SELECT 
    u.id AS user_id,
    u.username,
    COUNT(l.id) AS link_count,
    u.date_joined
FROM 
    auth_user u
LEFT JOIN 
    api_link l ON u.id = l.user_id
GROUP BY 
    u.id
ORDER BY 
    link_count DESC,
    u.date_joined ASC
LIMIT 10;