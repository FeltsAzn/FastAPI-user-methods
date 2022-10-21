# Реализация доступа к ресурсу

Простое приложение на FastAPI для доступа пользователя к сервису через GET, POST, PUT, DELETE.

База данных для хранения информации: PostreSQL

Реализована собственная защита от стороннего доступа на основе библиотеки **jwt**.

При создании нового пользователя или авторизации старого пользователя выдается JWT-токен для доступа к обработчикам приложения.

Каждый выданный токен имеет срок жизни в 1 час (реализована проверка создания токена и его времени жизни).

Приложение полностью асинхронное.


# Implementation of resource access

A simple FastAPI application for user access to the service via GET, POST, PUT, DELETE.

Database for storing information: PostreSQL

Implemented protection against external access based on the **jwt** library.

When a new user is created or an old user is authorized, a JWT token is issued to access application handlers.

Each issued token has a lifetime of 1 hour (checking the creation of the token and its lifetime is implemented).

The application is completely asynchronous.


![изображение](https://user-images.githubusercontent.com/107147438/197282935-a64f1bc2-5323-4275-b302-04b6a545767d.png)
