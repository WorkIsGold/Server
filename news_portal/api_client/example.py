from client import NewsAPIClient, APIError
import json
import requests


def demo_public_operations():
    """Демонстрация публичных операций (без аутентификации)"""
    print("=" * 50)
    print("1. Публичные операции (без токена)")
    print("=" * 50)

    client = NewsAPIClient(base_url="http://localhost:8000")

    # Получение списка новостей
    print("\n Список новостей:")
    news_list = client.get_news()
    print(json.dumps(news_list, indent=2, ensure_ascii=False))

    """# Фильтрация по автору
    print("\n Новости автора с ID=1:")
    news_by_author = client.get_news(author=1)
    print(json.dumps(news_by_author, indent=2, ensure_ascii=False))"""

    """# Пагинация - вторая страница
    print("\n Вторая страница новостей:")
    page2 = client.get_news(page=2)
    print(json.dumps(page2, indent=2, ensure_ascii=False))"""

    """# Поиск
    print("\n Поиск по слову 'важно':")
    search_results = client.get_news(search="важно")
    print(json.dumps(search_results, indent=2, ensure_ascii=False))"""


def demo_user_registration_and_auth():
    """Демонстрация регистрации и аутентификации"""
    print("\n" + "=" * 50)
    print("2. Регистрация и аутентификация")
    print("=" * 50)

    client = NewsAPIClient(base_url="http://localhost:8000")

    # Регистрация нового пользователя
    print("\n Регистрация пользователя testuser...")
    try:
        user = client.register(
            username="testuser",
            email="test@example.com",
            password="securepass123"
        )
        print(f" Пользователь создан: {user}")
    except APIError as e:
        if "already exists" in str(e):
            print(" Пользователь уже существует, пробуем войти...")
        else:
            raise

    # Вход и получение токена
    print("\n Вход в систему...")
    auth_data = client.login(username="testuser", password="securepass123")
    print(f" Токен получен: {auth_data.get('token', 'N/A')[:20]}...")


def demo_crud_operations():
    """Демонстрация CRUD операций с новостями"""
    print("\n" + "=" * 50)
    print("3. CRUD операции с новостями")
    print("=" * 50)

    # Создаем клиент с токеном (предполагается, что мы уже залогинены)
    client = NewsAPIClient(base_url="http://localhost:8000")

    # Вход (замените на реальные данные)
    try:
        client.login(username="testuser", password="securepass123")
    except APIError as e:
        print(f" Ошибка входа: {e}")
        return

    # CREATE - создание новости
    print("\n Создание новости...")
    new_news = client.create_news(
        title="Мой первый пост через API",
        content="""Это содержание новости, которое должно быть не менее 50 символов. 
        Здесь мы тестируем создание новости через API клиент. Убедимся, что валидация 
        работает корректно и новость сохраняется в базе данных.""",
        summary="Тестовая новость"
    )
    news_id = new_news['id']
    print(f" Создана новость ID={news_id}: {new_news['title']}")

    # READ - получение одной новости
    print(f"\n Получение новости ID={news_id}...")
    fetched = client.get_news(news_id=news_id)
    print(f" Заголовок: {fetched['title']}")
    print(f"   Автор: {fetched['author_name']}")
    print(f"   Дата: {fetched['date_created']}")

    # UPDATE - частичное обновление (PATCH)
    print(f"\n Обновление заголовка новости ID={news_id}...")
    updated = client.update_news(news_id, title="Обновленный заголовок (через PATCH)")
    print(f" Новый заголовок: {updated['title']}")

    """# UPDATE - полное обновление (PUT)
    print(f"\n Полное обновление новости ID={news_id}...")
    replaced = client.replace_news(
        news_id,
        title="Совсем другой заголовок",
        #content="""#Это совершенно новое содержание, которое также имеет длину
#        более 50 символов, чтобы пройти валидацию. Мы заменили новость полностью.""",
#        """summary="Полностью обновлено"
#    )
#    print(f" Обновленная новость: {replaced['title']}")"""

    """# LIST с фильтрацией
    print("\n Список моих новостей (фильтр по автору)...")
    my_news = client.get_news(author=1)  # предположим, что автор имеет ID=1
    if isinstance(my_news, dict) and 'results' in my_news:
        count = my_news['count']
        print(f" Всего новостей: {count}")
    else:
        print(f" Получено новостей: {len(my_news) if isinstance(my_news, list) else 'N/A'}")"""

    # DELETE - удаление новости
    print(f"\n Удаление новости ID={news_id}...")
    success = client.delete_news(news_id)
    if success:
        print(" Новость успешно удалена")

    # Проверяем, что новость действительно удалена
    print("\n Проверка удаления...")
    try:
        deleted_check = client.get_news(news_id=news_id)
        print(" Новость все еще существует!")  # не должно случиться
    except APIError as e:
        if e.status_code == 404:
            print(" Новость не найдена (удаление подтверждено)")
        else:
            print(f" Ошибка: {e}")


def demo_pagination_and_filtering():
    """Демонстрация пагинации и фильтрации"""
    print("\n" + "=" * 50)
    print("4. Пагинация и фильтрация")
    print("=" * 50)

    client = NewsAPIClient(base_url="http://localhost:8000")

    # Создаем несколько новостей для демонстрации (если их мало)
    # Здесь предполагается, что у нас уже есть данные

    """# Демонстрация пагинации
    print("\n Пагинация (страница 1, размер 2):")
    page1 = client.get_news(page=1)
    if isinstance(page1, dict) and 'results' in page1:
        print(f"Всего записей: {page1['count']}")
        print(f"Страница 1/{page1.get('num_pages', '?')}")
        for item in page1['results'][:2]:
            print(f"  - {item['title']}")"""

    # Демонстрация получения всех новостей через утилиту
    print("\n Получение всех новостей (обход пагинации):")
    all_news = client.get_all_news(max_pages=3)
    print(f" Загружено {len(all_news)} новостей")

    """# Комбинированная фильтрация
    print("\n Комбинированный поиск: author=1 & search='важно'")
    combined = client.get_news(author=1, search="важно")
    print(json.dumps(combined, indent=2, ensure_ascii=False)[:500])"""


def demo_error_handling():
    """Демонстрация обработки ошибок"""
    print("\n" + "=" * 50)
    print("5. Обработка ошибок")
    print("=" * 50)

    client = NewsAPIClient(base_url="http://localhost:8000")

    # Попытка создать новость без аутентификации
    print("\n Попытка создать новость без токена:")
    try:
        result = client.create_news("Без токена",
                                    "Содержание новости, которое достаточно длинное для прохождения валидации...")
        print(f"Неожиданный успех: {result}")
    except APIError as e:
        print(f" Ожидаемая ошибка: {e}")

    # Попытка получить несуществующую новость
    print("\n Запрос несуществующей новости:")
    try:
        result = client.get_news(news_id=99999)
        print(f"Неожиданный успех: {result}")
    except APIError as e:
        print(f" Ошибка {e.status_code}: {e}")

    # Ошибка валидации при создании новости
    print("\n Ошибка валидации (короткий content):")
    client.login(username="testuser", password="securepass123")
    try:
        short_content = "Слишком коротко"
        result = client.create_news("Тест", short_content)
    except APIError as e:
        print(f" Ошибка валидации: {e.response}")
        if 'content' in e.response:
            print(f"   Поле 'content': {e.response['content']}")


if __name__ == "__main__":
    """
    Запуск всех демонстраций
    Убедитесь, что сервер запущен на http://localhost:8000
    """

    print("\n ЗАПУСК ДЕМОНСТРАЦИИ API КЛИЕНТА")
    print("Убедитесь, что сервер запущен: python manage.py runserver")

    try:
        # Публичные операции
        demo_public_operations()

        # Регистрация и авторизация
        demo_user_registration_and_auth()

        # CRUD операции
        demo_crud_operations()

        # Пагинация и фильтрация
        demo_pagination_and_filtering()

        # Обработка ошибок
        demo_error_handling()

        print("\n" + "=" * 50)
        print(" Демонстрация завершена успешно!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("\n Невозможно подключиться к серверу!")
        print("   Убедитесь, что сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"\n Непредвиденная ошибка: {e}")