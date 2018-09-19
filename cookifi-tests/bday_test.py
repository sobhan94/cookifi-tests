import time
import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from unicodedata import decimal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Cookifi_bday_test(unittest.TestCase):
    def setUp(self):
        # using Chrome browser. ensure it is installed
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_bday(self):
        driver = self.driver
        # open cookifi site
        driver.get('https://cookifi.com/')
        wait = WebDriverWait(driver, 10)
        # wait for components to be loaded
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "EVENTS")))
        events = driver.find_element_by_partial_link_text('EVENTS')
        birthday = driver.find_element_by_partial_link_text('Birthday')
        ActionChains(driver).move_to_element(events).move_to_element(birthday).click().perform()
        # select a package
        wait.until(EC.presence_of_element_located((By.XPATH, "(//h3[contains(text(), 'Birthday dinner with Live Counters')])/../..")))
        package = driver.find_element_by_xpath("(//h3[contains(text(), 'Birthday dinner with Live Counters')])/../..")
        package.find_element_by_tag_name('a')
        package.click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[1]//label[1]//select[1]")))
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'LOGIN TO VIEW PRICE')))
        driver.find_element_by_partial_link_text('LOGIN TO VIEW PRICE').click()
        driver.find_element_by_partial_link_text('Login with Google').click()
        self.google_login()
        # Fill in the form
        wait.until(EC.presence_of_element_located((By.ID, "id_no_of_people")))
        locality = driver.find_element_by_id('id_locality')
        locality.clear()
        locality.send_keys("testing locality")
        no_of_people = Select(driver.find_element_by_id("id_no_of_people"))
        no_of_people.select_by_visible_text("50")
        # setting the selection for type of meal
        driver.find_element_by_id('id_pure_veg_1').click()
        # setting the date of the event, the current date as been set for tomorrow.
        # it can be changed later
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        date = driver.find_element_by_id("id_date")
        date.click()
        date.clear()
        date.send_keys(tomorrow.strftime("%Y-%m-%d"))
        # Se;ect meal
        meal = Select(driver.find_element_by_id("id_meal"))
        meal.select_by_visible_text("Lunch")
        form = driver.find_element_by_id("sendform")
        form.submit()
        # main menu
        no_of_veg = Select(driver.find_element_by_xpath("//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[1]//label[1]//select[1]"))
        no_of_veg.select_by_visible_text('20')
        no_of_nonveg = Select(driver.find_element_by_xpath("//div[@id='content']//div[@class='ng-scope']//div[@class='row']//div[2]//label[1]//select[1]"))
        no_of_nonveg.select_by_visible_text('30')
        driver.find_element_by_partial_link_text('Add Soup').click()
        self.add_bday_dish('Veg Clear Soup', 'Soup')
        self.add_bday_dish('Butter Garlic Prawns', 'Starter')
        self.add_bday_dish('Zafrani pulao', 'Rice')
        self.add_bday_dish('Butter Roti', 'Bread')
        self.add_bday_dish('Chicken Thai Green Curry', 'Main Course')
        self.add_bday_dish('Shahi Tukda', 'Desserts')
        self.add_bday_dish('Sweet Lassi', 'Drinks')
        self.add_bday_dish('Table', 'Add-on')
        #self.add_bday_dish('Bisleri Water Can (20l)', 'Add-on')
        proceed = driver.find_element_by_partial_link_text('PROCEED TO PAYMENT')
        proceed.click()
        # CLICK ON PAYMENT MODE
        payment = driver.find_element_by_xpath("//input[@value='hdfc']")
        payment.click()
        # click for payment
        proceed = driver.find_element_by_xpath("//input[@value='Proceed to payment']")
        proceed.click()

    def google_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        email = 'cookifi.test@gmail.com'
        password = 'mitu4555'
        wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        driver.find_element_by_id("identifierId").send_keys(email)
        driver.find_element_by_id("identifierNext").click()
        driver.implicitly_wait(10)
        driver.find_element_by_name("password").send_keys(password, Keys.RETURN)

    def add_bday_dish(self, dish, type):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        type_select = Select(driver.find_element_by_xpath("//select[contains(@ng-model, 'selectedCourse')]"))
        type_select.select_by_visible_text(type)
        search = driver.find_element_by_id('add_dish_search')
        search.send_keys(dish)
        dish_select = driver.find_element_by_xpath("(//H4[contains(text()," + "\'" + dish + "\'" + ")])/../../..")
        dish_select.find_element_by_xpath("(//div[contains(@class, 'add_remove_dish')])")
        dish_select.find_element_by_partial_link_text('Add').click()
        #wait.until(EC.presence_of_element_located((By.XPATH, "(//H4[contains(text()," + "\'" + dish + "\'"+ "]/../..//SPAN[@class='added large']")))


if __name__ == '__main__':
    unittest.main()
