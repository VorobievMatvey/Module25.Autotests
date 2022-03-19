import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


s = Service('/Users/vormat/chromedriver')

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(service=s)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')

   yield

   pytest.driver.quit()


def test_show_all_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('matvey.vorobiev@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('w1w2w3w4')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   pytest.driver.implicitly_wait(5)
   # Находим все фото питомцев
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   # Находим все имена питомцев
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   # Находим все описания питомцев. В описании заключены порода и возраст
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i].text
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0