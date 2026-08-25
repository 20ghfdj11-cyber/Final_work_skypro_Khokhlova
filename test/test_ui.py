import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from page.MainPage import Main


@pytest.fixture()
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.id("Kinopoisk_01")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title("Поиск фильма/сериала по валидному названию." "Позитивная проверка.")
@allure.description(
    "Проверить, что название введенного фильма соостветствует "
    "отображенному названию в верхней плашке"
    '"поиск: Девчата • результаты: 30"'
)
@allure.severity("Blocker")
# @pytest.mark.positive_test
def test_search_movie__main_page(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    title_search = main_page.search("Девчата")
    title_total = main_page.title()
    with allure.step(
        "Проверка, что название введенного фильма"
        "соостветствует отображенному названию"
        "в верхней плашке)."
    ):
        assert title_search == title_total


@allure.id("Kinopoisk_02")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title(
    "Поиск фильма/сериала в названии содержатся символы." "Негативная проверка."
)
@allure.description(
    "Ввести невалидное название фильма (символы),"
    "убедиться, что получаем сообщение:"
    '"К сожалению, по вашему запросу ничего не найдено..."'
)
@allure.severity("Minor")
# @pytest.mark.negative_test
def test_negative_1_search(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.search("#")
    with allure.step(
        "Проверка, что при невалидных данных"
        "(введении символов в поле поиска) видим сообщение:"
        '"К сожалению, по вашему запросу ничего не найдено...".'
    ):
        message = main_page.driver.find_element(
            By.XPATH, '//*[@id="block_left_pad"]' "/div/table/tbody/tr[1]/td/h2"
        ).text
        assert message == "К сожалению, по вашему запросу ничего не найдено..."



@allure.id("KinopoisK_03")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title("Поиск фильма/сериала по нескольким параметрам." "Позитивная проверка.")
@allure.description(
    "Ввести в поиск название фильма и год,"
    "убедиться, что результат поиска соответствует ожиданиям"
)
@allure.severity("Critical")
# @pytest.mark.positive_test
def test_positive_2_search(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    with allure.step(
        "Ввод в соответствующие поля" "названия фильма (title) и год (year)."
    ):
        title = "Девчата"
        year = "1961"
    main_page.search_title_year(title, year)
    with allure.step("Проверка, что что результат поиска" "соответствует ожиданиям."):
        result = main_page.driver.find_element(
            By.CSS_SELECTOR, '[itemprop="name"]'
        ).text
        # By.XPATH,'//*[@id="__next"]/div[1]/div[2]/
        # main/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/h1/span'
        assert result == f"{title} ({year})"


@allure.id("KinopoisK_04")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title('Проверка активности кнопки "Смотреть фильм".')
@allure.description("")
@allure.severity("Blocker")
# @pytest.mark.positive_test
def test_positive_button(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.search_title_year("Девчата", "1961")
    with allure.step(
        'Нажать на кнопку "Смотреть фильм",'
        "убедиться, что осуществлен переход"
        " на страницу авторизации"
    ):
        main_page.driver.find_element(
            By.CSS_SELECTOR, 'button[data-test-id="Offer"]'
        ).click()


@allure.id("Kinopoisk_05")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title("Поиск по строке из нескольких пробелов. Негативная проверка.")
@allure.description(
    "Ввести в поле поиска строку из нескольких пробелов, "
    "убедиться, что получаем сообщение: "
    '"К сожалению, по вашему запросу ничего не найдено..."'
)
@allure.severity("Minor")
# @pytest.mark.negative_test
def test_search_only_spaces(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.search("   ")
    with allure.step(
        "Проверка, что при вводе одних пробелов видим сообщение:"
        '"К сожалению, по вашему запросу ничего не найдено...".'
    ):
        message = main_page.driver.find_element(
            By.XPATH, '//*[@id="block_left_pad"]' "/div/table/tbody/tr[1]/td/h2"
        ).text
        assert message == "К сожалению, по вашему запросу ничего не найдено..."


@allure.id("Kinopoisk_06")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title(
    "Поиск фильма/сериала со спецсимволами в середине слова. Негативная проверка."
)
@allure.description(
    "Ввести название фильма с добавлением символов внутри "
    '(например, "Девч@ата"), убедиться, что получаем сообщение: '
    '"К сожалению, по вашему запросу ничего не найдено..."'
)
@allure.severity("Minor")
# @pytest.mark.negative_test
def test_search_with_symbols_inside(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.search("Девч@ата")
    with allure.step(
        "Проверка, что при вводе спецсимволов внутрь слова видим сообщение:"
        '"К сожалению, по вашему запросу ничего не найдено...".'
    ):
        message = main_page.driver.find_element(
            By.XPATH, '//*[@id="block_left_pad"]' "/div/table/tbody/tr[1]/td/h2"
        ).text
        assert message == "К сожалению, по вашему запросу ничего не найдено..."


@allure.id("Kinopoisk_07")
@allure.feature("Поиск фильма. Без авторизации.")
@allure.title("Поиск фильма/сериала на английском языке. Позитивная проверка.")
@allure.description(
    "Проверить, что поиск работает для латиницы."
    "Название введенного фильма соостветствует "
    "отображенному названию в верхней плашке"
)
@allure.severity("Normal")
# @pytest.mark.positive_test
def test_search_movie_latin(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    title_search = main_page.search("Avatar")
    title_total = main_page.title()
    with allure.step(
        "Проверка, что название введенного фильма"
        "соостветствует отображенному названию"
        "в верхней плашке."
    ):
        assert title_search == title_total
