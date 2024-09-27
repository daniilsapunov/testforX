Процесс запуска:
1) Склонировать проект
2) docker-compose build
3) docker-compose up
4) перейте по ссылке
5) Лучше использовать Postman 
6) /api/swagger/ - свагер
7) Скрипт
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