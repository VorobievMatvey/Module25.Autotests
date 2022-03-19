import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

s = Service('/Users/vormat/chromedriver')

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(service=s)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('matvey.vorobiev@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('w1w2w3w4')
   # Ожидаем, что кнопка будет активной
   element = WebDriverWait(pytest.driver, 5).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Переходим к моим питомцам
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
   # Проверяем, что мы оказались на странице моих питомцев
   assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Vormat"


   yield

   pytest.driver.quit()


def test_quantity_my_pets():
   # Ожидаем присутствия всех элементов на странице
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr'))
   )
   # Находим количество строк в таблице питомцев
   quantity = pytest.driver.find_elements(By.XPATH, '//tbody/tr')

   # Находим текст статистики профиля
   statistics = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text

   # Сохраняем только числа
   number = []
   for i in statistics.split():
      try:
         number.append(int(i))
      except ValueError:
         pass

   # Сравниваем с количеством питомцев в профиле (первое число в списке)
   assert len(quantity) == number[0]

def test_photo_my_pets():
   # Ожидаем присутствия всех элементов на странице
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/th/img'))
   )
   # Находим строки с фото в таблице питомцев
   images = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')

   photo = 0
   # Подсчитываем кол-во питомцев с фото
   for i in range(len(images)):
      if images[i].get_attribute('src')!='':
         photo +=1

   # Сравниваем питомцев с фото с "половиной" всех питомцев
   assert photo >= len(images)//2


def test_data_pets():
   # Ожидаем присутствия всех элементов на странице
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
   )
   # Сохраняем все элементы в таблице питомцев с тэгом td
   info = pytest.driver.find_elements(By.TAG_NAME, 'td')
   data = []
   names, types, age = [], [], []
   # Записываем в список все данные: (Имя, Порода, Возраст)
   for i in info:
      data.append(i.text)

   # Находим все имена, породы, возрасты и сохраняем в отдельные списки
   for n in range(0, len(data), 4):
      names.append(data[n])
      types.append(data[n+1])
      age.append(data[n+2])

   # Проверяем, что у каждого питомца есть имя, возраст и порода.
   for l in range(len(names)):
      assert names[l] != '' and types[l] != '' and age[l] != ''


def test_names_pets():
   # Ожидаем присутствия всех элементов на странице
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
   )
   # Сохраняем все элементы в таблице питомцев с тэгом td
   info = pytest.driver.find_elements(By.TAG_NAME, 'td')
   data = []
   names, types, age = [], [], []
   # Записываем в список все данные: (Имя, Порода, Возраст)
   for i in info:
      data.append(i.text)

   # Находим все имена и сохраняем в отдельном списке
   for n in range(0, len(data), 4):
      names.append(data[n])

   # Проверяем длину списка и длину "уникального" списка, чтобы проверить, что у всех питомцев разные имена
   assert len(names) == len(set(names))


def test_identical_pets():
   # Ожидаем присутствия всех элементов на странице
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
   )
   # Сохраняем все элементы в таблице питомцев с тэгом td
   info = pytest.driver.find_elements(By.TAG_NAME, 'td')
   data = []
   # Записываем в список все данные: (Имя, Порода, Возраст)
   for i in info:
      data.append(i.text)

   a = set()

   # Добавляем в сет кортеж состоящий из (Имя, Порода, Возраст) и проверяем на идентичность
   for n in range(0, len(data), 4):
      pet = (data[n], data[n+1],data[n+2])
      assert pet not in a
      a.add(pet)













