from typing import Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class Main:

    def __init__(self, driver: WebDriver) -> WebDriver:
        self.driver = driver
        self.driver.get("https://www.kinopoisk.ru/")
        self.driver.implicitly_wait(5)
        self.driver.maximize_window

    @allure.step("Обрабатываем капчу, если searchона появляется.")
    def captcha(self):
        """
        Данный метод обрабатывает капчу.
        """
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".CheckboxCaptcha-Button").click()
            self.driver.implicitly_wait(20)
        except NoSuchElementException:
            pass

    @allure.step('Переход в расширенный фильтр с главной страницы.')
    def open_advanced_filter(self):
        self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Расширенный поиск"]').click()

    @allure.step('Переход в ЛК. Кнопка "Войти".')
    def entrance_personal_account(self):
        self.driver.find_element(By.CSS_SELECTOR, 'button[class="styles_loginButton__LWZQp"]').click()

    @allure.step('Ввод невалидного названия фильма в строку поиска и нажать "поиск".')
    def search(self, title: str) -> str: # задали параметр, то что будем вводить в строку поиска  
        self.driver.find_element(By.CSS_SELECTOR, 'input#find_film').send_keys(title)
        self.driver.find_element(By.CSS_SELECTOR, 'input.el_18.submit.nice_button').click()
        return str(title)

    @allure.step('Вытаскиваем название искомого фильма из плажки "поиск: <название фильма> • результаты: <кол-во>".')
    def  title(self) -> str:
        title = self.driver.find_element(By.CSS_SELECTOR, 'div[class="search_results_top"]').text
        countrol_title = title.split()[1] # вытаскиваем название фильма "Девчата" из плажки "поиск: Девчата • результаты: 30"
        return str(countrol_title)
    
    @allure.step('Поиск фильма по нескольким параметрам (название + год).')
    def search_title_year(self, title: str, year: str):
        title = self.driver.find_element(By.CSS_SELECTOR, 'input#find_film').send_keys(title)
        year = self.driver.find_element(By.CSS_SELECTOR, 'input#year').send_keys(year)
        self.driver.find_element(By.CSS_SELECTOR, 'input.el_18.submit.nice_button').click()

    @allure.step('Ввод телефонного номера для входа в ЛК.')
    def number_phone(self, num: int) -> int:
        self.driver.find_element(By.CSS_SELECTOR, 'input#passp-field-phone').send_keys(num)

