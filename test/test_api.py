import allure
import requests

apiKey = {"X-API-KEY": "5R07BXR-HXQ4F98-NWCK6RW-8Y4ETD7"}
# "5R07BXR-HXQ4F98-NWCK6RW-8Y4ETD7" - мой ключ
# "S3Y3QWY-0RP4FF6-PQ4F0RM-PAG6PF7"
# "1PT50NM-Q56412B-GN4Y0QP-ZGM2ASF"
base_url_api = 'https://api.kinopoisk.dev/v1.4'


@allure.id('Kinopoisk_api_01')
@allure.title("Поиск фильма по id. Позитивная проверка.")
@allure.severity("Critical")
# @pytest.mark.positive_test
def test_search_by_id(id=""):
    id = "44168"
    with allure.step("Отправка запроса."):
        response = requests.get(f"{base_url_api}/movie/{id}", headers=apiKey)
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 200
        "Запрос должен возвращать статус 200"
    with allure.step("Проверка соответствия id."):
        result_id = response.json()
        assert str(result_id["id"]) == str(id)
    with allure.step("Проверка, что список фильмов не пустой"):
        assert len(result_id) > 0


@allure.id('Kinopoisk_api_02')
@allure.title("Поиск фильма по неверному id (вне диапазона)."
              "Негативная проверка.")
@allure.severity("Normal")
# @pytest.mark.negative_test
def test_search_eror_id(id=""):
    id = "d1000000001"
    with allure.step("Отправка запроса."):
        response = requests.get(f"{base_url_api}/movie/{id}", headers=apiKey)
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 400


@allure.id('Kinopoisk_api_03')
@allure.title("Поиск фильма по id без токена авторизации."
              "Негативная проверка.")
@allure.severity("Normal")
# @pytest.mark.negative_test
def test_search_no_apiKey(id=""):
    id = "100"
    with allure.step("Отправка запроса."):
        response = requests.get(f"{base_url_api}/movie/{id}")
    with allure.step("Проверка статуса кода"):
        assert response.status_code == 401


@allure.id('Kinopoisk_api_04')
@allure.title("Поиск фильма по названию. Позитивная проверка.")
@allure.severity("Critical")
# @pytest.mark.positive_test
def test_search_film_by_name(name_film=""):
    name_film = "Девчата"
    with allure.step("Отправка запроса."):
        response = requests.get(
            url=f"{base_url_api}/movie/search?query={name_film}",
            headers=apiKey)
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 200
        "Запрос должен возвращать статус 200"
    with allure.step("Проверка соотвтетсвия названия."):
        result_name = response.json()
        assert str(result_name["docs"][0]["name"]) == str(name_film)
    with allure.step("Проверка, что список фильмов не пустой"):
        assert len(result_name) > 0


@allure.id('Kinopoisk_api_04')
@allure.title("Поиск фильмов по рейтингу и жанру. Позитивная проверка.")
@allure.severity("Normal")
# @pytest.mark.positive_test
def test_rating():
    my_params = {
            'page': 10,
            'limit': 100,
            'rating.kp': '8-10',
            'genres.name': "комедия"
        }
    with allure.step("Отправка запроса."):
        response = requests.get(f"{base_url_api}/movie",
                                params=my_params, headers=apiKey)
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 200
        "Запрос должен возвращать статус 200"
    with allure.step("Проверка рейтингов всех фильмов"):
        movies = response.json()["docs"]
        with allure.step("Проверка рейтингов всех фильмов"):
            for movie in movies:
            # Получаем рейтинг Кинопоиска для текущего фильма
                rating = movie["rating"]["kp"]
            # Проверяем что рейтинг в диапазоне 8-10
            
            assert 8 <= rating <= 10
    with allure.step("Проверка, что список фильмов не пустой"):
        assert len(movies) > 0
